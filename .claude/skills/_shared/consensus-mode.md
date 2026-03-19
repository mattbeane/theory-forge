# Consensus Mode

When `state.json` has `consensus.stages.{skill_name}.enabled = true`, evaluations and analyses run multiple times to measure stability.

## How It Works

1. **Run N times** (default varies by skill; configurable in `state.json` → `consensus.stages.{skill_name}.n`)
2. **For each metric, compute consistency across runs**:
   - Mean, standard deviation, 95% confidence interval
   - Coefficient of variation (CV = SD / mean)
3. **Rate stability** using CV thresholds:

| Level | CV Threshold | Emoji | Meaning | Recommendation |
|-------|-------------|-------|---------|----------------|
| HIGH | < 10% | 🟢 | Defensible, stable signal | Report with confidence |
| MEDIUM | 10-25% | 🟡 | Mostly stable, some variance | Note variance, still usable |
| LOW | > 25% | 🔴 | Ambiguous, unstable | Requires human judgment; flag for review |

## Default N Values by Skill Type

| Skill Type | Default N | Rationale |
|-----------|-----------|-----------|
| Pattern discovery (hunt-patterns) | 25 | High variance in exploratory analysis |
| Qualitative mining (mine-qual) | 15 | Quote detection varies by run |
| Claim verification (verify-claims) | 10 | Scoring is more constrained |
| Eval rubrics (eval-zuckerman, etc.) | 5 | Structured rubrics are more stable |

## Output Format

When consensus is enabled, include in output for each metric:
```
metric_name:  4.2/5  (CV: 0.06, 🟢 HIGH)
```

Full consensus block:
```
mean ± SD (95% CI: [lower, upper])
CV: X%
Stability: 🟢/🟡/🔴
```

## Quick Mode

All consensus-enabled skills support `--quick` for a single run during iteration. This skips consensus and produces results faster but without stability metrics.

## Configuration

Use `/consensus-config` to:
- Enable/disable consensus per stage
- Set N per stage
- Adjust CV thresholds
- View current configuration
