"""
Style Validator - Deterministic rule checking for manuscript paragraphs.

This module provides fast, LLM-free validation of text against style rules
for top management journals. Rules are divided into:

HARD RULES: Violations cause immediate rejection and rewrite
- Bullet points
- Numbered lists
- Contribution claims formatted as lists

SOFT RULES: Violations are flagged; may trigger rewrite if severe
- Passive voice density
- Hedging density
- Orphaned empirical claims (stats without interpretation)
- Quotes without setup (except cold opens)
- Long quotes (>80 words)

LATEX SUPPORT: The validator can parse raw LaTeX and catch:
- \\item commands (itemize, enumerate environments)
- \\begin{itemize}, \\begin{enumerate}
- LaTeX-style bullets and lists
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ViolationType(Enum):
    """Types of style violations."""
    # Hard violations - must fix
    BULLET_POINT = "bullet_point"
    NUMBERED_LIST = "numbered_list"
    CONTRIBUTION_LIST = "contribution_list"

    # Soft violations - flag, maybe fix
    PASSIVE_VOICE = "passive_voice"
    HEDGING = "hedging"
    ORPHANED_RESULT = "orphaned_result"
    QUOTE_WITHOUT_SETUP = "quote_without_setup"
    LONG_QUOTE = "long_quote"


class Severity(Enum):
    """Severity of violations."""
    HARD = "hard"  # Must fix before continuing
    SOFT = "soft"  # Flag, fix if severe


@dataclass
class Violation:
    """A detected style violation."""
    type: ViolationType
    severity: Severity
    message: str
    location: Optional[str] = None  # e.g., line number or quote text
    suggestion: Optional[str] = None


@dataclass
class ValidationResult:
    """Result of validating a paragraph."""
    is_clean: bool
    violations: list[Violation]
    hard_violation_count: int
    soft_violation_count: int

    @property
    def needs_rewrite(self) -> bool:
        """Whether this paragraph needs rewriting."""
        return self.hard_violation_count > 0


class StyleValidator:
    """
    Validates paragraphs against style rules for management journals.

    Usage:
        validator = StyleValidator()
        result = validator.validate(paragraph_text, context)

        if result.needs_rewrite:
            # Send to fixer
            pass
    """

    # Passive voice indicators (be + past participle patterns)
    PASSIVE_PATTERNS = [
        r'\b(is|are|was|were|be|been|being)\s+(\w+ed|found|shown|seen|made|given|taken|done)\b',
        r'\b(it|this|that)\s+(is|was|has been)\s+(\w+ed|found|shown|observed|noted|suggested)\b',
    ]

    # Hedging language
    HEDGE_WORDS = [
        'may', 'might', 'could', 'possibly', 'perhaps', 'seemingly',
        'appears to', 'seems to', 'tends to', 'suggests that',
        'it is possible', 'it could be', 'one might argue',
        'to some extent', 'in some ways', 'somewhat',
    ]

    # Statistical result patterns (need interpretation within 2 sentences)
    STAT_PATTERNS = [
        r'[Hh]\d+\s+(is\s+)?(supported|confirmed|rejected)',
        r'β\s*=\s*[\d\.\-]+',
        r'p\s*[<>=]\s*[\d\.]+',
        r'\(\s*p\s*[<>=]',
        r'[Ss]ignificant(ly)?\s+(at|with)',
        r'[Cc]oefficient\s+(of|is|was)',
        r'[Rr]egression\s+results',
        r'\d+\s*percentage\s+points?',
    ]

    # Bullet point patterns (including LaTeX)
    BULLET_PATTERNS = [
        r'^\s*[-•●○▪▸]\s+',  # Common bullet characters
        r'^\s*\*\s+(?!\*)',   # Asterisk as bullet (not bold)
        r'\\item\s+',         # LaTeX \item command
        r'\\item\[',          # LaTeX \item with optional argument
    ]

    # LaTeX list environment patterns
    LATEX_LIST_PATTERNS = [
        r'\\begin\{itemize\}',
        r'\\begin\{enumerate\}',
        r'\\begin\{description\}',
    ]

    # Numbered list patterns (including LaTeX)
    NUMBERED_LIST_PATTERNS = [
        r'^\s*\d+[\.\)]\s+',           # 1. or 1)
        r'^\s*[a-z][\.\)]\s+',         # a. or a)
        r'^\s*\([a-z\d]+\)\s+',        # (a) or (1)
        r'^\s*[ivxIVX]+[\.\)]\s+',     # Roman numerals
        r'\\begin\{enumerate\}',        # LaTeX enumerate
    ]

    # Contribution list indicators
    CONTRIBUTION_LIST_PATTERNS = [
        r'(makes?|offers?)\s+(three|four|several|multiple)\s+contributions?',
        r'contributions?\s+(are|include)\s*:',
        r'[Ff]irst(ly)?,?\s+we\s+(extend|show|contribute)',
        r'[Ss]econd(ly)?,?\s+we\s+(extend|show|contribute)',
        r'[Tt]hird(ly)?,?\s+we\s+(extend|show|contribute)',
    ]

    def __init__(
        self,
        passive_threshold: float = 0.30,
        hedge_threshold: float = 0.20,
        max_quote_words: int = 80,
    ):
        """
        Initialize validator with thresholds.

        Args:
            passive_threshold: Max fraction of sentences that can be passive
            hedge_threshold: Max fraction of sentences with hedging
            max_quote_words: Maximum words in a block quote
        """
        self.passive_threshold = passive_threshold
        self.hedge_threshold = hedge_threshold
        self.max_quote_words = max_quote_words

        # Compile patterns for efficiency
        self._passive_re = [re.compile(p, re.IGNORECASE) for p in self.PASSIVE_PATTERNS]
        self._stat_re = [re.compile(p) for p in self.STAT_PATTERNS]
        self._bullet_re = [re.compile(p, re.MULTILINE) for p in self.BULLET_PATTERNS]
        self._numbered_re = [re.compile(p, re.MULTILINE) for p in self.NUMBERED_LIST_PATTERNS]
        self._contrib_re = [re.compile(p, re.IGNORECASE) for p in self.CONTRIBUTION_LIST_PATTERNS]
        self._latex_list_re = [re.compile(p) for p in self.LATEX_LIST_PATTERNS]

    def validate(
        self,
        text: str,
        is_cold_open: bool = False,
        is_section_open: bool = False,
        following_text: Optional[str] = None,
    ) -> ValidationResult:
        """
        Validate a paragraph against style rules.

        Args:
            text: The paragraph text to validate
            is_cold_open: Whether this is the paper's opening (quote exempt from setup rule)
            is_section_open: Whether this opens a section (quote may be exempt)
            following_text: Text that follows, for checking interpretation of stats

        Returns:
            ValidationResult with any violations found
        """
        violations = []

        # HARD RULES
        violations.extend(self._check_bullets(text))
        violations.extend(self._check_numbered_lists(text))
        violations.extend(self._check_latex_lists(text))
        violations.extend(self._check_contribution_lists(text))

        # SOFT RULES
        violations.extend(self._check_passive_voice(text))
        violations.extend(self._check_hedging(text))
        violations.extend(self._check_orphaned_results(text, following_text))
        violations.extend(self._check_quote_setup(text, is_cold_open, is_section_open))
        violations.extend(self._check_quote_length(text))

        hard_count = sum(1 for v in violations if v.severity == Severity.HARD)
        soft_count = sum(1 for v in violations if v.severity == Severity.SOFT)

        return ValidationResult(
            is_clean=len(violations) == 0,
            violations=violations,
            hard_violation_count=hard_count,
            soft_violation_count=soft_count,
        )

    def _check_bullets(self, text: str) -> list[Violation]:
        """Check for bullet points."""
        violations = []
        lines = text.split('\n')

        for i, line in enumerate(lines):
            for pattern in self._bullet_re:
                if pattern.match(line):
                    violations.append(Violation(
                        type=ViolationType.BULLET_POINT,
                        severity=Severity.HARD,
                        message="Bullet points are not permitted in this genre. Convert to prose.",
                        location=f"Line {i+1}: {line[:50]}...",
                        suggestion="Integrate these points into flowing paragraph text.",
                    ))
                    break  # One violation per line

        return violations

    def _check_numbered_lists(self, text: str) -> list[Violation]:
        """Check for numbered lists."""
        violations = []
        lines = text.split('\n')

        for i, line in enumerate(lines):
            for pattern in self._numbered_re:
                if pattern.match(line) or pattern.search(line):
                    violations.append(Violation(
                        type=ViolationType.NUMBERED_LIST,
                        severity=Severity.HARD,
                        message="Numbered lists are not permitted. Convert to prose.",
                        location=f"Line {i+1}: {line[:50]}...",
                        suggestion="Weave these points into narrative paragraphs.",
                    ))
                    break

        return violations

    def _check_latex_lists(self, text: str) -> list[Violation]:
        """Check for LaTeX list environments."""
        violations = []

        for pattern in self._latex_list_re:
            for match in pattern.finditer(text):
                env_name = match.group(0)
                violations.append(Violation(
                    type=ViolationType.BULLET_POINT if 'itemize' in env_name else ViolationType.NUMBERED_LIST,
                    severity=Severity.HARD,
                    message=f"LaTeX list environment detected: {env_name}. Lists are not permitted.",
                    location=env_name,
                    suggestion="Remove the list environment and convert items to flowing prose paragraphs.",
                ))

        # Also check for \item commands directly (may appear without environment in some contexts)
        item_pattern = re.compile(r'\\item\b')
        for match in item_pattern.finditer(text):
            # Get surrounding context
            start = max(0, match.start() - 20)
            end = min(len(text), match.end() + 30)
            context = text[start:end].strip()

            violations.append(Violation(
                type=ViolationType.BULLET_POINT,
                severity=Severity.HARD,
                message="LaTeX \\item command detected. List items are not permitted.",
                location=context[:60] + "..." if len(context) > 60 else context,
                suggestion="Convert list items to prose sentences within a paragraph.",
            ))

        return violations

    def _check_contribution_lists(self, text: str) -> list[Violation]:
        """Check for contribution claims formatted as lists."""
        violations = []

        for pattern in self._contrib_re:
            match = pattern.search(text)
            if match:
                violations.append(Violation(
                    type=ViolationType.CONTRIBUTION_LIST,
                    severity=Severity.HARD,
                    message="Contribution claims must be woven into prose, not listed.",
                    location=match.group(0),
                    suggestion="State contributions as narrative theoretical extensions: "
                              "'This research extends X by showing Y...'",
                ))

        return violations

    def _check_passive_voice(self, text: str) -> list[Violation]:
        """Check passive voice density."""
        sentences = self._split_sentences(text)
        if not sentences:
            return []

        passive_count = 0
        for sentence in sentences:
            for pattern in self._passive_re:
                if pattern.search(sentence):
                    passive_count += 1
                    break

        passive_ratio = passive_count / len(sentences)

        if passive_ratio > self.passive_threshold:
            return [Violation(
                type=ViolationType.PASSIVE_VOICE,
                severity=Severity.SOFT,
                message=f"Passive voice density ({passive_ratio:.0%}) exceeds threshold ({self.passive_threshold:.0%}).",
                suggestion="Use active voice: 'We find' not 'It was found'; "
                          "'The data show' not 'It is shown by the data'.",
            )]

        return []

    def _check_hedging(self, text: str) -> list[Violation]:
        """Check hedging language density."""
        text_lower = text.lower()
        word_count = len(text.split())

        if word_count == 0:
            return []

        hedge_count = sum(1 for h in self.HEDGE_WORDS if h in text_lower)
        hedge_ratio = hedge_count / (word_count / 10)  # Per 10 words

        if hedge_ratio > self.hedge_threshold:
            found_hedges = [h for h in self.HEDGE_WORDS if h in text_lower]
            return [Violation(
                type=ViolationType.HEDGING,
                severity=Severity.SOFT,
                message=f"High hedging density. Found: {', '.join(found_hedges[:5])}",
                suggestion="Be more direct: 'We show' not 'This may suggest'; "
                          "'The evidence indicates' not 'It is possible that'.",
            )]

        return []

    def _check_orphaned_results(
        self,
        text: str,
        following_text: Optional[str] = None
    ) -> list[Violation]:
        """Check for statistical results without interpretation."""
        violations = []

        # Find statistical claims
        stat_matches = []
        for pattern in self._stat_re:
            for match in pattern.finditer(text):
                stat_matches.append(match)

        if not stat_matches:
            return []

        # Check if interpretation follows
        # Interpretation indicators: "this means", "this suggests", "this pattern",
        # "revealing", "indicating", "because", "the mechanism"
        interpretation_patterns = [
            r'this\s+(means|suggests|indicates|reveals|shows|pattern)',
            r'(revealing|indicating|suggesting|showing)\s+that',
            r'(because|since|as)\s+\w+\s+\w+',
            r'the\s+(mechanism|explanation|reason|implication)',
            r'in\s+other\s+words',
            r'substantively',
        ]

        combined_text = text
        if following_text:
            combined_text += " " + following_text

        has_interpretation = any(
            re.search(p, combined_text, re.IGNORECASE)
            for p in interpretation_patterns
        )

        if not has_interpretation:
            violations.append(Violation(
                type=ViolationType.ORPHANED_RESULT,
                severity=Severity.SOFT,
                message="Statistical result appears without interpretation within 2 sentences.",
                location=stat_matches[0].group(0),
                suggestion="Follow statistical claims with substantive interpretation: "
                          "What does this mean? Why does it matter? "
                          "E.g., 'This 18-point gap reveals that...'",
            ))

        return violations

    def _check_quote_setup(
        self,
        text: str,
        is_cold_open: bool = False,
        is_section_open: bool = False,
    ) -> list[Violation]:
        """Check that quotes have preceding analytical claims."""
        # Find block quotes (text in quotation marks spanning multiple lines or >50 chars)
        quote_pattern = r'["""]([^"""]{50,})["""]|```quote\n(.*?)\n```'

        quotes = list(re.finditer(quote_pattern, text, re.DOTALL))

        if not quotes:
            return []

        # Cold opens are exempt
        if is_cold_open or is_section_open:
            # But must have framing after
            # This is hard to check in isolation; rely on section-level review
            return []

        violations = []

        for match in quotes:
            # Get text before the quote
            before_text = text[:match.start()].strip()

            # Check for analytical claim patterns
            claim_patterns = [
                r'\w+\s+(described|explained|noted|observed|recalled|stated)',
                r'(as|like)\s+one\s+\w+\s+(put|said|noted|explained)',
                r'this\s+(pattern|dynamic|mechanism|phenomenon)',
                r'(illustrat|demonstrat|reveal|show|exemplif)',
            ]

            has_setup = any(
                re.search(p, before_text[-200:], re.IGNORECASE)  # Check last 200 chars
                for p in claim_patterns
            )

            if not has_setup and before_text:
                quote_preview = match.group(0)[:50] + "..."
                violations.append(Violation(
                    type=ViolationType.QUOTE_WITHOUT_SETUP,
                    severity=Severity.SOFT,
                    message="Quote appears without preceding analytical claim.",
                    location=quote_preview,
                    suggestion="Precede quotes with the analytical point they illustrate: "
                              "'This dynamic was evident in how managers described...'",
                ))

        return violations

    def _check_quote_length(self, text: str) -> list[Violation]:
        """Check for overly long quotes."""
        quote_pattern = r'["""]([^"""]+)["""]'
        violations = []

        for match in re.finditer(quote_pattern, text):
            quote_text = match.group(1)
            word_count = len(quote_text.split())

            if word_count > self.max_quote_words:
                violations.append(Violation(
                    type=ViolationType.LONG_QUOTE,
                    severity=Severity.SOFT,
                    message=f"Quote is {word_count} words (max {self.max_quote_words}).",
                    location=quote_text[:50] + "...",
                    suggestion="Trim to essential content. Each quote should be a polished gem, "
                              "not a data dump. Extract the most vivid/essential portion.",
                ))

        return violations

    def _split_sentences(self, text: str) -> list[str]:
        """Split text into sentences."""
        # Simple sentence splitter
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]


# Convenience function for quick validation
def validate_paragraph(
    text: str,
    is_cold_open: bool = False,
    is_section_open: bool = False,
) -> ValidationResult:
    """Convenience function for quick paragraph validation."""
    validator = StyleValidator()
    return validator.validate(text, is_cold_open, is_section_open)
