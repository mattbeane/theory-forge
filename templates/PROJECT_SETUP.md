# Project Setup Template

Copy this structure into your project directory before starting.

## Directory Structure

```
your-project/
├── .claude/
│   └── commands/           # Copy from paper-mining-agents repo
│       ├── explore-data.md
│       ├── hunt-patterns.md
│       ├── find-theory.md
│       ├── find-lens.md
│       ├── mine-qual.md
│       ├── smith-frames.md
│       ├── verify-claims.md
│       └── draft-paper.md
├── data/
│   ├── quant/              # Your quantitative data files
│   │   ├── main_data.csv
│   │   └── secondary_data.xlsx
│   └── qual/               # Interview transcripts, field notes
│       ├── interviews/
│       │   ├── interview_001.txt
│       │   └── ...
│       └── fieldnotes/
├── analysis/               # Created by agents as you work
│   ├── exploration/
│   ├── patterns/
│   ├── theory/
│   ├── qualitative/
│   ├── framing/
│   └── verification/
├── literature/             # PDFs, notes on papers
├── output/                 # Final manuscript
│   ├── manuscript.tex
│   ├── references.bib
│   ├── tables/
│   └── figures/
├── PROJECT_CONTEXT.md      # Fill this in (see below)
└── DECISION_LOG.md         # Track your choices
```

## PROJECT_CONTEXT.md Template

Create this file to give the AI context about your project:

```markdown
# Project Context

## Research Domain
[What field is this? What topic?]

## Data Overview
[Brief description of your data—what it is, where it came from, what time period]

## Research Question (if any)
[What are you trying to understand? Or is this exploratory?]

## Target Journals
[Where might you submit? What genre conventions matter?]

## Anonymization Requirements
[What needs to be anonymized? Company names, locations, etc.]

## Your Expertise
[What domain knowledge do you bring? This helps calibrate suggestions.]

## Constraints
[Any limitations? Timeline, co-authors, etc.]
```

## DECISION_LOG.md Template

Track your choices as you work:

```markdown
# Decision Log

## [Date]: Data Exploration
- Ran /explore-data
- Key finding: [X]
- Decision: Pursue [Y] because [Z]

## [Date]: Pattern Selection
- Ran /hunt-patterns
- Promising patterns: [list]
- Selected: [X] because [reason]
- Killed: [Y] because [didn't survive controls]

## [Date]: Theory Selection
- Primary theory: [X]
- Sensitizing literature: [Y]
- Rationale: [Z]

## [Date]: Framing Selection
- Options generated: [list]
- Selected: [X]
- Rationale: [Y]

## [Date]: Frame Shift
- Previous frame: [X]
- New frame: [Y]
- Why: [Z]
```

## Quick Start Commands

After setup, run in order:

```
/explore-data          # Understand what you have
/hunt-patterns         # Find robust patterns
/find-theory          # Identify theory being violated
/find-lens            # Find sensitizing literature
/mine-qual            # Extract mechanism evidence
/smith-frames         # Generate framing options
/verify-claims        # Create verification package
/draft-paper          # Generate manuscript
```

You'll loop back as needed—especially to /hunt-patterns and /smith-frames.
