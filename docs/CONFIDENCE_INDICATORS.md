# Confidence Indicators

Theory-forge commands now surface **confidence and stability information** directly in their markdown output, making statistical consensus visible to researchers rather than just storing it in state.json.

## Overview

When consensus mode is enabled, skills that run N-run analysis will include confidence assessment sections in their output. This makes the uncertainty visible and helps researchers make informed decisions.

### Stability Badges

| Badge | Meaning | CV / Rate | Recommendation |
|-------|---------|-----------|----------------|
| 🟢 HIGH | Stable, reproducible | CV < 10% or rate ≥ 75% | Include with confidence |
| 🟡 MEDIUM | Mostly stable | CV 10-25% or rate 50-74% | Include, note variance |
| 🔴 LOW | Unstable, verify manually | CV > 25% or rate < 50% | Review carefully |
| ⚪ UNKNOWN | Insufficient data | n < 3 | Needs more runs |

## Command Output

### Pattern Hunting (`/hunt-patterns`)

When consensus mode is enabled, PATTERN_REPORT.md will include:

```markdown
## Confidence Assessment

*Based on 25 consensus runs (claude-sonnet-4-20250514)*

**Overall Stability:** 🟢 HIGH

### Metrics
| Finding | Value | 95% CI | CV | Stability |
|---------|-------|--------|-----|-----------|
| Effect size (β) | 0.38 | [0.34, 0.42] | 8% | 🟢 HIGH |
| R² | 0.24 | [0.21, 0.27] | 11% | 🟡 MEDIUM |

### ⚠️ Flags for Review
- Metric 'interaction_term' has LOW stability (CV=32%)

### Execution Details
- **Runs:** 25
- **Time:** 45.2s
- **Tokens:** 125,000
- **Est. Cost:** $0.75
```

### Qualitative Mining (`/mine-qual`)

When consensus mode is enabled, QUAL_EVIDENCE_REPORT.md will include stability for each quote:

```markdown
**Supporting evidence**:

> "Workers developed informal workarounds to get around the automation..."
> — INT-014, Nurse, Site A
> 🟢 HIGH (appeared in 14/15 runs, 93%)

> "The robots couldn't handle the edge cases..."
> — INT-023, Technician, Site B
> 🟡 MEDIUM (appeared in 10/15 runs, 67%)

**⚠️ Low-stability quotes** (review carefully):

> "Sometimes you just have to ignore the system..."
> — INT-007, Supervisor, Site A
> 🔴 LOW (appeared in 5/15 runs, 33%)
> *Warning: This quote may be cherry-picked. Consider dropping or noting as illustrative only.*
```

## Using the Formatters

The formatters in `lib/consensus/formatters.py` can be used programmatically:

```python
from lib.consensus import (
    format_confidence_section,      # Full markdown section
    format_metric_row,              # Single metric table row
    format_quote_row,               # Single quote table row
    format_metrics_inline,          # Inline text for prose
    format_stability_summary,       # Brief summary line
    format_quote_list_with_stability,  # Quote list with badges
    format_flagged_items_callout,   # Warning callout block
    stability_emoji,                # Just the emoji (🟢, 🟡, 🔴, ⚪)
    stability_label,                # Emoji + label (🟢 HIGH)
)
```

### Examples

```python
# Full confidence section
confidence_md = format_confidence_section(
    result,
    include_metrics=True,
    include_quotes=True,
    include_flags=True,
)

# Brief summary for status displays
summary = format_stability_summary(result)
# Returns: "🟢 HIGH (3 metrics, 5 quotes, 0 flags)"

# Inline metrics for prose
inline = format_metrics_inline(result)
# Returns: "Effect size=0.38 (95% CI: [0.34, 0.42], 🟢 HIGH)"

# Quote list with stability indicators
quote_md = format_quote_list_with_stability(result.quotes, warn_low_stability=True)
```

## Why This Matters

### Before Confidence Indicators

Single-run analysis outputs:

```
The effect size is β = 0.38.
```

- Non-reproducible: different prompt → different answer
- No uncertainty quantification
- Reviewers can't verify

### After Confidence Indicators

Consensus analysis outputs:

```
The effect size is β = 0.38 (95% CI: [0.34, 0.42], 🟢 HIGH stability).
```

- Reproducible: "We ran this 25 times"
- Defensible: confidence intervals for peer review
- Honest: LOW stability findings flagged, not hidden

## Configuration

Enable/disable consensus mode via `/consensus-config` or directly in state.json:

```json
{
  "consensus": {
    "stages": {
      "hunt_patterns": {
        "enabled": true,
        "n": 25
      },
      "mine_qual": {
        "enabled": true,
        "n": 15
      }
    }
  }
}
```

## Related Skills

- `/consensus-config` - Enable/disable consensus mode, adjust settings
- `/hunt-patterns` - Pattern hunting with metric stability
- `/mine-qual` - Qualitative mining with quote stability
- `/status` - See which stages have consensus results
