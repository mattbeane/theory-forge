"""
Manuscript Orchestrator - Controls section-by-section generation with validation.

This is the main entry point for generating a style-compliant manuscript.
It coordinates:
- Section-by-section generation with appropriate exemplars
- Paragraph-level validation
- Automatic fixing of violations
- Section-level review (with sanity checks)
- Statistics verification against available data
- Budget tracking (words, quotes, tables)

New in v2: Integrates DataInventory, StatisticsValidator, and SectionSanityChecker
to prevent hallucination of statistics and ensure methods accuracy.
"""

import json
from dataclasses import dataclass, field
from typing import Optional, Callable, Any
from enum import Enum
from pathlib import Path

from .config import ManuscriptConfig, SectionConfig, PaperType, QUOTE_SELECTION_GUIDANCE, COLD_OPEN_GUIDANCE
from .validator import StyleValidator, ValidationResult, Severity
from .exemplars import ExemplarDB, get_section_prompt_with_exemplar
from .prompts import (
    SECTION_WRITER_SYSTEM,
    QUANT_FORWARD_GUIDANCE,
    QUAL_FORWARD_GUIDANCE,
    PARAGRAPH_FIXER_PROMPT,
    SECTION_REVIEW_PROMPT,
    OPENING_ALTERNATIVES_PROMPT,
)

# New validation modules
from .data_inventory import DataInventory, InventoryResult, scan_paper_data
from .statistics_validator import StatisticsValidator, ValidationReport as StatsReport
from .section_sanity import SectionSanityChecker, SanityReport


