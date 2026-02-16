# Theory Forge

**A buffet of analytical capabilities for qualitative and mixed-methods research.**

Theory-forge is a collection of specialized AI agents (Claude Code slash commands) for producing theory-building papers from rich data — interviews, fieldnotes, spreadsheets, observations, surveys. Each agent handles one analytical task. You compose them however your project demands.

There's a suggested sequence for researchers who want guidance, but every command works standalone. Use what you need. Skip what you don't. Build your own agents for what's missing.

---

## How It Works

Each agent is a slash command you invoke in Claude Code. You stay in control — making judgment calls at every step — while the AI handles systematic work that's laborious by hand: scanning 30 interviews for disconfirming evidence, generating multiple theoretical framings, checking claims against raw data.

### Quick Start

```bash
git clone https://github.com/mattbeane/theory-forge.git
```

Open Claude Code in your project directory (with the `.claude/commands/` folder present), then:

```
/init-project          # Set up project structure
/explore-data          # Start exploring your data
/status                # Check progress anytime
```

### Project Structure

```
your-project/
├── .claude/commands/       # Agent prompts (from this repo)
├── data/
│   ├── quant/              # Quantitative data files
│   └── qual/               # Interviews, field notes
├── analysis/
│   ├── exploration/        # /explore-data outputs
│   ├── patterns/           # /hunt-patterns outputs
│   ├── framing/            # /style-engine outputs (frame-1/, frame-2/, etc.)
│   ├── absences/           # /surface-absences outputs
│   ├── process/            # /trace-process outputs
│   └── verification/       # Verification packages
├── literature/             # Theory papers, sensitizing literature, refs.bib
├── output/                 # Drafts, tables, figures, exports
├── DECISION_LOG.md         # Auto-tracked decisions
└── state.json              # Workflow state (auto-managed)
```

---

## The Commands

### Discovery & Analysis

| Command | What It Does |
|---------|-------------|
| `/explore-data` | Initial reconnaissance — what's in the data, what's interesting |
| `/hunt-patterns` | Find robust empirical patterns with adaptive stopping (RASC) |
| `/mine-qual` | Extract mechanism evidence from interviews, with adversarial checks |
| `/surface-absences` | Identify what's conspicuously *missing* from the data |
| `/trace-process` | Put data in temporal motion — phases, turning points, drift |

### Theory & Framing

| Command | What It Does |
|---------|-------------|
| `/find-theory` | Identify which theory your finding violates or extends |
| `/find-lens` | Find sensitizing literature that explains heterogeneity |
| `/style-engine` | Generate and evaluate multiple theoretical framings |
| `/new-frame` | Archive current framing, start fresh (expect 3-5 reframings) |
| `/compare-frames` | Side-by-side comparison of multiple framings |

### Evaluation & Verification

| Command | What It Does |
|---------|-------------|
| `/eval-contribution` | Diagnose contribution type — not all papers are theory violation |
| `/eval-zuckerman-lite` | Early puzzle check: is this a puzzle? Is the null compelling? |
| `/eval-zuckerman` | Full 10-criteria Zuckerman check on your framing |
| `/audit-claims` | Search ALL raw data for supporting AND challenging evidence |
| `/verify-claims` | Create verification package for external review |
| `/simulate-review` | Generate adversarial peer reviews before submission |

### Output & Integration

| Command | What It Does |
|---------|-------------|
| `/draft-paper` | Generate journal-ready manuscript |
| `/describe-ai-use` | Generate AI attribution statement for methods section |
| `/eval-paper-quality` | Systematic quality scoring against rubrics |
| `/export [format]` | Convert to LaTeX, Word, PDF, HTML |
| `/package-verification` | Create ZIP with reviewer instructions for external review |
| `/integrate-quant-qual` | Connect quantitative patterns with qualitative mechanisms |
| `/build-lit-review` | Build bibliography from identified theory/lens |

### Project Management

| Command | What It Does |
|---------|-------------|
| `/init-project` | Set up project structure and state tracking |
| `/status` | View workflow progress and next steps |
| `/create-agent` | Build bespoke analytical agents for project-specific needs |
| `/consensus-config` | Configure statistical consensus settings |
| `/student-mode` | Toggle student mode (predictions, explanations, audit trail) |
| `/repair-state` | Diagnose and fix state.json problems |

---

## A Suggested Path (Not the Only One)

Most theory-building papers follow a rough arc: find something interesting → figure out why it matters → frame it → verify it → write it up. Here's one path through the commands that follows this arc:

