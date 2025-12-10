# Style Enforcer for Qualitative Management Papers

A system for enforcing stylistic standards on academic manuscripts targeting top management journals (ASQ, Organization Science, Management Science).

## The Problem

When asking an LLM to "write the paper," it draws on its training distribution of academic writing—which is dominated by economics/strategy empirical papers (hypothesis-test structure), generic academic voice (passive, hedged), and bullet points. The model doesn't naturally produce the specific management theory-building register without continuous constraint enforcement.

## The Solution

This module implements a hybrid architecture:
1. **Section-controlled generation** with appropriate exemplars for each section type
2. **Paragraph-level validation** that catches violations immediately
3. **Automatic fixing** of violations before they accumulate
4. **Data inventory integration** to prevent hallucination of statistics (v2)
5. **Section sanity checks** to catch factual errors in methods, figures, etc. (v2)

## Key Style Rules

### HARD RULES (always enforced)

1. **No bullet points** - Ever. Not for lists, not for contributions, not for anything.
2. **No numbered lists** - Ever. Not "1. First..." Not "(a)..." Convert to prose.
3. **Contributions as narrative** - Never "This paper makes three contributions: First..."

### SOFT RULES (flagged, fixed if severe)

1. **Passive voice** - Flag if >30% of sentences are passive
2. **Hedging** - Flag excessive hedging ("may suggest", "appears to")
3. **Orphaned statistics** - Every statistical result must have interpretation within 2 sentences
4. **Quote setup** - Quotes need preceding analytical claim (except cold opens)
5. **Quote length** - Keep under 80 words

### SPECIAL PROVISIONS

1. **Cold opens** - A section (especially introduction) may open with a quote if:
   - The quote perfectly distills the core puzzle/finding
   - Analytical framing follows within 1-2 sentences
   - Used sparingly (max one per paper, maybe one per major section)

2. **Juicy quotes** - Prefer quotes that are:
   - Colorful (profanity, bluntness, colloquialisms are assets)
   - Voicey (you can hear the speaker)
   - Norm-violating or surprising
   - Compressed insight

## Paper Types

### Quant-Forward (default for warehouse papers)
- Quantitative analysis is the main tentpole
- Qualitative data illuminates mechanisms
- Tables/figures can be prominent
- Statistical claims can lead paragraphs
- BUT: always interpret, always connect to theory

### Qual-Forward (ASQ ethnographic tradition)
- Ethnographic evidence is primary
- Extended narrative development
- Quotes do heavy lifting
- Tables are supplementary

## Usage

### Basic Usage

```python
from style_enforcer import ManuscriptOrchestrator, ManuscriptConfig, PaperType

# Define your LLM calling function
def my_llm(system_prompt: str, user_prompt: str) -> str:
    # Your LLM API call here
    return response

# Create config
config = ManuscriptConfig(
    paper_type=PaperType.QUANT_FORWARD,
    target_venue="Organization Science",
)

# Create orchestrator
orchestrator = ManuscriptOrchestrator(
    config=config,
    llm_call=my_llm,
)

# Generate a section
result = orchestrator.generate_section(
    section_name="introduction",
    paper_plan={
        "hook_type": "empirical_surprise",
        "main_argument": "Workers stay rather than flee automation",
        "contributions": ["extend anticipatory sensemaking", "show signaling mechanism"],
    },
    evidence={
        "key_finding": "18-19 percentage point drop in resignations",
        "best_quote": "Telling them now that you got robotics here, they'll all leave.",
    },
    allow_cold_open=True,
)

print(result.content)
```

### Generate Opening Alternatives

```python
# Get both theoretical and empirical opening options
alternatives = orchestrator.generate_opening_alternatives(
    paper_summary="Study of worker response to automation in warehouses",
    key_finding="Workers stay rather than flee as automation approaches",
    best_quote="Telling them now that you got robotics here, they'll all leave.",
)

# Review both and choose
print(alternatives["full_response"])
```

### Validate Existing Text

