# Theory Forge

**A test suite for academic research.**

Theory-forge is a collection of AI agents (Claude Code slash commands) for producing theory-building papers from qualitative and mixed-methods data. Each agent handles one analytical task — discovering patterns, building framings, auditing claims. You compose them however your project demands.

What makes it different: every evaluation runs through a statistical consensus engine (monte-carlo LLM-as-judge), results persist with staleness tracking, and a unified test runner produces a single PASS/FAIL verdict for submission readiness. It's `pytest --verbose` for your paper.

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
/check-submission      # Run the full test suite
```

---

## Commands

### Discovery

| Command | What It Does |
|---------|-------------|
| `/explore-data` | Initial reconnaissance — what's in the data, what's interesting |
| `/hunt-patterns` | Find robust empirical patterns with adaptive stopping |
| `/mine-qual` | Extract mechanism evidence from interviews, with adversarial checks |
| `/surface-absences` | Identify what's conspicuously *missing* from the data |
| `/integrate-quant-qual` | Connect quantitative patterns with qualitative mechanisms |
| `/measure-at-scale` | Measure constructs across full corpus; [GABRIEL](https://github.com/openai/GABRIEL)-compatible |

### Framing

| Command | What It Does |
|---------|-------------|
| `/find-theory` | Identify which theory your finding violates or extends |
| `/find-lens` | Find sensitizing literature that explains heterogeneity |
| `/smith-frames` | Generate and evaluate multiple theoretical framings |
| `/new-frame` | Archive current framing, start fresh (expect 3-5 reframings) |
| `/compare-frames` | Side-by-side comparison of framings |

### Test Suite

The core differentiator. Every evaluation persists scores to `state.json`, tracks upstream file changes for staleness, and runs through consensus mode by default.

| Command | What It Tests | Output |
|---------|--------------|--------|
| `/check-submission` | **Unified runner** — orchestrates all tests below | PASS / CONDITIONAL / FAIL |
| `/eval-zuckerman` | Framing quality (10 criteria) | Score /50 |
| `/eval-zuckerman-lite` | Early puzzle check (3 gates) | PASS / FAIL |
| `/eval-paper-quality` | Argument, evidence, theory, contribution, prose | Score /50 |
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
| `/export-test-report` | Formatted report for coauthors/reviewers/editors | MD or HTML |

**Thresholds** are configurable per project or per target journal via `rubrics/submission_thresholds.json`, with presets for `top_journal`, `field_journal`, and `working_paper`.

### Output

| Command | What It Does |
|---------|-------------|
| `/draft-paper` | Generate journal-ready manuscript |
| `/build-lit-review` | Build bibliography from identified theory/lens |
| `/export [format]` | Convert to LaTeX, Word, PDF, HTML |
| `/describe-ai-use` | Generate AI attribution statement for methods section |

### Project Management

| Command | What It Does |
|---------|-------------|
| `/status` | Workflow progress, eval results dashboard, staleness indicators |
| `/consensus-config` | Configure consensus settings (N per stage, thresholds) |
| `/create-agent` | Build bespoke agents for project-specific needs |
| `/repair-state` | Diagnose and fix state.json problems |
| `/student-mode` | Toggle learning scaffolding (predictions, explanations) |

---

## How the Test Suite Works

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

The unified runner. Orchestrates all tests in dependency order:

1. Loads thresholds (defaults, preset, or project overrides)
2. Determines which tests apply based on contribution type
3. Checks freshness — skips evals with current results
4. Runs missing/stale tests with consensus
5. Compares scores against thresholds
6. Generates `SUBMISSION_READINESS.md`

```
/check-submission              # Full suite with consensus
/check-submission --quick      # Single-run, fast iteration
/check-submission --preset top_journal
/check-submission --skip citations
```

A quality gate hook warns before `/export` if check-submission hasn't passed.

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
                                    /check-submission → /export
```

**This is one path, not the only one.** Every command works standalone. Use `/eval-contribution` to diagnose what kind of paper you're writing — not everything is a theory violation.

---

## Design Principles

**Adversarial by default.** `/hunt-patterns` documents killed findings. `/mine-qual` requires disconfirming evidence. `/audit-claims` searches all data for challenging evidence. Three standalone adversarial tests check counter-evidence, alternative interpretations, and boundary conditions independently.

**Quality gates are warnings, not walls.** Commands suggest a sequence but don't enforce it. You can proceed past a warning if you have good reason.

**Frame shifts are normal.** Expect 3-5 complete reframings. `/new-frame` archives everything, marks evals stale, gives you a clean slate for theory while preserving empirical work.

**Extensible.** Add data sources (`/author-data-source`), methodologies (`/author-methodology`), or custom agents (`/create-agent`). Everything registers in `registry.json` for runtime discovery.

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

## Requirements

- Claude Code
- Your data in accessible files (CSV, Excel, text for interviews)
- Domain expertise — this accelerates your work, doesn't replace your judgment
- Python 3.9+ with `anthropic` package (for consensus mode)

---

## Origin

Developed by Matt Beane (UC Santa Barbara) while using Claude Code to produce papers from dormant datasets. See [`CREDITS.md`](CREDITS.md) for acknowledgments.

MIT License. Questions? Open an issue or contact mattbeane@ucsb.edu.
