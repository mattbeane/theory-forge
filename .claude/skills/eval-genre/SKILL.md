---
name: eval-genre
description: Ensure the paper reflects the appropriate epistemological genre—particularly distinguishing iterative/inductive disco...
---

# Genre Enforcement: Inductive vs. Deductive Framing

You are the GENRE-EVAL agent. Your job is to ensure the paper reflects the appropriate epistemological genre—particularly distinguishing **iterative/inductive discovery** from **hypothetico-deductive testing**.

## Why This Matters

Many qualitative and mixed-methods papers fail at review because the *writing* follows a deductive structure even though the *research* was inductive. Reviewers sense the mismatch: "This feels like the authors knew what they would find before they started."

The genre-appropriate framing for theory-building papers (ASQ, Organization Science, ethnographic work) is:

**Discovery logic**: "Here's what I observed → here's the puzzle it creates → here's what I noticed that explains it → here's the theory that helps make sense of it"

NOT **deductive logic**: "Here's theory → here's what it predicts → here's my test of that prediction"

this skill catches hypo-deductive framing in papers that should use discovery framing.

## When to Run This

Run this AFTER `/draft-paper` and BEFORE submission. This is especially critical for:
- Organization Science submissions (which explicitly value exploratory/theory-building)
- ASQ submissions (which expect qualitative depth and discovery)
- Any paper based on ethnographic, grounded theory, or inductive approaches

For the complete list of genre red flags to search for, see [red-flags.md](red-flags.md)


## Steps

1. **Read the Abstract and Introduction carefully**
   - Is the framing "Here's what I found" or "Here's what I expected to find"?
   - Does it start with observation/puzzle or with theory/prediction?

2. **Read the Theory Section header and first paragraph**
   - Is it called "Theoretical Framework" (neutral) or "Hypothesis Development" (deductive)?
   - Does it build toward predictions or toward sensitizing concepts?

3. **Check the FULL theory section for findings front-loading** (CRITICAL)
   - List the paper's 3-5 major findings/discoveries (from findings section or abstract)
   - For each finding, search the theory section: is this finding stated, implied, or derivable?
   - Check: Does the theory section NAME a new concept/mechanism before evidence is presented?
   - Check: Does the theory section EXTEND an existing framework to the paper's case before evidence?
   - Check: Does the theory section describe a COMPLETE mechanism that matches the findings?
   - If a reader could predict every major finding from the theory section alone, this is FAIL
   - This is the most commonly missed genre failure — theory sections that build the answer before the findings

4. **Search for red-flag language**
   - Grep for: hypothesis, predict, expect, test, H1, H2, confirm, support
   - Flag any instances in abstract, intro, or theory sections

4. **Check the Methods section**
   - Does it describe an iterative process or a test protocol?
   - Is qualitative data used for discovery or for "verification" of pre-formed expectations?

5. **Check temporal claims**
   - Does the paper claim to have discovered things through the research?
   - Or does it read as if the findings were known in advance?

## Output Format

Create `analysis/quality/GENRE_EVAL.md`:

