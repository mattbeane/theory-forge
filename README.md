# Theory Forge

**Build theory-generating papers from qualitative and mixed-methods data.**

A toolkit for researchers who have rich data (interviews, fieldnotes, observations) and want to develop inductive, theory-building papers for top management journals. Works with qual-only or qual+quant multimethod designs—the iterative workflow supports triangulation between data types.

---

## This Tool Is For Experienced Researchers

Theory-forge accelerates your work. It doesn't do the thinking for you.

**What it does:**
- Runs systematic pattern hunts across your data
- Surfaces evidence you might miss
- Generates framing options to consider
- Catches genre mismatches before reviewers do
- Verifies claims against your actual evidence

**What it doesn't do:**
- Replace your judgment about what's interesting
- Know your field's unwritten rules
- Guarantee your framing will work
- Substitute for having done the reading

If you're worried about AI replacing researchers: the researchers who can *supervise* AI are more valuable than ever. Theory-forge is designed to be supervised — it surfaces its reasoning, flags uncertainty, and requires you to make the calls.

Your job is to catch when the AI is wrong. That skill is why you're irreplaceable.

---

## Related: ResearchKit Quals

We're separately working on [ResearchKit Quals](https://github.com/mattbeane/research-quals) — a draft framework for naming and assessing the tacit research skills that matter when doing this kind of work. The two projects share a concern (helping researchers produce rigorous work) and inform each other, but they're independent and both works-in-progress.

Theory-forge development surfaces which research skills are hardest to replace with AI. The competency work in research-quals helps us think about what "ready to use AI tools" means. But we don't yet know the right relationship between the two — whether skill assessment should affect tool behavior, and if so how. For now, they evolve independently.

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
git clone https://github.com/mattbeane/theory-forge.git
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
| `/hunt-patterns` | Find robust empirical patterns (with RASC adaptive stopping) | After exploration |
| `/eval-zuckerman-lite` | **Early puzzle check**: Is this a puzzle? Is the null compelling? | After patterns, BEFORE theory |
| `/find-theory` | Identify theory being violated | After puzzle check passes |
| `/find-lens` | Find sensitizing/interpretive literature | After identifying theory |
| `/mine-qual` | Extract mechanism evidence from interviews | After finding lens |
| `/style-engine` | Generate and evaluate theoretical framings (style engine) | After qual mining |
| `/eval-zuckerman` | **Full framing check**: All 10 Zuckerman criteria | After framing, BEFORE verification |
| `/audit-claims` | Search raw data for supporting AND challenging evidence | Before verification |
| `/verify-claims` | Create verification package for external review | After framing check passes |
| `/draft-paper` | Generate journal-ready manuscript | After verification |

### Analysis Extensions

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/surface-absences` | **Identify what's conspicuously missing** from data (Glaser's "surfacing absences") | After exploration, anytime |
| `/trace-process` | **Put data in temporal motion** — phases, turning points, drift, evolution | After exploration, anytime |
| `/create-agent` | **Build bespoke analytical agents** for project-specific needs | Anytime |

### Evaluation & Quality

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/eval-contribution` | **Diagnose contribution type** — not all papers are "theory violation" | Before eval-zuckerman |
| `/integrate-quant-qual` | Connect quantitative patterns with qualitative mechanisms | After hunt-patterns AND mine-qual |
| `/compare-frames` | Side-by-side comparison of multiple theoretical framings | After 2+ /new-frame iterations |
| `/simulate-review` | Generate adversarial peer reviews before submission | After draft-paper |
| `/build-lit-review` | Build bibliography from identified theory/lens | After find-theory AND find-lens |

