"""
Title Grammar — A generative framework for academic paper titles.

Derived from structural analysis of 1,000 highly-cited papers (2015–2025)
across 9 venues spanning technical HCI/AI, managerial/organizational,
and generalist science journals.

The grammar decomposes a title into 5 dimensions:
1. Structure: The physical architecture of the title
2. Lead concept: What occupies the headline position
3. Rhetorical move: The framing device wrapping the lead
4. Valence: Emotional/evaluative orientation
5. Subtitle function: What work the subtitle does (if present)

Plus a cross-cutting alignment check against the paper's contribution chain.

Empirical basis:
- 9 venues: CHI, TOCHI, NeurIPS, HRI, ASQ, OrgSci, ManSci, Nature, Science
- Sorted by citation count (top ~100-120 per venue)
- Structural markers: colon rate, question rate, word count, rhetorical patterns
- Validated against 9 exemplar papers from theory-forge's style_enforcer

Key finding: The headline:subtitle structure is a social science / HCI convention.
Nature (1% colon) and Science (5% colon) almost never use it. NeurIPS (30%) and
TOCHI (18%) use it less than half the time. The grammar must account for
discipline-specific norms, not assume a universal structure.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Dimension 1: Structure
# ---------------------------------------------------------------------------

class TitleStructure(Enum):
    """Physical architecture of the title."""
    HEADLINE_SUBTITLE = "headline_subtitle"      # Two-part, colon-separated
    HEADLINE_ONLY = "headline_only"              # Standalone, no subtitle
    NAME_DESCRIPTION = "name_description"        # Tool/system name + description (CS)
    QUESTION_ANSWER = "question_answer"          # Question headline + answering subtitle
    QUESTION_ONLY = "question_only"              # Standalone question, no subtitle


STRUCTURE_META = {
    TitleStructure.HEADLINE_SUBTITLE: {
        "label": "Headline: Subtitle",
        "description": "Two-part title separated by colon. The dominant form in social science and HCI.",
        "prevalence": {
            "ASQ": 0.60, "OrgSci": 0.67, "ManSci": 0.41, "CHI": 0.60,
            "TOCHI": 0.18, "NeurIPS": 0.30, "HRI": 0.32, "Nature": 0.01, "Science": 0.05,
        },
    },
    TitleStructure.HEADLINE_ONLY: {
        "label": "Standalone Headline",
        "description": "Single-unit title with no subtitle. The norm in generalist science, common in technical venues.",
        "prevalence": {
            "Nature": 0.99, "Science": 0.95, "TOCHI": 0.80, "NeurIPS": 0.68,
            "HRI": 0.62, "ManSci": 0.47, "ASQ": 0.35, "CHI": 0.34, "OrgSci": 0.18,
        },
    },
    TitleStructure.NAME_DESCRIPTION: {
        "label": "Name: Description",
        "description": "Artifact/tool/system name as headline, description as subtitle. Dominant CS systems pattern.",
        "prevalence": {"CHI": 0.17, "NeurIPS": 0.11},
    },
    TitleStructure.QUESTION_ANSWER: {
        "label": "Question: Answer",
        "description": "Rhetorical question as headline, subtitle resolves or scopes it.",
        "prevalence": {"OrgSci": 0.10, "ManSci": 0.08, "ASQ": 0.03},
    },
    TitleStructure.QUESTION_ONLY: {
        "label": "Standalone Question",
        "description": "Question with no subtitle. Rarer but occurs in management journals.",
        "prevalence": {"OrgSci": 0.05, "ManSci": 0.04},
    },
}


# ---------------------------------------------------------------------------
# Dimension 2: Lead Concept
# ---------------------------------------------------------------------------

class LeadConcept(Enum):
    """What's foregrounded in the headline position."""
    METHOD = "method"                    # The measurement/instrument/approach leads
    PHENOMENON = "phenomenon"            # An observed dynamic or pattern leads
    FINDING = "finding"                  # A specific discovery or result leads
    RECONCEPTUALIZATION = "reconceptualization"  # A reframing of existing concepts leads
    CLAIM = "claim"                      # A broad thesis or argument leads
    IMPLICATION = "implication"          # A design prescription or recommendation leads
    ARTIFACT = "artifact"               # A named tool/system/dataset leads (CS)
    SITE = "site"                       # The empirical context is itself the draw
    PROCESS = "process"                  # An ongoing activity is theorized as important