```markdown
# Genre Evaluation: Inductive vs. Deductive Framing

**Paper**: [Title]
**Target Journal**: [Journal]
**Date evaluated**: [Date]

---

## Verdict Summary

**Appropriate genre for target journal**: [Inductive/Discovery / Deductive/Testing / Either]

**Paper's current framing**: [Inductive / Deductive / Mixed]

**Match**: [Yes / No - needs revision]

---

## Structure Analysis

### Theory Section

**Section title**: [What is it called?]
**Framing**: [Hypothesis Development / Sensitizing Concepts / Analytical Framework]
**Assessment**: [PASS / FAIL / NEEDS REVISION]

**Evidence**:
> [Quote showing structure]

### Abstract/Introduction

**Opens with**: [Observation/Puzzle / Theory/Prediction]
**Assessment**: [PASS / FAIL / NEEDS REVISION]

**Evidence**:
> [Quote showing framing]

### Front-Loading Check: Abstract

**Abstract first sentence**: [Quote]
**Is this a premise or a discovery?**: [Premise (OK) / Discovery front-loaded as premise (FAIL)]
**Naive question the paper answers**: [State it]
**Does abstract start from naive position?**: [Yes / No]
**Assessment**: [PASS / FAIL]

**If FAIL, discoveries presented as premises**:
- [Discovery 1 stated as if given]
- [Discovery 2 stated as if given]
- ...

### Front-Loading Check: Theory Section (CRITICAL)

**Paper's major findings/discoveries:**
1. [Finding 1]
2. [Finding 2]
3. [Finding 3]
4. [Finding 4 if applicable]
5. [Finding 5 if applicable]

**Findings already present in theory section:**

| Finding | Present in Theory? | Where? | How? |
|---------|-------------------|--------|------|
| [Finding 1] | Yes/No | [Section/line] | [Stated / Implied / Derivable] |
| [Finding 2] | Yes/No | [Section/line] | [Stated / Implied / Derivable] |
| ... | ... | ... | ... |

**Front-loading ratio**: [N of M findings present in theory section]

**New concepts/mechanisms named before evidence?**: [Yes — list them / No]

**Existing frameworks extended to paper's case before evidence?**: [Yes — list them / No]

**Could a reader predict all major findings from theory section alone?**: [Yes (FAIL) / No (PASS)]

**Assessment**: [PASS / FAIL]

**If FAIL, specific front-loaded content:**
- [Quote 1 — what it front-loads]
- [Quote 2 — what it front-loads]
- ...

---

## Language Scan

### Red-Flag Terms Found

| Term | Location | Context | Problem? |
|------|----------|---------|----------|
| "hypothesis" | Line X | "Rather than test as a hypothesis..." | No - disclaiming |
| "predict" | Line Y | "Theory predicts that..." | YES - implies deduction |
| ... | ... | ... | ... |

### Problematic Passages

**Passage 1** (Lines X-Y):
> [Quote]

**Problem**: [What's wrong]
**Fix**: [Suggested revision]

---

**Passage 2** (Lines X-Y):
...

---

## Temporal Logic Check

**Does the paper claim to have discovered things through research?**: [Yes / No]

**Examples of discovery language**:
- [Quote or "None found"]

**Examples of deductive language**:
- [Quote or "None found"]

**Assessment**: [PASS / NEEDS REVISION]

---

## Overall Assessment

| Check | Status |
|-------|--------|
| Theory section appropriately framed | ✓/✗ |
| Abstract/intro uses discovery framing | ✓/✗ |
| Abstract starts from naive position (not front-loaded) | ✓/✗ |
| Theory section does NOT front-load findings | ✓/✗ |
| No red-flag hypothesis language | ✓/✗ |
| Temporal logic reads as discovery | ✓/✗ |

**Overall verdict**: [PASS / REVISE / MAJOR REVISION NEEDED]

**Note:** Theory-section front-loading is a BLOCKING failure. If the theory section builds the complete mechanism that findings will show, the paper reads as deductive regardless of language. This must be PASS for overall PASS.

---

## Recommended Revisions

1. **[Location]**: [Current] → [Suggested revision]

2. **[Location]**: [Current] → [Suggested revision]

...

---

## Genre-Appropriate Reframings

If the paper needs major revision, here are key passages rewritten in discovery framing:

### Abstract (revised)

> [Rewritten version using discovery language]

### Theory section opening (revised)

> [Rewritten version as sensitizing concepts rather than hypothesis development]
```

## After You're Done

Tell the user:
- Whether the framing matches the target journal's genre expectations
- Specific passages that need revision
- Suggested rewrites for problem areas

If MAJOR REVISION needed: The entire theory section structure may need rethinking. The researcher did inductive work but wrote it up deductively—common problem, fixable with careful revision.

## Integration with Other Commands

- Run AFTER `/draft-paper`
- Run ALONGSIDE `/eval-zuckerman` (Zuckerman focuses on puzzle/motivation; this focuses on epistemological genre)
- Run BEFORE final submission

For the register match check criteria, see [register-match.md](register-match.md)


## Register Match

### Abstract Register
**Opens with**: [Research question / Theoretical claim / Sample sizes / Empirical finding]
**Core concept named?**: [Yes / No]
**Method presentation**: [Concise clause / Dominates abstract]
**Assessment**: [PASS / NEEDS REVISION]

### Introduction Citation Density
**Paragraphs before first substantive citation**: [N]
**Average citations per paragraph (post-hook)**: [N]
**Cold open used?**: [Yes (N paragraphs) / No]
**Literature pivot by paragraph 3?**: [Yes / No / N/A]
**Assessment**: [PASS / NEEDS REVISION]

### Theory-Empirics Balance
**Introduction reads as**: [Theoretical contribution / Evidence report / Mixed]
**Comparable to published exemplars?**: [Yes / No - explain gap]
**Assessment**: [PASS / NEEDS REVISION]

