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

from .config import PaperType


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

    # Qual-forward specific violations (genre-dependent)
    HYPOTHESIS_LANGUAGE_IN_QUAL = "hypothesis_language_in_qual"
    MECHANISM_PREVIEW_IN_THEORY = "mechanism_preview_in_theory"
    QUOTE_WITHOUT_FOLLOWTHROUGH = "quote_without_followthrough"
    FINDINGS_NOT_PROGRESSIVE = "findings_not_progressive"

    # Multimethod inductive paper specific violations
    EXPECTED_PATTERNS_SECTION = "expected_patterns_section"
    PATTERN_NUMBERING = "pattern_numbering"
    ENUMERATED_CONTRIBUTIONS = "enumerated_contributions"
    MISSING_ITERATIVE_METHODS = "missing_iterative_methods"
    SPECULATIVE_FINDINGS = "speculative_findings"


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
    # NOTE: Asterisk bullet pattern removed - too many false positives from
    # table footnotes (e.g., "* Projected figures.") and markdown italics
    BULLET_PATTERNS = [
        r'^\s*[-•●○▪▸]\s+',  # Common bullet characters
        # r'^\s*\*\s+(?!\*)',   # DISABLED: catches table footnotes
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
    # NOTE: Pattern for (a) or (1) style removed - too many false positives from
    # citation years like "(2021)" at start of lines in PDF conversions
    NUMBERED_LIST_PATTERNS = [
        r'^\s*\d+[\.\)]\s+',           # 1. or 1)
        r'^\s*[a-z][\.\)]\s+',         # a. or a)
        # r'^\s*\([a-z\d]+\)\s+',      # DISABLED: catches citation years (2021)
        r'^\s*[ivxIVX]+[\.\)]\s+',     # Roman numerals
        r'\\begin\{enumerate\}',        # LaTeX enumerate
    ]

    # Contribution list indicators
    # NOTE: Ordinal transitions ("First, we find X. Second, we contribute Y.") are OK.
    # Only flag the "makes three contributions:" setup pattern.
    CONTRIBUTION_LIST_PATTERNS = [
        r'(makes?|offers?)\s+(three|four|several|multiple)\s+contributions?',
        r'contributions?\s+(are|include)\s*:',
    ]

    # ==========================================================================
    # QUAL-FORWARD SPECIFIC PATTERNS
    # These are used when paper_type is QUAL_FORWARD
    # ==========================================================================

    # Hypothesis-testing language (inappropriate for inductive papers)
    HYPOTHESIS_LANGUAGE_PATTERNS = [
        r'\b[Hh]ypothesis\s+\d',  # H1, H2, etc.
        r'\b[Hh]\d\s*(:|is)',  # H1:, H1 is supported
        r'\b(support|confirm|validate|test)\s+(the\s+)?(hypothesis|prediction|proposition)',
        r'\b(as\s+predicted|as\s+hypothesized|consistent\s+with\s+our\s+prediction)',
        r'\bwe\s+predict(ed)?\s+that\b',
        r'\bour\s+findings\s+(support|confirm|validate)\b',
        r'\bthe\s+results\s+(support|confirm|validate)\s+[Hh]\d',
    ]

    # Mechanism preview language (inappropriate in intro/theory for qual papers)
    # These patterns catch when the theory section reveals findings rather than setting up
    # sensitizing concepts and research questions
    # NOTE: Relaxed patterns to reduce false positives on published papers
    MECHANISM_PREVIEW_PATTERNS = [
        # Original patterns - causal claims (strong indicators)
        r'\bwe\s+(find|show|demonstrate|argue)\s+that\s+\w+\s+(leads?\s+to|causes?|produces?)',
        r'\bour\s+analysis\s+(reveals?|shows?)\s+that',
        r'\bthe\s+mechanism\s+(is|involves?|works?)',
        r'\bthis\s+(occurs?|happens?)\s+because',
        r'\bwe\s+theorize\s+that\s+\w+\s+(leads?\s+to|results?\s+in)',
        # Theory-building patterns (only flag when combined with enumeration)
        r'\bwe\s+develop\s+a\s+theory\s+of\b',  # Should emerge in findings
        r'\bwe\s+theorize\s+(three|two|four|several)\b',  # Enum theorizing = findings work
        # NOTE: Removed 'we theorize that' alone - too broad, legitimate in modern intros
        r'\bthe\s+key\s+insight\s+is\s+that\b',  # Punchline belongs in findings
        r'\bthe\s+core\s+argument\s+is\s+that\b',  # Core argument should emerge
        r'\ba\s+key\s+theoretical\s+claim\s+is\s+that\b',  # Labeling claims as theoretical
        # NOTE: Removed 'we propose that' alone - too common in legitimate usage
        # Context-specific patterns for warehouse automation papers
        r'\b\w+\s+nodes?\s+are\s+(designated|exploitation|exploration)\b',  # "X nodes are..."
        r'\bthese\s+facilities\s+(absorb|receive|serve|function|are)\b',  # Empirical claims
        # NOTE: Removed 'managers expect/anticipate' - too common in legitimate theory
    ]

    # Speculative findings patterns (inappropriate in theory section)
    # Theory section should NOT describe what "might" happen in detail - that's speculating findings
    SPECULATIVE_FINDINGS_PATTERNS = [
        r'\b\w+-focused\s+facilities\s+might\b',  # "Exploration-focused facilities might..."
        r'\bif\s+\w+-focused\s+facilities\s+exist\b',  # "If exploration-focused facilities exist..."
        r'\bat\s+such\s+facilities[,\s]',  # "At such facilities, productivity might..."
        r'\bwe\s+would\s+attend\s+to\b',  # "we would attend to: X, Y, Z"
        r'\bif\s+such\s+differentiation\s+occurs\b',  # Extended speculation
        r'\bthe\s+question\s+is\s+whether\s+such\b',  # Setting up speculative framework
    ]

    # Theory-building language (expected in qual papers)
    THEORY_BUILDING_LANGUAGE = [
        r'\bI\s+found\s+that\b',
        r'\bthis\s+suggests\s+that\b',
        r'\bthe\s+data\s+(reveal|suggest|indicate)',
        r'\bemerged?\s+from\s+(the\s+)?data',
        r'\binductively\b',
        r'\bgrounded\s+(in|theory)\b',
        r'\b(named|labeled|termed)\s+this\s+(phenomenon|concept|dynamic)',
    ]

    # Progressive concept development indicators
    PROGRESSIVE_CONCEPT_INDICATORS = [
        r'\bfirst\b.*\bsecond\b.*\bthird\b',  # Ordinal progression
        r'\bbegan\s+by\b.*\bthen\b',
        r'\binitially\b.*\bsubsequently\b',
        r'\bphase\s+\d\b',
        r'\bstage\s+\d\b',
    ]

    # ==========================================================================
    # MULTIMETHOD INDUCTIVE PAPER PATTERNS
    # These catch hypo-deductive anti-patterns that should not appear in
    # papers using quantitative data for triangulation, not hypothesis testing
    # ==========================================================================

    # Expected Patterns / Pattern X anti-patterns (multimethod inductive papers)
    EXPECTED_PATTERNS_ANTIPATTERNS = [
        r'\b[Ee]xpected\s+[Pp]atterns?\b',  # "Expected Pattern(s)" header
        r'\bthree\s+(expected\s+)?patterns?\b',  # "three expected patterns"
        r'\b[Pp]attern\s+\d+\b',  # "Pattern 1", "Pattern 2"
        r'\bwe\s+(would\s+)?expect\s+to\s+observe\b',  # "we would expect to observe"
        r'\bobservable\s+implications?\b',  # "observable implications"
        r'\byields?\s+a\s+prediction\b',  # "yields a prediction"
    ]

    # Enumerated contribution patterns (beyond "makes three contributions")
    ENUMERATED_CONTRIBUTION_PATTERNS = [
        r'\b[Ff]irst,\s+we\s+(contribute|extend|show|demonstrate)\b',
        r'\b[Ss]econd,\s+we\s+(contribute|extend|show|demonstrate)\b',
        r'\b[Tt]hird,\s+we\s+(contribute|extend|show|demonstrate)\b',
        r'\b[Oo]ur\s+(first|second|third)\s+contribution\b',
    ]

    # Prior theory vs our prediction distinction
    # These are OK when describing what PRIOR WORK predicts, flagged when describing OUR predictions
    OUR_PREDICTION_PATTERNS = [
        r'\bwe\s+(therefore\s+)?(expect|predict)\s+that\b',  # "We expect that"
        r'\bthis\s+(suggests|implies)\s+that\s+\w+\s+should\b',  # "This suggests X should"
        r'\bour\s+(framework|theory|model)\s+(predicts|suggests)\b',  # "Our framework predicts"
    ]

    # Iterative methods language (REQUIRED for multimethod inductive)
    ITERATIVE_METHODS_INDICATORS = [
        r'\biterative(ly)?\b.*\b(qual|quant)',
        r'\bquant.*\bqual|qual.*\bquant\b',  # mentions both in proximity
        r'\bpuzzle\b.*\breturned\s+to\b',
        r'\bemerged\s+from\s+(this|the)\s+(iterative|analytical)\s+process\b',
        r'\btwo\s+(interdependent|iterative)\s+(analytical\s+)?streams\b',  # Resourcing paper phrasing
    ]

    def __init__(
        self,
        passive_threshold: float = 0.30,
        hedge_threshold: float = 0.20,
        max_quote_words: int = 80,
        paper_type: PaperType = PaperType.QUANT_FORWARD,
    ):
        """
        Initialize validator with thresholds.

        Args:
            passive_threshold: Max fraction of sentences that can be passive
            hedge_threshold: Max fraction of sentences with hedging
            max_quote_words: Maximum words in a block quote
            paper_type: QUAL_FORWARD or QUANT_FORWARD (affects which rules apply)
        """
        self.passive_threshold = passive_threshold
        self.hedge_threshold = hedge_threshold
        self.max_quote_words = max_quote_words
        self.paper_type = paper_type

        # For qual-forward papers, allow longer quotes (they do heavy lifting)
        if paper_type == PaperType.QUAL_FORWARD:
            self.max_quote_words = 120

        # Compile patterns for efficiency
        self._passive_re = [re.compile(p, re.IGNORECASE) for p in self.PASSIVE_PATTERNS]
        self._stat_re = [re.compile(p) for p in self.STAT_PATTERNS]
        self._bullet_re = [re.compile(p, re.MULTILINE) for p in self.BULLET_PATTERNS]
        self._numbered_re = [re.compile(p, re.MULTILINE) for p in self.NUMBERED_LIST_PATTERNS]
        self._contrib_re = [re.compile(p, re.IGNORECASE) for p in self.CONTRIBUTION_LIST_PATTERNS]
        self._latex_list_re = [re.compile(p) for p in self.LATEX_LIST_PATTERNS]

        # Compile qual-forward specific patterns
        self._hypothesis_re = [re.compile(p, re.IGNORECASE) for p in self.HYPOTHESIS_LANGUAGE_PATTERNS]
        self._mechanism_preview_re = [re.compile(p, re.IGNORECASE) for p in self.MECHANISM_PREVIEW_PATTERNS]
        self._theory_building_re = [re.compile(p, re.IGNORECASE) for p in self.THEORY_BUILDING_LANGUAGE]
        self._speculative_findings_re = [re.compile(p, re.IGNORECASE) for p in self.SPECULATIVE_FINDINGS_PATTERNS]

        # Compile multimethod inductive paper patterns
        self._expected_patterns_re = [re.compile(p, re.IGNORECASE) for p in self.EXPECTED_PATTERNS_ANTIPATTERNS]
        self._enumerated_contrib_re = [re.compile(p, re.IGNORECASE) for p in self.ENUMERATED_CONTRIBUTION_PATTERNS]
        self._our_prediction_re = [re.compile(p, re.IGNORECASE) for p in self.OUR_PREDICTION_PATTERNS]
        self._iterative_methods_re = [re.compile(p, re.IGNORECASE | re.DOTALL) for p in self.ITERATIVE_METHODS_INDICATORS]

    def validate(
        self,
        text: str,
        is_cold_open: bool = False,
        is_section_open: bool = False,
        following_text: Optional[str] = None,
        section_name: Optional[str] = None,
    ) -> ValidationResult:
        """
        Validate a paragraph against style rules.

        Args:
            text: The paragraph text to validate
            is_cold_open: Whether this is the paper's opening (quote exempt from setup rule)
            is_section_open: Whether this opens a section (quote may be exempt)
            following_text: Text that follows, for checking interpretation of stats
            section_name: Name of section (e.g., "theory", "findings") for context-aware checks

        Returns:
            ValidationResult with any violations found
        """
        violations = []

        # HARD RULES (apply to all paper types)
        violations.extend(self._check_bullets(text))
        violations.extend(self._check_numbered_lists(text))
        violations.extend(self._check_latex_lists(text))
        violations.extend(self._check_contribution_lists(text))

        # SOFT RULES (apply to all paper types)
        violations.extend(self._check_passive_voice(text))
        violations.extend(self._check_hedging(text))
        violations.extend(self._check_orphaned_results(text, following_text))
        violations.extend(self._check_quote_setup(text, is_cold_open, is_section_open))
        violations.extend(self._check_quote_length(text))

        # QUAL-FORWARD SPECIFIC RULES
        if self.paper_type == PaperType.QUAL_FORWARD:
            violations.extend(self._check_hypothesis_language(text, section_name))
            violations.extend(self._check_mechanism_preview(text, section_name))
            violations.extend(self._check_quote_followthrough(text))
            violations.extend(self._check_speculative_findings(text, section_name))
            # Multimethod inductive checks
            violations.extend(self._check_expected_patterns(text, section_name))
            violations.extend(self._check_enumerated_contributions(text))
            violations.extend(self._check_our_predictions(text, section_name))

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
        in_tablenotes = False
        in_figure_or_table = False

        for i, line in enumerate(lines):
            # Track tablenotes environment (standard LaTeX for table footnotes)
            if r'\begin{tablenotes}' in line:
                in_tablenotes = True
                continue
            if r'\end{tablenotes}' in line:
                in_tablenotes = False
                continue
            if in_tablenotes:
                continue

            # Heuristic: Skip lines that look like figure/table content
            # (short lines with bullets are often from converted PDF figures)
            line_stripped = line.strip()
            if len(line_stripped) < 60 and line_stripped.startswith('•'):
                # Short bullet line - likely from figure/table, skip
                continue

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
        # BUT: skip \item in tablenotes environments (standard LaTeX for table footnotes)
        item_pattern = re.compile(r'\\item\b')
        for match in item_pattern.finditer(text):
            # Get surrounding context
            start = max(0, match.start() - 50)
            end = min(len(text), match.end() + 30)
            context = text[start:end].strip()

            # Skip if this is within a tablenotes environment
            if 'tablenotes' in context.lower():
                continue

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
        # Find BLOCK quotes only (>100 chars to avoid inline quotes)
        # Increased threshold from 50 to 100 to reduce false positives
        quote_pattern = r'["""]([^"""]{100,})["""]|```quote\n(.*?)\n```'

        quotes = list(re.finditer(quote_pattern, text, re.DOTALL))

        if not quotes:
            return []

        # Cold opens are exempt
        if is_cold_open or is_section_open:
            return []

        violations = []

        for match in quotes:
            # Get text before the quote
            before_text = text[:match.start()].strip()

            # Check for analytical claim patterns - expanded to reduce false positives
            # Published papers use many ways to set up quotes
            claim_patterns = [
                r'\w+\s+(described|explained|noted|observed|recalled|stated|said|wrote|argued|suggested)',
                r'(as|like)\s+one\s+\w+\s+(put|said|noted|explained)',
                r'this\s+(pattern|dynamic|mechanism|phenomenon|finding|observation)',
                r'(illustrat|demonstrat|reveal|show|exemplif|captur|indicat)',
                r'(he|she|they|we|I)\s+(found|saw|heard|learned|discovered)',
                r'(interviewee|informant|respondent|participant|surgeon|manager|worker)',
                r'(typical|common|frequent|representative|characteristic)',
                r'(for\s+example|for\s+instance|e\.g\.|such\s+as)',
                r'(according\s+to|in\s+the\s+words\s+of)',
                r':\s*$',  # Colon at end often precedes a quote
            ]

            has_setup = any(
                re.search(p, before_text[-300:], re.IGNORECASE)  # Check last 300 chars
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

    # ==========================================================================
    # QUAL-FORWARD SPECIFIC CHECKS
    # ==========================================================================

    def _check_hypothesis_language(
        self,
        text: str,
        section_name: Optional[str] = None,
    ) -> list[Violation]:
        """
        Check for hypothesis-testing language inappropriate in inductive papers.

        In qual-forward/inductive papers:
        - Hypothesis-testing language is NEVER appropriate
        - Theory is BUILT in findings, not tested
        - Language like "H1 is supported" contradicts inductive logic
        """
        violations = []

        for pattern in self._hypothesis_re:
            match = pattern.search(text)
            if match:
                violations.append(Violation(
                    type=ViolationType.HYPOTHESIS_LANGUAGE_IN_QUAL,
                    severity=Severity.HARD,
                    message="Hypothesis-testing language detected in inductive paper.",
                    location=match.group(0),
                    suggestion="Use theory-building language instead: 'I found that...', "
                              "'This suggests...', 'The data reveal...'. "
                              "Inductive papers BUILD theory through findings, not test hypotheses.",
                ))

        return violations

    def _check_mechanism_preview(
        self,
        text: str,
        section_name: Optional[str] = None,
    ) -> list[Violation]:
        """
        Check for mechanism preview in intro/theory sections.

        In qual-forward papers:
        - Intro/Theory should set up PUZZLE and SENSITIZING CONCEPTS
        - The mechanism (the "punchline") should be held for FINDINGS
        - Previewing the mechanism undermines the inductive logic
        """
        violations = []

        # Only flag in intro and theory sections
        if section_name and section_name.lower() not in ['introduction', 'intro', 'theory', 'theoretical']:
            return []

        for pattern in self._mechanism_preview_re:
            match = pattern.search(text)
            if match:
                violations.append(Violation(
                    type=ViolationType.MECHANISM_PREVIEW_IN_THEORY,
                    severity=Severity.SOFT,
                    message="Mechanism preview detected in intro/theory section.",
                    location=match.group(0),
                    suggestion="In inductive papers, hold the mechanism for findings. "
                              "Intro/theory should set up the PUZZLE and SENSITIZING CONCEPTS, "
                              "not reveal what you found. The reader should be hooked by "
                              "WHAT happened, not told WHY until findings.",
                ))

        return violations

    def _check_quote_followthrough(self, text: str) -> list[Violation]:
        """
        Check that quotes have analytical follow-through, not just setup.

        In qual-forward papers, quotes do heavy argumentative lifting.
        Pattern should be: Setup → Quote → FURTHER DEVELOPMENT
        Not just: Setup → Quote → Next topic
        """
        violations = []

        # Find quotes
        quote_pattern = r'["""]([^"""]{50,})["""]'
        quotes = list(re.finditer(quote_pattern, text, re.DOTALL))

        if not quotes:
            return []

        for match in quotes:
            # Get text after the quote (next 150 chars or to end)
            after_start = match.end()
            after_text = text[after_start:after_start + 150].strip()

            # Check for analytical follow-through
            followthrough_patterns = [
                r'^[^.]*\b(this|these|that|such)\s+\w+\s+(show|reveal|illustrate|demonstrate|suggest|indicate)',
                r'^[^.]*\b(in\s+other\s+words)',
                r'^[^.]*\b(here\s+we\s+see)',
                r'^[^.]*\b(this\s+captures|this\s+illustrates)',
                r'^[^.]*\b(the\s+\w+\s+(here|evident))',
            ]

            has_followthrough = any(
                re.search(p, after_text, re.IGNORECASE)
                for p in followthrough_patterns
            )

            # Also check if it just moves to next topic (weak pattern)
            next_topic_patterns = [
                r'^[^.]{0,30}\.\s*[A-Z]',  # Very short sentence then new topic
                r'^\s*$',  # Nothing after
            ]

            is_orphaned = any(
                re.search(p, after_text[:50])
                for p in next_topic_patterns
            )

            if is_orphaned and not has_followthrough:
                quote_preview = match.group(0)[:50] + "..."
                violations.append(Violation(
                    type=ViolationType.QUOTE_WITHOUT_FOLLOWTHROUGH,
                    severity=Severity.SOFT,
                    message="Quote may lack analytical follow-through.",
                    location=quote_preview,
                    suggestion="After each quote, continue the analytical work. "
                              "Don't just move to the next topic. Pattern: "
                              "Setup → Quote → 'This illustrates how...' or 'Here we see...'",
                ))

        return violations

    # ==========================================================================
    # MULTIMETHOD INDUCTIVE PAPER CHECKS
    # ==========================================================================

    def _check_expected_patterns(
        self,
        text: str,
        section_name: Optional[str] = None,
    ) -> list[Violation]:
        """
        Check for "Expected Patterns" / "Pattern 1/2/3" anti-patterns.

        In multimethod inductive papers, patterns should EMERGE from analysis,
        not be pre-specified. Sections titled "Expected Patterns" or references
        to "Pattern 1", "Pattern 2" indicate hypo-deductive framing.
        """
        violations = []

        for pattern in self._expected_patterns_re:
            match = pattern.search(text)
            if match:
                violations.append(Violation(
                    type=ViolationType.EXPECTED_PATTERNS_SECTION,
                    severity=Severity.HARD,
                    message="Pre-specified pattern language detected in inductive paper.",
                    location=match.group(0),
                    suggestion="Inductive papers discover patterns through analysis, not pre-specify them. "
                              "Replace 'Expected Patterns' with 'Research Questions' or 'Empirical Questions'. "
                              "Replace 'Pattern 1' with descriptive labels that emerged from analysis. "
                              "Reframe 'we expect to observe' as 'we examine whether'.",
                ))

        return violations

    def _check_speculative_findings(
        self,
        text: str,
        section_name: Optional[str] = None,
    ) -> list[Violation]:
        """
        Check for speculative findings language in theory section.

        Theory sections should NOT describe in detail what "might" happen or what
        we "would attend to" if various conditions exist. This speculates findings
        into existence rather than letting them emerge from analysis.

        The theory section should set up sensitizing concepts and ONE compound
        research question, then briefly state what we find (1-2 sentences max).
        """
        violations = []

        # Only check in theory/background sections
        if section_name and section_name.lower() not in ['theory', 'theoretical', 'background', 'lens']:
            return []

        for pattern in self._speculative_findings_re:
            match = pattern.search(text)
            if match:
                violations.append(Violation(
                    type=ViolationType.SPECULATIVE_FINDINGS,
                    severity=Severity.HARD,
                    message="Speculative findings language in theory section.",
                    location=match.group(0),
                    suggestion="Theory section should NOT speculate what 'might' happen or describe "
                              "hypothetical facility types in detail. Instead: (1) Set up sensitizing "
                              "concepts from peer-reviewed literature, (2) Pose ONE compound research "
                              "question, (3) Briefly state what you find (1-2 sentences). "
                              "The detailed typology/framework should emerge in FINDINGS.",
                ))

        return violations

    def _check_enumerated_contributions(self, text: str) -> list[Violation]:
        """
        Check for enumerated contribution patterns.

        Beyond "makes three contributions:", also catches:
        - "First, we contribute... Second, we contribute..."
        - "Our first contribution... Our second contribution..."
        """
        violations = []

        for pattern in self._enumerated_contrib_re:
            match = pattern.search(text)
            if match:
                violations.append(Violation(
                    type=ViolationType.ENUMERATED_CONTRIBUTIONS,
                    severity=Severity.HARD,
                    message="Enumerated contribution pattern detected.",
                    location=match.group(0),
                    suggestion="State contributions as narrative theoretical extensions, not numbered lists. "
                              "Example: 'This research extends X by showing Y. We demonstrate that...' "
                              "The contribution should read as joining a scholarly conversation, not checking boxes.",
                ))

        return violations

    def _check_our_predictions(
        self,
        text: str,
        section_name: Optional[str] = None,
    ) -> list[Violation]:
        """
        Check for prediction language attributable to US (not prior theory).

        It's acceptable to say "Prior work predicts X" or "Standard theory expects Y"
        when setting up a puzzle. It's NOT acceptable to say "We predict" or
        "Our framework suggests X should show" in an inductive paper.
        """
        violations = []

        # Only check in theory sections where this matters most
        if section_name and section_name.lower() not in ['theory', 'theoretical', 'background']:
            return []

        for pattern in self._our_prediction_re:
            match = pattern.search(text)
            if match:
                violations.append(Violation(
                    type=ViolationType.HYPOTHESIS_LANGUAGE_IN_QUAL,
                    severity=Severity.HARD,
                    message="Prediction language attributable to this paper (not prior theory).",
                    location=match.group(0),
                    suggestion="In inductive papers, avoid stating what WE predict/expect. "
                              "Instead: 'This raises the question of whether...' or "
                              "'We examine whether...' or 'This directs attention to...'. "
                              "Describing what PRIOR THEORY predicts is acceptable for setting up puzzles.",
                ))

        return violations

    def check_iterative_methods_present(
        self,
        methods_text: str,
    ) -> Optional[Violation]:
        """
        Check that multimethod inductive papers include iterative analysis language.

        Required elements (at least one):
        - Explicit mention of iterative qual-quant movement
        - Description of puzzle emerging from one data source
        - Description of returning to other data source
        - Statement that framework/typology emerged from this iteration
        """
        has_iterative_indicator = any(
            pattern.search(methods_text)
            for pattern in self._iterative_methods_re
        )

        if not has_iterative_indicator:
            return Violation(
                type=ViolationType.MISSING_ITERATIVE_METHODS,
                severity=Severity.SOFT,  # Soft because some papers may have different structure
                message="Methods section may lack iterative analysis language.",
                suggestion="Multimethod inductive papers should describe how analysis moved "
                          "iteratively between qual and quant data. Example: 'Initial fieldwork "
                          "revealed X. We then examined quantitative data to Y. This puzzle drove "
                          "us back to qualitative evidence, where we found Z. The framework "
                          "presented in findings emerged from this iterative process.'",
            )

        return None


# Convenience function for quick validation
def validate_paragraph(
    text: str,
    is_cold_open: bool = False,
    is_section_open: bool = False,
    paper_type: PaperType = PaperType.QUANT_FORWARD,
    section_name: Optional[str] = None,
) -> ValidationResult:
    """Convenience function for quick paragraph validation."""
    validator = StyleValidator(paper_type=paper_type)
    return validator.validate(
        text,
        is_cold_open,
        is_section_open,
        section_name=section_name,
    )
