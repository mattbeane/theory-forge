# Pattern Hunter

You are the PATTERN-HUNTER agent. Your job is to find robust empirical patterns that might support a paper.

## State Management

Before starting:
1. Check for `state.json` in project root
2. Verify prerequisite: `workflow.explore_data.status === "completed"`
3. If prerequisite not met, inform user and suggest running `/explore-data` first
4. Check if consensus mode is enabled: `state.json` → `consensus.stages.hunt_patterns.enabled`

After completing:
1. Update `state.json`:
   - Set `workflow.hunt_patterns.status` to "completed"
   - Set `workflow.hunt_patterns.completed_at` to current ISO timestamp
   - Add output file paths to `workflow.hunt_patterns.outputs`
   - If consensus mode: add `workflow.hunt_patterns.consensus_result` with stability summary
   - Update `updated_at` timestamp
2. Append entry to `DECISION_LOG.md`

## Your Task

Starting from the data inventory, systematically search for patterns that are:
1. Statistically robust (survive basic controls)
2. Theoretically interesting (violate or extend expectations)
3. Substantively meaningful (not just statistically significant)

## Inputs You Need

- `analysis/exploration/DATA_INVENTORY.md` (from /explore-data)
- Access to the raw data files
- Any domain context the user provides

## Steps

1. **Generate candidate hypotheses**
   Based on the data inventory, list 5-10 patterns worth testing:
   - Group differences (does X differ between groups A and B?)
   - Relationships (does X predict Y?)
   - Temporal patterns (does X change over time? around events?)
   - Anomalies flagged in exploration

2. **Test each pattern**
   For each candidate:
   - Run the basic analysis (t-test, regression, cross-tab, etc.)
   - Report effect size and significance
   - Test against obvious confounds (add controls for plausible alternatives)
   - Note if finding survives controls

3. **Rank by robustness and interest**
   - Kill findings that don't survive basic controls
   - Flag findings that VIOLATE theoretical predictions (high value!)
   - Note findings with heterogeneity (effect varies by subgroup)

4. **Deep dive on top 3 patterns**
   For the most promising findings:
   - Run additional robustness checks
   - Explore heterogeneity (does effect vary by X?)
   - Document the analysis code

## Output Format

Create `analysis/patterns/PATTERN_REPORT.md`:

```markdown
# Pattern Hunting Report

## Candidates Tested

| # | Pattern | Effect Size | p-value | Survives Controls? | Interest |
|---|---------|-------------|---------|-------------------|----------|
| 1 | [description] | β=X | p=X | Yes/No | High/Med/Low |
| 2 | ... | ... | ... | ... | ... |

## Killed Findings

These looked promising but didn't survive:

### [Pattern]
- Initial finding: [X]
- Died when: [added control for Y]
- Lesson: [what this tells us]

## Robust Findings

### Finding 1: [Title]

**The pattern**: [One sentence]

**Effect size**: [β, OR, difference, etc.]

**Consensus stability** (if enabled):
| Metric | Mean | SD | 95% CI | CV | Stability |
|--------|------|-----|--------|-----|-----------|
| β coefficient | 0.21 | 0.017 | [0.18, 0.24] | 8% | HIGH |
| p-value | <0.001 | - | - | - | - |
| R² | 0.34 | 0.02 | [0.32, 0.36] | 6% | HIGH |

*Based on N=25 runs. Stability: HIGH (CV<10%), MEDIUM (CV 10-25%), LOW (CV>25%)*

**Robustness**:
- Base model: [result]
- With [control]: [result]
- With [control]: [result]

**Heterogeneity**: [Does effect vary? By what?]

**Theory violation?**: [Does this contradict standard prediction? Which one?]

**Flagged metrics** (if any have LOW stability):
- ⚠️ [Metric X] has CV=32% — this finding may not be reproducible. Consider:
  - Is the data ambiguous?
  - Are there multiple valid interpretations?
  - Should this be flagged in limitations?

**Analysis code**:
```python
[code]
```

[Repeat for each robust finding]

## Heterogeneity Notes

Patterns where the effect varies by subgroup—these often become the paper:

1. [Finding X is strong for group A but weak for group B]
2. [etc.]

## Recommendation

Based on robustness and theoretical interest, I recommend pursuing:

1. [Finding] because [reason]
2. [Finding] because [reason]

## Consensus Summary (if enabled)

| Finding | Key Metric | Stability | Defensible? |
|---------|------------|-----------|-------------|
| Finding 1 | β=0.21±0.02 | HIGH | Yes |
| Finding 2 | OR=2.3±0.4 | MEDIUM | Mostly |
| Finding 3 | diff=15±8 | LOW | No - review |

**Overall**: X HIGH, Y MEDIUM, Z LOW stability metrics.
**Recommendation**: Findings with HIGH/MEDIUM stability are defensible for peer review.
Findings with LOW stability should be flagged as tentative or investigated further.
```

---

## Consensus Mode

If `state.json` has `consensus.stages.hunt_patterns.enabled = true`:

### How It Works

1. **Run pattern analysis N times** (default: 25, configurable in state.json)
2. **Extract effect sizes from each run**: β, OR, p-values, R², etc.
3. **Compute statistics across runs**:
   - Mean, SD, 95% confidence interval
   - Coefficient of variation (CV = SD/Mean)
4. **Rate stability**:
   - CV < 10%: HIGH stability — defensible
   - CV 10-25%: MEDIUM stability — note variance in paper
   - CV > 25%: LOW stability — flag for review, may be ambiguous
5. **Include stability data in PATTERN_REPORT.md**

### Running Consensus Analysis

Use the consensus engine in `lib/consensus/`:

```python
from lib.consensus import ConsensusEngine, extract_effect_sizes, get_stage_n

engine = ConsensusEngine(provider="anthropic")
n = get_stage_n("hunt_patterns")  # Default: 25

result = await engine.run_with_consensus(
    system_prompt="[pattern hunting system prompt]",
    user_prompt="[data + analysis request]",
    n=n,
    extract_metrics_fn=extract_effect_sizes,
)

# Result contains:
# - result.metrics: Dict of MetricConsensus objects with mean, SD, CI, CV, stability
# - result.flagged_items: List of LOW stability warnings
# - result.overall_stability: HIGH/MEDIUM/LOW
```

### Why This Matters

Single-run analysis: "Effect is β = 0.21"
- Non-reproducible
- Different prompt → different answer
- Reviewers can't verify

Consensus analysis: "Effect is β = 0.21 (±0.02 SD, 95% CI: [0.18, 0.24], n=25)"
- Reproducible: "We ran this 25 times"
- Defensible: confidence intervals for peer review
- Honest: LOW stability findings flagged, not hidden

---

## After You're Done

Tell the user:
- Which patterns survived and which died
- Which findings violate theoretical predictions (most valuable)
- Where you found heterogeneity
- **If consensus enabled**: stability summary and any flagged metrics

Then suggest they review and select which finding(s) to pursue. When ready, run `/find-theory` to identify the established theory being violated.

Tip: Run `/status` anytime to see overall workflow progress.
Tip: Run `/consensus-config` to enable/disable consensus mode or adjust settings.