```
/explore-data → /hunt-patterns → /eval-zuckerman-lite
                                        │
                          Is this a puzzle? ──► No? Try a different pattern.
                                        │
                                       Yes
                                        │
            /find-theory → /find-lens → /mine-qual ↔ /style-engine
                                                │
                                        /eval-zuckerman
                                                │
                                  Framing solid? ──► No? /new-frame, loop back.
                                                │
                                               Yes
                                                │
                        /audit-claims → /verify-claims → /draft-paper
```

**But this is just one path.** Your project might need something different:

- **Processual data?** Run `/trace-process` early — the temporal structure may BE the finding.
- **Not a theory violation?** Skip the Zuckerman gates entirely. Use `/eval-contribution` to figure out what kind of paper you're writing, then evaluate against the appropriate criteria.
- **Exploratory?** Start with `/surface-absences` — what's conspicuously missing may be more interesting than what's present.
- **Need a custom analysis?** Use `/create-agent` to build a bespoke agent for your specific analytical need.

The commands are composable. The sequence above is a sensible default for theory-violation papers, not a requirement.

---

## Theoretical Grounding

Theory-forge draws on several frameworks for how AI can productively support qualitative research:

### Glaser's Four Abductive Moves

Glaser & First Loan (forthcoming, *Strategic Organization*) identify four moves for AI-augmented qualitative analysis:

| Move | Theory-forge command |
|------|---------------------|
| **Multiplying lenses** — interpreting data through multiple theoretical frames | `/style-engine` |
| **Surfacing absences** — identifying conspicuous omissions | `/surface-absences` |
| **Bridging levels** — connecting micro and macro | `/integrate-quant-qual` |
| **Testing categories** — adversarial checking of emerging concepts | `/mine-qual`, `/audit-claims` |

Plus **interpretive vigilance** — the researcher's ongoing responsibility to supervise AI output. This is embedded in every command through required researcher review points.

See [`docs/VERN_GLASER_FRAMEWORK_MAP.md`](docs/VERN_GLASER_FRAMEWORK_MAP.md) for the full mapping.

### The Style Engine Concept

The `/style-engine` (formerly `/smith-frames`) draws on Reimer & Peter's concept from IS research: GenAI as a tool that renders the same empirical reality through multiple theoretical styles. The same data, viewed through different lenses, yields different — and complementary — insights.

### Multiple Contribution Types

Not every paper violates a theory. Theory-forge supports multiple contribution types, each with its own evaluation framework:

| Type | Evaluation Framework |
|------|---------------------|
| Theory Violation | Zuckerman's 10 criteria |
| Theory Elaboration | Fisher & Aguinis criteria |
| Phenomenon Description | Weick's criteria |
| Methodological | Abbott's heuristics |
| Practical Insight | Corley & Gioia criteria |

Run `/eval-contribution` to diagnose which type your paper is before applying evaluation criteria.

---

## Key Design Choices

### Adversarial Evidence Is Standard

Theory-forge is designed to make cherry-picking harder, not easier. Adversarial evidence surfacing is built into the standard workflow:

- `/hunt-patterns` documents "killed findings" that didn't survive controls
- `/mine-qual` requires a disconfirming evidence section
- `/audit-claims` explicitly searches ALL data for challenging evidence
- `/style-engine` evaluates counter-evidence and "survivability" for each framing

The philosophy: reviewers are adversarial. Find problems first, or they will.

### Quality Gates Are Warnings, Not Walls

Commands suggest a sequence but don't enforce it. If you run `/find-theory` before `/hunt-patterns`, you'll get a warning:

```
⚠️  Quality Gate: /hunt-patterns should be completed before /find-theory.
    You need robust empirical patterns before identifying which theory they violate.
```

You can proceed if you have good reason. The gates help prevent wasted effort; they don't assume they know your project better than you do.

### AI Attribution Built In

`/describe-ai-use` generates a methods-section-ready attribution statement based on what you actually did — which commands you ran, what decisions you made, whether you used consensus mode. Based on the attribution approach used in "Developmental Uncertainty" (Beane, submitted to *Organization Science*). See [`templates/AI_ATTRIBUTION_BOILERPLATE.md`](templates/AI_ATTRIBUTION_BOILERPLATE.md) for modular boilerplate components.

### Statistical Consensus Mode

For peer-review-ready analysis, consensus mode runs LLM-dependent stages multiple times:

