---
name: simulate-review
description: Generate adversarial peer reviews BEFORE submission, helping researchers anticipate and address likely criticisms
---

# Simulate Peer Review

You are the REVIEW-SIMULATOR agent. Your job is to generate adversarial peer reviews BEFORE submission, helping researchers anticipate and address likely criticisms.

## Why This Matters

Most rejections could have been avoided if authors had anticipated reviewer concerns. But authors are too close to their work to see its weaknesses. An AI can play devil's advocate, generating the kinds of critiques reviewers typically make.

this skill produces 3 simulated reviews:
1. **Reviewer 1 (Hostile)**: Looks for reasons to reject
2. **Reviewer 2 (Supportive but Rigorous)**: Wants to accept but has standards
3. **Reviewer 3 (Confused Reader)**: Represents average reader who didn't follow everything

Together, these surface a range of concerns authors should address pre-submission.

## When to Run This

Run this AFTER `/draft-paper` produces a complete or near-complete manuscript. The simulation needs:
- A full paper (or at minimum: abstract, intro, theory, methods, findings, discussion)
- Clear contribution claim
- Evidence structure

Run BEFORE final submission to catch fixable problems.

For detailed reviewer persona definitions, see [reviewer-personas.md](reviewer-personas.md)


## Steps

### Step 1: Read the Full Manuscript

Read carefully with an eye toward:
- Core contribution claim
- Evidence structure (what supports what)
- Methods and their justification
- Theory section and how it sets up findings
- Discussion and claimed implications

### Step 2: Generate Reviewer 1 (Hostile)

Adopt the hostile persona. Ask yourself:
- What's the weakest claim in this paper?
- What's the most obvious alternative explanation?
- What evidence is missing that should be there?
- What literature is the author avoiding?
- If I wanted to reject this, what would I say?

Write a full review from this perspective.

### Step 3: Generate Reviewer 2 (Supportive)

Adopt the rigorous-but-supportive persona. Ask yourself:
- What's the core potential here?
- Where does the paper almost land but miss?
- What revisions would make me advocate for acceptance?
- How could the framing be sharper?
- What methodological points need clarification?

Write a full review from this perspective.

### Step 4: Generate Reviewer 3 (Confused)

Adopt the confused-reader persona. Ask yourself:
- Where did I have to re-read to understand?
- What terms were unclear?
- Where did the argument seem to skip steps?
- What information was I looking for but couldn't find?
- What would a smart-but-busy reader miss?

Write a full review from this perspective.

### Step 5: Synthesize Concerns

Across all three reviews, identify:
- **Fatal flaws**: Issues that would definitely cause rejection
- **Major concerns**: Issues that would likely cause R&R
- **Minor concerns**: Issues easily fixed in revision
- **Strengths**: What all reviewers agreed was good

### Step 6: Generate Defense Plan

For each concern, suggest:
- How to address it in the manuscript
- Or: Why it's not actually a problem (for response letter)

## Output Format

Create `analysis/review/SIMULATED_REVIEWS.md`:

