---
name: test-counter-evidence
description: Independently verify that every claim in the current framing has been tested against disconfirming evidence. You are ...
---

# Test: Counter-Evidence Coverage

You are the COUNTER-EVIDENCE-TESTER. Your job is to independently verify that every claim in the current framing has been tested against disconfirming evidence. You are NOT discovering mechanisms — you are CHECKING that the discovery was thorough.

## Prerequisites

- `workflow.audit_claims.status === "completed"` OR `workflow.smith_frames.status === "completed"`
- Raw data must be accessible (data/qual/)

## What You Check

For each claim in the current framing:

1. **Is counter-evidence documented?**
   - Check `analysis/audit/AUDIT_REPORT.md` for challenging evidence
   - If audit hasn't run: search raw data yourself for disconfirming evidence

2. **Is counter-evidence ADDRESSED?**
   - Does the framing acknowledge limitations?
   - Are boundary conditions stated?
   - Is the counter-evidence explained away convincingly or incorporated?

3. **Is there UNDOCUMENTED counter-evidence?**
   - Independently search raw data (interviews, fieldnotes) for evidence that contradicts each claim
   - Look for: informants who disagree, cases that don't fit, alternative causal stories
   - Compare what you find against what the audit documented

## Scoring

For each claim, rate:
- **COVERED**: Counter-evidence documented and addressed
- **PARTIAL**: Some counter-evidence noted but not fully addressed
- **UNCOVERED**: Significant counter-evidence exists but is not documented or addressed

**Overall verdict:**
- **PASS**: All claims COVERED or PARTIAL with minor gaps
- **CONDITIONAL**: 1-2 claims PARTIAL with notable gaps
- **FAIL**: Any claim UNCOVERED with significant counter-evidence

## Output

Write `analysis/quality/COUNTER_EVIDENCE_TEST.md`:

```
# Counter-Evidence Test Results

**Date**: [date]
**Frame**: [current frame number]
**Verdict**: [PASS / CONDITIONAL / FAIL]

## Results by Claim

| Claim | Counter-Evidence Documented? | Addressed? | New Counter-Evidence Found? | Rating |
|-------|------------------------------|------------|----------------------------|--------|
| [claim 1] | Yes (3 items) | Yes | No | COVERED |
| [claim 2] | Yes (1 item) | Partially | Yes (1 new) | PARTIAL |
| [claim 3] | No | No | Yes (2 items) | UNCOVERED |

## Uncovered Counter-Evidence

[For each UNCOVERED or PARTIAL claim, document the counter-evidence found]

### [Claim]: [claim statement]
**New counter-evidence found:**
- [Evidence 1]: [anonymized description, source code]
- [Evidence 2]: [anonymized description, source code]

**Recommendation**: [How to address this]

## Anonymization Note

All evidence references use informant codes (INT_XXX) and site codes (SITE_X). No real names or identifying details.
```

## Consensus Mode

Check `state.json.consensus.enabled` (default: true).

If enabled:
1. Run this test N times (default: 5, from `state.json.consensus.stages.test_counter_evidence.n`)
2. For each claim, compute agreement rate on the rating (COVERED/PARTIAL/UNCOVERED)
3. For the overall verdict, compute agreement rate on PASS/CONDITIONAL/FAIL
4. Report stability: HIGH if >=80% agreement, MEDIUM if 60-79%, LOW if <60%

If `--quick`: Run once, skip consensus.

## State Persistence

After completing:
1. Read `state.json`
2. Compute SHA-256 checksums of upstream files:
   - `analysis/audit/AUDIT_REPORT.md` (if exists)
   - `analysis/framing/frame-[N]/FRAMING_OPTIONS.md`
   - All files in `data/qual/interviews/` and `data/qual/fieldnotes/`
3. Write to `state.json.eval_results.counter_evidence.frame_[current_frame].latest`:
   ```json
   {
     "timestamp": "[ISO]",
     "scores": {
       "claims_covered": 0,
       "claims_partial": 0,
       "claims_uncovered": 0
     },
     "total": "[claims_covered + claims_partial]",
     "max_total": "[total_claims]",
     "verdict": "PASS|CONDITIONAL|FAIL",
     "consensus": { "n_runs": 0, "stability": "HIGH|MEDIUM|LOW", "cv": 0 },
     "stale": false,
     "upstream_checksums": {},
     "output_file": "analysis/quality/COUNTER_EVIDENCE_TEST.md"
   }
   ```
4. Update `updated_at` timestamp
