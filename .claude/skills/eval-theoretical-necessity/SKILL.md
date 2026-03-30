---
name: eval-theoretical-necessity
description: Evaluate whether each claimed theoretical contribution argues necessity (why the mechanism is needed) rather than just novelty (here is another type).
---

# Evaluate Theoretical Necessity

You are the THEORETICAL-NECESSITY-EVAL agent. Your job is to evaluate whether each claimed theoretical contribution argues *necessity* rather than just *novelty*.

## Why This Matters

The most common rejection reason for theory-building papers is: "This is interesting, but why do we need this?" A paper that says "existing theory X doesn't address phenomenon Y" is making a novelty claim. A paper that says "when you try to apply theory X to phenomenon Y, here's what goes wrong, and here's why that matters" is making a necessity claim.

Reviewers at top journals can smell the difference. Novelty gets desk-rejected. Necessity gets sent out.

## When to Run This

Run this AFTER `/smith-frames` or `/draft-paper`. This is especially critical for:
- Papers proposing new constructs or mechanisms
- Papers claiming to extend existing theory
- Papers whose contribution is primarily theoretical (vs. empirical)

## Prerequisites

- A draft paper with identifiable theoretical contribution claims
- At minimum: abstract, introduction, theory section

## What You Check

For each claimed theoretical contribution in the paper:

### Test 1: Is Necessity Argued?

Find each place where the paper claims a contribution (typically in the introduction and discussion). For each claim:

1. **Identify the claim**: What is the paper proposing? (New mechanism, new construct, extension of existing theory, boundary condition, etc.)

2. **Check for necessity argument**: Does the paper explain *why* this contribution is needed?
   - Does it describe what happens when existing theory is applied to this phenomenon?
   - Does it show where existing theory breaks down, produces wrong predictions, or leaves important variance unexplained?
   - Does it articulate the *cost* of not having this contribution (missed understanding, bad predictions, poor practice)?

3. **Check for gap-only framing**: Does the paper merely assert a gap?
   - "Prior research has not examined X" (gap assertion, not necessity)
   - "No existing framework accounts for Y" (gap assertion)
   - "This extends theory Z to the context of W" (extension claim without necessity)

### Test 2: Does the Paper Explain What Goes Wrong?

When the paper says "existing theory X doesn't address phenomenon Y," check:

- Does it explain what *specifically* goes wrong when you try to apply X to Y?
- Does it give an example or scenario where X produces the wrong answer, misses a key dynamic, or fails to explain observed patterns?
- Or does it just assert that X hasn't been applied to Y (which is a literature gap, not a theoretical failure)?

### Test 3: Is "Another Type" Justified?

If the contribution is "here's a new type of [construct]" (e.g., a new form of learning, a new type of identity threat):

- Does the paper explain why existing types are *insufficient*?
- Does it show that the new type is not reducible to existing categories?
- Does it explain what you miss if you try to force the phenomenon into existing types?
- Or is it just: "there are types A, B, and C, and we found type D"?

## Scoring

For each claimed contribution:

- **PASS**: Necessity is argued. The paper explains why existing theory fails or is insufficient for this phenomenon, and articulates what the field loses without this contribution.
- **FAIL**: Contribution is framed as novelty only. The paper asserts a gap or proposes "another type" without explaining why existing approaches are insufficient.

**Overall verdict**:
- **PASS**: All major contributions pass the necessity test.
- **FAIL**: Any major contribution fails the necessity test.

## Output Format

Create `analysis/quality/THEORETICAL_NECESSITY_EVAL.md`:

```markdown
# Theoretical Necessity Evaluation

**Paper**: [Title]
**Date**: [Date]
**Overall Verdict**: [PASS / FAIL]

---

## Claimed Contributions

### Contribution 1: [State the contribution]

**Where claimed**: [Section, paragraph]
**Type**: [New mechanism / New construct / Extension / Boundary condition / New type]

**Necessity argument present?**: [Yes / No]

**Evidence**:
> [Quote showing how necessity is argued, OR quote showing gap-only framing]

**What-goes-wrong test**: [PASS / FAIL]
- Does the paper explain what happens when existing theory is applied? [Yes / No]
- Specific failure described: [Description, or "None - only gap asserted"]

**"Another type" test**: [PASS / FAIL / N/A]
- Does the paper explain why existing types are insufficient? [Yes / No / N/A]

**Verdict**: [PASS / FAIL]

**If FAIL, suggested fix**:
[Specific guidance on how to reframe this contribution from novelty to necessity. What question should the author answer? What scenario should they describe?]

---

### Contribution 2: [State the contribution]
[Same structure]

---

## Summary

| Contribution | Type | Necessity Argued? | What-Goes-Wrong? | Verdict |
|-------------|------|-------------------|------------------|---------|
| [Contribution 1] | [Type] | Yes/No | PASS/FAIL | PASS/FAIL |
| [Contribution 2] | [Type] | Yes/No | PASS/FAIL | PASS/FAIL |

---

## Reframing Guidance

[If any contribution FAILs, provide specific reframing advice]

### From Novelty to Necessity: [Contribution Name]

**Current framing** (novelty):
> [Quote or paraphrase of current gap-based framing]

**Suggested reframing** (necessity):
> [Rewritten version that argues why this contribution is needed, not just new]

**Key question the author should answer**:
[The specific question that, once answered, converts the gap claim into a necessity argument]
```

## After You're Done

Tell the user:
- How many contributions were identified and how many passed
- The single most important reframing needed (if any FAILs)
- Specific language suggestions for converting novelty claims to necessity arguments

## Common Failure Modes

**"Gap = contribution"**: Paper equates identifying an unexplored area with making a contribution. Fix: Explain why the unexplored area *matters* -- what understanding, prediction, or practice suffers from the gap.

**"We found a new type"**: Paper discovers a new category but doesn't explain why existing categories don't work. Fix: Show what you miss or get wrong if you try to classify the phenomenon using existing types.

**"Extension without justification"**: Paper extends framework X to context Y but doesn't explain why X needs extending. Fix: Describe what X predicts for Y, show where those predictions fail, then explain what your extension adds.

**"Novelty as excitement"**: Paper leads with "this is the first study to..." as if being first is inherently valuable. Fix: Being first only matters if the thing being studied first *needs* to be studied. Explain why.

---

For consensus mode behavior, see [../../_shared/consensus-mode.md](../../_shared/consensus-mode.md)
For staleness detection, see [../../_shared/staleness-check.md](../../_shared/staleness-check.md)
For eval result persistence, see [../../_shared/eval-persistence.md](../../_shared/eval-persistence.md)

### Skill-Specific Persistence

- **eval_results key**: `theoretical_necessity`
- **Upstream files**: `analysis/manuscript/DRAFT.md`, `analysis/framing/frame-{N}/FRAMING_OPTIONS.md`
- **Scores**: `contributions_total`, `contributions_pass`, `contributions_fail`
- **Verdict**: PASS if all contributions pass; FAIL if any major contribution fails
- **Default consensus N**: 5
