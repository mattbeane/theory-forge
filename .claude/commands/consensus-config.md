# Consensus Configuration

You are the CONSENSUS-CONFIG agent. Your job is to help users configure statistical consensus settings for their paper mining project.

## Arguments

The user may specify:
- `$ARGUMENTS` - Subcommand: `enable`, `disable`, `show`, `set <stage> <n>`, `thresholds`

## What Is Consensus Mode?

Consensus mode runs LLM-dependent stages multiple times (N runs) and computes statistical aggregates:
- **Effect sizes** get confidence intervals (mean ± SD, 95% CI)
- **Quotes** get stability scores (appeared in X/N runs)
- **Claims** get defensibility ratings (DEFENSIBLE / MOSTLY DEFENSIBLE / NOT DEFENSIBLE)

This makes your analysis **reproducible and defensible** for peer review.

## Commands

### `/consensus-config` or `/consensus-config show`

Display current consensus settings:

```
╔══════════════════════════════════════════════════════════════════╗
║  CONSENSUS CONFIGURATION                                         ║
╚══════════════════════════════════════════════════════════════════╝

Status: ENABLED

─────────────────────────────────────────────────────────────────────
STAGE SETTINGS
─────────────────────────────────────────────────────────────────────

  Stage              N runs    Enabled
  ─────────────────────────────────────
  hunt-patterns      25        ✓
  mine-qual          15        ✓
  verify-claims      10        ✓

─────────────────────────────────────────────────────────────────────
EVALUATION STAGES
─────────────────────────────────────────────────────────────────────

  Stage                    N runs    Enabled
  ──────────────────────────────────────────
  eval-zuckerman           5         ✓
  eval-paper-quality       5         ✓
  eval-becker              5         ✓
  eval-genre               5         ✓
  eval-contribution        5         ✓
  eval-limitations         5         ✓
  eval-citations           5         ✓
  simulate-review          5         ✓
  check-submission         7         ✓
  test-counter-evidence    5         ✓
  test-alt-interpretations 5         ✓
  test-boundary-conditions 5         ✓

─────────────────────────────────────────────────────────────────────
STABILITY THRESHOLDS
─────────────────────────────────────────────────────────────────────

  Numeric metrics (CV-based):
    HIGH stability:    CV < 10%
    MEDIUM stability:  CV 10-25%
    LOW stability:     CV > 25%

  Quote appearance:
    HIGH stability:    ≥ 75% of runs
    MEDIUM stability:  50-74% of runs
    LOW stability:     < 50% of runs

─────────────────────────────────────────────────────────────────────
ESTIMATED COST
─────────────────────────────────────────────────────────────────────

  Per full pipeline run: ~$0.50-1.00
  (Based on claude-sonnet-4-20250514 @ ~$6/M tokens)

─────────────────────────────────────────────────────────────────────
```

### `/consensus-config enable`

Enable consensus mode for all supported stages.

Updates `state.json`:
```json
{
  "consensus": {
    "enabled": true,
    "stages": {
      "hunt_patterns": { "n": 25, "enabled": true },
      "mine_qual": { "n": 15, "enabled": true },
      "verify_claims": { "n": 10, "enabled": true }
    }
  }
}
```

### `/consensus-config disable`

Disable consensus mode (revert to single-run analysis).

### `/consensus-config set <stage> <n>`

Set the number of runs for a specific stage.

Examples:
- `/consensus-config set hunt-patterns 50` — Run pattern hunting 50 times
- `/consensus-config set mine-qual 20` — Run qual mining 20 times
- `/consensus-config set verify-claims 5` — Run verification 5 times (faster, less precise)

### `/consensus-config thresholds`

Show and optionally modify stability thresholds.

```
Current thresholds:
  high_stability_cv: 0.10 (CV < 10% = HIGH)
  medium_stability_cv: 0.25 (CV < 25% = MEDIUM)
  quote_high_stability: 0.75 (≥75% appearance = HIGH)
  quote_medium_stability: 0.50 (≥50% appearance = MEDIUM)

To modify, update state.json → consensus.thresholds
```

## State Schema

Consensus configuration lives in `state.json` under the `consensus` key:

```json
{
  "consensus": {
    "enabled": true,
    "default_n": 10,
    "stages": {
      "hunt_patterns": {
        "n": 25,
        "enabled": true
      },
      "mine_qual": {
        "n": 15,
        "enabled": true
      },
      "verify_claims": {
        "n": 10,
        "enabled": true
      },
      "eval_zuckerman": { "n": 5, "enabled": true },
      "eval_paper_quality": { "n": 5, "enabled": true },
      "eval_becker": { "n": 5, "enabled": true },
      "eval_genre": { "n": 5, "enabled": true },
      "eval_contribution": { "n": 5, "enabled": true },
      "eval_limitations": { "n": 5, "enabled": true },
      "eval_citations": { "n": 5, "enabled": true },
      "simulate_review": { "n": 5, "enabled": true },
      "check_submission": { "n": 7, "enabled": true },
      "test_counter_evidence": { "n": 5, "enabled": true },
      "test_alt_interpretations": { "n": 5, "enabled": true },
      "test_boundary_conditions": { "n": 5, "enabled": true }
    },
    "thresholds": {
      "high_stability_cv": 0.10,
      "medium_stability_cv": 0.25,
      "quote_high_stability": 0.75,
      "quote_medium_stability": 0.50
    },
    "provider": "anthropic",
    "model": "claude-sonnet-4-20250514"
  }
}
```

## When to Enable Consensus

**Enable consensus when:**
- Preparing analysis for peer review
- Wanting defensible effect sizes with confidence intervals
- Checking for cherry-picked quotes in qualitative analysis
- Final verification before drafting

**Disable consensus when:**
- Early exploration (single runs are faster and cheaper)
- Quick iteration on framing options
- Cost is a concern (consensus costs N× more)

## Cost Estimates

Using Claude Sonnet ($3/M input, $15/M output, ~$6/M average):

| Stage | Default N | Tokens/run | Cost |
|-------|-----------|------------|------|
| hunt-patterns | 25 | ~2,000 | ~$0.30 |
| mine-qual | 15 | ~3,000 | ~$0.27 |
| verify-claims | 10 | ~2,500 | ~$0.15 |
| **Total** | | | **~$0.72** |

For comparison, GPT-4o-mini is ~10× cheaper (~$0.07 total).

## Execution

The consensus engine is in `lib/consensus/`. See the module documentation for programmatic usage.

To run consensus analysis manually:

```python
import asyncio
from lib.consensus import ConsensusEngine, extract_effect_sizes

async def main():
    engine = ConsensusEngine(provider="anthropic")
    result = await engine.run_with_consensus(
        system_prompt="You are analyzing patterns...",
        user_prompt="[data here]",
        n=25,
        extract_metrics_fn=extract_effect_sizes,
    )
    print(f"Stability: {result.overall_stability}")
    for name, metric in result.metrics.items():
        print(f"  {name}: {metric.mean:.3f} ± {metric.std:.3f} (CV={metric.cv:.1%})")

asyncio.run(main())
```

### Evaluation Stages (NEW)

These stages run evaluations with consensus for the submission test suite:

| Stage | Default N | Purpose |
|-------|-----------|---------|
| eval_zuckerman | 5 | Zuckerman 10-criteria evaluation |
| eval_paper_quality | 5 | Paper quality rubric |
| eval_becker | 5 | Becker concept evaluation |
| eval_genre | 5 | Genre consistency check |
| eval_contribution | 5 | Contribution type diagnosis |
| eval_limitations | 5 | Limitations framing check |
| eval_citations | 5 | Citation coverage check |
| simulate_review | 5 | Simulated peer review |
| check_submission | 7 | Unified test runner (higher N for aggregate) |
| test_counter_evidence | 5 | Counter-evidence coverage test |
| test_alt_interpretations | 5 | Alternative interpretations survivability |
| test_boundary_conditions | 5 | Boundary conditions documentation |

### Quick Mode

Any command that supports consensus can be run with `--quick` to skip consensus:
- Runs the evaluation once (N=1)
- Skips stability computation
- Still persists results to `state.json.eval_results`
- Useful during active development/iteration when you want fast feedback
- NOT recommended for final submission checks

Example: `/eval-zuckerman --quick` or `/check-submission --quick`

### Default: Enabled

As of v1.2.0, consensus mode is **enabled by default** for all stages including evaluations. This means every evaluation runs N times and reports stability metrics. The rationale: a single-run evaluation is like running your test suite once and hoping it passes. Consensus catches evaluation instability — if a criterion scores 5/5 on one run but 2/5 on another, that's a signal the paper's handling of that criterion is ambiguous.

To disable: `/consensus-config disable`
To run a single eval without consensus: append `--quick` to any eval command

## Tips

1. **Start with consensus enabled** (default) — disable only for fast iteration
2. **Higher N = more precision** but diminishing returns past N=50
3. **LOW stability findings aren't wrong** — they reveal ambiguity in your data
4. **Quote stability catches cherry-picking** — a quote that appears in 3/15 runs is suspect
5. **Run `/status`** to see consensus results from previous stages
6. **Use `--quick` for fast feedback** during active development, full consensus for final checks
