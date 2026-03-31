# Theory Forge

**AI-assisted theory building from qualitative and mixed-methods data, with systematic quality checks.**

Theory-forge is a collection of AI agents (Claude Code skills) that handle the full arc of producing a theory-building paper — discovering patterns, building framings, auditing claims, drafting manuscripts. Each agent handles one analytical task. You compose them however your project demands.

What makes it different: built-in quality checks that run multiple times through a statistical consensus engine, persist scores across sessions with automatic staleness tracking, and produce a single submission-readiness verdict via `/check-submission`. You see exactly where your paper is strong, where it's weak, and what to fix — before reviewers do.

If you're coming from a software engineering background: think of it as a CI pipeline for research papers — scored rubrics as assertions, consensus stability as flaky-test detection, `/check-submission` as `pytest --verbose`.

---

## Quick Start

```bash
git clone https://github.com/mattbeane/theory-forge.git
```

Open Claude Code in your project directory, then:

```
/init-project          # Set up project structure
/explore-data          # Start exploring your data
/status                # Check progress anytime
/check-submission      # Submission readiness check
```

---

## Skills

### Discovery

| Skill | What It Does |
|---------|-------------|
| `/explore-data` | Initial reconnaissance — what's in the data, what's interesting |
| `/hunt-patterns` | Find robust empirical patterns with adaptive stopping |
| `/mine-qual` | Extract mechanism evidence from interviews, with adversarial checks |
| `/surface-absences` | Identify what's conspicuously *missing* from the data |
| `/integrate-quant-qual` | Connect quantitative patterns with qualitative mechanisms |
| `/measure-at-scale` | Measure constructs across full corpus; [GABRIEL](https://github.com/openai/GABRIEL)-compatible |

### Framing

| Skill | What It Does |
|---------|-------------|
| `/find-theory` | Identify which theory your finding violates or extends |
| `/find-lens` | Find sensitizing literature that explains heterogeneity |
| `/smith-frames` | Generate and evaluate multiple theoretical framings |
| `/new-frame` | Archive current framing, start fresh (expect 3-5 reframings) |
| `/compare-frames` | Side-by-side comparison of framings |

### Quality Checks

Every evaluation persists scores across sessions, tracks upstream file changes for staleness, and runs through consensus mode by default.

| Skill | What It Checks | Output |
|---------|---------------|--------|
| `/check-submission` | **Submission readiness** — runs all checks below | PASS / CONDITIONAL / FAIL |
| `/eval-zuckerman` | Framing quality (10 criteria) | Score /50 |
| `/eval-zuckerman-lite` | Early puzzle check (3 gates) | PASS / FAIL |
| `/eval-paper-quality` | Argument, evidence, theory, contribution, prose | Score /50 |
| `/eval-introduction` | Introduction arc, gap typology, stakes, reader psychology | Score /30 |
| `/eval-findings` | Concept organization, evidence-theory interleaving, quote handling, narrative | Score /30 |
| `/eval-methods` | Setting justification, data description, analytical transparency, iteration | Score /30 |
| `/eval-lit-review` | Conversation identification, puzzle construction, citation depth, narrative arc | Score /35 |
| `/eval-discussion` | Contribution positioning, implications, boundaries, coherence | Score /30 |
| `/eval-abstract` | Hook, arc compression, method/finding/contribution signals | Score /25 |
| `/eval-tables-figures` | Analytical purpose, design clarity, captions, text integration | Score /25 |
| `/eval-contribution` | Contribution type diagnosis | Type + confidence |
| `/eval-becker` | Generalizability | PASS / FAIL |
| `/eval-genre` | Inductive vs. deductive register | PASS / FAIL |
| `/eval-limitations` | Boundary conditions in manuscript | PASS / FAIL |
| `/eval-citations` | Literature coverage | Count + verdict |
| `/audit-claims` | Raw data audit for all claims | Concern flags |
| `/verify-claims` | Verification package for external review | Defensibility ratings |
| `/simulate-review` | Adversarial peer reviews | Fatal flaw count |
| `/test-counter-evidence` | Counter-evidence documented and addressed? | PASS / FAIL |
| `/test-alt-interpretations` | Alternative explanations less plausible? | PASS / FAIL |
| `/test-boundary-conditions` | Scope conditions documented? | PASS / FAIL |
| `/export-test-report` | Quality report for coauthors/reviewers/editors | MD or HTML |

**Thresholds** are configurable per project or per target journal via `rubrics/submission_thresholds.json`, with presets for `top_journal`, `field_journal`, and `working_paper`.

**Want to review the eval standards?** Open `docs/theory-forge-navigator.html` in any browser — a self-contained interface that lets you walk through every check across all 7 section evals, annotate where you agree/disagree/have questions, and export your annotations as JSON or Markdown.

### Output

| Skill | What It Does |
|---------|-------------|
| `/draft-paper` | Generate journal-ready manuscript |
| `/build-lit-review` | Build bibliography from identified theory/lens |
| `/export [format]` | Convert to LaTeX, Word, PDF, HTML |
| `/describe-ai-use` | Generate AI attribution statement for methods section |

### Project Management

| Skill | What It Does |
|---------|-------------|
| `/status` | Workflow progress, eval results dashboard, staleness indicators |
| `/consensus-config` | Configure consensus settings (N per stage, thresholds) |
| `/create-agent` | Build bespoke agents for project-specific needs |
| `/extend-forge` | Add a new skill to theory-forge — full build-and-wire workflow, then returns to research |
| `/repair-state` | Diagnose and fix state.json problems |
| `/student-mode` | Toggle learning scaffolding (predictions, explanations) |

---

## How Quality Checks Work

### Consensus Mode (Default: On)

Every evaluation runs N times (typically 5-10), computing per-criterion stability:

```
/eval-zuckerman results:
  motivate_paper:     4.2/5  (CV: 0.06, 🟢 HIGH)
  know_audience:      3.8/5  (CV: 0.12, 🟡 MEDIUM)
  puzzle_in_world:    2.1/5  (CV: 0.31, 🔴 LOW)    ← flag for review
```

- 🟢 HIGH: CV < 10% — defensible, stable signal
- 🟡 MEDIUM: CV 10-25% — mostly stable, note variance
- 🔴 LOW: CV > 25% — ambiguous, requires human judgment

Use `--quick` on any eval for a single run when iterating.

### Staleness Detection

Each eval tracks SHA-256 checksums of its upstream files. When you change a draft or reframe, downstream evals are automatically marked stale. `/check-submission` re-runs only what's changed.

### `/check-submission`

Runs all relevant checks in dependency order, skips anything with current results, and generates `SUBMISSION_READINESS.md` — a single document showing where your paper stands against configurable thresholds.

```
/check-submission              # Full suite with consensus
/check-submission --quick      # Single-run, fast iteration
/check-submission --preset top_journal
/check-submission --skip citations
```

A quality gate warns before `/export` if submission readiness hasn't been checked.

---

## A Suggested Path

Most theory-building papers follow: find something → figure out why → frame it → verify it → write it.

```
/explore-data → /hunt-patterns → /eval-zuckerman-lite
                                        │
                          Is this a puzzle? → No? Try a different pattern.
                                        │
                                       Yes
                                        │
            /find-theory → /find-lens → /mine-qual ↔ /smith-frames
                                                │
                                        /eval-zuckerman
                                                │
                                  Framing solid? → No? /new-frame, loop.
                                                │
                                               Yes
                                                │
                        /audit-claims → /verify-claims → /draft-paper
                                                │
                                  Section-level evals (run any/all):
                                  /eval-introduction, /eval-findings,
                                  /eval-methods, /eval-lit-review,
                                  /eval-discussion, /eval-abstract,
                                  /eval-tables-figures
                                                │
                                    /check-submission → /export
```

**This is one path, not the only one.** Every skill works standalone. Use `/eval-contribution` to diagnose what kind of paper you're writing — not everything is a theory violation.

---

## Design Principles

**Adversarial by default.** `/hunt-patterns` documents killed findings. `/mine-qual` requires disconfirming evidence. `/audit-claims` searches all data for challenging evidence. Three standalone adversarial tests check counter-evidence, alternative interpretations, and boundary conditions independently.

**Quality gates are warnings, not walls.** Skills suggest a sequence but don't enforce it. You can proceed past a warning if you have good reason.

**Frame shifts are normal.** Expect 3-5 complete reframings. `/new-frame` archives everything, marks evals stale, gives you a clean slate for theory while preserving empirical work.

**Extensible.** See below.

---

## Multiple Contribution Types

| Type | Evaluation Framework |
|------|---------------------|
| Theory Violation | Zuckerman's 10 criteria |
| Theory Elaboration | Fisher & Aguinis |
| Phenomenon Description | Weick |
| Methodological | Abbott's heuristics |
| Practical Insight | Corley & Gioia |

---

## Add Your Own Tools

Theory-forge is designed to be extended. Three skills scaffold new capabilities:

**`/author-data-source [tool-name]`** — Add support for a new data format (Dedoose, NVivo, MAXQDA, Otter.ai, etc.). Creates a Python importer, documentation, and a registry entry so skills like `/explore-data` auto-discover the source.

**`/author-methodology [tradition-name]`** — Add a new evaluation framework or analytical tradition (narrative analysis, process tracing, QCA, etc.). Creates a rubric, an eval skill, and documentation. The new eval is immediately available via `/eval [name]` and `/check-submission`.

**`/create-agent`** — Build a bespoke analytical agent for project-specific needs. Custom agents live alongside core skills and register in `registry.json`.

To contribute upstream: run the authoring skill, fork the repo, copy the generated files, open a PR. The skills produce everything needed.

---

## Requirements

- Claude Code
- Your data in accessible files (CSV, Excel, text for interviews)
- Domain expertise — this accelerates your work, doesn't replace your judgment
- Python 3.9+ with `anthropic` package (for consensus mode)

---

## Origin

Developed by Matt Beane (UC Santa Barbara) while using Claude Code to produce papers from dormant datasets. See [`CREDITS.md`](CREDITS.md) for acknowledgments.

MIT License. Questions? Open an issue or contact mattbeane@ucsb.edu.
