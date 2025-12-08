# Paper Mining Agents

**Turn dormant research data into submittable papers using AI-assisted analysis.**

This repo provides a structured workflow for qualitative researchers (and quant-curious ethnographers) to develop papers from existing datasets using Claude Code.

---

## What This Is

A set of specialized prompts ("agents") that guide you through the full data-to-paper pipeline:

1. **Explore** your data
2. **Find** robust patterns
3. **Identify** the theory you're violating
4. **Find** the sensitizing literature that explains heterogeneity
5. **Mine** qualitative evidence for mechanisms
6. **Generate** and evaluate framings
7. **Verify** claims before drafting
8. **Draft** a journal-ready manuscript

Each agent is a slash command you invoke in Claude Code. You stay in control—making judgment calls at each transition—while the AI handles the grunt work.

---

## Quick Start

### 1. Install Claude Desktop

Download from [claude.ai/download](https://claude.ai/download). Claude Desktop now includes Claude Code.

### 2. Clone this repo

```bash
git clone https://github.com/[your-username]/paper-mining-agents.git
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
| `/find-theory` | Identify theory being violated | After finding patterns |
| `/find-lens` | Find sensitizing/interpretive literature | After identifying theory |
| `/mine-qual` | Extract mechanism evidence from interviews | After finding lens |
| `/smith-frames` | Generate and evaluate theoretical framings | After qual mining |
| `/verify-claims` | Create verification package for external review | Before drafting |
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
/find-theory
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

### Quality Gates

The workflow includes hooks that warn you when running commands out of sequence:

```
⚠️  Quality Gate: /hunt-patterns should be completed before /find-theory.
    You need robust empirical patterns before identifying which theory they violate.
```

These are warnings, not blocks—you can proceed if you have good reason, but they help prevent wasted effort.

---

## Requirements

- Claude Desktop (includes Claude Code)
- Your data in accessible files (CSV, Excel, text files for interviews)
- Domain expertise (this accelerates your work; it doesn't replace your judgment)

---

## What This Doesn't Do

- Collect data for you
- Replace your theoretical intuition
- Make judgment calls about what's interesting
- Know your field's genre conventions (you do)
- Guarantee publication (nothing does)

---

## Origin

This workflow was developed by Matt Beane (UC Santa Barbara) after using Claude Code to produce three papers from dormant datasets in 5 days. The full story is in `docs/FROM_DATA_TO_PAPERS_TUTORIAL.md`.

---

## License

MIT. Use it, modify it, share it.

---

## Questions?

Open an issue or contact mattbeane@ucsb.edu
