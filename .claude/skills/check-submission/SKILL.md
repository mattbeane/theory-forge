---
name: check-submission
description: Submission Readiness Check
---

# Submission Readiness Check

You are the SUBMISSION-CHECKER agent. Run ALL relevant evaluations against the current paper state and produce a single PASS/FAIL report. This is the equivalent of `pytest --verbose` for an academic paper.

## Arguments

- `$ARGUMENTS` may contain:
  - `config` — Show/edit threshold configuration
  - `--quick` — Single-run mode (no consensus, N=1)
  - `--preset [name]` — Use a threshold preset: "top_journal", "field_journal", "working_paper"
  - `--skip [eval_name]` — Skip specific evaluation(s)
  - `--force` — Run even if previous results are fresh (normally skips current results)

## Prerequisites

Before running:
1. Read `state.json` — verify project is initialized
2. At minimum, `workflow.smith_frames.status === "completed"` (you need a framing to evaluate)
3. Ideally, `workflow.draft_paper.status === "completed"` for the full suite

## Step 1: Load Configuration

1. Read `state.json`
2. Load thresholds from `rubrics/submission_thresholds.json`
3. If `--preset` specified, merge preset thresholds over defaults
4. Apply project overrides from `state.json.submission_thresholds.overrides`
5. Display active thresholds

## Step 2: Determine Test Suite

Based on contribution type and workflow state, determine which tests to run:

### Always Run (Core Suite)
| Test | Eval Key | What It Checks |
|------|----------|---------------|
| Contribution Type | `contribution` | What kind of paper this is |
| Paper Quality | `paper_quality` | Argument, evidence, theory, contribution, prose |
| Introduction | `introduction` | Arc structure, gap construction, stakes, RQ, reader psychology |
| Limitations | `limitations` | Boundary conditions properly framed |
| Citations | `citations` | Adequate literature coverage |
| Counter-Evidence | `counter_evidence` | Disconfirming evidence addressed |
| Alt Interpretations | `alt_interpretations` | Alternative explanations considered |
| Boundary Conditions | `boundary_conditions` | Scope conditions documented |

### Contribution-Type Conditional
| Test | When | Eval Key |
|------|------|----------|
| Zuckerman | Type 1: Theory violation | `zuckerman` |
| Becker | All types | `becker` |
| Genre | After draft | `genre` |

### Workflow-State Conditional
| Test | When | Eval Key |
|------|------|----------|
| Audit Claims | After /audit-claims | `audit_claims` |
| Verify Claims | After /verify-claims | `claim_verification` |
| Simulated Review | After /draft-paper | `simulate_review` |

## Step 3: Check Freshness

For each test in the suite:
1. Look up `state.json.eval_results.[eval_key].frame_[current_frame].latest`
2. If result exists AND `stale === false` AND `--force` not set:
   - Read `upstream_checksums` from the stored result
   - Compute current SHA-256 of each upstream file:
     ```bash
     shasum -a 256 [file_path] | cut -d' ' -f1
     ```
   - If ALL checksums match: result is FRESH — use cached result
   - If ANY checksum differs: result is STALE — mark for re-run
3. If no result exists: mark for re-run
4. Report: "X tests fresh, Y tests need re-run, Z tests not yet run"

## Step 4: Run Missing/Stale Tests

For each test needing a run, execute the corresponding evaluation:

**If consensus mode enabled (default) and `--quick` not set:**
1. Run each evaluation following its own command instructions
2. Each eval persists its own results to state.json (via their State Persistence sections)
3. Consensus stats (n_runs, stability, CV, CI) are included automatically

**If `--quick` mode:**
1. Run each evaluation once (N=1)
2. Still persist results to state.json
3. Skip stability computation

**Run order matters** — some evals depend on others:
1. First: `eval-contribution` (determines which other evals apply)
2. Then: Independent evals in parallel (paper_quality, limitations, citations, becker)
3. Then: Type-specific evals (zuckerman if Type 1)
4. Then: Adversarial tests (counter_evidence, alt_interpretations, boundary_conditions)
5. Last: simulate_review (if draft exists)

## Step 5: Evaluate Against Thresholds

For each test result, compare against configured thresholds:

### Score-Based Tests (zuckerman, paper_quality, claim_verification)
- Read `total` from eval result
- Compare against `min_score` from thresholds
- PASS if total >= min_score, FAIL otherwise
- For zuckerman: also check `min_criteria_pass` (count of criteria scoring >= 4)

### Verdict-Based Tests (becker, genre, limitations, counter_evidence, alt_interpretations, boundary_conditions)
- Read `verdict` from eval result
- Compare against `required_verdict` from thresholds
- PASS if verdict meets or exceeds required level

### Count-Based Tests (citations, audit_claims, simulate_review)
- Citations: PASS if count >= `min_count`
- Audit claims: PASS if high_concern_count <= `max_high_concern`
- Simulate review: PASS if fatal_flaws_count <= `max_fatal_flaws`

