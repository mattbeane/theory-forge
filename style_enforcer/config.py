"""
Configuration for manuscript sections and overall manuscript structure.

Defines per-section rules, constraints, and budgets for:
- Word counts
- Quote allowances
- Table/figure placement
- Required elements
- Special rules (cold opens, contribution format, etc.)
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class HookType(Enum):
    """Types of opening hooks."""
    THEORETICAL_PUZZLE = "theoretical_puzzle"
    EMPIRICAL_SURPRISE = "empirical_surprise"


class PaperType(Enum):
    """Type of paper (affects style expectations)."""
    QUAL_FORWARD = "qual_forward"      # Ethnographic, qual as figure
    QUANT_FORWARD = "quant_forward"    # Large datasets, quant as figure


@dataclass
class SectionConfig:
    """Configuration for a single manuscript section."""

    name: str
    min_words: int = 0
    max_words: int = 10000
    quote_budget: tuple[int, int] = (0, 10)  # (min, max)
    table_budget: tuple[int, int] = (0, 5)
    figure_budget: tuple[int, int] = (0, 5)

    # Structural requirements
    required_elements: list[str] = field(default_factory=list)
    prohibited_elements: list[str] = field(default_factory=list)

    # Special rules
    allow_cold_open: bool = False
    allow_hypothesis_language: bool = True  # But must have interpretation
    contribution_format: str = "narrative_only"  # Never "list"

    # Exemplar guidance
    exemplar_key: Optional[str] = None  # Key into ExemplarDB

    def __post_init__(self):
        # Enforce: contribution format can never be "list"
        if self.contribution_format != "narrative_only":
            raise ValueError("contribution_format must be 'narrative_only'")


@dataclass
class ManuscriptConfig:
    """Configuration for entire manuscript."""

    paper_type: PaperType = PaperType.QUANT_FORWARD
    target_venue: str = "Organization Science"

    # Opening hook choice
    hook_type: HookType = HookType.EMPIRICAL_SURPRISE

    # Overall budgets
    total_word_target: int = 12000
    total_quote_budget: tuple[int, int] = (8, 15)
    total_table_budget: tuple[int, int] = (3, 6)
    total_figure_budget: tuple[int, int] = (2, 4)

    # Section configurations
    sections: dict[str, SectionConfig] = field(default_factory=dict)

    def __post_init__(self):
        if not self.sections:
            self.sections = self._default_sections()

    def _default_sections(self) -> dict[str, SectionConfig]:
        """Default section configurations for quant-forward paper."""
        return {
            "abstract": SectionConfig(
                name="Abstract",
                min_words=150,
                max_words=250,
                quote_budget=(0, 0),
                table_budget=(0, 0),
                required_elements=[
                    "research_question",
                    "method_summary",
                    "key_finding",
                    "contribution_preview",
                ],
                exemplar_key="abstract",
            ),

            "introduction": SectionConfig(
                name="Introduction",
                min_words=1000,
                max_words=1800,
                quote_budget=(0, 2),  # Maybe one cold open
                table_budget=(0, 0),
                allow_cold_open=True,
                required_elements=[
                    "hook",
                    "puzzle_or_gap",
                    "this_paper_does",
                    "contribution_preview",
                    "paper_structure",
                ],
                exemplar_key="introduction",
            ),

            "theory": SectionConfig(
                name="Theoretical Development",
                min_words=2500,
                max_words=4000,
                quote_budget=(0, 2),
                table_budget=(0, 1),  # Maybe a typology
                required_elements=[
                    "literature_review",
                    "gap_identification",
                    "theoretical_framework",
                    "propositions_or_expectations",
                ],
                prohibited_elements=[
                    "numbered_hypotheses_list",
                ],
                exemplar_key="theory",
            ),

            "methods": SectionConfig(
                name="Methods / Empirical Setting",
                min_words=1500,
                max_words=2500,
                quote_budget=(0, 1),
                table_budget=(1, 2),  # Summary stats, sample description
                required_elements=[
                    "setting_description",
                    "data_sources",
                    "sample_description",
                    "analytical_approach",
                ],
                exemplar_key="methods",
            ),

            "findings": SectionConfig(
                name="Findings",
                min_words=3000,
                max_words=5500,
                quote_budget=(6, 12),  # Main quote section
                table_budget=(2, 4),
                figure_budget=(1, 3),
                allow_cold_open=True,  # Can open analytical subsection with data
                allow_hypothesis_language=True,
                required_elements=[
                    "quantitative_patterns",
                    "mechanism_illumination",
                    "quote_evidence",
                ],
                exemplar_key="findings",
            ),

            "discussion": SectionConfig(
                name="Discussion",
                min_words=2000,
                max_words=3500,
                quote_budget=(0, 1),
                table_budget=(0, 1),
                required_elements=[
                    "summary_of_findings",
                    "theoretical_contributions",
                    "practical_implications",
                    "limitations",
                    "future_research",
                ],
                prohibited_elements=[
                    "contribution_list",  # Must be narrative
                ],
                exemplar_key="discussion",
            ),
        }

    def get_section(self, section_name: str) -> SectionConfig:
        """Get configuration for a section."""
        # Normalize name
        key = section_name.lower().replace(" ", "_")
        if key in self.sections:
            return self.sections[key]

        # Try partial match
        for k, v in self.sections.items():
            if key in k or k in key:
                return v

        raise KeyError(f"Unknown section: {section_name}")


# Preset configurations for common paper types

QUANT_FORWARD_ORGSCI = ManuscriptConfig(
    paper_type=PaperType.QUANT_FORWARD,
    target_venue="Organization Science",
    hook_type=HookType.EMPIRICAL_SURPRISE,
    total_word_target=12000,
)

QUANT_FORWARD_MANSCI = ManuscriptConfig(
    paper_type=PaperType.QUANT_FORWARD,
    target_venue="Management Science",
    hook_type=HookType.EMPIRICAL_SURPRISE,
    total_word_target=10000,  # ManSci tends shorter
    total_quote_budget=(5, 10),  # Fewer quotes
)

def _qual_forward_sections() -> dict[str, SectionConfig]:
    """Section configurations for qual-forward/inductive papers.

    Key differences from quant-forward:
    - Theory section sets up sensitizing concepts, NOT mechanism
    - Findings section BUILDS theory progressively (findings = theory)
    - Methods emphasizes embeddedness, first-person voice
    - Extended quotes (60-120+ words) do heavy argumentative lifting
    """
    return {
        "abstract": SectionConfig(
            name="Abstract",
            min_words=150,
            max_words=300,  # Slightly longer for qual
            quote_budget=(0, 0),
            table_budget=(0, 0),
            required_elements=[
                "research_question",
                "method_summary",
                "phenomenon_naming",  # Must name the core concept
                "contribution_preview",
            ],
            exemplar_key="abstract",
        ),

        "introduction": SectionConfig(
            name="Introduction",
            min_words=1200,
            max_words=2200,  # Often longer for qual
            quote_budget=(0, 1),  # Maybe one cold open
            table_budget=(0, 0),
            allow_cold_open=True,
            required_elements=[
                "puzzle_without_punchline",  # Puzzle but NOT mechanism reveal
                "sensitizing_question",  # What we want to understand
                "this_paper_does",
                "contribution_preview_without_mechanism",  # Preview contribution type, not finding
            ],
            prohibited_elements=[
                "mechanism_preview",  # DON'T reveal the theoretical finding
                "hypothesis_language",
            ],
            exemplar_key="introduction",
        ),

        "theory": SectionConfig(
            name="Theoretical Background / Prior Research",
            min_words=2000,
            max_words=3500,
            quote_budget=(0, 1),
            table_budget=(0, 1),
            required_elements=[
                "sensitizing_concepts",  # Lenses for analysis
                "prior_work_engagement",  # What we know
                "what_prior_work_assumes",  # Gaps/taken-for-granted
                "research_question_refinement",
            ],
            prohibited_elements=[
                "mechanism_explanation",  # Save for findings
                "numbered_hypotheses_list",
                "propositions",
                "predictions",
                "expected_patterns_section",  # Hypo-deductive framing
                "pattern_numbering",  # "Pattern 1", "Pattern 2" etc.
            ],
            allow_hypothesis_language=False,  # Theory-building only
            exemplar_key="theory",
        ),

        "methods": SectionConfig(
            name="Research Setting and Methods",
            min_words=1800,
            max_words=3000,  # Often longer for qual
            quote_budget=(0, 2),  # Sometimes quotes about method
            table_budget=(0, 2),
            required_elements=[
                "rich_setting_description",  # Vivid context
                "access_and_embeddedness",  # How researcher got in
                "data_sources_narrative",  # Data described in narrative form
                "analytical_approach_inductive",  # Abductive/grounded theory language
                "iterative_analysis_description",  # Required for multimethod: qual-quant iteration
            ],
            # First-person voice is expected in qual methods
            exemplar_key="methods",
        ),

        "findings": SectionConfig(
            name="Findings",
            min_words=4000,
            max_words=7000,  # Often longest section - theory built here
            quote_budget=(12, 25),  # Extended quotes do heavy lifting
            table_budget=(0, 2),
            figure_budget=(0, 2),
            allow_cold_open=True,
            allow_hypothesis_language=False,  # Theory-building language only
            required_elements=[
                "progressive_concept_development",  # Build theory through section
                "phenomenon_naming",  # Name the emergent concept(s)
                "evidence_concept_interleaving",  # Evidence and analysis woven together
                "emergent_model",  # Full theoretical model by section end
            ],
            prohibited_elements=[
                "quantitative_patterns_lead",  # Don't lead with numbers
                "hypothesis_testing_language",
            ],
            exemplar_key="findings_qual",  # Use qual-specific exemplar
        ),

        "discussion": SectionConfig(
            name="Discussion",
            min_words=2500,
            max_words=4000,  # Often longer for theoretical elaboration
            quote_budget=(0, 1),
            table_budget=(0, 1),
            required_elements=[
                "theoretical_contribution_narrative",  # Contribution as prose
                "connection_to_sensitizing_concepts",  # How findings extend prior work
                "boundary_conditions",
                "implications",
                "limitations",
                "future_research",
            ],
            prohibited_elements=[
                "contribution_list",  # Must be narrative
                "three_contributions_format",
            ],
            exemplar_key="discussion",
        ),
    }


QUAL_FORWARD_ASQ = ManuscriptConfig(
    paper_type=PaperType.QUAL_FORWARD,
    target_venue="Administrative Science Quarterly",
    hook_type=HookType.THEORETICAL_PUZZLE,
    total_word_target=14000,
    total_quote_budget=(15, 25),  # More quotes
    total_table_budget=(1, 3),   # Fewer tables
    sections=_qual_forward_sections(),  # Use qual-specific sections
)


# Quote selection guidance (injected into prompts)
QUOTE_SELECTION_GUIDANCE = """
When selecting quotes from interview data, prefer:

