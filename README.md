# Paper Mining Agents

**Turn dormant research data into submittable papers using AI-assisted analysis.**

This repo provides a structured workflow for qualitative researchers (and quant-curious ethnographers) to develop papers from existing datasets using Claude Code.

---

## What This Is

A set of specialized prompts ("agents") that guide you through the full data-to-paper pipeline:

1. **Explore** your data
2. **Find** robust patterns
3. **Check the puzzle** — Is this surprising? Is the null compelling? (Zuckerman lite)
4. **Identify** the theory you're violating
5. **Find** the sensitizing literature that explains heterogeneity
6. **Mine** qualitative evidence for mechanisms
7. **Generate** and evaluate framings
8. **Check the framing** — Full Zuckerman criteria before committing
9. **Verify** claims before drafting
10. **Draft** a journal-ready manuscript

Each agent is a slash command you invoke in Claude Code. You stay in control—making judgment calls at each transition—while the AI handles the grunt work.

---

## Quick Start

### 1. Install Claude Desktop

Download from [claude.ai/download](https://claude.ai/download). Claude Desktop now includes Claude Code.

### 2. Clone this repo

```bash
git clone https://github.com/mattbeane/paper-mining-agent-suite.git
```

### 3. Point Claude at your project

Open Claude Desktop and navigate to the directory containing:
- This repo (or copy the `.claude/commands/` folder into your project)
- Your data files

### 4. Initialize your project

Run the initialization command to set up the full structure:
```
/init-project
```

This creates:
```
your-project/
├── .claude/
│   ├── commands/        # Agent prompts
│   └── hooks.json       # Quality gate validations
├── data/
│   ├── quant/           # Quantitative data files
│   └── qual/            # Interview transcripts, field notes
│       ├── interviews/
│       └── fieldnotes/
├── analysis/
│   ├── exploration/     # /explore-data outputs
│   ├── patterns/        # /hunt-patterns outputs
│   ├── framing/         # Frame iterations (frame-1/, frame-2/, etc.)
│   └── verification/    # Verification packages
├── literature/
│   ├── primary/         # Core theory papers
│   ├── sensitizing/     # Sensitizing literature
│   └── refs.bib         # Bibliography
├── output/
│   ├── drafts/          # Generated manuscripts
│   └── exports/         # LaTeX, Word, PDF conversions
├── PROJECT_CONTEXT.md   # Fill in your project details
├── DECISION_LOG.md      # Auto-tracked decisions
└── state.json           # Workflow state (auto-managed)
```

### 5. Run the pipeline

Start with:
```
/explore-data
```

Check progress anytime with:
```
/status
```

Then follow the workflow, invoking each agent when ready.

---

## The Agents

### Core Pipeline

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/explore-data` | Initial data reconnaissance | Start here |
| `/hunt-patterns` | Find robust empirical patterns | After exploration |
| `/eval-zuckerman-lite` | **Early puzzle check**: Is this a puzzle? Is the null compelling? | After patterns, BEFORE theory |
| `/find-theory` | Identify theory being violated | After puzzle check passes |
| `/find-lens` | Find sensitizing/interpretive literature | After identifying theory |
| `/mine-qual` | Extract mechanism evidence from interviews | After finding lens |
| `/smith-frames` | Generate and evaluate theoretical framings | After qual mining |
| `/eval-zuckerman` | **Full framing check**: All 10 Zuckerman criteria | After framing, BEFORE verification |
| `/verify-claims` | Create verification package for external review | After framing check passes |
| `/draft-paper` | Generate journal-ready manuscript | After verification |

### Project Management

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/init-project` | Set up project structure and state tracking | Before starting |
| `/status` | View workflow progress and next steps | Anytime |
| `/switch-project` | Switch between papers (multi-project mode) | Multi-paper workflows |
| `/new-frame` | Start fresh theoretical iteration | When reframing |
| `/new-frame list` | View all frame attempts | Reviewing progress |
| `/new-frame compare` | Compare framings side-by-side | Choosing direction |

### Output & Integration

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/export [format]` | Convert to LaTeX, Word, PDF, HTML | After drafting |
| `/package-verification` | Create ZIP for external review | After verification |
| `/import-refs [source]` | Import references from BibTeX, Zotero, DOI | Literature gathering |

---

## The Workflow

```
/explore-data
     │
     ▼
  [Review output] ──► Not interesting? Stop or get different data
     │
     ▼
/hunt-patterns
     │
     ▼
  [Review findings] ──► Select which patterns to pursue
     │
     ▼
┌────────────────────────────────────────────────────────┐
│  /eval-zuckerman-lite  ◄── EARLY PUZZLE CHECK          │
│  • Is this a puzzle in the world (not a lit gap)?      │
│  • Is the null hypothesis compelling?                  │
│  • Who is your audience (row vs column)?               │
└────────────────────────────────────────────────────────┘
     │
     ▼
  [Pass?] ──► No? Reframe the pattern or find a different one
     │
     ▼
/find-theory  ◄── Now you know WHICH theory you're violating
     │
     ▼
  [Review] ──► Is this the right theory to violate?
     │
     ▼
/find-lens
     │
     ▼
  [Review] ──► Does this literature explain the heterogeneity?
     │
     ├──────────────────────┐
     ▼                      ▼
/mine-qual              /smith-frames
     │                      │
     └──────────┬───────────┘
                ▼
         [Choose framing]
                │
                ▼
┌────────────────────────────────────────────────────────┐
│  /eval-zuckerman  ◄── FULL FRAMING CHECK               │
│  • All 10 Zuckerman criteria                           │
│  • One idea? Null built up AND saved?                  │
│  • Lit review or puzzle-focused theory section?        │
└────────────────────────────────────────────────────────┘
                │
                ▼
  [Pass?] ──► No? Loop back to /smith-frames
                │
                ▼
         /verify-claims
                │
                ▼
         [Send to external reviewer - different AI or colleague]
                │
                ▼
         /draft-paper
                │
                ▼
            [Done!]
```

**Key insight**: You make the judgment calls. The agents accelerate; you decide.

---

## Critical Concepts

### The Sensitizing Literature

The most important intellectual move in this pipeline is finding the **sensitizing literature**—the second body of work that explains *why* your finding varies.

**Pattern**:
1. You find a robust empirical pattern
2. It violates an established theoretical prediction
3. But not everyone violates it—there's heterogeneity
4. The sensitizing literature explains *who* violates and *why*

**Example** (from prior published work):
- Finding: Some surgical trainees skilled up fast despite minimal formal practice
- Theory violated: Deliberate practice predicts skill requires repetition
- Heterogeneity: Only *some* trainees achieved rapid skill gains
- Sensitizing literature: Deviance and workarounds
- Contribution: "Shadow learning" explains skill variance outside formal training

### Frame Shifts Are Normal

Expect 3-5 complete reframings per paper. Your first hypothesis will almost certainly be wrong. The workflow accommodates this with explicit frame management:

```
/new-frame              # Archive current frame, start fresh
/new-frame list         # See all your frame attempts
/new-frame compare      # Compare framings side-by-side
```

Each frame preserves your empirical work (data exploration, patterns) while giving you a clean slate for theory, lens, and framing.

### External Verification

The `/verify-claims` agent produces a self-contained package (ZIP file) you should send to a *different* AI system or a skeptical colleague. The model that helped you build the analysis shouldn't be the only one checking it.

Use `/package-verification` to automatically create the ZIP with checksums and reviewer instructions.

### State Tracking

The `state.json` file tracks your progress through the pipeline. See [`docs/STATE_SCHEMA.md`](docs/STATE_SCHEMA.md) for the full schema and details on what's deterministic vs model-dependent.

### Quality Gates

The workflow includes hooks that warn you when running commands out of sequence:

```
⚠️  Quality Gate: /hunt-patterns should be completed before /find-theory.
    You need robust empirical patterns before identifying which theory they violate.
```

These are warnings, not blocks—you can proceed if you have good reason, but they help prevent wasted effort.

### Zuckerman Criteria (Two-Stage Check)

Ezra Zuckerman's "Tips for Article-Writers" provides 10 criteria that capture what makes academic papers compelling. This workflow integrates them at two points:

**Stage 1: `/eval-zuckerman-lite`** (after `/hunt-patterns`, before `/find-theory`)
- Is this a puzzle in the world (not a literature gap)?
- Is the null hypothesis compelling?
- Who is your audience (row vs column)?

**Stage 2: `/eval-zuckerman`** (after `/smith-frames`, before `/verify-claims`)
- Full 10-criteria evaluation
- One idea? Null built up AND saved?
- Lit review or puzzle-focused theory section?
- Clear narrative arc?

The early check prevents you from investing in theory development for a non-puzzle. The full check ensures your framing is sound before you commit to verification and drafting.

See `Zuckerman_UP_2008_Tips_For_Writers.pdf` in this repo for the original memo.

---

## Requirements

- Claude Desktop (includes Claude Code)
- Your data in accessible files (CSV, Excel, text files for interviews)
- Domain expertise (this accelerates your work; it doesn't replace your judgment)

---

## Style Enforcer Module

The `style_enforcer/` module provides automated validation and generation for qualitative management papers targeting ASQ, Organization Science, and Management Science.

### The Problem

LLMs draw on economics/strategy papers (hypothesis-test structure), generic academic voice (passive, hedged), and bullet points. They don't naturally produce the management theory-building register without continuous constraint enforcement.

### Key Features

```python
from style_enforcer import StyleValidator, ManuscriptOrchestrator

# Validate existing text
validator = StyleValidator()
result = validator.validate(manuscript_text)

if result.hard_violation_count > 0:
    for v in result.violations:
        print(f"{v.type.value}: {v.message}")
```

**Hard Rules (always enforced):**
- No bullet points—ever
- No numbered lists—convert to prose
- Contributions as narrative (not "This paper makes three contributions: First...")

**Soft Rules (flagged if severe):**
- Passive voice <30%
- Hedging density
- Orphaned statistics (must interpret within 2 sentences)
- Quote setup and length

**v2 Hallucination Prevention:**
- `DataInventory`: Scans available data files
- `StatisticsValidator`: Flags unverified statistical claims
- `SectionSanityChecker`: Section-level validation (methods accuracy, figures)

See `style_enforcer/README.md` for full documentation.

---

## Living Paper & Pre-Review

This workflow integrates with **[Living Paper](https://github.com/mattbeane/living-paper)**, a standalone tool for bidirectional claim-evidence traceability. Living Paper is a separate project designed for adoption by qualitative researchers everywhere—both retrospectively (existing papers) and prospectively (new research).

### What Living Paper Does

- Maintains verifiable links between claims and evidence
- Supports three-tier access control (PUBLIC, CONTROLLED, WITNESS_ONLY)
- Enables pre-review: adversarial self-audit before submission
- Enforces quant/qual hierarchy in claim adjudication

### Integration with Paper-Mining-Agents

After running `/verify-claims`, you can ingest the verification output into Living Paper:

```bash
# In your project directory
python living_paper/lp.py init
python living_paper/lp.py ingest \
  --claims analysis/verification/claims.jsonl \
  --evidence analysis/verification/evidence.jsonl \
  --links analysis/verification/links.csv

# Generate pre-review report
python living_paper/lp.py prereview --out prereview_report.md
```

### Quant/Qual Adjudication Rules

When adjudicating contested claims:

1. **Quant claims = almost always ground truth** — but pause to ask what quant might be missing when qual contradicts
2. **Qual perceptions contradicting quant** → reclassify as "illustrates mistaken beliefs"
3. **Mechanism claims** → can be challenged by qual, BUT quant patterns can rule out mechanisms

See the [Living Paper repo](https://github.com/mattbeane/living-paper) for full documentation.

---

## What This Doesn't Do

- Collect data for you
- Replace your theoretical intuition
- Make judgment calls about what's interesting
- Know your field's genre conventions (you do)
- Guarantee publication (nothing does)

---

## Comparison with Critiques of GenAI in Qualitative Research

Nguyen & Welch (2025) published a rigorous critique of GenAI use in qualitative data analysis, arguing that LLMs are fundamentally unsuited for this work due to epistemic risks including hallucination, unreliability, and anthropomorphic fallacies.

Their critique targets a specific use case—LLMs as *autonomous* coding/analysis tools that replace human interpretation. This workflow takes a structurally different approach: the human remains the theorist and interpreter; the LLM accelerates search and enforces structure.

See [`nguyen-welch-comparison.md`](nguyen-welch-comparison.md) for a detailed analysis of how this workflow relates to their critique.

**Citation**: Nguyen, D. C., & Welch, C. (2025). Generative artificial intelligence in qualitative data analysis: Analyzing—or just chatting? *Organizational Research Methods, 29*(1), 3–39. https://doi.org/10.1177/10944281251377154

---

## Origin

This workflow was developed by Matt Beane (UC Santa Barbara) after using Claude Code to produce three papers from dormant datasets in 5 days. The full story is in `docs/FROM_DATA_TO_PAPERS_TUTORIAL.md`.

---

## License

MIT. Use it, modify it, share it.

---

## Questions?

Open an issue or contact mattbeane@ucsb.edu