class GenerationStatus(Enum):
    """Status of generation process."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    VALIDATING = "validating"
    FIXING = "fixing"
    COMPLETE = "complete"
    FAILED = "failed"


@dataclass
class SectionDraft:
    """A draft of a manuscript section."""
    name: str
    content: str
    word_count: int
    quote_count: int
    table_count: int
    validation_result: Optional[ValidationResult] = None
    status: GenerationStatus = GenerationStatus.PENDING
    revision_count: int = 0


@dataclass
class ManuscriptState:
    """Current state of manuscript generation."""
    config: ManuscriptConfig
    sections: dict[str, SectionDraft] = field(default_factory=dict)
    total_words: int = 0
    total_quotes: int = 0
    total_tables: int = 0

    def to_dict(self) -> dict:
        """Serialize state for checkpointing."""
        return {
            "sections": {
                name: {
                    "content": draft.content,
                    "word_count": draft.word_count,
                    "status": draft.status.value,
                }
                for name, draft in self.sections.items()
            },
            "total_words": self.total_words,
            "total_quotes": self.total_quotes,
        }


@dataclass
class GenerationResult:
    """Result of generating a section or paragraph."""
    success: bool
    content: str
    violations: list[str] = field(default_factory=list)
    was_fixed: bool = False
    fix_iterations: int = 0
    sanity_report: Optional[SanityReport] = None
    stats_report: Optional[StatsReport] = None
    warnings: list[str] = field(default_factory=list)


class ManuscriptOrchestrator:
    """
    Orchestrates manuscript generation with style enforcement.

    Usage:
        # Initialize with config
        orchestrator = ManuscriptOrchestrator(
            config=QUANT_FORWARD_ORGSCI,
            llm_call=my_llm_function,  # Function that calls your LLM
        )

        # Generate a section
        result = orchestrator.generate_section(
            section_name="introduction",
            paper_plan=my_paper_plan,
            evidence=my_evidence,
        )

        # Or generate entire manuscript
        manuscript = orchestrator.generate_manuscript(
            paper_plan=full_paper_plan,
            evidence=all_evidence,
        )
    """

    def __init__(
        self,
        config: ManuscriptConfig,
        llm_call: Callable[[str, str], str],
        max_fix_iterations: int = 3,
        verbose: bool = True,
        paper_path: Optional[str | Path] = None,
    ):
        """
        Initialize orchestrator.

        Args:
            config: Manuscript configuration
            llm_call: Function(system_prompt, user_prompt) -> response
            max_fix_iterations: Max times to retry fixing a paragraph
            verbose: Whether to print progress
            paper_path: Path to paper directory (for data inventory, figures)
        """
        self.config = config
        self.llm_call = llm_call
        self.max_fix_iterations = max_fix_iterations
        self.verbose = verbose
        self.paper_path = Path(paper_path) if paper_path else None

        # Core validators
        self.validator = StyleValidator()
        self.exemplar_db = ExemplarDB()
        self.state = ManuscriptState(config=config)

        # New validators for hallucination prevention
        self.stats_validator = StatisticsValidator()
        self.sanity_checker = SectionSanityChecker()

        # Data inventory (if paper path provided)
        self.data_inventory: Optional[InventoryResult] = None
        self.figures_path: Optional[Path] = None

        if self.paper_path:
            self._load_data_inventory()

    def generate_section(
        self,
        section_name: str,
        paper_plan: dict[str, Any],
        evidence: dict[str, Any],
        allow_cold_open: bool = False,
    ) -> GenerationResult:
        """
        Generate a single section with style enforcement.

        Args:
            section_name: Name of section to generate
            paper_plan: Plan for this section (structure, arguments, etc.)
            evidence: Data/quotes/tables to incorporate
            allow_cold_open: Whether a cold open is permitted

        Returns:
            GenerationResult with final content
        """
        section_config = self.config.get_section(section_name)

        if self.verbose:
            print(f"\n{'='*60}")
            print(f"Generating section: {section_name}")
            print(f"{'='*60}")

        # Build the system prompt
        system_prompt = self._build_section_system_prompt(section_config)

        # Build the user prompt with evidence and plan
        user_prompt = self._build_section_user_prompt(
            section_config=section_config,
            paper_plan=paper_plan,
            evidence=evidence,
            allow_cold_open=allow_cold_open,
        )

        # Generate initial draft
        if self.verbose:
            print("Generating initial draft...")

        draft = self.llm_call(system_prompt, user_prompt)

        # Validate and fix paragraph by paragraph
        paragraphs = self._split_paragraphs(draft)
        validated_paragraphs = []

        for i, para in enumerate(paragraphs):
            is_section_open = (i == 0)

            result = self._validate_and_fix_paragraph(
                paragraph=para,
                is_cold_open=(allow_cold_open and i == 0),
                is_section_open=is_section_open,
                section_config=section_config,
            )

            validated_paragraphs.append(result.content)

            if self.verbose and result.was_fixed:
                print(f"  Paragraph {i+1}: Fixed after {result.fix_iterations} iterations")

        # Reassemble section
        final_content = "\n\n".join(validated_paragraphs)

        # Section-level review
        if self.verbose:
            print("Running section-level review...")

        review_result = self._review_section(final_content, section_config)

        # NEW: Run sanity checks
        sanity_report = None
        stats_report = None
        warnings = []

        if self.verbose:
            print("Running sanity checks...")

        # Statistics validation
        stats_report = self.stats_validator.validate(final_content, self.data_inventory)
        if stats_report.suspicious_claims > 0:
            warnings.append(f"⚠️  {stats_report.suspicious_claims} suspicious statistics detected!")
            for claim in stats_report.get_suspicious():
                warnings.append(f"   - {claim.raw_text}: {claim.notes}")

        if stats_report.no_data_claims > 0:
            warnings.append(f"⚠️  {stats_report.no_data_claims} statistics have no data source")

        # Section sanity check
        sanity_report = self.sanity_checker.check_section(
            section_name=section_name,
            section_text=final_content,
            inventory=self.data_inventory,
            figures_path=self.figures_path,
        )

        if sanity_report.critical_count > 0:
            warnings.append(f"🚨 {sanity_report.critical_count} critical sanity issues!")
            for issue in sanity_report.issues:
                if issue.severity.value == "critical":
                    warnings.append(f"   - {issue.message}")

        # Print warnings if verbose
        if self.verbose and warnings:
            print("\n--- WARNINGS ---")
            for w in warnings:
                print(w)
            print("----------------\n")

        # Update state
        self.state.sections[section_name] = SectionDraft(
            name=section_name,
            content=final_content,
            word_count=len(final_content.split()),
            quote_count=self._count_quotes(final_content),
            table_count=self._count_tables(final_content),
            status=GenerationStatus.COMPLETE,
        )

        self._update_totals()

        if self.verbose:
            print(f"Section complete: {len(final_content.split())} words")

        return GenerationResult(
            success=True,
            content=final_content,
            sanity_report=sanity_report,
            stats_report=stats_report,
            warnings=warnings,
        )

    def generate_manuscript(
        self,
        paper_plan: dict[str, Any],
        evidence: dict[str, Any],
    ) -> dict[str, GenerationResult]:
        """
        Generate entire manuscript section by section.

        Args:
            paper_plan: Full paper plan with per-section details
            evidence: All evidence organized by section

        Returns:
            Dict mapping section names to GenerationResults
        """
        results = {}

        section_order = ["abstract", "introduction", "theory", "methods", "findings", "discussion"]

        for section_name in section_order:
            if section_name not in self.config.sections:
                continue

            section_plan = paper_plan.get(section_name, {})
            section_evidence = evidence.get(section_name, {})

            # Introduction and findings sections may use cold opens
            allow_cold_open = section_name in ["introduction", "findings"]

            result = self.generate_section(
                section_name=section_name,
                paper_plan=section_plan,
                evidence=section_evidence,
                allow_cold_open=allow_cold_open,
            )

            results[section_name] = result

        return results

    def generate_opening_alternatives(
        self,
        paper_summary: str,
        key_finding: str,
        best_quote: str,
    ) -> dict[str, str]:
        """
        Generate two alternative openings for user to choose.

        Args:
            paper_summary: Brief summary of paper
            key_finding: The main empirical finding
            best_quote: Best candidate quote for cold open

        Returns:
            Dict with "theoretical_puzzle" and "empirical_surprise" options
        """
        prompt = OPENING_ALTERNATIVES_PROMPT.format(
            paper_summary=paper_summary,
            key_finding=key_finding,
            best_quote=best_quote,
        )

        response = self.llm_call(
            "You generate academic paper openings in the style of top management journals.",
            prompt,
        )

        # Parse response to extract both options
        # (Simplified - in production, use structured output)
        return {
            "full_response": response,
            "note": "Review both options and select the one that best fits your paper's strengths.",
        }

    def _build_section_system_prompt(self, section_config: SectionConfig) -> str:
        """Build system prompt for section generation."""
        # Get paper type guidance
        if self.config.paper_type == PaperType.QUANT_FORWARD:
            type_guidance = QUANT_FORWARD_GUIDANCE
        else:
            type_guidance = QUAL_FORWARD_GUIDANCE

        system = SECTION_WRITER_SYSTEM.format(
            paper_type=self.config.paper_type.value,
            paper_type_guidance=type_guidance,
        )

        # Add exemplar if available
        exemplar_text = get_section_prompt_with_exemplar(section_config.name.lower())
        if exemplar_text:
            system += "\n\n" + exemplar_text

        # Add quote guidance for findings
        if "finding" in section_config.name.lower():
            system += "\n\n" + QUOTE_SELECTION_GUIDANCE

        # Add cold open guidance if permitted
        if section_config.allow_cold_open:
            system += "\n\n" + COLD_OPEN_GUIDANCE

        return system

    def _build_section_user_prompt(
        self,
        section_config: SectionConfig,
        paper_plan: dict[str, Any],
        evidence: dict[str, Any],
        allow_cold_open: bool,
    ) -> str:
        """Build user prompt for section generation."""
        prompt_parts = []

        prompt_parts.append(f"## SECTION TO WRITE: {section_config.name}")
        prompt_parts.append(f"\nTarget length: {section_config.min_words}-{section_config.max_words} words")

        if section_config.quote_budget[1] > 0:
            prompt_parts.append(f"Quote budget: {section_config.quote_budget[0]}-{section_config.quote_budget[1]} quotes")

        if section_config.required_elements:
            prompt_parts.append(f"\nRequired elements: {', '.join(section_config.required_elements)}")

        if allow_cold_open:
            prompt_parts.append("\nNote: A cold open (quote first) is permitted for this section if you have a perfect quote.")

        # Add paper plan
        prompt_parts.append("\n## SECTION PLAN")
        prompt_parts.append(json.dumps(paper_plan, indent=2))

        # Add evidence
        if evidence:
            prompt_parts.append("\n## EVIDENCE TO INCORPORATE")
            prompt_parts.append(json.dumps(evidence, indent=2))

        prompt_parts.append("\n## INSTRUCTIONS")
        prompt_parts.append("Write the section following the plan and incorporating the evidence.")
        prompt_parts.append("Adhere strictly to the style rules in the system prompt.")
        prompt_parts.append("Do not use bullet points or numbered lists.")
        prompt_parts.append("Ensure all statistical claims are interpreted.")

        return "\n".join(prompt_parts)

    def _validate_and_fix_paragraph(
        self,
        paragraph: str,
        is_cold_open: bool,
        is_section_open: bool,
        section_config: SectionConfig,
    ) -> GenerationResult:
        """Validate a paragraph and fix any violations."""
        current = paragraph
        iterations = 0
        was_fixed = False

        while iterations < self.max_fix_iterations:
            # Validate
            result = self.validator.validate(
                text=current,
                is_cold_open=is_cold_open,
                is_section_open=is_section_open,
            )

            if not result.needs_rewrite:
                break

            # Fix hard violations
            was_fixed = True
            iterations += 1

            # Get the first hard violation to fix
            hard_violations = [v for v in result.violations if v.severity == Severity.HARD]
            if not hard_violations:
                break

            violation = hard_violations[0]

            # Get relevant exemplar for fixing
            exemplar = self.exemplar_db.get(section_config.name.lower())
            exemplar_text = exemplar.text if exemplar else "Write in flowing academic prose without lists or bullets."

            # Build fix prompt
            fix_prompt = PARAGRAPH_FIXER_PROMPT.format(
                paragraph=current,
                violation_type=violation.type.value,
                violation_message=violation.message,
                violation_suggestion=violation.suggestion or "",
                exemplar=exemplar_text[:500],  # Truncate exemplar
            )

            # Call LLM to fix
            current = self.llm_call(
                "You fix style violations in academic writing. Return only the fixed paragraph.",
                fix_prompt,
            )

        return GenerationResult(
            success=True,
            content=current,
            was_fixed=was_fixed,
            fix_iterations=iterations,
        )

    def _review_section(self, content: str, section_config: SectionConfig) -> dict:
        """Run section-level review."""
        prompt = SECTION_REVIEW_PROMPT.format(
            section_name=section_config.name,
            section_text=content,
            min_words=section_config.min_words,
            max_words=section_config.max_words,
            quote_min=section_config.quote_budget[0],
            quote_max=section_config.quote_budget[1],
            required_elements=", ".join(section_config.required_elements),
        )

        response = self.llm_call(
            "You review academic writing for style compliance.",
            prompt,
        )

        return {"review": response}

    def _split_paragraphs(self, text: str) -> list[str]:
        """Split text into paragraphs."""
        paragraphs = text.split("\n\n")
        return [p.strip() for p in paragraphs if p.strip()]

    def _count_quotes(self, text: str) -> int:
        """Count quotes in text."""
        import re
        quotes = re.findall(r'["""]([^"""]+)["""]', text)
        # Only count substantial quotes (>20 chars)
        return sum(1 for q in quotes if len(q) > 20)

    def _count_tables(self, text: str) -> int:
        """Count table references in text."""
        import re
        return len(re.findall(r'[Tt]able\s+\d+', text))

    def _load_data_inventory(self):
        """Load data inventory from paper path."""
        if not self.paper_path:
            return

        # Scan data directory
        data_path = self.paper_path / "data"
        if data_path.exists():
            inventory = DataInventory()
            self.data_inventory = inventory.scan(data_path)
            if self.verbose:
                print(f"Data inventory loaded: {self.data_inventory.total_files} files")
                if self.data_inventory.missing_common:
                    print(f"  Missing: {', '.join(self.data_inventory.missing_common)}")

        # Find figures directory
        for figures_dir in ["figures", "submission/figures", "Figures"]:
            candidate = self.paper_path / figures_dir
            if candidate.exists():
                self.figures_path = candidate
                if self.verbose:
                    print(f"Figures directory: {self.figures_path}")
                break

    def _update_totals(self):
        """Update total counts from sections."""
        self.state.total_words = sum(
            s.word_count for s in self.state.sections.values()
        )
        self.state.total_quotes = sum(
            s.quote_count for s in self.state.sections.values()
        )
        self.state.total_tables = sum(
            s.table_count for s in self.state.sections.values()
        )

    def get_status(self) -> dict:
        """Get current generation status."""
        status = {
            "sections": {
                name: {
                    "status": draft.status.value,
                    "word_count": draft.word_count,
                    "quote_count": draft.quote_count,
                }
                for name, draft in self.state.sections.items()
            },
            "totals": {
                "words": self.state.total_words,
                "quotes": self.state.total_quotes,
                "tables": self.state.total_tables,
            },
            "targets": {
                "words": self.config.total_word_target,
                "quotes": self.config.total_quote_budget,
                "tables": self.config.total_table_budget,
            },
        }

        # Add data inventory status
        if self.data_inventory:
            status["data_inventory"] = {
                "total_files": self.data_inventory.total_files,
                "tabular_files": self.data_inventory.tabular_files,
                "interview_files": self.data_inventory.interview_files,
                "missing": self.data_inventory.missing_common,
            }

        return status


# Convenience function for quick manuscript generation
def generate_manuscript(
    paper_plan: dict[str, Any],
    evidence: dict[str, Any],
    llm_call: Callable[[str, str], str],
    paper_type: PaperType = PaperType.QUANT_FORWARD,
    target_venue: str = "Organization Science",
) -> dict[str, GenerationResult]:
    """
    Convenience function to generate a manuscript.

    Args:
        paper_plan: Full paper plan
        evidence: All evidence
        llm_call: LLM calling function
        paper_type: Type of paper
        target_venue: Target journal

    Returns:
        Dict of section results
    """
    config = ManuscriptConfig(
        paper_type=paper_type,
        target_venue=target_venue,
    )

    orchestrator = ManuscriptOrchestrator(
        config=config,
        llm_call=llm_call,
    )

    return orchestrator.generate_manuscript(paper_plan, evidence)
