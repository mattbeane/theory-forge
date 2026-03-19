# Evaluation Result Persistence

After any evaluation completes, results are persisted to `state.json` for cross-session tracking.

## Storage Format

Write to `eval_results.{eval_type}.frame_{current_frame}.latest`:

```json
{
  "timestamp": "[current ISO timestamp]",
  "scores": {
    "[criterion_1]": 4.2,
    "[criterion_2]": 3.8
  },
  "total": 38,
  "max_total": 50,
  "verdict": "PASS",
  "consensus": {
    "n_runs": 5,
    "stability": "HIGH",
    "cv": 0.08,
    "ci_lower": 35.2,
    "ci_upper": 40.8
  },
  "stale": false,
  "stale_reason": null,
  "upstream_checksums": {
    "analysis/framing/frame-1/FRAMING_OPTIONS.md": "sha256:abc123...",
    "analysis/patterns/PATTERN_REPORT.md": "sha256:def456..."
  },
  "output_file": "analysis/evals/[eval_type]_frame_[N].md"
}
```

## Fields

| Field | Required | Description |
|-------|----------|-------------|
| `timestamp` | Yes | ISO timestamp of evaluation completion |
| `scores` | Yes | Per-criterion scores (keys vary by eval type) |
| `total` | If applicable | Sum score (null for non-numeric evals) |
| `max_total` | If applicable | Maximum possible score |
| `verdict` | Yes | `PASS`, `FAIL`, or `CONDITIONAL` |
| `consensus` | If consensus enabled | Stability metrics from N-run analysis |
| `stale` | Yes | Whether upstream files have changed |
| `stale_reason` | If stale | Which file changed |
| `upstream_checksums` | Yes | SHA-256 hashes for staleness detection |
| `output_file` | Yes | Path to the generated evaluation report |

## Post-Persistence

1. Update `state.json` root `updated_at` timestamp
2. Log to `DECISION_LOG.md`: `"{eval_type} — {verdict} ({score}/{max} | {stability})"`
3. If verdict is `FAIL`, add to any active warnings list
