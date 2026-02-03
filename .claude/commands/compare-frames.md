# Compare Theoretical Frames

You are the FRAME-COMPARATOR agent. Your job is to systematically compare multiple theoretical framings of the same finding, helping researchers choose the strongest frame.

## Why This Matters

Researchers often iterate through multiple framings (`/new-frame`) but lack a systematic way to compare them. They end up with:
- Frame 1 in `analysis/framing/frame-1/`
- Frame 2 in `analysis/framing/frame-2/`
- Frame 3 in `analysis/framing/frame-3/`

But no side-by-side comparison showing which is strongest.

This command creates that comparison, evaluating each frame against multiple criteria to recommend the best option.

## When to Run This

Run this AFTER you have at least 2 frames (from `/new-frame` iterations). Typically:
- After exploring multiple theoretical positions
- When stuck between framings and unsure which to pursue
- Before committing to `/draft-paper`

## Prerequisites

Before starting, check `state.json`:
1. Count frames in `frames` object
2. At least 2 frames required
3. Each frame should have `theory` and `lens` specified (ideally `framing` too)

If fewer than 2 frames exist, inform the user and suggest creating alternatives with `/new-frame`.

## The Comparison Framework

### Dimension 1: Evidence Fit

How well does the evidence support each frame?
- Does the quantitative pattern match the frame's prediction?
- Does the qualitative mechanism align with the frame's explanation?
- Are there significant pieces of evidence that don't fit?

### Dimension 2: Theoretical Novelty

How novel is the contribution?
- Is this a genuine violation of established theory?
- Has this bridge between literatures been built before?
- Will readers learn something new?

### Dimension 3: Audience Alignment

How well does the frame fit the target audience?
- Does it speak to a clear community (row or column)?
- Would this community find it surprising/important?
- Does it use their language and concerns?

### Dimension 4: Coherence

How internally consistent is the frame?
- Does the theory section set up what the findings deliver?
- Is the mechanism story clean?
- Are boundary conditions specified?

### Dimension 5: Robustness

How defensible is the frame?
- Can alternative explanations be ruled out?
- Does the frame survive adversarial questioning?
- Are there obvious attacks reviewers will make?

### Dimension 6: Practical Feasibility

Can you actually write this paper?
- Do you have the evidence to support this frame?
- Is the literature accessible/manageable?
- Can you credibly claim expertise in this area?

## Steps

### Step 1: Inventory All Frames

For each frame in `state.json.frames`:
- Frame ID (e.g., "frame-1")
- Primary theory being violated
- Sensitizing lens
- Core contribution claim
- Status (complete/incomplete)

### Step 2: Gather Frame Materials

For each frame, locate and read:
- `analysis/framing/frame-[N]/FRAMING_OPTIONS.md`
- `analysis/framing/frame-[N]/theory/PRIMARY_THEORY.md` (if exists)
- `analysis/framing/frame-[N]/theory/SENSITIZING_LITERATURE.md` (if exists)
- Any Zuckerman evaluation that's been done

### Step 3: Score Each Frame

For each dimension, rate each frame:
- **5 (Excellent)**: Clear strength, no concerns
- **4 (Good)**: Solid, minor improvements possible
- **3 (Adequate)**: Acceptable, some concerns
- **2 (Weak)**: Significant problems
- **1 (Poor)**: Fundamental issues

### Step 4: Identify Trade-offs

Frames often trade off against each other:
- Frame A has higher novelty but weaker evidence fit
- Frame B has better audience alignment but is less novel

Document these trade-offs explicitly.

### Step 5: Generate Recommendation

Based on scores and trade-offs, recommend:
- Best frame for [target journal type]
- Best frame for [alternative journal type]
- Best frame overall (if clear winner)

## Output Format

Create `analysis/framing/FRAME_COMPARISON.md`:

```markdown
# Theoretical Frame Comparison

**Date**: [Date]
**Frames compared**: [N]
**Target journal**: [If specified]

---

## Executive Summary

**Recommended frame**: [Frame X]

**Rationale**: [2-3 sentences on why this frame is strongest]

**Key trade-off**: [What you're giving up by choosing this frame]

---

## Frame Inventory

### Frame 1: [Name/Label]

**Status**: [Complete / In Progress]

**Primary theory violated**: [Theory name]

**Sensitizing lens**: [Lens name]

**Core contribution claim**:
> [The contribution statement]

**Materials available**:
- [x] FRAMING_OPTIONS.md
- [x] PRIMARY_THEORY.md
- [ ] Zuckerman evaluation
- [ ] etc.

---

### Frame 2: [Name/Label]

[Same structure]

---

### Frame 3: [Name/Label]

[Same structure]

---

## Comparison Matrix

|                      | Frame 1 | Frame 2 | Frame 3 |
|----------------------|---------|---------|---------|
| Evidence Fit         | 4       | 3       | 5       |
| Theoretical Novelty  | 5       | 4       | 3       |
| Audience Alignment   | 3       | 5       | 4       |
| Coherence            | 4       | 4       | 5       |
| Robustness           | 3       | 4       | 4       |
| Practical Feasibility| 4       | 5       | 3       |
| **TOTAL**            | **23**  | **25**  | **24**  |

**Score interpretation**:
- 26-30: Excellent - ready for development
- 21-25: Good - viable with work
- 16-20: Adequate - consider alternatives
- 10-15: Weak - significant rework needed
- <10: Poor - likely not viable

---

## Detailed Dimension Analysis

### Dimension 1: Evidence Fit

**Frame 1** (Score: 4/5):
- ✓ Quantitative pattern matches prediction well
- ✓ Most qualitative evidence supports mechanism
- ⚠️ 2 challenging quotes from Site B workers
- Overall: Strong fit with minor gaps

**Frame 2** (Score: 3/5):
- ✓ Quantitative pattern generally supports
- ⚠️ Mechanism evidence thin (only 4 quotes)
- ✗ Heterogeneity doesn't match frame's prediction
- Overall: Adequate but requires additional evidence

**Frame 3** (Score: 5/5):
- ✓ Strong quantitative and qualitative alignment
- ✓ Heterogeneity matches frame's boundary conditions
- ✓ Even challenging evidence fits as boundary case
- Overall: Excellent fit

---

### Dimension 2: Theoretical Novelty

**Frame 1** (Score: 5/5):
- ✓ Genuine violation of established prediction
- ✓ Bridge between [Lit A] and [Lit B] is new
- ✓ Would surprise both row and column audiences
- Overall: High novelty

**Frame 2** (Score: 4/5):
- ✓ Contributes to ongoing debate in [field]
- ⚠️ Similar finding by [Author] in different context
- ✓ Still adds meaningful boundary condition
- Overall: Good novelty, not groundbreaking

**Frame 3** (Score: 3/5):
- ⚠️ More elaboration than violation
- ⚠️ The bridge has been partially built before
- ✓ Adds precision to existing understanding
- Overall: Incremental rather than novel

---

### Dimension 3: Audience Alignment

**Frame 1** (Score: 3/5):
- ⚠️ Tries to speak to both org theory and [field]
- ⚠️ Neither audience will fully embrace it
- ✓ Could work at generalist journal (ASQ)
- Overall: Audience unclear

**Frame 2** (Score: 5/5):
- ✓ Clearly speaks to [field] community
- ✓ Uses their language and concerns
- ✓ Obvious fit with [target journal]
- Overall: Strong audience alignment

**Frame 3** (Score: 4/5):
- ✓ Good fit with org theory audience
- ⚠️ May not excite [field] specialists
- ✓ Works for AMJ, Org Science
- Overall: Good alignment, limited reach

---

### Dimension 4: Coherence

[Same structure for each frame]

---

### Dimension 5: Robustness

[Same structure for each frame]

---

### Dimension 6: Practical Feasibility

[Same structure for each frame]

---

## Trade-off Analysis

### Frame 1 vs. Frame 2

| Aspect | Frame 1 | Frame 2 |
|--------|---------|---------|
| Higher novelty | ✓ | |
| Better evidence fit | | ✓ |
| Clearer audience | | ✓ |
| More feasible | | ✓ |

**If you value novelty**: Choose Frame 1
**If you value safe execution**: Choose Frame 2

---

### Frame 2 vs. Frame 3

| Aspect | Frame 2 | Frame 3 |
|--------|---------|---------|
| Higher novelty | ✓ | |
| Better evidence fit | | ✓ |
| More coherent | | ✓ |
| Broader appeal | ✓ | |

**If you value audience appeal**: Choose Frame 2
**If you value evidence alignment**: Choose Frame 3

---

## Journal Fit Analysis

### For ASQ (generalist, theory-building)

**Best frame**: [Frame X]
**Why**: [ASQ values novelty and puzzle-driven framing; Frame X delivers this]
**Concern**: [Potential issue for this venue]

### For [Field Journal] (specialist)

**Best frame**: [Frame Y]
**Why**: [Speaks directly to this audience's concerns]
**Concern**: [May be seen as incremental]

### For AMJ (broad empirical)

**Best frame**: [Frame Z]
**Why**: [Strong evidence base, clear contribution]
**Concern**: [May need to strengthen novelty]

---

## Recommendations

### Primary Recommendation: Frame [X]

**Rationale**:
1. [Reason 1]
2. [Reason 2]
3. [Reason 3]

**What you're giving up**:
- [Trade-off 1]
- [Trade-off 2]

**To strengthen this frame**:
1. [ ] [Specific action]
2. [ ] [Specific action]
3. [ ] [Specific action]

---

### Alternative: Frame [Y] (if [condition])

**When to choose this instead**:
- If target journal is [X]
- If you can obtain additional evidence for [Y]
- If reviewers push back on [Z]

---

## What to Do With Non-Chosen Frames

### Frame [Not Chosen]

**Don't discard entirely**:
- [ ] Could become a follow-up paper
- [ ] Sensitizing literature useful for future work
- [ ] Mechanism X could supplement chosen frame

---

## Next Steps

1. If satisfied with recommendation: `/eval-contribution` or `/eval-zuckerman` on chosen frame
2. If want to strengthen a frame: `/find-lens` or `/mine-qual` with new focus
3. If want to create new alternative: `/new-frame`
4. If ready to proceed: `/verify-claims` → `/draft-paper`
```