1. COLORFUL LANGUAGE: Profanity, bluntness, colloquialisms are assets, not liabilities.
   Real humans don't speak in sanitized academic-ese.

2. VOICE: You should be able to hear the speaker. Quotes that could have been
   written by anyone are weak. Quotes that sound like *this specific person* are strong.

3. NORM-VIOLATING: Surprising statements, counterintuitive observations, things that
   make the reader go "wait, really?"

4. COMPRESSED INSIGHT: The quote distills a mechanism or finding into vivid form.
   It does the work of a paragraph in a sentence.

Bad quote: "We found the implementation process to be challenging but ultimately
beneficial for our operational efficiency."

Good quote: "Once I hit that threshold, I'm done. So we actually—there's at least
a theory that some of our incentives may actually have made our attendance worse."

The goal: make the reader feel "this is a real person in a real situation."
Each quote is a polished gem. Fewer, better quotes beat more, adequate quotes.
"""


# Cold open guidance
COLD_OPEN_GUIDANCE = """
A cold open begins with raw data—a quote that perfectly distills the core phenomenon.
It creates an "oh, this is real life" feeling that hooks the reader before any
analytical framing.

Rules for cold opens:
1. The quote must encapsulate the paper's central puzzle or finding
2. It must be immediately followed (within 1-2 sentences) by analytical framing
3. Use sparingly: one cold open per paper maximum, maybe one per major section

Good cold open: Opens with a warehouse manager's quote that captures the core
paradox, then immediately contextualizes: "This prediction—that workers would flee
automation—proved spectacularly wrong. In this paper, we explain why."

Do not use a cold open just because it's permitted. Use it when you have a
quote so perfect it would be a crime to bury it after setup text.
"""