### Overall Verdict
- **PASS**: ALL tests meet thresholds
- **CONDITIONAL**: 1-2 tests miss thresholds by small margin (within 10% of threshold value)
- **FAIL**: Any test significantly below threshold

## Step 6: Generate Report

Write `analysis/quality/SUBMISSION_READINESS.md`:

```
# Submission Readiness Report

**Project**: [from state.json.project_name]
**Date**: [current date]
**Target Journal**: [from state.json.metadata.target_journal or "Not specified"]
**Threshold Preset**: [preset name or "defaults"]
**Consensus Mode**: [enabled/disabled, N per stage]

---

## Overall Verdict: [PASS / CONDITIONAL / FAIL]

[If PASS]: All tests pass configured thresholds. Paper is ready for submission.
[If CONDITIONAL]: Minor issues found. Address warnings before submission.
[If FAIL]: Significant issues must be resolved before submission.

---

## Test Results

| # | Test | Score | Threshold | Stability | Verdict |
|---|------|-------|-----------|-----------|---------|
| 1 | Contribution Type | [type] | — | — | INFO |
| 2 | Zuckerman | 39/50 | >=35 | HIGH (CV=8%) | PASS |
| 3 | Paper Quality | 37/50 | >=35 | HIGH (CV=6%) | PASS |
| 4 | Becker | PASS | PASS | HIGH (100%) | PASS |
| 5 | Genre | PASS | PASS | — | PASS |
| 6 | Limitations | PASS | PASS | — | PASS |
| 7 | Citations | 87 | >=40 | — | PASS |
| 8 | Audit Claims | 0 HIGH | <=0 | — | PASS |
| 9 | Claim Verification | 32/40 | >=28 | MED (CV=12%) | PASS |
| 10 | Simulated Review | 0 fatal | <=0 fatal | — | PASS |
| 11 | Counter-Evidence | PASS | PASS | HIGH (100%) | PASS |
| 12 | Alt Interpretations | PASS | PASS | HIGH (80%) | PASS |
| 13 | Boundary Conditions | PASS | PASS | HIGH (100%) | PASS |

**Summary**: 12/12 PASS | 0 FAIL | 0 STALE

---

## Failures Requiring Action

[For each FAIL, provide:]
### [Test Name]: FAIL ([score] vs threshold [threshold])

**What's wrong**: [Specific issues from the eval output]
**How to fix**: [Actionable steps]
**Commands to run**: [Specific theory-forge commands]

---

## Warnings

[Items near threshold (within 15%) or with MEDIUM/LOW stability]

### [Test Name]: WARNING — Near Threshold
- Score: [X] (threshold: [Y], margin: [Z]%)
- Consider strengthening before submission

### [Test Name]: WARNING — Low Stability
- CV: [X]% across [N] runs
- Results may not be reproducible; consider re-running with higher N

---

## Stale Results

[If any tests were skipped because prerequisites not met]

---

## Consensus Details

[Per-eval stability breakdown, only if consensus mode was used]

---

## Cost Summary

- Total evaluations run: [N]
- Total API calls: [N x consensus_n per eval]
- Estimated cost: $[X]
- Time elapsed: [Y]s
```

## Step 7: State Management

After completing:
1. Update `state.json`:
   - Write to `eval_results.check_submission.frame_[current_frame].latest`:
     ```json
     {
       "timestamp": "[ISO]",
       "verdict": "PASS|CONDITIONAL|FAIL",
       "scores": {
         "tests_passed": 12,
         "tests_failed": 0,
         "tests_stale": 0,
         "tests_skipped": 1,
         "tests_total": 13
       },
       "total": 12,
       "max_total": 13,
       "details": {
         "zuckerman": {"score": 39, "threshold": 35, "verdict": "PASS"},
         "paper_quality": {"score": 37, "threshold": 35, "verdict": "PASS"}
       },
       "consensus": {
         "n_runs": "varies by test",
         "stability": "[worst across all tests]"
       },
       "stale": false,
       "upstream_checksums": {
         "[all files checked by all sub-evals]": "sha256:..."
       },
       "output_file": "analysis/quality/SUBMISSION_READINESS.md",
       "preset": "[preset name or null]",
       "cost_usd": 0.0,
       "duration_seconds": 0.0
     }
     ```
   - Set `workflow.check_submission.status` to "completed"
   - Set `workflow.check_submission.completed_at` to current ISO timestamp
   - Set `workflow.check_submission.verdict` to overall verdict
   - Add output path to `workflow.check_submission.outputs`
   - Update `updated_at` timestamp
2. Append entry to `DECISION_LOG.md`

## Subcommand: `config`

If `$ARGUMENTS` contains "config":
1. Display current thresholds (from submission_thresholds.json + project overrides)
2. Show available presets
3. Ask user what to change
4. Write changes to `state.json.submission_thresholds.overrides`

## Tips

- Run `/check-submission --quick` during active development for fast feedback
- Run `/check-submission` (full consensus) before actual submission
- Run `/check-submission --preset top_journal` to see if your paper meets top-venue standards
- If a test fails, the report tells you which command to run to fix the issue
- Use `/check-submission config` to adjust thresholds for your specific journal
