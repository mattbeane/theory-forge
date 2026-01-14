"""
Cross-Section Coherence Validator for Inductive Papers.

This module performs semantic analysis across paper sections to detect
structural problems that pattern-matching cannot catch:

1. Pre-announcement: Theory section describes what findings should reveal
2. Mechanism preview: Theory explains WHY before findings provide evidence
3. Missing gap: No clear identification of what's unknown
4. Confirmatory structure: Paper reads as hypothesis-test rather than discovery

The validator operates in two passes:
- Pass 1: Extract contributions from findings/discussion
- Pass 2: Validate that intro/theory set up puzzle/gap, NOT pre-announce findings

Usage:
    validator = CoherenceValidator(llm_client)
    report = validator.validate(paper_sections)

    if report.has_violations:
        print(report.format_report())
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

from .extractors import (
    ContributionExtractor,
    ExtractedContribution,
    TheoryAnalyzer,
    TheoryAnalysis,
    PreannouncementEvidence,
)


class CoherenceViolationType(Enum):
    """Types of cross-section coherence violations."""
    # Theory section pre-announces findings
    FINDINGS_PREANNOUNCED = "findings_preannounced"

    # Theory section describes mechanism that should emerge from findings
    MECHANISM_PREANNOUNCED = "mechanism_preannounced"

    # No clear gap identified before research question
    MISSING_GAP_STATEMENT = "missing_gap_statement"

    # Research question doesn't follow from gap
    RQ_GAP_MISMATCH = "rq_gap_mismatch"

    # Research question doesn't match what findings actually answer
    RQ_FINDINGS_MISMATCH = "rq_findings_mismatch"

    # Theory section has more detail about "our" framework than prior lit
    THEORY_IMBALANCE = "theory_imbalance"

    # Findings feel confirmatory rather than discovery (holistic assessment)
    CONFIRMATORY_STRUCTURE = "confirmatory_structure"


@dataclass
class CoherenceViolation:
    """A cross-section coherence violation."""
    type: CoherenceViolationType
    severity: str  # "critical", "warning", "info"
    message: str
    evidence: Optional[str] = None
    suggestion: Optional[str] = None


@dataclass
class CoherenceReport:
    """Report from cross-section coherence validation."""
    contributions: list[ExtractedContribution] = field(default_factory=list)
    theory_analysis: Optional[TheoryAnalysis] = None
    violations: list[CoherenceViolation] = field(default_factory=list)
    structure_rating: int = 0  # 1-5 scale

    @property
    def has_violations(self) -> bool:
        return len(self.violations) > 0

    @property
    def critical_count(self) -> int:
        return sum(1 for v in self.violations if v.severity == "critical")

    @property
    def warning_count(self) -> int:
        return sum(1 for v in self.violations if v.severity == "warning")

    @property
    def is_properly_inductive(self) -> bool:
        return self.structure_rating >= 4 and self.critical_count == 0

    def format_report(self) -> str:
        """Format the report for display."""
        lines = []
        lines.append("=" * 60)
        lines.append("CROSS-SECTION COHERENCE ANALYSIS")
        lines.append("=" * 60)

        # Contributions summary
        lines.append("\nEXTRACTED CONTRIBUTIONS (from Findings/Discussion):")
        if self.contributions:
            for i, c in enumerate(self.contributions, 1):
                concept = f" ['{c.named_concept_if_any}']" if c.named_concept_if_any else ""
                lines.append(f"  {i}. {c.claim}{concept}")
        else:
            lines.append("  (No contributions extracted)")

        # Theory analysis
        if self.theory_analysis:
            lines.append("\nTHEORY SECTION ANALYSIS:")

            # Gap statement
            if self.theory_analysis.gap_statement:
                lines.append(f"\n  Gap Statement: Present")
                lines.append(f"    \"{self.theory_analysis.gap_statement[:200]}...\"")
            else:
                lines.append(f"\n  Gap Statement: MISSING")

            # Research questions
            if self.theory_analysis.research_questions:
                lines.append(f"\n  Research Questions:")
                for rq in self.theory_analysis.research_questions:
                    lines.append(f"    - {rq}")

            # Pre-announcements
            if self.theory_analysis.preannouncements:
                lines.append(f"\n  PRE-ANNOUNCEMENTS DETECTED ({len(self.theory_analysis.preannouncements)}):")
                for pa in self.theory_analysis.preannouncements:
                    lines.append(f"\n  \u26a0\ufe0f  {pa.severity.upper()} SEVERITY")
                    lines.append(f"      Finding: \"{pa.finding_claim[:100]}...\"")
                    lines.append(f"      Theory text: \"{pa.theory_text[:150]}...\"")
                    lines.append(f"      Issue: {pa.similarity_explanation}")

        # Violations
        if self.violations:
            lines.append("\n" + "-" * 60)
            lines.append("VIOLATIONS:")
            for v in self.violations:
                icon = "\u274c" if v.severity == "critical" else "\u26a0\ufe0f"
                lines.append(f"\n{icon} [{v.severity.upper()}] {v.type.value}")
                lines.append(f"   {v.message}")
                if v.evidence:
                    lines.append(f"   Evidence: \"{v.evidence[:150]}...\"")
                if v.suggestion:
                    lines.append(f"   Suggestion: {v.suggestion}")

        # Overall assessment
        lines.append("\n" + "-" * 60)
        lines.append("OVERALL STRUCTURE RATING:")
        rating_desc = {
            5: "Pure inductive (discovery)",
            4: "Mostly inductive",
            3: "Mixed (some preview)",
            2: "Mostly deductive (confirmatory)",
            1: "Pure deductive (confirmation)",
        }
        desc = rating_desc.get(self.structure_rating, "Unknown")
        lines.append(f"  {self.structure_rating}/5 - {desc}")

        if self.is_properly_inductive:
            lines.append("\n\u2705 Paper has proper inductive structure.")
        else:
            lines.append("\n\u274c Paper needs structural revision for inductive framing.")
            if self.theory_analysis and self.theory_analysis.preannouncements:
                lines.append("   Key issue: Theory section pre-announces findings.")
                lines.append("   Recommendation: Rewrite theory to end with genuine")
                lines.append("   questions, not previewed answers.")

        lines.append("\n" + "=" * 60)
        return "\n".join(lines)


class CoherenceValidator:
    """
    Validates cross-section coherence for inductive papers.

    The validator extracts what the paper claims as contributions from
    findings/discussion, then checks whether intro/theory properly set up
    a puzzle and gap WITHOUT pre-announcing those findings.
    """

    def __init__(self, llm_client: Any):
        """
        Initialize with an LLM client.

        Args:
            llm_client: Any LLM client with a chat()/generate() method.
        """
        self.llm = llm_client
        self.contribution_extractor = ContributionExtractor(llm_client)
        self.theory_analyzer = TheoryAnalyzer(llm_client)

    def validate(
        self,
        paper_sections: dict[str, str],
    ) -> CoherenceReport:
        """
        Validate cross-section coherence of a paper.

        Args:
            paper_sections: Dictionary mapping section names to text.
                          Expected keys: "introduction", "theory", "findings", "discussion"

        Returns:
            CoherenceReport with analysis and violations
        """
        # Normalize section names
        sections = self._normalize_sections(paper_sections)

        # Step 1: Extract what the paper claims as contributions
        contributions = self.contribution_extractor.extract(
            findings=sections.get("findings", ""),
            discussion=sections.get("discussion", ""),
        )

        # Step 2: Analyze theory section structure
        theory_analysis = self.theory_analyzer.analyze(
            intro=sections.get("introduction", ""),
            theory=sections.get("theory", ""),
            contributions=contributions,
        )

        # Step 3: Check for structural coherence violations
        violations = self._check_coherence(contributions, theory_analysis)

        return CoherenceReport(
            contributions=contributions,
            theory_analysis=theory_analysis,
            violations=violations,
            structure_rating=theory_analysis.structure_rating if theory_analysis else 0,
        )

    def _normalize_sections(self, sections: dict[str, str]) -> dict[str, str]:
        """Normalize section name variations."""
        normalized = {}

        for key, value in sections.items():
            key_lower = key.lower()

            if any(k in key_lower for k in ["intro", "introduction"]):
                normalized["introduction"] = value
            elif any(k in key_lower for k in ["theory", "theoretical", "background", "literature", "lens"]):
                normalized["theory"] = value
            elif any(k in key_lower for k in ["finding", "result", "empirical"]):
                normalized["findings"] = value
            elif any(k in key_lower for k in ["discussion", "contribution", "conclusion"]):
                normalized["discussion"] = value
            elif "method" in key_lower:
                normalized["methods"] = value
            else:
                normalized[key_lower] = value

        return normalized

    def _check_coherence(
        self,
        contributions: list[ExtractedContribution],
        theory_analysis: Optional[TheoryAnalysis],
    ) -> list[CoherenceViolation]:
        """Generate violations based on extracted data and analysis."""
        violations = []

        if not theory_analysis:
            return violations

        # Check for pre-announcements (most critical)
        for pa in theory_analysis.preannouncements:
            severity = "critical" if pa.severity == "high" else "warning"
            violations.append(CoherenceViolation(
                type=CoherenceViolationType.FINDINGS_PREANNOUNCED,
                severity=severity,
                message=f"Theory section pre-announces finding: '{pa.finding_claim[:80]}...'",
                evidence=pa.theory_text,
                suggestion="Rewrite theory to set up the QUESTION without answering it. "
                          "The mechanism/framework should EMERGE in findings, not be "
                          "previewed in theory.",
            ))

        # Check for mechanism pre-announcements specifically
        mechanism_contributions = [
            c for c in contributions
            if c.mechanism_if_any
        ]
        for mc in mechanism_contributions:
            # Check if any preannouncement relates to a mechanism
            for pa in theory_analysis.preannouncements:
                if mc.mechanism_if_any and mc.mechanism_if_any.lower() in pa.theory_text.lower():
                    violations.append(CoherenceViolation(
                        type=CoherenceViolationType.MECHANISM_PREANNOUNCED,
                        severity="critical",
                        message=f"Mechanism '{mc.mechanism_if_any[:50]}...' explained in "
                               f"theory before findings reveal it.",
                        evidence=pa.theory_text,
                        suggestion="In inductive papers, the mechanism (WHY things happen) "
                                  "should be discovered through analysis, not previewed "
                                  "in theory. Remove mechanism explanation from theory section.",
                    ))

        # Check for missing gap statement
        if not theory_analysis.gap_statement:
            violations.append(CoherenceViolation(
                type=CoherenceViolationType.MISSING_GAP_STATEMENT,
                severity="warning",
                message="No clear gap statement identified in theory section.",
                suggestion="Theory should explicitly identify what prior work "
                          "hasn't explained. E.g., 'Prior work has focused on X, "
                          "but we don't know Y' or 'Existing theory assumes Z, "
                          "yet this leaves unexplained...'",
            ))

        # Check for confirmatory overall structure
        if theory_analysis.structure_rating <= 2:
            violations.append(CoherenceViolation(
                type=CoherenceViolationType.CONFIRMATORY_STRUCTURE,
                severity="critical",
                message=f"Paper has confirmatory (deductive) structure "
                       f"(rating: {theory_analysis.structure_rating}/5).",
                suggestion="Restructure so theory poses QUESTIONS and findings "
                          "provide ANSWERS. Reader should experience findings as "
                          "discovery, not confirmation of what theory already said.",
            ))
        elif theory_analysis.structure_rating == 3:
            violations.append(CoherenceViolation(
                type=CoherenceViolationType.CONFIRMATORY_STRUCTURE,
                severity="warning",
                message=f"Paper has mixed inductive/deductive structure "
                       f"(rating: {theory_analysis.structure_rating}/5).",
                suggestion="Review theory section for any text that previews "
                          "findings. Even partial preview weakens the inductive logic.",
            ))

        return violations


def validate_paper_coherence(
    paper_sections: dict[str, str],
    llm_client: Any,
) -> CoherenceReport:
    """
    Convenience function for quick coherence validation.

    Args:
        paper_sections: Dictionary mapping section names to text
        llm_client: LLM client for semantic analysis

    Returns:
        CoherenceReport with analysis and violations
    """
    validator = CoherenceValidator(llm_client)
    return validator.validate(paper_sections)
