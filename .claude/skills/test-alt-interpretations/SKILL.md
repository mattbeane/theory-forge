---
name: test-alt-interpretations
description: Independently generate alternative explanations for the empirical patterns and evaluate whether the proposed framing ...
---

# Test: Alternative Interpretations

You are the ALT-INTERPRETATIONS-TESTER. Your job is to independently generate alternative explanations for the empirical patterns and evaluate whether the proposed framing is more plausible than the alternatives. This is a SURVIVABILITY test.

## Prerequisites

- `workflow.smith_frames.status === "completed"`
- Pattern report must exist: `analysis/patterns/PATTERN_REPORT.md`

## What You Do

### Step 1: Understand the Current Framing

Read:
- `analysis/framing/frame-[N]/FRAMING_OPTIONS.md` — the chosen framing
- `analysis/patterns/PATTERN_REPORT.md` — the empirical patterns
- `analysis/theory/PRIMARY_THEORY.md` — the theoretical anchor

Identify the core causal claim: "X happens because Y (mechanism), which is surprising because Z (theory violation/extension)."

### Step 2: Generate Alternative Interpretations

WITHOUT looking at the current framing's adversarial checks, independently generate 3-5 alternative interpretations of the SAME empirical patterns:

For each alternative:
1. **Name it**: A 1-sentence theoretical label
2. **Explain it**: How would this theory explain the patterns?
3. **What evidence would support it**: What would you expect to see in the data?
4. **What evidence would contradict it**: What would rule this out?

### Step 3: Evaluate Plausibility

For each alternative, rate (1-5):
- **Data fit**: How well does it explain ALL the patterns? (not just some)
- **Parsimony**: Is it simpler than the proposed framing?
- **Novelty**: Does it offer a more interesting contribution?
- **Mechanism clarity**: Does it specify a clearer causal path?

Compare each alternative against the proposed framing on the same criteria.

### Step 4: Verdict

- **PASS**: Proposed framing is more plausible than all alternatives (or alternatives are acknowledged)
- **CONDITIONAL**: 1 alternative is comparably plausible but the proposed framing is still defensible
- **FAIL**: An alternative is more plausible than the proposed framing, OR the proposed framing doesn't acknowledge a strong alternative

## Output

Write `analysis/quality/ALT_INTERPRETATIONS_TEST.md`:

```
# Alternative Interpretations Test

**Date**: [date]
**Frame**: [current frame]
**Verdict**: [PASS / CONDITIONAL / FAIL]

## Current Framing Summary
[1-2 sentences]

## Alternative Interpretations

### Alternative 1: [Name]
**Explanation**: [How it explains the patterns]
**Data fit**: [X/5] | **Parsimony**: [X/5] | **Novelty**: [X/5] | **Mechanism**: [X/5]
**Total**: [X/20]
**vs. Proposed Framing**: [More/Less/Equally plausible]

### Alternative 2: [Name]
[same structure]

...

## Comparison Matrix

| Dimension | Proposed | Alt 1 | Alt 2 | Alt 3 |
|-----------|----------|-------|-------|-------|
| Data fit | X/5 | X/5 | X/5 | X/5 |
| Parsimony | X/5 | X/5 | X/5 | X/5 |
| Novelty | X/5 | X/5 | X/5 | X/5 |
| Mechanism | X/5 | X/5 | X/5 | X/5 |
| **Total** | **X/20** | **X/20** | **X/20** | **X/20** |

## Recommendation

[If FAIL: Which alternative should be considered]
[If CONDITIONAL: What needs to be acknowledged]
[If PASS: Why the proposed framing survives]
```

## Consensus Mode

If enabled: Run N times (default 5). For each alternative, compute mean plausibility scores across runs. Rate stability of verdict agreement.

## State Persistence

After completing:
1. Read `state.json`
2. Compute SHA-256 of upstream files:
   - `analysis/framing/frame-[N]/FRAMING_OPTIONS.md`
   - `analysis/patterns/PATTERN_REPORT.md`
   - `analysis/theory/PRIMARY_THEORY.md`
3. Write to `state.json.eval_results.alt_interpretations.frame_[current_frame].latest`:
   ```json
   {
     "timestamp": "[ISO]",
     "scores": {
       "proposed_score": 0,
       "best_alternative_score": 0,
       "alternatives_count": 0,
       "alternatives_acknowledged": 0
     },
     "total": "[proposed_score]",
     "max_total": 20,
     "verdict": "PASS|CONDITIONAL|FAIL",
     "consensus": {},
     "stale": false,
     "upstream_checksums": {},
     "output_file": "analysis/quality/ALT_INTERPRETATIONS_TEST.md"
   }
   ```
4. Update `updated_at` timestamp