### Project Management

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/init-project` | Set up project structure and state tracking | Before starting |
| `/status` | View workflow progress and next steps | Anytime |
| `/switch-project` | Switch between papers (multi-project mode) | Multi-paper workflows |
| `/new-frame` | Start fresh theoretical iteration | When reframing |
| `/new-frame list` | View all frame attempts | Reviewing progress |
| `/new-frame compare` | Compare framings side-by-side | Choosing direction |
| `/consensus-config` | Configure statistical consensus settings | Before final analysis |
| `/student-mode` | Toggle student mode (predictions, explanations, audit trail) | For learning/supervision |
| `/repair-state` | **Diagnose and fix state.json problems** | When state seems corrupted or out of sync |

### Output & Integration

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/describe-ai-use` | **Generate AI attribution statement** for methods section | After drafting |
| `/eval-paper-quality` | Systematic quality scoring (rubric-eval) | After drafting |
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
/mine-qual              /style-engine
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
  [Pass?] ──► No? Loop back to /style-engine
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

### Multiple Contribution Models (Beyond Zuckerman)

Not all valuable papers violate theoretical predictions. This workflow now supports multiple contribution types:

| Type | What It Is | Evaluation Framework |
|------|------------|---------------------|
| **Theory Violation** | Paper shows established theory is wrong under conditions | Zuckerman's 10 criteria |
| **Theory Elaboration** | Paper adds precision without contradiction | Fisher & Aguinis criteria |
| **Phenomenon Description** | The phenomenon itself is the contribution | Weick's criteria |
| **Methodological** | New way of studying something | Abbott's heuristics |
| **Practical Insight** | Actionable knowledge for practitioners | Corley & Gioia criteria |
| **Literature Integration** | Synthesis of existing work | Palmatier et al. criteria |

Run `/eval-contribution` BEFORE `/eval-zuckerman` to diagnose which type your paper is, then get evaluated against the appropriate criteria—not just Zuckerman.

### Zuckerman's Framework (For Theory Violation Papers)

Ezra Zuckerman's "Tips for Article-Writers" provides the fundamental moves for **theory violation** papers:

1. **The puzzle** — a real-world phenomenon that existing theory can't explain
2. **Build up and save the null** — make the conventional explanation compelling before showing why it fails
3. **The contribution** — your proposed explanation for the puzzle

This workflow builds on Zuckerman's framework. See `Zuckerman_UP_2008_Tips_For_Writers.pdf` in this repo for the original memo.

**Important**: Zuckerman is excellent for theory violation papers (ASQ, Org Science style). But if your paper is elaborating theory, describing a phenomenon, or developing methodology, Zuckerman may not be the right fit. Use `/eval-contribution` to check.

### The Sensitizing Literature (Optional Gambit)

One powerful move for executing Step 3 (the contribution) is finding the **sensitizing literature**—a second body of work that explains *why* your finding varies. This works especially well when your data shows heterogeneity.

**When this gambit works well:**
1. You find a robust empirical pattern
2. It violates an established theoretical prediction
3. But not everyone violates it—there's heterogeneity
4. The sensitizing literature explains *who* violates and *why*

**When to use a different approach:**
- Your contribution is a new mechanism, not a moderator
- Your finding is uniform (everyone violates, no heterogeneity to explain)
- Your puzzle is "how does X work?" rather than "why do only some violate?"

**Example** (from prior published work):
- Finding: Some surgical trainees skilled up fast despite minimal formal practice
- Theory violated: Deliberate practice predicts skill requires repetition
- Heterogeneity: Only *some* trainees achieved rapid skill gains
- Sensitizing literature: Deviance and workarounds
- Contribution: "Shadow learning" explains skill variance outside formal training

### Theory-Building vs Theory-Testing Language

If your paper is **building theory** (discovering patterns, proposing mechanisms) rather than **testing hypotheses**, use language appropriate to that genre. See [`docs/THEORY_BUILDING_STYLE.md`](docs/THEORY_BUILDING_STYLE.md) for a detailed rubric.

**Key distinction:**
- Theory-building: "The data suggest...", "is consistent with...", "the pattern indicates..."
- Theory-testing: "The data confirm...", "supports the hypothesis...", "validates..."

A single paper can't do both. This is a style choice—some papers legitimately test pre-specified hypotheses.

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

### Presubmission Review Instructions

The package includes `PRESUBMISSION_REVIEW_INSTRUCTIONS.md`—a detailed guide that instructs external reviewers to provide **thorough, constructive, point-by-point feedback** comparable to a rigorous journal review. This ensures you get:

