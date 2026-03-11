# Export Test Report

Generate a formatted test report from all evaluation results for sharing with coauthors, reviewers, or editors.

## Arguments

- `$ARGUMENTS` may contain:
  - `--for coauthors` — Full detail, all scores, action items (default)
  - `--for reviewers` — Methodology focus, explain what consensus means
  - `--for editors` — Executive summary only
  - `--format html` — Generate HTML (default: markdown)

## Prerequisites

- At least one evaluation must have results in `state.json.eval_results`
- Ideally, `/check-submission` has been run for a complete picture

## Steps

### Step 1: Load All Results

Read `state.json.eval_results` for the current frame. For each eval:
- Extract latest result (scores, verdict, consensus, staleness)
- Load thresholds from `rubrics/submission_thresholds.json` + project overrides

### Step 2: Generate Report

#### For Coauthors (default)
Full detail:
- Every eval score with threshold comparison
- Stability ratings with explanation
- Stale results flagged
- Action items for failures
- Timeline of evaluation runs
- Cost summary
- Methodology note: "Evaluations run N times with LLM-as-judge, scores aggregated with stability metrics"

#### For Reviewers
Methodology focus:
- Summary table of evaluations performed
- Explanation of consensus methodology (N runs, CV, stability)
- Link to verification package if it exists
- Claim-evidence coverage summary
- AI attribution statement (reference /describe-ai-use output if available)

#### For Editors
Executive summary:
- Overall verdict (1 line)
- Key strengths (2-3 bullets)
- Areas of concern (if any)
- Verification status

### Step 3: Output

**Markdown**: Write to `analysis/quality/TEST_REPORT.md`
**HTML**: Write to `analysis/quality/TEST_REPORT.html` with inline CSS for clean printing

## State Persistence

This command is read-only — it doesn't update eval results.
Update `state.json`:
- Set `workflow.export_test_report.status` to "completed"
- Set `workflow.export_test_report.completed_at` to current ISO timestamp
- Add output path to `workflow.export_test_report.outputs`