```python
from style_enforcer import StyleValidator

validator = StyleValidator()

text = '''
This paper makes three contributions. First, we extend...
Second, we show... Third, we document...
'''

result = validator.validate(text)

if result.needs_rewrite:
    for v in result.violations:
        print(f"{v.type.value}: {v.message}")
        print(f"  Suggestion: {v.suggestion}")
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      MANUSCRIPT ORCHESTRATOR                     │
│  - Holds paper plan (sections, arguments, evidence allocation)   │
│  - Manages section-by-section generation                         │
│  - Tracks word counts, quote budgets, contribution claims        │
└─────────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ SECTION CONFIG  │  │   EXEMPLAR DB   │  │  STYLE RULES    │
│                 │  │                 │  │                 │
│ Per-section:    │  │ Reference paper │  │ HARD RULES:     │
│ - word limits   │  │ excerpts for    │  │  - no bullets   │
│ - quote budget  │  │ each section    │  │  - no lists     │
│ - required      │  │ type            │  │  - narrative    │
│   elements      │  │                 │  │    contrib.     │
└─────────────────┘  └─────────────────┘  └─────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │       SECTION WRITER          │
              │                               │
              │ Generates with:               │
              │ - Style system prompt         │
              │ - Section-specific exemplar   │
              │ - Quote selection guidance    │
              └───────────────────────────────┘
                              │
                              │ streams paragraphs
                              ▼
              ┌───────────────────────────────┐
              │     PARAGRAPH VALIDATOR       │
              │                               │
              │ Checks for violations         │
              │ (deterministic, fast)         │
              └───────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
              [CLEAN]              [VIOLATION]
                 │                      │
                 │                      ▼
                 │         ┌─────────────────────┐
                 │         │   PARAGRAPH FIXER   │
                 │         │                     │
                 │         │ Targeted rewrite    │
                 │         │ with exemplar       │
                 │         └─────────────────────┘
                 │                      │
                 └──────────┬───────────┘
                            ▼
                     SECTION DRAFT
```

## Files

- `__init__.py` - Package exports
- `validator.py` - Deterministic style rule checking (with LaTeX support)
- `config.py` - Section and manuscript configuration
- `exemplars.py` - Reference paper excerpts
- `prompts.py` - Prompt templates
- `orchestrator.py` - Main orchestration logic
- `data_inventory.py` - Scan data files to prevent hallucination (v2)
- `statistics_validator.py` - Flag unverified statistical claims (v2)
- `section_sanity.py` - Section-level sanity checks (v2)

## v2 Features: Hallucination Prevention

The v2 release adds critical safeguards against LLM hallucination of statistics:

### Data Inventory

```python
from style_enforcer import DataInventory, scan_paper_data

# Scan a paper's data directory
inventory = scan_paper_data("/path/to/paper")

print(f"Found {inventory.total_files} data files")
print(f"Missing: {inventory.missing_common}")  # e.g., ['survey response data']
```

### Statistics Validator

```python
from style_enforcer import StatisticsValidator

validator = StatisticsValidator()
report = validator.validate(manuscript_text, inventory)

if report.suspicious_claims > 0:
    print("⚠️  Suspicious statistics detected!")
    for claim in report.get_suspicious():
        print(f"  - {claim.raw_text}: {claim.notes}")
```

### Section Sanity Checker

```python
from style_enforcer import SectionSanityChecker

checker = SectionSanityChecker()
sanity = checker.check_methods(
    methods_text=methods_section,
    inventory=inventory,
    actual_process="iterative mixed-method: qual discovery, survey design, quant analysis"
)

if sanity.critical_count > 0:
    print("🚨 Critical sanity issues!")
```

### Integrated with Orchestrator

```python
orchestrator = ManuscriptOrchestrator(
    config=config,
    llm_call=my_llm,
    paper_path="/path/to/paper",  # NEW: enables data inventory
)

result = orchestrator.generate_section("methods", paper_plan, evidence)

# Check for warnings
if result.warnings:
    for w in result.warnings:
        print(w)
```

## Key Insights Encoded

These rules derive from analysis comparing published papers (Shadow Learning, Inverted Apprenticeships, Resourcing a Technological Portfolio) with Claude-drafted papers (Wait and See, Learning to Automate, When Misfit Motivates, Developmental Uncertainty).

1. **Published papers read like joining a scholarly conversation**; drafts read like building a case for findings.

2. **Quotes are rare gems** that need to be polished. Each must do heavy work.

3. **No orphaned empirical claims**. The problem isn't hypothesis language per se—it's statistical results that sit there without interpretation.

4. **Cold opens work** precisely because they violate expected structure. Use sparingly.

5. **Voice matters**. Active, direct, confident about empirics, humble about theory.
