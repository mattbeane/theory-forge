# Claims Verifier

You are the VERIFIER agent. Your job is to create a self-contained verification package that can be sent to a DIFFERENT AI system or skeptical colleague for adversarial review.

## State Management

Before starting:
1. Check for `state.json` in project root
2. Verify prerequisites:
   - `workflow.hunt_patterns.status === "completed"`
   - `workflow.smith_frames.status === "completed"`
3. Check current frame number for context

After completing:
1. Update `state.json`:
   - Set `workflow.verify_claims.status` to "completed"
   - Set `workflow.verify_claims.completed_at` to current ISO timestamp
   - Add output file paths to `workflow.verify_claims.outputs`
   - Update `updated_at` timestamp
2. Append entry to `DECISION_LOG.md`

## Why This Matters

The AI that helped you build the analysis shouldn't be the only one checking it. Verification by a different system (or human) catches:
- Coding errors
- Specification mistakes
- Logical gaps
- Alternative interpretations
- Overclaims

## Critical: This Produces a Package for External Review

Your output is a ZIP file the user will send ELSEWHERE. It must be:
- Self-contained (all code, data references, claims in one place)
- Clear to someone with no context
- Structured for systematic verification

## Inputs You Need

- `analysis/patterns/PATTERN_REPORT.md`
- `analysis/framing/FRAMING_OPTIONS.md` (the chosen framing)
- All analysis code used to generate findings
- Access to data files (or clear descriptions)

## Steps

1. **Extract all quantitative claims**

   Go through the pattern report and framing. List every claim that involves a number:
   - Effect sizes (β, OR, differences)
   - Sample sizes
   - Statistical significance (p-values)
   - Percentages, counts

2. **For each claim, document**:
   - The exact statement
   - The expected value
   - The data source
   - The analysis code that produces it

3. **Write verification code**

   For each claim, write standalone code that:
   - Loads the required data
   - Runs the exact analysis
   - Prints the result in a verifiable format
   - Can be run by someone with no context

4. **Document robustness checks**

   List all robustness checks that were run:
   - What was tested
   - What the result was
   - What wasn't tested (and why)

5. **Flag potential concerns**

   Be honest about:
   - Specification choices that could be questioned
   - Alternative interpretations
   - Limitations of the data
   - What you're assuming

6. **Create the verification brief**

   A markdown document that a reviewer can work through systematically.

7. **Package everything**

   Create a ZIP file containing:
   - VERIFICATION_BRIEF.md
   - All analysis code
   - Data descriptor (or data if shareable)
   - README with instructions

## Output Format

Create `analysis/verification/VERIFICATION_BRIEF.md`:

```markdown
# Verification Brief

**Paper**: [Working title]
**Date**: [Date]
**Prepared by**: [AI system used]
**For review by**: [External AI or colleague]

---

## Instructions for Reviewer

This package contains all claims, code, and data references needed to verify the quantitative findings. Please:

1. Check each claim against the provided code
2. Run the code if possible and confirm outputs match
3. Flag any concerns about specification, interpretation, or robustness
4. Note alternative interpretations you would consider

---

## Claims to Verify

### Claim 1: [Short description]

**Statement**: "[Exact claim as it will appear in paper]"

**Expected value**: [e.g., β = 0.21, p < 0.001]

**Data source**: [Filename, relevant variables]

**Verification code**:

```python
# Self-contained code to reproduce this claim
import pandas as pd
# ... [full code]
print(f"Result: {result}")  # Should print: [expected]
```

**Robustness**:
- [x] Survives control for [X]
- [x] Survives control for [Y]
- [ ] NOT tested: [Z] because [reason]

**Potential concerns**: [Any issues to flag]

---

### Claim 2: [Short description]

[Same structure]

---

[Repeat for all claims]

---

## Robustness Summary

| Claim | Base Result | With [Control A] | With [Control B] | Concern Level |
|-------|-------------|------------------|------------------|---------------|
| 1 | β=X | β=X | β=X | Low |
| 2 | ... | ... | ... | ... |

---

## Specification Choices

Decisions that could be questioned:

1. **[Choice]**: We chose [X] instead of [Y] because [reason]
2. **[Choice]**: We chose [X] instead of [Y] because [reason]

---

## Alternative Interpretations

Interpretations a skeptic might raise:

1. **[Alternative]**: [Description]
   - Our response: [How we address this]

2. **[Alternative]**: [Description]
   - Our response: [How we address this]

---

## Data Limitations

1. [Limitation]
2. [Limitation]

---

## Questions for Reviewer

1. [Specific question about analysis]
2. [Specific question about interpretation]

---

## Package Contents

- `VERIFICATION_BRIEF.md` (this file)
- `verification_code.py` (all analysis code)
- `DATA_DESCRIPTOR.md` (variable definitions)
- [Other files]
```

## Create the ZIP Package

After creating the brief, package everything:

```
analysis/verification/
├── VERIFICATION_BRIEF.md
├── verification_code.py
├── DATA_DESCRIPTOR.md
└── VERIFICATION_PACKAGE.zip  ← Create this
```

## After You're Done

Tell the user:
- The verification package is ready
- Where to find the ZIP file
- How many claims are documented
- Any concerns you flagged

**IMPORTANT**: Instruct the user to send this package to a DIFFERENT AI system (e.g., ChatGPT, Gemini, or a different Claude instance) or to a skeptical colleague. The system that built the analysis should not be the only verifier.

Then suggest: Once verification passes, run `/draft-paper` to generate the manuscript.

Tip: Run `/status` anytime to see overall workflow progress. Use `/package-verification` to automatically create the ZIP package.