```
/consensus-config enable
```

| Stage | Single Run | Consensus |
|-------|-----------|-----------|
| `/hunt-patterns` | β = 0.21 | β = 0.21 (±0.02 SD, n=25) |
| `/mine-qual` | "Here's a quote" | Quote appeared in 14/15 runs (93% stability) |

LOW stability (CV > 25%) reveals ambiguity rather than hiding it.

### Frame Shifts Are Normal

Expect 3-5 complete reframings per paper. The workflow accommodates this:

```
/new-frame              # Archive current frame, start fresh
/new-frame list         # See all your frame attempts
/new-frame compare      # Compare framings side-by-side
```

Each frame preserves your empirical work while giving you a clean slate for theory and framing.

### External Verification

`/verify-claims` produces a self-contained package you should send to a *different* AI system or a skeptical colleague. The model that helped build the analysis shouldn't be the only one checking it. `/package-verification` creates the ZIP with checksums and reviewer instructions.

---

## Student Mode

For researchers learning the craft or working under supervision:

```
/student-mode on
```

This adds prediction prompts (write what you expect before AI runs), explanation layers (AI shows its reasoning), and comparison tables (your predictions vs. AI findings). Integrated into core commands. `/mine-qual` is strictest — requires reading 3-5 interviews manually before AI runs.

Student mode doesn't change the analysis — it adds scaffolding for learning. See [`docs/STUDENT_MODE_FEATURE_OPTIONS.md`](docs/STUDENT_MODE_FEATURE_OPTIONS.md) for design rationale.

---

## Living Paper Integration

When you run `/verify-claims`, it automatically creates a [Living Paper](https://github.com/mattbeane/living-paper) verification package — auditable links between claims and evidence, with a standalone HTML reviewer interface. No separate installation needed.

---

## Related: Research-Quals

[Research-quals](https://github.com/mattbeane/research-quals) is a separate project developing competency-based training for the research judgment skills that matter when using tools like this. The two projects inform each other but evolve independently. See research-quals for details.

---

## Contributing: Add Your Own Data Sources & Methodologies

Theory-forge is extensible. You can add support for new data formats and new methodological traditions without touching core code.

### Add a Data Source

Support a new qualitative/quantitative data tool (Dedoose, NVivo, MAXQDA, Otter.ai, etc.):

```
/author-data-source [tool-name]
```

This creates:
- A Python importer (`tools/importers/[name].py`) that normalizes the format
- Documentation (`data_sources/[name].md`) with export/import instructions
- A registry entry so commands like `/explore-data` auto-discover the source

### Add a Methodology

Add a new evaluation framework or analytical tradition (grounded theory, process tracing, narrative analysis, etc.):

```
/author-methodology [tradition-name]
```

This creates:
- An evaluation rubric (`rubrics/[name].json`) with calibrated criteria
- An eval command (`.claude/commands/eval-[name].md`) runnable via `/eval [name]`
- Documentation (`methodologies/[name].md`)
- A registry entry so `/eval-contribution` and `/eval` know about it

### The Registry

`registry.json` in the project root indexes everything extensible: data sources, methodologies, and custom agents. Commands check this file at runtime to discover what's available.

### Contributing Upstream

To share what you've built:
1. Run `/author-data-source` or `/author-methodology` to generate the files
2. Fork theory-forge
3. Copy the generated files into your fork
4. Open a PR

The commands produce everything needed for a complete contribution — no guessing about which files to create or what format to use.

### Build a Custom Agent

For project-specific analytical needs (not general enough to contribute upstream):

```
/create-agent
```

Custom agents are registered in both `state.json` and `registry.json` and live alongside core commands.

---

## Technical Requirements

- Claude Code (via Claude Desktop or standalone)
- Your data in accessible files (CSV, Excel, text files for interviews)
- Domain expertise (this accelerates your work; it doesn't replace your judgment)
- **For consensus mode**: Python 3.9+ with `anthropic` or `openai` package
- **For systematic scoring**: `pip install rubric-eval` + `ANTHROPIC_API_KEY` (optional)

---

## Origin

Developed by Matt Beane (UC Santa Barbara) while using Claude Code to produce papers from dormant datasets. Theory-forge is a work in progress — the command set, the suggested workflow, and the theoretical grounding are all evolving. Contributions, critiques, and alternative approaches are welcome.

---

## License

MIT. Use it, modify it, share it.

---

## Questions?

Open an issue or contact mattbeane@ucsb.edu