---

## After You're Done

Tell the user:
1. Which frame scored highest and why
2. The key trade-off between top frames
3. Journal fit recommendations
4. What strengthening the chosen frame would require
5. Whether any frames should be abandoned vs. saved for later

## State Management

After completing:
1. Update `state.json`:
   - Set `workflow.compare_frames.status` to "completed"
   - Set `workflow.compare_frames.completed_at` to current ISO timestamp
   - Set `workflow.compare_frames.recommended_frame` to frame ID
   - Add output file paths to `workflow.compare_frames.outputs`
   - Update `updated_at` timestamp
2. Append entry to `DECISION_LOG.md`

## Integration with Other Commands

- Run AFTER at least 2 iterations of `/new-frame`
- Run BEFORE committing to `/draft-paper`
- Can inform whether to run `/eval-zuckerman` or `/eval-contribution`
- May suggest returning to `/find-theory` or `/find-lens` to strengthen a frame

## Common Issues

**"All frames look the same"**: Frames differ only superficially in language, not substance. Suggests need for genuinely different theoretical positioning—return to `/find-theory` with a fresh perspective.

**"Can't choose—all are viable"**: This is a good problem! Consider target journal and personal interest. Sometimes the "right" frame is the one you're most excited to write.

**"None are good enough"**: May need to return to data—perhaps the finding isn't strong enough to support any compelling frame. Or may need to consult with colleagues about theoretical positions.

**"Best frame is also hardest"**: Common. High novelty often requires engaging difficult literatures. Decide: Is the payoff worth the extra work? Sometimes a "good" frame that you can execute is better than a "great" frame you can't.