LEAD_META = {
    LeadConcept.METHOD: {
        "label": "Method / Instrument",
        "color": "#2563eb",
        "description": "The measurement or analytical innovation leads. Rare in titles except methods papers.",
        "discipline_notes": "Common in NeurIPS (algorithmic contributions), rare in org science titles.",
    },
    LeadConcept.PHENOMENON: {
        "label": "Phenomenon",
        "color": "#7c3aed",
        "description": "The observed dynamics or pattern leads. The reader enters through what's happening.",
        "discipline_notes": "The workhorse of social science titles.",
    },
    LeadConcept.FINDING: {
        "label": "Finding / Claim",
        "color": "#dc2626",
        "description": "A specific discovery or empirical result leads.",
        "discipline_notes": "The Nature/Science default. Also common in ManSci.",
    },
    LeadConcept.RECONCEPTUALIZATION: {
        "label": "Reconceptualization",
        "color": "#059669",
        "description": "A reframing of existing concepts leads. Signals theory-building.",
        "discipline_notes": "Strong move in ASQ and OrgSci. Coinages like 'Innovation Blindness', 'Stretchwork'.",
    },
    LeadConcept.CLAIM: {
        "label": "Broad Claim",
        "color": "#d97706",
        "description": "A general thesis or argument leads, not tied to specific finding.",
    },
    LeadConcept.IMPLICATION: {
        "label": "Design Implication",
        "color": "#db2777",
        "description": "What to build or change leads. Dates quickly as systems evolve.",
        "discipline_notes": "Rare as lead in top venues. More common in practitioner outlets.",
    },
    LeadConcept.ARTIFACT: {
        "label": "Named Artifact",
        "color": "#0891b2",
        "description": "A tool, system, dataset, or benchmark name IS the headline.",
        "discipline_notes": "17% of CHI titles, 11% of NeurIPS. The dominant systems-paper pattern.",
    },
    LeadConcept.SITE: {
        "label": "Empirical Site / Context",
        "color": "#6d28d9",
        "description": "The empirical situation is itself the draw. Implies: this thing happening in the world deserves scholarly attention.",
        "discipline_notes": "Common in sociology (ASR, AJS). 'Big Data Surveillance' is the archetype.",
    },
    LeadConcept.PROCESS: {
        "label": "Process / Activity",
        "color": "#ca8a04",
        "description": "An ongoing organizational or cognitive activity is named as theoretically significant.",
        "discipline_notes": "Gerund-leading titles: 'Resourcing...', 'Managing...', 'Filtering...'. 21% of ASQ/OrgSci.",
    },
}


# ---------------------------------------------------------------------------
# Dimension 3: Rhetorical Move
# ---------------------------------------------------------------------------

class RhetoricalMove(Enum):
    """The framing device wrapping the lead concept."""
    METAPHOR = "metaphor"            # X is like Y / figurative language
    DECLARATION = "declaration"      # Direct statement: X is Z
    PARADOX = "paradox"              # X despite Y / unexpected tension
    REFRAMING = "reframing"          # X as Y / reconceptualization
    COINAGE = "coinage"              # New term introduced in headline
    CONTRAST = "contrast"            # Beyond X / moving past a prior view
    QUESTION = "question"            # Poses a puzzle for the reader to enter
    PROCESS_GERUND = "process_gerund"  # Gerund names an ongoing activity
    QUOTATION = "quotation"          # Informant voice or cultural artifact as headline
    DESCRIPTIVE = "descriptive"      # No rhetorical move — states what the paper is about
    NAMING = "naming"                # Proper name of artifact/tool (CS convention)