### Register Verdict
**Overall register match**: [PASS / REVISE]
```

Add register results to the Overall Assessment table:

| Check | Status |
|-------|--------|
| ... existing checks ... | |
| Abstract register matches target journal | ✓/✗ |
| Introduction citation density adequate | ✓/✗ |
| Cold open (if used) pivots to theory by P3 | ✓/✗ |
| Theory-empirics balance matches journal | ✓/✗ |

---

For the argument construction check criteria, see [argument-construction.md](argument-construction.md)


## Argument Construction

### Paragraph Openings
**Paragraphs sampled**: [N]
**Citation-first violations**: [N] — [list locations]
**Narration violations**: [N] — [list locations]
**Assessment**: [PASS / NEEDS REVISION]

### Transitions & Cohesion
**Boundaries checked**: [N]
**Topic jumps found**: [N] — [list locations]
**The Turn present?**: [Yes, at paragraph N / No / Multiple (problem)]
**Assessment**: [PASS / NEEDS REVISION]

### Introduction Arc
**WORLD**: [Present / Missing]
**PROBLEM**: [Present / Missing]
**GAP**: [Mechanism-specific / Vague "more research needed"]
**QUESTION**: [Present / Missing]
**PREVIEW**: [Present / Missing]
**Assessment**: [PASS / NEEDS REVISION]

### Discussion Structure
**Puzzle reconnect**: [Yes / No]
**Contribution paragraphs follow 4-move pattern**: [Yes / Partial / No]
**Final paragraph**: [Zoom-out / Paradox restatement / Summary (FAIL)]
**Assessment**: [PASS / NEEDS REVISION]

### Citation Deployment
**Consensus stacks used?**: [Yes / No]
**Author-in-prose engagement found?**: [Yes, N instances / No]
**Gap claims uncited?**: [Yes / No — overcited gaps weaken the claim]
**Assessment**: [PASS / NEEDS REVISION]

### Paragraph Granularity
**Paragraphs sampled**: [N]
**Single-sentence paragraphs**: [N] — [list locations]
**Two-sentence underdeveloped paragraphs**: [N] — [list locations]
**Assessment**: [PASS / NEEDS REVISION]
```

Add to the Overall Assessment table:

| Check | Status |
|-------|--------|
| ... existing checks ... | |
| Paragraph openings are claims (not citations) | ✓/✗ |
| Transitions thread concepts between paragraphs | ✓/✗ |
| Introduction follows WORLD→GAP arc | ✓/✗ |
| Discussion reconnects puzzle, doesn't summarize | ✓/✗ |
| Citation functions deployed appropriately | ✓/✗ |
| All paragraphs ≥3 sentences (no stubs) | ✓/✗ |

---

## Common Patterns

**"Dressed-up deduction"**: Paper was actually inductive but author wrote it deductively because that's how they were trained. Fix: Reframe theory section as "sensitizing concepts I brought to the field" rather than "hypotheses derived from literature."

**"Retroductive discovery"**: Researchers often discover patterns and then use theory to explain them (retroduction). This is legitimate! The writing should reflect it: "The pattern led me to Steiner's framework, which helped explain why..."

**"Journal mismatch"**: Some papers genuinely ARE hypothesis-testing and belong at AMJ or Management Science. If the research was truly deductive, don't force discovery framing—just target the right journal.

**"Quant-report register"**: Paper passes all language checks (no deductive terms) but reads like a research report—data-heavy opening, thin literature engagement, abstract leading with sample sizes. Common in mixed-methods papers written by quantitative researchers. Fix: Restructure abstract to lead with question/claim, add literature engagement to introduction within first 3 paragraphs, ensure theory section has substantive (not string) citations.

**"Front-loaded abstract"**: Abstract opens with discoveries presented as premises. E.g., "Managers cannot evaluate skill fit because..." when "managers decide" and "skill fit evaluation" are themselves discoveries. The paper knew its answer before posing its question. Fix: Identify the naive question ("What happens to workers when X?"), open with that, present the puzzle, THEN reveal what you found. Also check theory sections for the same error—sections that present complete mechanisms before findings should be reframed as "theoretical resources" with tentative language.

---

For consensus mode behavior, see [../../_shared/consensus-mode.md](../../_shared/consensus-mode.md)
For staleness detection, see [../../_shared/staleness-check.md](../../_shared/staleness-check.md)
For eval result persistence, see [../../_shared/eval-persistence.md](../../_shared/eval-persistence.md)

### Skill-Specific Persistence

- **eval_results key**: `genre`
- **Upstream files**: `analysis/manuscript/DRAFT.md`
- **Scores**: `structure_score`, `language_score`, `temporal_logic_score`
- **Verdict**: PASS if all scores above threshold; FAIL otherwise
- **Default consensus N**: 5
