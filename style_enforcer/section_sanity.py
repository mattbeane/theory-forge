"""
Section Sanity Checker - Section-level validation beyond paragraph rules.

This module catches issues that only become visible at the section level:
1. Methods section accuracy against actual research process
2. Figure/table references matching available files
3. Data claims matching available data sources
4. Section coherence and flow
5. Required elements presence

Key insight: Paragraph-level validation misses structural problems.
The Methods section can pass all style rules but still be factually wrong.
"""

import re
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
from pathlib import Path

from .config import PaperType
from .data_inventory import DataInventory, InventoryResult, DataType
from .statistics_validator import StatisticsValidator, ValidationReport


class SanityIssueType(Enum):
    """Types of section-level issues."""
    MISSING_FIGURE = "missing_figure"
    MISSING_TABLE = "missing_table"
    MISSING_DATA_SOURCE = "missing_data_source"
    METHODS_MISMATCH = "methods_mismatch"
    MISSING_ELEMENT = "missing_element"
    COHERENCE_ISSUE = "coherence_issue"
    UNVERIFIED_STAT = "unverified_stat"
    PLACEHOLDER_REMAINING = "placeholder_remaining"


class IssueSeverity(Enum):
    """Severity of section issues."""
    CRITICAL = "critical"   # Must fix before submission
    WARNING = "warning"     # Should fix
    INFO = "info"           # May want to address


@dataclass
class SanityIssue:
    """A section-level sanity issue."""
    issue_type: SanityIssueType
    severity: IssueSeverity
    section: str
    message: str
    location: Optional[str] = None
    suggestion: Optional[str] = None


@dataclass
class SanityReport:
    """Report from section sanity check."""
    section_name: str
    issues: list[SanityIssue]
    critical_count: int
    warning_count: int
    passed: bool

    @property
    def needs_attention(self) -> bool:
        """Whether there are issues needing attention."""
        return self.critical_count > 0 or self.warning_count > 0