RHETORICAL_META = {
    RhetoricalMove.METAPHOR: {
        "label": "Metaphor",
        "color": "#8b5cf6",
        "description": "Figurative language — 'Text as Telemetry', 'The Lure of the Virtual'.",
    },
    RhetoricalMove.DECLARATION: {
        "label": "Declaration",
        "color": "#64748b",
        "description": "Direct statement of what the paper addresses. 'The Cognitive Dynamics of AI-Assisted Work'.",
    },
    RhetoricalMove.PARADOX: {
        "label": "Paradox",
        "color": "#ef4444",
        "description": "Sets up a tension or contradiction. 'The Transparency Paradox', 'When Helping Hurts'.",
    },
    RhetoricalMove.REFRAMING: {
        "label": "Reframing (X as Y)",
        "color": "#10b981",
        "description": "Repositions a known concept. 'Cognitive Load as Conversation', 'Routines as Shock Absorbers'.",
    },
    RhetoricalMove.COINAGE: {
        "label": "Coinage",
        "color": "#f59e0b",
        "description": "Introduces a new term. 'Shadow Learning', 'Stretchwork', 'Innovation Blindness'.",
    },
    RhetoricalMove.CONTRAST: {
        "label": "Contrast (Beyond X)",
        "color": "#6366f1",
        "description": "Defines contribution by what it moves past. 'Beyond Self-Report', 'Beyond Routines as Things'.",
    },
    RhetoricalMove.QUESTION: {
        "label": "Question",
        "color": "#f97316",
        "description": "Poses a puzzle. 'What Difference Does a Robot Make?', 'Do Accelerators Work?'.",
        "discipline_notes": "15% of OrgSci, 12% of ManSci, 5% of ASQ. Rare in STEM venues.",
    },
    RhetoricalMove.PROCESS_GERUND: {
        "label": "Process (Gerund)",
        "color": "#ca8a04",
        "description": "Gerund names an activity. 'Resourcing a Technological Portfolio', 'Filtering Institutional Logics'.",
        "discipline_notes": "19% overall. Up to 30% in TOCHI/HRI. Cross-disciplinary workhorse.",
    },
    RhetoricalMove.QUOTATION: {
        "label": "Quotation",
        "color": "#be185d",
        "description": "Informant voice or cultural phrase IS the headline. '\"Okay, whatever\"', '\"If Chemists Don't Do It...\"'.",
        "discipline_notes": "7% of CHI, 4% of OrgSci. Signals qualitative/ethnographic work.",
    },
    RhetoricalMove.DESCRIPTIVE: {
        "label": "Descriptive (No Move)",
        "color": "#94a3b8",
        "description": "States the topic directly with no rhetorical device. The Nature/Science default.",
        "discipline_notes": "~99% of Nature, ~95% of Science. The unmarked choice in STEM.",
    },
    RhetoricalMove.NAMING: {
        "label": "Naming (Artifact)",
        "color": "#0891b2",
        "description": "The headline IS a proper name — tool, dataset, benchmark. 'AlphaFold', 'CoAuthor', 'SuperGLUE'.",
        "discipline_notes": "17% of CHI, 11% of NeurIPS. Signals a systems/artifact contribution.",
    },
}


# ---------------------------------------------------------------------------
# Dimension 4: Valence
# ---------------------------------------------------------------------------

