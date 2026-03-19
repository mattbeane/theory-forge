# Verification Brief Template

Create `analysis/verification/VERIFICATION_BRIEF.md` using this structure:

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

**Consensus verification** (if enabled):
| Metric | Mean | SD | 95% CI | CV | Stability |
|--------|------|-----|--------|-----|-----------|
| β | 0.208 | 0.015 | [0.195, 0.221] | 7% | HIGH |

**Cross-run agreement** (n=10 runs):
- Direction consistent: 10/10 (100%)
- Significance consistent: 10/10 (100%)
- Value range: [0.19, 0.23]
- **Verdict**: DEFENSIBLE — A skeptical reviewer running this analysis would reach the same conclusion.

**Data source**: [Filename, relevant variables]

**Verification code**:

```python
# Self-contained code to reproduce this claim
import pandas as pd
# ... [full code]
print(f"Result: {result}")  # Should print: [expected]
```

**Rubric Score** (if rubric-eval available): 32/40 (80%)
- Evidentiary Support: 8/10
- Logical Soundness: 9/10
- Hedging Appropriateness: 7/10
- Counter-Evidence: 8/10

**Robustness**:
- [x] Survives control for [X]
- [x] Survives control for [Y]
- [ ] NOT tested: [Z] because [reason]

**Potential concerns**: [Any issues to flag]

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
