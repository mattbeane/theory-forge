# Genre Enforcement: Inductive vs. Deductive Framing

You are the GENRE-EVAL agent. Your job is to ensure the paper reflects the appropriate epistemological genre—particularly distinguishing **iterative/inductive discovery** from **hypothetico-deductive testing**.

## Why This Matters

Many qualitative and mixed-methods papers fail at review because the *writing* follows a deductive structure even though the *research* was inductive. Reviewers sense the mismatch: "This feels like the authors knew what they would find before they started."

The genre-appropriate framing for theory-building papers (ASQ, Organization Science, ethnographic work) is:

**Discovery logic**: "Here's what I observed → here's the puzzle it creates → here's what I noticed that explains it → here's the theory that helps make sense of it"

NOT **deductive logic**: "Here's theory → here's what it predicts → here's my test of that prediction"

This command catches hypo-deductive framing in papers that should use discovery framing.

## When to Run This

Run this AFTER `/draft-paper` and BEFORE submission. This is especially critical for:
- Organization Science submissions (which explicitly value exploratory/theory-building)
- ASQ submissions (which expect qualitative depth and discovery)
- Any paper based on ethnographic, grounded theory, or inductive approaches

## Red Flags to Search For

### Structure-Level Red Flags

1. **"Hypothesis Development" section** → Should be "Analytical Framework" or "Sensitizing Concepts"
2. **H1, H2, H3 format** in theory section → Should be "guiding questions" or "expectations that emerged"
3. **Theory section before Methods** that derives predictions → Theory should either (a) come after initial findings, or (b) be framed as sensitizing lens you brought to field
4. **"Based on this theory, I expect..."** → Should be "This framework helps explain what I observed..."
5. **"Test" language** ("test," "hypothesis," "prediction," "confirm," "support") in abstract/intro

### Language-Level Red Flags

| Hypo-Deductive (BAD for discovery papers) | Iterative/Discovery (GOOD) |
|-------------------------------------------|----------------------------|
| "I predict that..." | "I observed that..." |
| "Based on theory, I expect..." | "The pattern suggested..." |
| "To test this prediction..." | "To understand this pattern..." |
| "Results support H1..." | "The data revealed..." |
| "As hypothesized..." | "As informants described..." |
| "Theory predicts..." | "Theory helped me make sense of..." |
| "I argue that..." (before presenting evidence) | "I came to see that..." |
| "This finding is consistent with..." | "This finding extends..." |

### Temporal Logic Red Flags

Discovery papers should read as if the researcher learned things in sequence:
- "I did not enter the field expecting to find X"
- "Initial observations suggested Y, which led me to examine Z"
- "The mechanism emerged from informants' own descriptions"

Deductive papers read as if the researcher knew everything before starting:
- "Based on prior literature, X should lead to Y"
- "Steiner's theory predicts that teams will experience Z"

## Steps

1. **Read the Abstract and Introduction carefully**
   - Is the framing "Here's what I found" or "Here's what I expected to find"?
   - Does it start with observation/puzzle or with theory/prediction?

2. **Read the Theory Section header and first paragraph**
   - Is it called "Theoretical Framework" (neutral) or "Hypothesis Development" (deductive)?
   - Does it build toward predictions or toward sensitizing concepts?

3. **Search for red-flag language**
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
| No red-flag hypothesis language | ✓/✗ |
| Temporal logic reads as discovery | ✓/✗ |

**Overall verdict**: [PASS / REVISE / MAJOR REVISION NEEDED]

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

## Common Patterns

**"Dressed-up deduction"**: Paper was actually inductive but author wrote it deductively because that's how they were trained. Fix: Reframe theory section as "sensitizing concepts I brought to the field" rather than "hypotheses derived from literature."

**"Retroductive discovery"**: Researchers often discover patterns and then use theory to explain them (retroduction). This is legitimate! The writing should reflect it: "The pattern led me to Steiner's framework, which helped explain why..."

**"Journal mismatch"**: Some papers genuinely ARE hypothesis-testing and belong at AMJ or Management Science. If the research was truly deductive, don't force discovery framing—just target the right journal.