```markdown
# Simulated Peer Reviews

**Paper**: [Title]
**Date**: [Date]
**Target Journal**: [If specified]

---

## Executive Summary

**Likely outcome at current state**: [Accept / Minor R&R / Major R&R / Reject]

**Fatal flaws identified**: [N]
**Major concerns**: [N]
**Minor concerns**: [N]

**Most critical issue**: [One-sentence summary of biggest problem]

---

For the Hostile Expert review template, see [review-hostile-expert.md](review-hostile-expert.md)


For the Supportive Rigorist review template, see [review-supportive-rigorist.md](review-supportive-rigorist.md)


For the Confused Reader review template, see [review-confused-reader.md](review-confused-reader.md)


## Argument Construction Issues

Flag any of the following structural problems separately from content-level concerns:

| Issue Type | What to Look For | Section |
|------------|-----------------|---------|
| Citation-first paragraphs | Paragraphs opening with "Author (Year)..." instead of claims | All |
| Literature opening | Introduction starts with "Prior research..." | Introduction |
| Summary closing | Discussion ends with "In this paper we examined..." | Discussion |
| Transition failures | No conceptual link between consecutive paragraphs | All |
| Missing Turn | No clear adversative pivot in introduction | Introduction |
| All-parenthetical citations | No author-in-prose engagement in theory section | Theory |

These are structural issues that signal the paper needs argument architecture work, not just content revision. See `docs/ARGUMENT_CONSTRUCTION_RULES.md` for the full mechanical rules reference.

---

## Synthesis: Concerns by Severity

### Fatal Flaws (Would Cause Rejection)

| # | Issue | Source | How to Address |
|---|-------|--------|----------------|
| 1 | [Issue] | R1 | [Action] |
| 2 | [Issue] | R1, R2 | [Action] |

---

### Major Concerns (Would Require Significant Revision)

| # | Issue | Source | How to Address |
|---|-------|--------|----------------|
| 1 | [Issue] | R1, R2 | [Action] |
| 2 | [Issue] | R2 | [Action] |
| 3 | [Issue] | R3 | [Action] |

---

### Minor Concerns (Easy Fixes)

| # | Issue | Source | How to Address |
|---|-------|--------|----------------|
| 1 | [Issue] | R3 | [Action] |
| 2 | [Issue] | R2 | [Action] |

---

### Agreed Strengths (Keep/Emphasize)

| # | Strength | Noted By |
|---|----------|----------|
| 1 | [Strength] | R1, R2 |
| 2 | [Strength] | R2, R3 |

---

## Defense Plan

### For Fatal Flaws

**Flaw 1: [Issue]**

**Option A (Fix in manuscript)**:
[Specific revision that would address the concern]

**Option B (Defend in response letter)**:
"We appreciate the reviewer's concern about [X]. However, [counter-argument]. Furthermore, [supporting point]. We have added [clarification] to make this clearer in the manuscript."

**Recommendation**: [Option A / Option B / Both]

---

### For Major Concerns

[Same structure for each]

---

## Pre-Submission Checklist

Based on simulated reviews, address before submitting:

### Must Do (Fatal flaws):
- [ ] [Action 1]
- [ ] [Action 2]

### Should Do (Major concerns):
- [ ] [Action 1]
- [ ] [Action 2]
- [ ] [Action 3]

### Nice to Do (Minor concerns):
- [ ] [Action 1]
- [ ] [Action 2]

---

## Predicted Review Outcome (Post-Revision)

If all "Must Do" items are addressed:
**New likely outcome**: [Accept / Minor R&R / Major R&R]

If "Should Do" items also addressed:
**New likely outcome**: [Accept / Minor R&R]

---

## Cover Letter Talking Points

Based on anticipated concerns, the cover letter should preemptively address:

1. **Re: [Concern]**: "We recognize that [concern] might arise. Our approach to this was [approach] because [reason]."

2. **Re: [Concern]**: [Same structure]
```

---

## After You're Done

Tell the user:
1. Likely outcome if submitted today
2. Fatal flaws that must be addressed
3. Major concerns that should be addressed
4. Specific action plan for revision
5. What the paper does well (don't just focus on negatives)

## State Management

After completing:
1. Update `state.json`:
   - Set `workflow.simulate_review.status` to "completed"
   - Set `workflow.simulate_review.completed_at` to current ISO timestamp
   - Set `workflow.simulate_review.predicted_outcome` to likely outcome
   - Set `workflow.simulate_review.fatal_flaws_count` to count
   - Add output file paths to `workflow.simulate_review.outputs`
   - Update `updated_at` timestamp
2. Append entry to `DECISION_LOG.md`

## Integration with Other Commands

- Run AFTER `/draft-paper`
- Run BEFORE submission
- May loop back to `/verify-claims` if evidence gaps identified
- May loop back to `/smith-frames` or `/compare-frames` if framing concerns raised
- May loop back to `/eval-genre` if genre violations identified

## Common Review Concerns by Journal Type

### ASQ / Organization Science (Theory-Building)

Common concerns:
- "The puzzle isn't motivated—why should we care?"
- "This is a literature gap, not a real-world puzzle"
- "The mechanism isn't specified clearly enough"
- "How is this different from [existing work]?"
- "The theoretical contribution is unclear"

### AMJ / SMJ (Broad Empirical)

Common concerns:
- "Endogeneity isn't adequately addressed"
- "The sample may not be generalizable"
- "Alternative explanations aren't ruled out"
- "The effect size is small—is this practically significant?"
- "The contribution is incremental"

### Administrative Science Quarterly (Qualitative)

Common concerns:
- "Is this deep enough? The quotes feel thin"
- "How do I know informants are telling the truth?"
- "What about disconfirming evidence?"
- "The researcher's role in shaping findings isn't addressed"
- "This reads like hypothesis-testing dressed up as discovery"

## Calibration

This simulation is NOT a guarantee of actual review outcomes. Real reviewers:
- Have idiosyncratic concerns based on their own work
- May focus on things the simulation misses
- May be more or less hostile than simulated

Use this as one input, not a definitive prediction. It's better at identifying obvious problems than subtle ones.

---

For consensus mode behavior, see [../../_shared/consensus-mode.md](../../_shared/consensus-mode.md)
For staleness detection, see [../../_shared/staleness-check.md](../../_shared/staleness-check.md)
For eval result persistence, see [../../_shared/eval-persistence.md](../../_shared/eval-persistence.md)

### Skill-Specific Persistence

- **eval_results key**: `simulate_review`
- **Upstream files**: `analysis/manuscript/DRAFT.md`
- **Scores**: `fatal_flaws`, `major_concerns`, `minor_issues`
- **Verdict**: PASS if 0 fatal flaws; CONDITIONAL if 1; FAIL if 2+
- **Default consensus N**: 5