- Specific claims flagged with concerns (with page/section references)
- Alternative explanations that should be addressed
- Clarity issues where readers might misinterpret your argument
- Internal consistency checks (numbers, definitions, terminology)
- A structured "skeptical reviewer" perspective
- Prioritized action list

The goal is to surface every issue before submission, while the feedback remains constructive and actionable. See `templates/PRESUBMISSION_REVIEW_INSTRUCTIONS.md` for the full instructions.

### State Tracking

The `state.json` file tracks your progress through the pipeline. See [`docs/STATE_SCHEMA.md`](docs/STATE_SCHEMA.md) for the full schema and details on what's deterministic vs model-dependent.

### Quality Gates

The workflow includes hooks that warn you when running commands out of sequence:

```
⚠️  Quality Gate: /hunt-patterns should be completed before /find-theory.
    You need robust empirical patterns before identifying which theory they violate.
```

These are warnings, not blocks—you can proceed if you have good reason, but they help prevent wasted effort.

### Adversarial Evidence (Standard Feature)

Theory-forge is designed to make cherry-picking harder, not easier. **Adversarial evidence surfacing is built into the standard workflow**—not just a student mode feature.

Where it appears:
- **`/hunt-patterns`** — documents "killed findings" that didn't survive controls
- **`/mine-qual`** — requires disconfirming evidence section
- **`/audit-claims`** — explicitly adversarial; searches ALL data for challenging evidence
- **`/style-engine`** — evaluates counter-evidence, alternative interpretations, and "survivability" for each framing
- **`/verify-claims`** — documents alternative interpretations and specification choices

The philosophy: reviewers are adversarial. If you don't find problems first, they will. See [`docs/ADVERSARIAL_EVIDENCE.md`](docs/ADVERSARIAL_EVIDENCE.md) for the full rationale.

### Zuckerman Criteria (Two-Stage Check)

Ezra Zuckerman's "Tips for Article-Writers" provides 10 criteria that capture what makes academic papers compelling. This workflow integrates them at two points:

**Stage 1: `/eval-zuckerman-lite`** (after `/hunt-patterns`, before `/find-theory`)
- Is this a puzzle in the world (not a literature gap)?
- Is the null hypothesis compelling?
- Who is your audience (row vs column)?

**Stage 2: `/eval-zuckerman`** (after `/style-engine`, before `/verify-claims`)
- Full 10-criteria evaluation
- One idea? Null built up AND saved?
- Lit review or puzzle-focused theory section?
- Clear narrative arc?

The early check prevents you from investing in theory development for a non-puzzle. The full check ensures your framing is sound before you commit to verification and drafting.

See `Zuckerman_UP_2008_Tips_For_Writers.pdf` in this repo for the original memo.

### Statistical Consensus Mode

For peer-review-ready analysis, enable **consensus mode**. This runs LLM-dependent stages multiple times and computes statistical aggregates:

```
/consensus-config enable
```

**What consensus mode provides:**

| Stage | Single-Run Output | Consensus Output |
|-------|-------------------|------------------|
| `/hunt-patterns` | β = 0.21 | β = 0.21 (±0.02 SD, 95% CI: [0.18, 0.24], n=25) |
| `/mine-qual` | "Here's a supporting quote" | Quote appeared in 14/15 runs (93% stability) |
| `/verify-claims` | "Claim verified" | 10/10 runs confirmed direction & significance |

**Stability ratings:**
- **HIGH** (CV < 10%): Defensible for peer review
- **MEDIUM** (CV 10-25%): Include with noted uncertainty
- **LOW** (CV > 25%): Flag for investigation—data may be ambiguous

**Why this matters:**
- Single-run analysis is non-reproducible (different prompt → different answer)
- Consensus analysis shows confidence: "We ran this 25 times and got consistent results"
- LOW stability reveals ambiguity rather than hiding it
- Quote stability catches cherry-picking

Configure with `/consensus-config`. See `lib/consensus/` for the Python implementation.

---

## Prerequisites

**Theory-forge assumes you already have qualitative methods training.** This tool accelerates skilled researchers — it doesn't replace skill development.

