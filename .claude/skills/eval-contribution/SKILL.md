---
name: eval-contribution
description: Diagnose what TYPE of contribution a paper is making, then apply the appropriate evaluation framework—not just Zuckerman
---

# Evaluate Contribution Type

You are the CONTRIBUTION-EVAL agent. Your job is to diagnose what TYPE of contribution a paper is making, then apply the appropriate evaluation framework—not just Zuckerman.

## Why This Matters

Zuckerman's criteria are excellent for "theory violation" papers—those that contradict established predictions. But many valuable papers make different types of contributions:

- **Theory elaboration** papers don't violate—they add precision
- **Phenomenon description** papers don't position—they reveal
- **Methodological** papers don't test—they enable
- **Practical insight** papers don't advance theory—they inform practice

Evaluating all papers against Zuckerman is like judging all athletes on sprinting speed. A shot-putter might be excellent without being fast.

## When to Run This

Run this BEFORE `/eval-zuckerman`. this skill determines WHETHER Zuckerman is the right framework, then routes to the appropriate evaluation.

Run this AFTER `/smith-frames` when you have a working framing.

For the full contribution type taxonomy (6 types with criteria), see [contribution-taxonomy.md](contribution-taxonomy.md)


## Diagnosis Process

### Step 1: Read the Abstract and Introduction

Look for:
- What QUESTION is the paper answering?
- How is the CONTRIBUTION framed?
- What would SUCCESS look like?

### Step 2: Classify Using Decision Tree

```
Is the paper primarily...

→ CHALLENGING existing theory?
  → Does it claim theory is WRONG (under conditions)?
    → Yes: TYPE 1 - Theory Violation
  → Does it claim theory is INCOMPLETE (needs precision)?
    → Yes: TYPE 2 - Theory Elaboration

→ DESCRIBING something new?
  → Is the phenomenon itself the main contribution?
    → Yes: TYPE 3 - Phenomenon Description
  → Is the method for studying it the main contribution?
    → Yes: TYPE 4 - Methodological

→ GUIDING practice?
  → Is actionable advice the primary goal?
    → Yes: TYPE 5 - Practical Insight

→ ORGANIZING existing knowledge?
  → Is synthesis/integration the primary goal?
    → Yes: TYPE 6 - Literature Integration
```

### Step 3: Check for Mismatches

Common problems:
- **Framed as Type 1 but evidence supports Type 2**: Paper claims to "violate" theory but actually just elaborates it
- **Framed as Type 3 but structured as Type 1**: Paper has rich description but forces a violation frame
- **Mixed types without acknowledgment**: Paper tries to be Types 1, 3, AND 5 simultaneously

### Step 4: Recommend Appropriate Framework

Based on diagnosis, route to the right evaluation:
- Type 1 → `/eval-zuckerman`
- Type 2 → Apply Fisher & Aguinis criteria (below)
- Type 3 → Apply Weick criteria (below)
- Type 4 → Apply Abbott criteria (below)
- Type 5 → Apply Corley & Gioia criteria (below)
- Type 6 → Apply Palmatier criteria (below)

## Output Format

Create `analysis/framing/CONTRIBUTION_DIAGNOSIS.md`:

```markdown
# Contribution Type Diagnosis

**Paper**: [Title]
**Date evaluated**: [Date]
**Target journal**: [If specified]

---

## Diagnosis Summary

**Diagnosed contribution type**: [Type 1-6 with name]

**Confidence**: [High / Medium / Low]

**Appropriate evaluation framework**: [Framework name]

---

## Diagnostic Evidence

### Question Being Answered

The paper is asking: "[Reconstruct the core question]"

This is a [challenge/describe/guide/organize] question, indicating Type [X].

### Contribution Framing

The paper claims to: "[Quote contribution statement]"

Key framing words: [violate/extend/specify/reveal/enable/guide/synthesize/etc.]

This framing indicates Type [X].

### Evidence Structure

The paper provides: [What kind of evidence?]

This evidence is best suited for Type [X].

---

## Mismatch Analysis

**Does framing match evidence?**: [Yes / No]

**If no, describe the mismatch**:
- Paper is FRAMED as: [Type X]
- Paper's EVIDENCE supports: [Type Y]
- Recommendation: [Reframe to match evidence / Gather different evidence]

---

## Framework-Specific Evaluation

### [Framework Name] Criteria

| Criterion | Rating | Evidence |
|-----------|--------|----------|
| [Criterion 1] | ✓/⚠️/✗ | [Quote/explanation] |
| [Criterion 2] | ✓/⚠️/✗ | [Quote/explanation] |
| [Criterion 3] | ✓/⚠️/✗ | [Quote/explanation] |
| [Criterion 4] | ✓/⚠️/✗ | [Quote/explanation] |
| [Criterion 5] | ✓/⚠️/✗ | [Quote/explanation] |

**Overall**: [X/5 criteria met strongly]

---

## Detailed Criterion Analysis

### Criterion 1: [Name]

**Rating**: [✓/⚠️/✗]

**Evidence**:
> [Quote from paper]

**Analysis**: [Why this rating]

**Suggestion** (if needed): [Specific fix]

---

[Repeat for each criterion]

---

## Comparison: If Evaluated as Type 1 (Zuckerman)

Would this paper pass Zuckerman criteria?

| Zuckerman Criterion | Likely Rating | Why |
|---------------------|---------------|-----|
| Motivate the paper | [✓/⚠️/✗] | [Brief] |
| Compelling null | [✓/⚠️/✗] | [Brief] |
| Save the null | [✓/⚠️/✗] | [Brief] |
| Puzzle in world | [✓/⚠️/✗] | [Brief] |

**Verdict**: [Zuckerman framework is/is not appropriate for this paper because...]

---

## Recommendations

### If diagnosis is correct:

1. [Specific improvement for identified type]
2. [Another improvement]
3. [Target journals that value this type]

### If reframing needed:

**Current frame**: [Type X]
**Recommended frame**: [Type Y]
**What would need to change**:
1. [Specific change]
2. [Specific change]
3. [Specific change]

---

## Next Steps

Based on contribution type [X], recommended next commands:

1. [Command] - [Why]
2. [Command] - [Why]
```

---

For detailed evaluation criteria by contribution type, see [criteria-by-type.md](criteria-by-type.md)


## After You're Done

Tell the user:
1. The diagnosed contribution type
2. Whether their current framing matches their evidence
3. How the paper rates on the APPROPRIATE criteria (not just Zuckerman)
4. Specific suggestions for strengthening the contribution
5. Whether `/eval-zuckerman` is the right next step (or an alternative)

## Integration with Other Commands

- Run BEFORE `/eval-zuckerman` to determine if Zuckerman is appropriate
- Run AFTER `/smith-frames` when framing is established
- If Type 1, proceed to `/eval-zuckerman`
- If other types, use the evaluation produced by this skill

## Registry-Aware Evaluation

Before running the diagnosis, read `registry.json` from the project root. The `methodologies` array may contain additional contribution types beyond the 6 built-in types.

For each methodology entry in the registry:
- If it has a `contribution_type` number and is NOT one of the built-in types (1-6), include it in the decision tree as an additional type
- If it has an `eval_command`, route to that command for evaluation
- If it has a `rubric` path, use that rubric for criterion-by-criterion evaluation

When presenting results, list ALL available evaluation frameworks — both built-in and registered — so the user sees the full menu of options.

If the paper doesn't fit any built-in type but matches a registered methodology, use that methodology's criteria. If it doesn't fit ANY registered type, say so and suggest the contributor create one with `/author-methodology`.

---

## Common Mistakes

**Forcing violation frame onto elaboration evidence**: Paper claims to "challenge" theory but evidence actually adds precision without contradiction. Fix: Reframe as elaboration.

**Burying phenomenon under theory**: Paper has rich, novel phenomenon description but buries it under theoretical positioning. Fix: Lead with the phenomenon.

**Applying Zuckerman to everything**: Not all valuable papers violate theoretical predictions. Some elaborate, describe, or guide. Don't force a framework that doesn't fit.

**Mixing types without integration**: Paper tries to violate theory, describe a phenomenon, AND guide practice all at once. Fix: Choose a primary contribution type; others can be secondary.

**Ignoring registered methodologies**: If someone has added a methodology via `/author-methodology`, it exists for a reason. Check the registry before defaulting to the 6 built-in types.

---

For consensus mode behavior, see [../../_shared/consensus-mode.md](../../_shared/consensus-mode.md)
For staleness detection, see [../../_shared/staleness-check.md](../../_shared/staleness-check.md)
For eval result persistence, see [../../_shared/eval-persistence.md](../../_shared/eval-persistence.md)

### Skill-Specific Persistence

- **eval_results key**: `contribution`
- **Upstream files**: `analysis/framing/frame-{N}/FRAMING_OPTIONS.md`, `analysis/patterns/PATTERN_REPORT.md`
- **Scores**: `contribution_type`, `confidence`, `criteria_1` through `criteria_5`
- **Verdict**: PASS if HIGH confidence; CONDITIONAL if MEDIUM; FAIL if LOW
- **Default consensus N**: 5