class SectionSanityChecker:
    """
    Performs section-level sanity checks beyond style validation.

    This catches issues that paragraph-level validation misses:
    - Methods section accuracy
    - Figure/table references
    - Data availability
    - Required section elements

    Usage:
        checker = SectionSanityChecker()

        # Load data inventory
        inventory = DataInventory().scan("/path/to/data")

        # Check methods section
        report = checker.check_methods(
            methods_text=methods_section,
            inventory=inventory,
            actual_process="iterative mixed-method: qual discovery, survey design, quant analysis, triangulation"
        )

        # Check findings section
        report = checker.check_findings(
            findings_text=findings_section,
            inventory=inventory,
            figures_path=Path("/path/to/figures"),
        )
    """

    # Required elements by section - QUANT-FORWARD (default)
    REQUIRED_ELEMENTS_QUANT = {
        "abstract": ["research question", "method", "finding", "contribution"],
        "introduction": ["hook", "gap", "contribution", "roadmap"],
        "theory": ["literature review", "theoretical framework", "mechanism"],
        "methods": ["setting", "data collection", "analysis approach", "validity"],
        "findings": ["main finding", "evidence", "mechanism"],
        "discussion": ["contribution", "implications", "limitations", "future research"],
    }

    # Required elements by section - QUAL-FORWARD / INDUCTIVE
    # Key differences:
    # - Theory: sensitizing concepts, NOT mechanism preview
    # - Findings: progressive concept development, phenomenon naming
    # - Methods: embeddedness, access story
    REQUIRED_ELEMENTS_QUAL = {
        "abstract": ["research question", "method", "phenomenon naming", "contribution"],
        "introduction": ["puzzle", "gap", "contribution preview", "roadmap"],
        "theory": ["sensitizing concepts", "prior work", "what prior work assumes", "research question"],
        "methods": ["setting", "access", "embeddedness", "data sources", "analysis approach"],
        "findings": ["progressive development", "phenomenon naming", "evidence", "emergent model"],
        "discussion": ["theoretical contribution", "connection to prior work", "implications", "limitations", "future research"],
    }

    # Backward compatibility alias
    REQUIRED_ELEMENTS = REQUIRED_ELEMENTS_QUANT

    # Patterns for detecting placeholders left in text
    PLACEHOLDER_PATTERNS = [
        r'\[TODO[^\]]*\]',
        r'\[TBD[^\]]*\]',
        r'\[PLACEHOLDER[^\]]*\]',
        r'\[INSERT[^\]]*\]',
        r'\[PENDING[^\]]*\]',
        r'\[AWAITING[^\]]*\]',
        r'XXX',
        r'\?\?\?',
    ]

    # Figure/table reference patterns
    FIGURE_REF_PATTERN = re.compile(r'[Ff]igure\s+(\d+)')
    TABLE_REF_PATTERN = re.compile(r'[Tt]able\s+(\d+)')

    def __init__(self, paper_type: PaperType = PaperType.QUANT_FORWARD):
        """Initialize the sanity checker.

        Args:
            paper_type: QUAL_FORWARD or QUANT_FORWARD (affects required elements)
        """
        self._placeholder_re = [re.compile(p, re.IGNORECASE) for p in self.PLACEHOLDER_PATTERNS]
        self._stats_validator = StatisticsValidator()
        self.paper_type = paper_type

    def check_section(
        self,
        section_name: str,
        section_text: str,
        inventory: Optional[InventoryResult] = None,
        figures_path: Optional[Path] = None,
        tables_path: Optional[Path] = None,
    ) -> SanityReport:
        """
        Perform sanity check on a section.

        Args:
            section_name: Name of the section (e.g., "methods", "findings")
            section_text: The section text
            inventory: Data inventory
            figures_path: Path to figures directory
            tables_path: Path to tables directory

        Returns:
            SanityReport with any issues found
        """
        issues = []

        # Check for remaining placeholders
        issues.extend(self._check_placeholders(section_name, section_text))

        # Check figure/table references
        if figures_path:
            issues.extend(self._check_figure_refs(section_name, section_text, figures_path))
        if tables_path:
            issues.extend(self._check_table_refs(section_name, section_text, tables_path))

        # Check statistics if we have inventory
        if inventory:
            issues.extend(self._check_statistics(section_name, section_text, inventory))

        # Check required elements
        issues.extend(self._check_required_elements(section_name, section_text))

        critical = sum(1 for i in issues if i.severity == IssueSeverity.CRITICAL)
        warning = sum(1 for i in issues if i.severity == IssueSeverity.WARNING)

        return SanityReport(
            section_name=section_name,
            issues=issues,
            critical_count=critical,
            warning_count=warning,
            passed=critical == 0,
        )

    def check_methods(
        self,
        methods_text: str,
        inventory: Optional[InventoryResult] = None,
        actual_process: Optional[str] = None,
    ) -> SanityReport:
        """
        Special check for Methods section accuracy.

        The Methods section is where hallucination is most dangerous—
        describing a research process that didn't happen.

        Args:
            methods_text: The methods section text
            inventory: Data inventory
            actual_process: Description of actual research process

        Returns:
            SanityReport
        """
        issues = self.check_section("methods", methods_text, inventory).issues

        # Check for common methods hallucinations
        issues.extend(self._check_methods_hallucinations(methods_text, inventory))

        # Check against actual process if provided
        if actual_process:
            issues.extend(self._check_methods_accuracy(methods_text, actual_process))

        critical = sum(1 for i in issues if i.severity == IssueSeverity.CRITICAL)
        warning = sum(1 for i in issues if i.severity == IssueSeverity.WARNING)

        return SanityReport(
            section_name="methods",
            issues=issues,
            critical_count=critical,
            warning_count=warning,
            passed=critical == 0,
        )

    def check_findings(
        self,
        findings_text: str,
        inventory: Optional[InventoryResult] = None,
        figures_path: Optional[Path] = None,
        tables_path: Optional[Path] = None,
    ) -> SanityReport:
        """
        Check Findings section for data integrity.

        Args:
            findings_text: The findings section text
            inventory: Data inventory
            figures_path: Path to figures
            tables_path: Path to tables

        Returns:
            SanityReport
        """
        return self.check_section(
            section_name="findings",
            section_text=findings_text,
            inventory=inventory,
            figures_path=figures_path,
            tables_path=tables_path,
        )

    def _check_placeholders(
        self,
        section_name: str,
        text: str,
    ) -> list[SanityIssue]:
        """Check for remaining placeholders."""
        issues = []

        for pattern in self._placeholder_re:
            for match in pattern.finditer(text):
                issues.append(SanityIssue(
                    issue_type=SanityIssueType.PLACEHOLDER_REMAINING,
                    severity=IssueSeverity.CRITICAL,
                    section=section_name,
                    message=f"Placeholder remaining in text: {match.group(0)}",
                    location=match.group(0),
                    suggestion="Fill in placeholder or remove section",
                ))

        return issues

    def _check_figure_refs(
        self,
        section_name: str,
        text: str,
        figures_path: Path,
    ) -> list[SanityIssue]:
        """Check that referenced figures exist."""
        issues = []

        # Find all figure references
        for match in self.FIGURE_REF_PATTERN.finditer(text):
            fig_num = match.group(1)

            # Look for figure file
            figure_exists = self._figure_file_exists(figures_path, fig_num)

            if not figure_exists:
                issues.append(SanityIssue(
                    issue_type=SanityIssueType.MISSING_FIGURE,
                    severity=IssueSeverity.CRITICAL,
                    section=section_name,
                    message=f"Figure {fig_num} referenced but file not found",
                    location=f"Figure {fig_num}",
                    suggestion=f"Add figure file to {figures_path} or remove reference",
                ))

        return issues

    def _figure_file_exists(self, figures_path: Path, fig_num: str) -> bool:
        """Check if a figure file exists."""
        if not figures_path.exists():
            return False

        # Try common naming patterns
        patterns = [
            f"fig{fig_num}.*",
            f"figure{fig_num}.*",
            f"Figure{fig_num}.*",
            f"fig_{fig_num}.*",
            f"figure_{fig_num}.*",
        ]

        for pattern in patterns:
            matches = list(figures_path.glob(pattern))
            if matches:
                return True

        return False

    def _check_table_refs(
        self,
        section_name: str,
        text: str,
        tables_path: Path,
    ) -> list[SanityIssue]:
        """Check that referenced tables exist."""
        issues = []

        for match in self.TABLE_REF_PATTERN.finditer(text):
            table_num = match.group(1)

            # Tables are often in the document itself (LaTeX), so this is less critical
            # But flag if tables_path was provided and file doesn't exist
            if tables_path and tables_path.exists():
                table_exists = self._table_file_exists(tables_path, table_num)
                if not table_exists:
                    issues.append(SanityIssue(
                        issue_type=SanityIssueType.MISSING_TABLE,
                        severity=IssueSeverity.WARNING,
                        section=section_name,
                        message=f"Table {table_num} referenced; verify it exists in document",
                        location=f"Table {table_num}",
                    ))

        return issues

    def _table_file_exists(self, tables_path: Path, table_num: str) -> bool:
        """Check if a table file exists."""
        patterns = [
            f"table{table_num}.*",
            f"Table{table_num}.*",
            f"tab{table_num}.*",
        ]

        for pattern in patterns:
            matches = list(tables_path.glob(pattern))
            if matches:
                return True

        return False

    def _check_statistics(
        self,
        section_name: str,
        text: str,
        inventory: InventoryResult,
    ) -> list[SanityIssue]:
        """Check statistical claims against available data."""
        issues = []

        stats_report = self._stats_validator.validate(text, inventory)

        for claim in stats_report.get_suspicious():
            issues.append(SanityIssue(
                issue_type=SanityIssueType.UNVERIFIED_STAT,
                severity=IssueSeverity.CRITICAL,
                section=section_name,
                message=f"Suspicious statistic: {claim.raw_text}",
                location=claim.location,
                suggestion=claim.notes,
            ))

        for claim in stats_report.get_unverified():
            # Only flag as critical if we have no data source
            severity = (
                IssueSeverity.CRITICAL
                if claim.notes and "no" in claim.notes.lower() and "data" in claim.notes.lower()
                else IssueSeverity.WARNING
            )
            issues.append(SanityIssue(
                issue_type=SanityIssueType.UNVERIFIED_STAT,
                severity=severity,
                section=section_name,
                message=f"Unverified statistic: {claim.raw_text}",
                location=claim.location,
                suggestion="Verify against source data",
            ))

        return issues

    def _check_required_elements(
        self,
        section_name: str,
        text: str,
    ) -> list[SanityIssue]:
        """Check for required section elements."""
        issues = []

        # Select requirements based on paper type
        if self.paper_type == PaperType.QUAL_FORWARD:
            requirements = self.REQUIRED_ELEMENTS_QUAL
        else:
            requirements = self.REQUIRED_ELEMENTS_QUANT

        required = requirements.get(section_name.lower(), [])
        text_lower = text.lower()

        # This is a heuristic check - look for keywords
        # Includes both quant and qual-specific keywords
        element_keywords = {
            # Common elements
            "research question": ["question", "ask", "investigate", "examine", "explore"],
            "method": ["method", "approach", "design", "collected", "analyzed"],
            "finding": ["find", "show", "reveal", "demonstrate", "evidence"],
            "contribution": ["contribut", "extend", "advance", "shed light"],
            "hook": ["puzzle", "surprising", "paradox", "tension"],
            "gap": ["gap", "missing", "underexplored", "limited understanding"],
            "roadmap": ["proceed", "organize", "section", "first", "then"],
            "literature review": ["literature", "prior", "research", "scholar"],
            "theoretical framework": ["theor", "framework", "mechanism", "predict"],
            "mechanism": ["mechanism", "process", "dynamic", "how", "why"],
            "setting": ["setting", "site", "organization", "company", "warehouse", "hospital", "factory"],
            "data collection": ["collect", "gather", "interview", "observe", "survey"],
            "analysis approach": ["analyz", "cod", "process", "approach"],
            "validity": ["valid", "reliable", "robust", "triangulat"],
            "implications": ["implic", "practitioner", "manager", "organization"],
            "limitations": ["limit", "caveat", "boundary", "caution"],
            "future research": ["future", "further", "additional research"],

            # Qual-forward specific elements
            "puzzle": ["puzzle", "surprising", "paradox", "counterintuit", "unexpected"],
            "contribution preview": ["contribut", "extend", "shed light", "advance"],
            "sensitizing concepts": ["prior", "literature", "concept", "lens", "framework", "approach"],
            "prior work": ["prior", "literature", "research", "scholar", "studies"],
            "what prior work assumes": ["assumes", "taken for granted", "overlook", "neglect", "ignore"],
            "access": ["access", "gained entry", "negotiated", "introduced", "relationship"],
            "embeddedness": ["embedded", "immersed", "spent", "months", "years", "observed", "participated"],
            "data sources": ["interview", "observation", "archiv", "document", "field note"],
            "progressive development": ["first", "second", "third", "phase", "stage", "began", "then", "subsequently"],
            "phenomenon naming": ["term", "call", "label", "named", "concept", "phenomenon"],
            "evidence": ["quote", "said", "explained", "described", "observed", "data", "evidence"],
            "emergent model": ["model", "framework", "process", "dynamic", "mechanism", "explain"],
            "theoretical contribution": ["contribut", "extend", "theory", "conceptual", "advance"],
            "connection to prior work": ["prior", "literature", "extend", "build on", "contrast with"],
        }

        for element in required:
            keywords = element_keywords.get(element, [element])
            found = any(kw in text_lower for kw in keywords)

            if not found:
                issues.append(SanityIssue(
                    issue_type=SanityIssueType.MISSING_ELEMENT,
                    severity=IssueSeverity.WARNING,
                    section=section_name,
                    message=f"Required element may be missing: {element}",
                    suggestion=f"Ensure {element} is addressed in this section",
                ))

        return issues

    def _check_methods_hallucinations(
        self,
        text: str,
        inventory: Optional[InventoryResult],
    ) -> list[SanityIssue]:
        """Check for common methods section hallucinations."""
        issues = []

        # Check for survey claims without survey data
        survey_claims = [
            r'survey\s+data',
            r'questionnaire',
            r'response\s+rate',
            r'weekly\s+survey',
            r'daily\s+survey',
        ]

        if inventory and not inventory.has_data_type(DataType.SURVEY):
            for pattern in survey_claims:
                if re.search(pattern, text, re.IGNORECASE):
                    issues.append(SanityIssue(
                        issue_type=SanityIssueType.MISSING_DATA_SOURCE,
                        severity=IssueSeverity.CRITICAL,
                        section="methods",
                        message=f"Survey method described but no survey data found",
                        suggestion="Remove survey claims or verify data availability",
                    ))
                    break

        # Check for interview count claims without transcripts
        interview_pattern = r'(\d+)\s*(?:semi-structured\s+)?interviews?'
        if inventory and not inventory.has_data_type(DataType.INTERVIEW):
            match = re.search(interview_pattern, text, re.IGNORECASE)
            if match:
                issues.append(SanityIssue(
                    issue_type=SanityIssueType.MISSING_DATA_SOURCE,
                    severity=IssueSeverity.WARNING,
                    section="methods",
                    message=f"Interview count ({match.group(1)}) stated but no transcript files found",
                    suggestion="Verify interview count against actual transcripts",
                ))

        return issues

    def _check_methods_accuracy(
        self,
        methods_text: str,
        actual_process: str,
    ) -> list[SanityIssue]:
        """
        Check if methods description matches actual research process.

        This is a heuristic check comparing key terms.
        """
        issues = []

        # Extract key process terms from actual process
        process_lower = actual_process.lower()
        methods_lower = methods_text.lower()

        # Key terms that should appear if mentioned in actual process
        key_terms = [
            ("iterative", "iterative"),
            ("mixed-method", "mixed method"),
            ("triangulat", "triangulat"),
            ("qual", "qualitative"),
            ("quant", "quantitative"),
            ("survey", "survey"),
            ("interview", "interview"),
            ("ethnograph", "ethnograph"),
            ("observation", "observ"),
        ]

        for process_term, methods_term in key_terms:
            # If it's in the actual process but not in methods
            if process_term in process_lower and methods_term not in methods_lower:
                issues.append(SanityIssue(
                    issue_type=SanityIssueType.METHODS_MISMATCH,
                    severity=IssueSeverity.WARNING,
                    section="methods",
                    message=f"Actual process includes '{process_term}' but Methods doesn't mention '{methods_term}'",
                    suggestion=f"Consider adding description of {process_term} approach",
                ))

        return issues


def check_manuscript_sanity(
    sections: dict[str, str],
    paper_path: Optional[str] = None,
    paper_type: PaperType = PaperType.QUANT_FORWARD,
) -> dict[str, SanityReport]:
    """
    Convenience function to check all sections of a manuscript.

    Args:
        sections: Dict mapping section names to section text
        paper_path: Path to paper directory (for data/figures)
        paper_type: QUAL_FORWARD or QUANT_FORWARD (affects required elements)

    Returns:
        Dict mapping section names to SanityReports
    """
    checker = SectionSanityChecker(paper_type=paper_type)
    reports = {}

    # Set up paths
    inventory = None
    figures_path = None

    if paper_path:
        paper_dir = Path(paper_path)
        data_path = paper_dir / "data"
        figures_path = paper_dir / "figures"

        if not figures_path.exists():
            figures_path = paper_dir / "submission" / "figures"

        if data_path.exists():
            inventory = DataInventory().scan(data_path)

    for section_name, section_text in sections.items():
        reports[section_name] = checker.check_section(
            section_name=section_name,
            section_text=section_text,
            inventory=inventory,
            figures_path=figures_path,
        )

    return reports