class Valence(Enum):
    """Emotional/evaluative orientation of the title."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


VALENCE_META = {
    Valence.POSITIVE: {
        "label": "Positive / Constructive",
        "color": "#22c55e",
        "description": "Frames contribution as enabling, improving, or advancing.",
        "prevalence_note": "~9% of titles across all venues. The marked optimistic choice.",
    },
    Valence.NEGATIVE: {
        "label": "Negative / Critical",
        "color": "#ef4444",
        "description": "Frames contribution around costs, biases, failures, or hidden problems.",
        "prevalence_note": "~7% of titles. Slightly more common in ASQ (11%) and ManSci (12.5%).",
    },
    Valence.NEUTRAL: {
        "label": "Neutral / Descriptive",
        "color": "#94a3b8",
        "description": "No evaluative loading. States what is, not whether it's good or bad.",
        "prevalence_note": "~84% of titles. The overwhelming default across all disciplines.",
    },
}


# ---------------------------------------------------------------------------
# Dimension 5: Subtitle Function (when subtitle exists)
# ---------------------------------------------------------------------------

class SubtitleFunction(Enum):
    """What work the subtitle does relative to the headline."""
    SPECIFICATION = "specification"          # Specifies method or approach
    MECHANISM = "mechanism"                  # Enumerates how something works
    SCOPING = "scoping"                      # Scopes the domain or context
    CAUSAL_CLAIM = "causal_claim"            # States what causes what
    DOMAIN_GROUNDING = "domain_grounding"    # Grounds in a specific setting
    NARRATIVE = "narrative"                  # Compressed empirical story
    EMPIRICAL_GROUNDING = "empirical_grounding"  # "Evidence from X"
    HOW_MECHANISM = "how_mechanism"          # "How X does Y" — process subtitle
    NONE = "none"                            # No subtitle (headline-only titles)


SUBTITLE_META = {
    SubtitleFunction.SPECIFICATION: {
        "label": "Specifies method/approach",
        "color": "#3b82f6",
        "description": "'A Computational Framework for...', 'A Text-Trace Framework for...'",
    },
    SubtitleFunction.MECHANISM: {
        "label": "Enumerates mechanism",
        "color": "#8b5cf6",
        "description": "'How Extraneous Load Accumulates, Persists, and Degrades Performance'",
    },
    SubtitleFunction.SCOPING: {
        "label": "Scopes domain",
        "color": "#f97316",
        "description": "'Cognitive Load and the Hidden Costs of Proactive AI'",
    },
    SubtitleFunction.CAUSAL_CLAIM: {
        "label": "States causal claim",
        "color": "#dc2626",
        "description": "'How Cognitive Load Trajectories Shape AI-Assisted Performance'",
    },
    SubtitleFunction.DOMAIN_GROUNDING: {
        "label": "Grounds in domain",
        "color": "#059669",
        "description": "'Load Dynamics in Professional Human-LLM Interaction'",
    },
    SubtitleFunction.NARRATIVE: {
        "label": "Compressed story",
        "color": "#a855f7",
        "description": "'How Fairtown Hospital Preserved Results While Degrading Its Older Surgical Robot'",
    },
    SubtitleFunction.EMPIRICAL_GROUNDING: {
        "label": "Empirical grounding",
        "color": "#14b8a6",
        "description": "'Evidence from Application Software Developers in the iOS and Android Ecosystems'",
    },
    SubtitleFunction.HOW_MECHANISM: {
        "label": "How-mechanism",
        "color": "#6366f1",
        "description": "'How Structured Flexibility Sustains Organizational Hybridity'",
        "discipline_notes": "18% of ASQ subtitles, 13% of OrgSci subtitles start with 'How'.",
    },
    SubtitleFunction.NONE: {
        "label": "No subtitle",
        "color": "#cbd5e1",
        "description": "Title is headline-only. The norm in Nature/Science, common in NeurIPS/TOCHI.",
    },
}


# ---------------------------------------------------------------------------
# Dimension 6: Headline → Subtitle Relation (when subtitle exists)
# ---------------------------------------------------------------------------

class HeadlineSubtitleRelation(Enum):
    """How the headline and subtitle connect logically."""
    EVOKES = "evokes"                # Headline evokes, subtitle specifies
    UNPACKS = "unpacks"              # Subtitle unpacks headline's compressed claim
    RESOLVES = "resolves"            # Subtitle resolves headline's tension/paradox
    INSTANTIATES = "instantiates"    # Subtitle instantiates headline's abstraction
    OPERATIONALIZES = "operationalizes"  # Subtitle operationalizes headline's concept
    EXPLAINS = "explains"            # Subtitle explains headline's mechanism
    SUPERSEDES = "supersedes"        # Subtitle builds on what headline moves beyond
    LOCATES = "locates"              # Subtitle locates headline in a domain
    ENABLES = "enables"              # Headline enables what subtitle describes
    ANSWERS = "answers"              # Subtitle answers headline's question
    ILLUSTRATES = "illustrates"      # Subtitle illustrates headline with specific case
    DESCRIBES = "describes"          # Subtitle describes what the artifact/tool does
    NONE = "none"                    # No subtitle


# ---------------------------------------------------------------------------
# Contribution Dependency Chains (paper-type-specific)
# ---------------------------------------------------------------------------

@dataclass
class DependencyLink:
    """A single link in the contribution chain."""
    source: str
    target: str
    relation: str
    description: str


# The original chain — valid for methods-contribution papers
METHODS_CHAIN = [
    DependencyLink("Reconceptualization", "Method", "justifies",
                   "The theoretical reframing justifies the measurement approach"),
    DependencyLink("Method", "Phenomenon", "reveals",
                   "The instrument makes the phenomenon visible"),
    DependencyLink("Phenomenon", "Finding", "contains",
                   "The broader phenomenon contains specific findings"),
    DependencyLink("Finding", "Implication", "motivates",
                   "The discovery motivates the design prescription"),
]

# Chain for qualitative/organizational papers (method is backgrounded)
QUALITATIVE_CHAIN = [
    DependencyLink("Site", "Phenomenon", "surfaces",
                   "The empirical site makes the phenomenon observable"),
    DependencyLink("Phenomenon", "Reconceptualization", "demands",
                   "The phenomenon demands a new conceptual frame"),
    DependencyLink("Reconceptualization", "Finding", "yields",
                   "The new frame yields specific findings"),
    DependencyLink("Finding", "Implication", "motivates",
                   "Findings motivate theoretical or practical implications"),
]

# Chain for CS/artifact papers
ARTIFACT_CHAIN = [
    DependencyLink("Problem", "Artifact", "motivates",
                   "The identified problem motivates the tool/system"),
    DependencyLink("Artifact", "Method", "embodies",
                   "The artifact embodies a technical approach"),
    DependencyLink("Method", "Finding", "produces",
                   "The method produces evaluation results"),
    DependencyLink("Finding", "Implication", "supports",
                   "Results support claims about the artifact's value"),
]


# ---------------------------------------------------------------------------
# Deep Patterns — recurring title strategies
# ---------------------------------------------------------------------------

@dataclass
class TitlePattern:
    """A recurring strategy for what a title claims the paper IS."""
    name: str
    description: str
    typical_lead: list[LeadConcept]
    typical_rhetorical: list[RhetoricalMove]
    identity: str           # What author identity the pattern projects
    longevity: str          # How well the title ages
    risk: str               # The pattern's main weakness
    discipline_affinity: list[str]  # Where this pattern is most at home


DEEP_PATTERNS = [
    TitlePattern(
        name="The Telescope",
        description="Lead with the instrument, let findings follow.",
        typical_lead=[LeadConcept.METHOD],
        typical_rhetorical=[RhetoricalMove.METAPHOR, RhetoricalMove.CONTRAST],
        identity="Methodologist",
        longevity="High if the instrument gets adopted",
        risk="Methods-paper discount — reviewers may undervalue substantive contribution",
        discipline_affinity=["NeurIPS", "ManSci"],
    ),
    TitlePattern(
        name="The Discovery",
        description="Lead with what was found; instrument is implied.",
        typical_lead=[LeadConcept.FINDING, LeadConcept.PHENOMENON],
        typical_rhetorical=[RhetoricalMove.DECLARATION, RhetoricalMove.DESCRIPTIVE],
        identity="Scientist",
        longevity="Medium — findings get replicated or superseded",
        risk="Feels domain-bound; may not signal broader contribution",
        discipline_affinity=["Nature", "Science", "ManSci"],
    ),
    TitlePattern(
        name="The Provocation",
        description="Lead with a tension or paradox, draw readers in.",
        typical_lead=[LeadConcept.FINDING, LeadConcept.CLAIM],
        typical_rhetorical=[RhetoricalMove.PARADOX, RhetoricalMove.QUESTION],
        identity="Critic / Puzzle-poser",
        longevity="Low — once the problem is fixed, the provocation dates",
        risk="Undersells positive contribution; can feel like a gotcha",
        discipline_affinity=["ASQ", "OrgSci", "ManSci"],
    ),
    TitlePattern(
        name="The Reframing",
        description="Lead with a new way of seeing; method and findings are instances.",
        typical_lead=[LeadConcept.RECONCEPTUALIZATION],
        typical_rhetorical=[RhetoricalMove.REFRAMING, RhetoricalMove.COINAGE],
        identity="Theorist",
        longevity="Highest if the reframing sticks",
        risk="Sounds abstract without subtitle doing heavy grounding work",
        discipline_affinity=["ASQ", "OrgSci"],
    ),
    TitlePattern(
        name="The Blueprint",
        description="Lead with what to build; method and findings justify.",
        typical_lead=[LeadConcept.IMPLICATION],
        typical_rhetorical=[RhetoricalMove.COINAGE, RhetoricalMove.DECLARATION],
        identity="Designer",
        longevity="Low — design prescriptions date as systems improve",
        risk="Paper remembered for tagline, not the science",
        discipline_affinity=["CHI", "HRI"],
    ),
    TitlePattern(
        name="The Artifact",
        description="Lead with the named system/tool; subtitle describes what it does.",
        typical_lead=[LeadConcept.ARTIFACT],
        typical_rhetorical=[RhetoricalMove.NAMING],
        identity="Builder",
        longevity="High if the artifact gets adopted (AlphaFold, BERT)",
        risk="Meaningless name if the tool doesn't get traction",
        discipline_affinity=["CHI", "NeurIPS", "HRI"],
    ),
    TitlePattern(
        name="The Witness",
        description="Lead with the empirical site; the situation itself is the argument.",
        typical_lead=[LeadConcept.SITE],
        typical_rhetorical=[RhetoricalMove.DESCRIPTIVE, RhetoricalMove.DECLARATION],
        identity="Fieldworker / Reporter",
        longevity="Medium — tied to the moment, but can define a research area",
        risk="Looks atheoretical if not paired with conceptual subtitle",
        discipline_affinity=["ASQ", "OrgSci", "Science"],
    ),
    TitlePattern(
        name="The Practitioner",
        description="Lead with an ongoing process; names an activity as theoretically important.",
        typical_lead=[LeadConcept.PROCESS],
        typical_rhetorical=[RhetoricalMove.PROCESS_GERUND],
        identity="Process theorist",
        longevity="Medium — process terms can become standard vocabulary",
        risk="Can read as descriptive rather than analytical",
        discipline_affinity=["ASQ", "OrgSci", "CHI", "HRI", "TOCHI"],
    ),
]


# ---------------------------------------------------------------------------
# Title dataclass for tagged titles
# ---------------------------------------------------------------------------

@dataclass
class TaggedTitle:
    """A title decomposed into its grammatical dimensions."""
    title: str
    venue: str
    year: Optional[int] = None
    doi: Optional[str] = None

    # Headline and subtitle (if split)
    headline: Optional[str] = None
    subtitle: Optional[str] = None

    # Grammar dimensions
    structure: Optional[TitleStructure] = None
    lead: Optional[LeadConcept] = None
    rhetorical: Optional[RhetoricalMove] = None
    valence: Optional[Valence] = None
    subtitle_fn: Optional[SubtitleFunction] = None
    relation: Optional[HeadlineSubtitleRelation] = None

    # Classification metadata
    confidence: float = 0.0       # 0-1, how confident the classification is
    method: str = "unclassified"  # "heuristic", "manual", "llm"
    notes: str = ""

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "title": self.title,
            "venue": self.venue,
            "year": self.year,
            "doi": self.doi,
            "headline": self.headline,
            "subtitle": self.subtitle,
            "structure": self.structure.value if self.structure else None,
            "lead": self.lead.value if self.lead else None,
            "rhetorical": self.rhetorical.value if self.rhetorical else None,
            "valence": self.valence.value if self.valence else None,
            "subtitle_fn": self.subtitle_fn.value if self.subtitle_fn else None,
            "relation": self.relation.value if self.relation else None,
            "confidence": self.confidence,
            "method": self.method,
            "notes": self.notes,
        }


# ---------------------------------------------------------------------------
# Discipline profiles — what's normal for each venue
# ---------------------------------------------------------------------------

@dataclass
class DisciplineProfile:
    """Baseline expectations for titles in a given venue."""
    venue: str
    typical_structures: list[tuple[TitleStructure, float]]  # (structure, prevalence)
    typical_leads: list[LeadConcept]
    typical_rhetorical: list[RhetoricalMove]
    valence_distribution: dict[Valence, float]  # approximate
    mean_word_count: float
    notes: str = ""


DISCIPLINE_PROFILES = {
    "ASQ": DisciplineProfile(
        venue="ASQ",
        typical_structures=[
            (TitleStructure.HEADLINE_SUBTITLE, 0.60),
            (TitleStructure.HEADLINE_ONLY, 0.35),
            (TitleStructure.QUESTION_ANSWER, 0.03),
        ],
        typical_leads=[LeadConcept.PHENOMENON, LeadConcept.RECONCEPTUALIZATION, LeadConcept.PROCESS],
        typical_rhetorical=[RhetoricalMove.COINAGE, RhetoricalMove.DECLARATION, RhetoricalMove.PROCESS_GERUND, RhetoricalMove.METAPHOR],
        valence_distribution={Valence.NEUTRAL: 0.84, Valence.NEGATIVE: 0.11, Valence.POSITIVE: 0.05},
        mean_word_count=10.7,
        notes="Theory-building journal. Coinages and reframings signal contribution. 'How...' subtitles at 18%.",
    ),
    "OrgSci": DisciplineProfile(
        venue="OrgSci",
        typical_structures=[
            (TitleStructure.HEADLINE_SUBTITLE, 0.67),
            (TitleStructure.HEADLINE_ONLY, 0.18),
            (TitleStructure.QUESTION_ANSWER, 0.10),
        ],
        typical_leads=[LeadConcept.PHENOMENON, LeadConcept.RECONCEPTUALIZATION, LeadConcept.PROCESS],
        typical_rhetorical=[RhetoricalMove.DECLARATION, RhetoricalMove.QUESTION, RhetoricalMove.PROCESS_GERUND, RhetoricalMove.COINAGE],
        valence_distribution={Valence.NEUTRAL: 0.84, Valence.NEGATIVE: 0.08, Valence.POSITIVE: 0.09},
        mean_word_count=12.1,
        notes="Highest colon rate and question rate. 'Evidence from...' subtitle pattern at 7%.",
    ),
    "ManSci": DisciplineProfile(
        venue="ManSci",
        typical_structures=[
            (TitleStructure.HEADLINE_SUBTITLE, 0.41),
            (TitleStructure.HEADLINE_ONLY, 0.47),
            (TitleStructure.QUESTION_ANSWER, 0.08),
        ],
        typical_leads=[LeadConcept.FINDING, LeadConcept.PHENOMENON],
        typical_rhetorical=[RhetoricalMove.DECLARATION, RhetoricalMove.QUESTION, RhetoricalMove.DESCRIPTIVE],
        valence_distribution={Valence.NEUTRAL: 0.75, Valence.NEGATIVE: 0.125, Valence.POSITIVE: 0.09},
        mean_word_count=9.9,
        notes="Most questions are 'Does X affect Y?' style. Empirical-grounding subtitles common.",
    ),
    "CHI": DisciplineProfile(
        venue="CHI",
        typical_structures=[
            (TitleStructure.HEADLINE_SUBTITLE, 0.43),
            (TitleStructure.HEADLINE_ONLY, 0.34),
            (TitleStructure.NAME_DESCRIPTION, 0.17),
        ],
        typical_leads=[LeadConcept.ARTIFACT, LeadConcept.PROCESS, LeadConcept.PHENOMENON],
        typical_rhetorical=[RhetoricalMove.NAMING, RhetoricalMove.PROCESS_GERUND, RhetoricalMove.QUOTATION],
        valence_distribution={Valence.NEUTRAL: 0.82, Valence.NEGATIVE: 0.09, Valence.POSITIVE: 0.12},
        mean_word_count=11.6,
        notes="Longest titles. Tool-naming is a major pattern. Quoted phrases signal qual work.",
    ),
    "TOCHI": DisciplineProfile(
        venue="TOCHI",
        typical_structures=[
            (TitleStructure.HEADLINE_ONLY, 0.80),
            (TitleStructure.HEADLINE_SUBTITLE, 0.18),
        ],
        typical_leads=[LeadConcept.PHENOMENON, LeadConcept.PROCESS],
        typical_rhetorical=[RhetoricalMove.DESCRIPTIVE, RhetoricalMove.PROCESS_GERUND],
        valence_distribution={Valence.NEUTRAL: 0.92, Valence.NEGATIVE: 0.03, Valence.POSITIVE: 0.02},
        mean_word_count=7.8,
        notes="Shortest titles, fewest colons outside STEM. Strongly descriptive register.",
    ),
    "NeurIPS": DisciplineProfile(
        venue="NeurIPS",
        typical_structures=[
            (TitleStructure.HEADLINE_ONLY, 0.68),
            (TitleStructure.NAME_DESCRIPTION, 0.11),
            (TitleStructure.HEADLINE_SUBTITLE, 0.19),
        ],
        typical_leads=[LeadConcept.METHOD, LeadConcept.ARTIFACT, LeadConcept.FINDING],
        typical_rhetorical=[RhetoricalMove.DESCRIPTIVE, RhetoricalMove.NAMING, RhetoricalMove.PROCESS_GERUND],
        valence_distribution={Valence.NEUTRAL: 0.88, Valence.NEGATIVE: 0.03, Valence.POSITIVE: 0.12},
        mean_word_count=7.6,
        notes="Technical descriptive titles dominate. Named artifacts common.",
    ),
    "HRI": DisciplineProfile(
        venue="HRI",
        typical_structures=[
            (TitleStructure.HEADLINE_ONLY, 0.62),
            (TitleStructure.HEADLINE_SUBTITLE, 0.32),
        ],
        typical_leads=[LeadConcept.PHENOMENON, LeadConcept.PROCESS],
        typical_rhetorical=[RhetoricalMove.PROCESS_GERUND, RhetoricalMove.DESCRIPTIVE, RhetoricalMove.DECLARATION],
        valence_distribution={Valence.NEUTRAL: 0.87, Valence.NEGATIVE: 0.03, Valence.POSITIVE: 0.11},
        mean_word_count=10.5,
        notes="Gerund-heavy (30%). Bridges technical and social science conventions.",
    ),
    "Nature": DisciplineProfile(
        venue="Nature",
        typical_structures=[
            (TitleStructure.HEADLINE_ONLY, 0.99),
        ],
        typical_leads=[LeadConcept.FINDING],
        typical_rhetorical=[RhetoricalMove.DESCRIPTIVE],
        valence_distribution={Valence.NEUTRAL: 0.92, Valence.NEGATIVE: 0.025, Valence.POSITIVE: 0.06},
        mean_word_count=8.7,
        notes="Almost never uses colons. Pure descriptive: what was found or built. No rhetorical games.",
    ),
    "Science": DisciplineProfile(
        venue="Science",
        typical_structures=[
            (TitleStructure.HEADLINE_ONLY, 0.95),
            (TitleStructure.HEADLINE_SUBTITLE, 0.05),
        ],
        typical_leads=[LeadConcept.FINDING],
        typical_rhetorical=[RhetoricalMove.DESCRIPTIVE],
        valence_distribution={Valence.NEUTRAL: 0.88, Valence.NEGATIVE: 0.075, Valence.POSITIVE: 0.13},
        mean_word_count=9.8,
        notes="Like Nature but slightly more colons. Descriptive default.",
    ),
}