Before using theory-forge, you should have:
- Coded at least one dataset by hand
- Written at least one qualitative methods section
- Read extensively in your theoretical area
- Experienced peer review (ideally both sides)

See [`docs/PREREQUISITES.md`](docs/PREREQUISITES.md) for details on why these matter and what happens if you skip them.

For a more structured take on what research skills matter, see the (separate, draft) [ResearchKit Quals](https://github.com/mattbeane/research-quals) project.

### For Advisors

If you supervise students using theory-forge, see [`docs/ADVISOR_GUIDE.md`](docs/ADVISOR_GUIDE.md) for:
- How to structure supervised use
- Warning signs of over-reliance on AI
- Gate checkpoints for review
- Conversation starters at each stage

### Student Mode

For researchers new to theory-forge or working under supervision, enable student mode:

```
/student-mode on
```

This adds:
- **Prediction prompts** — write what you expect before AI runs
- **Explanation layers** — AI shows its reasoning ("Why I Did This" sections)
- **Comparison tables** — your predictions vs. AI findings
- **Enhanced audit trail** — logs predictions vs. findings to `STUDENT_WORK.md`

**Integrated into 6 core commands**: `/explore-data`, `/hunt-patterns`, `/find-theory`, `/find-lens`, `/mine-qual`, `/style-engine`

The `/mine-qual` command is strictest—it requires reading 3-5 interviews manually before AI runs, ensuring students can't skip the interpretive work.

Student mode doesn't change the analysis—it adds scaffolding for learning. See [`docs/STUDENT_MODE_FEATURE_OPTIONS.md`](docs/STUDENT_MODE_FEATURE_OPTIONS.md) for design rationale.

---

## Technical Requirements

- Claude Desktop (includes Claude Code)
- Your data in accessible files (CSV, Excel, text files for interviews)
- Domain expertise (this accelerates your work; it doesn't replace your judgment)
- **For consensus mode**: Python 3.9+ with `anthropic` or `openai` package installed
- **For systematic scoring**: `pip install rubric-eval` + `ANTHROPIC_API_KEY` (optional but recommended)

---

## Visual Dashboard

Running `/status` generates a `dashboard.html` file in your project root. Open it in any browser for a visual overview:

- Workflow progress with stage cards
- Current frame info (theory, lens, framing)
- Consensus mode status and stability summary
- Next step guidance

The dashboard auto-updates each time you run `/status`. Just refresh your browser after running commands.

---

## Style Enforcer Module

Automated validation for qualitative management papers (ASQ, Org Science, Management Science). Enforces hard rules (no bullets, no numbered lists) and soft rules (passive voice, hedging, quote setup). See `style_enforcer/README.md` for details.

---

## Living Paper Integration (Seamless)

Living Paper is **bundled** with this workflow—no separate installation needed. When you run `/verify-claims`, it automatically:

1. Ingests your claims, evidence, and links into the Living Paper database
2. Runs verification checks
3. Generates a reviewer package you can send directly to journal reviewers

### What Living Paper Does

- Maintains verifiable links between claims and evidence
- Supports three-tier access control (PUBLIC, CONTROLLED, WITNESS_ONLY)
- Generates standalone HTML reviewer interfaces (reviewers just double-click to open)
- Enforces quant/qual hierarchy in claim adjudication

### The Flow

```
/audit-claims     →  Searches raw data for supporting AND challenging evidence
                     Outputs: analysis/audit/claims.jsonl, evidence.jsonl, links.csv

/verify-claims    →  Creates verification package + auto-runs Living Paper
                     Outputs: analysis/verification/reviewer_package/
                              (HTML interface reviewers can open directly)
```

No manual `lp.py` commands needed—the workflow handles it.

### Standalone Use

For more control, see the [Living Paper repo](https://github.com/mattbeane/living-paper).

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

## Origin

This workflow was developed by Matt Beane (UC Santa Barbara) after using Claude Code to produce three papers from dormant datasets in 5 days. Full story available upon request.

---

## License

MIT. Use it, modify it, share it.

---

## Questions?

Open an issue or contact mattbeane@ucsb.edu
