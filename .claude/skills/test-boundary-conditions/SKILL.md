---
name: test-boundary-conditions
description: Identify the conditions under which the paper's claims would NOT hold, and verify that the paper acknowledges them
---

# Test: Boundary Conditions

You are the BOUNDARY-CONDITIONS-TESTER. Your job is to identify the conditions under which the paper's claims would NOT hold, and verify that the paper acknowledges them.

## Prerequisites

- `workflow.smith_frames.status === "completed"`
- Claims must exist in framing or audit output

## What You Check

### Step 1: Identify Claims

Read the current framing and extract all substantive claims:
- Causal claims ("X leads to Y")
- Scope claims ("This applies to Z")
- Mechanism claims ("The mechanism is W")

### Step 2: Generate Boundary Conditions

For each claim, independently identify 2-4 boundary conditions — situations where the claim would NOT hold:

Categories:
- **Setting boundaries**: Different industry, org size, culture, geography
- **Temporal boundaries**: Different era, pace of change, lifecycle stage
- **Actor boundaries**: Different roles, experience levels, motivations
- **Mechanism boundaries**: When the causal path breaks down
- **Methodological boundaries**: Measurement artifacts, selection effects

### Step 3: Check Acknowledgment

For each boundary condition:
1. Is it mentioned in the paper/framing? (Check limitations, discussion, methods)
2. Is it framed as a BOUNDARY CONDITION (not an apology)?
   - Good: "This mechanism likely operates differently in..."
   - Bad: "A limitation is that we only studied..."
3. Are boundary conditions that MATTER MORE given more attention?

### Step 4: Verdict

- **PASS**: All significant boundary conditions documented and properly framed
- **CONDITIONAL**: Most documented, 1-2 missing but minor
- **FAIL**: Significant boundary conditions undocumented or misframed as limitations

## Output

Write `analysis/quality/BOUNDARY_CONDITIONS_TEST.md`:

```
# Boundary Conditions Test Results

**Date**: [date]
**Frame**: [current frame number]
**Verdict**: [PASS / CONDITIONAL / FAIL]

## Results by Claim

| Claim | Boundary Condition | Documented? | Properly Framed? | Rating |
|-------|-------------------|-------------|-----------------|--------|
| [claim 1] | Setting: org size | Yes | Yes | COVERED |
| [claim 1] | Temporal: pace of change | Yes | No (framed as limitation) | MISFRAMED |
| [claim 2] | Actor: experience level | No | — | UNDOCUMENTED |
| [claim 2] | Mechanism: trust absent | Yes | Yes | COVERED |

## Summary

| Rating | Count |
|--------|-------|
| COVERED | N |
| MISFRAMED | N |
| UNDOCUMENTED | N |
| **Total** | **N** |

## Undocumented Boundary Conditions

[For each UNDOCUMENTED condition:]

### [Claim]: [claim statement]
**Missing boundary**: [description]
**Why it matters**: [why this condition would change the outcome]
**Recommendation**: Add to Discussion section as scope condition

## Misframed Boundary Conditions

[For each MISFRAMED condition:]

### [Claim]: [claim statement]
**Current framing**: "A limitation is that we only studied..."
**Better framing**: "This mechanism likely operates differently in contexts where..."
**Why it matters**: Boundary conditions are features of theory, not apologies for method

## Anonymization Note

All evidence references use informant codes (INT_XXX) and site codes (SITE_X). No real names or identifying details.
```

## Consensus Mode

If enabled: Run N times (default 5). Compute agreement rate on boundary condition identification and verdict.

## State Persistence

After completing:
1. Read `state.json`
2. Compute SHA-256 of upstream files:
   - `analysis/framing/frame-[N]/FRAMING_OPTIONS.md`
   - `output/drafts/*.md` (if draft exists)
   - `analysis/audit/AUDIT_REPORT.md` (if exists)
3. Write to `state.json.eval_results.boundary_conditions.frame_[current_frame].latest`:
   ```json
   {
     "timestamp": "[ISO]",
     "scores": {
       "conditions_documented": 0,
       "conditions_undocumented": 0,
       "conditions_misframed": 0,
       "conditions_total": 0
     },
     "total": "[documented + properly_framed]",
     "max_total": "[total conditions]",
     "verdict": "PASS|CONDITIONAL|FAIL",
     "consensus": {},
     "stale": false,
     "upstream_checksums": {},
     "output_file": "analysis/quality/BOUNDARY_CONDITIONS_TEST.md"
   }
   ```
4. Update `updated_at` timestamp
