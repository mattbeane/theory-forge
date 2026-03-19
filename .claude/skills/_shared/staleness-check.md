# Staleness Detection

Evaluations track SHA-256 checksums of their upstream files. When upstream files change, previous results are automatically marked stale.

## Before Running an Evaluation

1. Read `state.json` → `eval_results.{eval_type}.frame_{current_frame}.latest`
2. If a previous result exists:
   a. Compute current SHA-256 of upstream files:
      ```bash
      shasum -a 256 [file1] [file2] ... | cut -d' ' -f1
      ```
   b. Compare against stored `upstream_checksums`
   c. If **ALL match**: "Previous results are current (ran [timestamp]). Re-run anyway? [Y/n]"
   d. If **ANY differ**: "Upstream files changed since last eval. Running fresh evaluation."
3. If no previous result exists: proceed with evaluation.

## Upstream Files by Evaluation

Each evaluation tracks specific files:

| Eval Skill | Upstream Files |
|-----------|---------------|
| eval-zuckerman | `analysis/framing/frame-{N}/FRAMING_OPTIONS.md` |
| eval-contribution | `analysis/framing/frame-{N}/FRAMING_OPTIONS.md`, `analysis/patterns/PATTERN_REPORT.md` |
| eval-genre | `analysis/manuscript/DRAFT.md` |
| eval-becker | `analysis/framing/frame-{N}/FRAMING_OPTIONS.md` |
| verify-claims | `analysis/audit/claims.jsonl`, `evidence.jsonl`, `links.csv` |
| check-submission | All upstream eval results (meta-staleness) |

## How Staleness Propagates

When `/new-frame` is run:
- All framing-dependent evals are marked stale
- Pattern-level results remain valid (empirical work is preserved)
- `/check-submission` re-runs only stale evaluations
