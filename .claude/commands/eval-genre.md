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

### Front-Loading Red Flags (Critical for Abstracts)

Discovery papers must start from the **naive question**, not from the answer.

**The naive question**: What a reader would ask before having read your paper. For automation studies: "What happens to workers when technology arrives?" NOT "How do managers decide which workers to assign to automation?"

**Front-loading error**: Abstract or intro opens with discoveries presented as premises.

| Front-Loading (BAD) | Naive-First (GOOD) |
|---------------------|---------------------|
| "Managers cannot evaluate skill fit because..." | "What happens to workers when automation arrives?" |
| "Selection operates through reliability..." | "Job insecurity theory predicts displacement, yet..." |
| "When organizations select workers for X, they Y..." | "Workers at a facility stayed longer. Why?" |

**How to detect front-loading:**
1. Read the abstract's first sentence
2. Ask: Could a naive reader accept this as given? Or is this something the paper discovers?
3. If discoveries are stated as premises, the abstract is front-loading

**Example failure** (actual case):
> "When genuinely novel technology arrives, managers cannot evaluate skill fit because the relevant performance criteria do not yet exist."

This presents as premise what the paper actually discovers:
- That managers are the ones deciding (discovery)
- That they cannot evaluate skill fit (discovery)
- That this is because criteria don't exist (discovery)

**Fixed version**:
> "What happens to workers when automation arrives? Job insecurity theory predicts displacement: workers perceive threats and flee. Yet at a fulfillment facility deploying robotic automation, median tenure among temporary workers quadrupled..."

**Front-loading also infects prior work sections.** Sections titled "Selection Under Epistemic Impossibility" that present complete theoretical mechanisms BEFORE findings are front-loading. Rename to "Theoretical Resources" and reframe as possibilities ("may eliminate," "might be") rather than conclusions ("we term," "the result is").

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

### Front-Loading Check

**Abstract first sentence**: [Quote]
**Is this a premise or a discovery?**: [Premise (OK) / Discovery front-loaded as premise (FAIL)]
**Naive question the paper answers**: [State it]
**Does abstract start from naive position?**: [Yes / No]
**Assessment**: [PASS / FAIL]

**If FAIL, discoveries presented as premises**:
- [Discovery 1 stated as if given]
- [Discovery 2 stated as if given]
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

## Register Match Check

Genre enforcement has TWO dimensions:
1. **Language check** (above): Catches deductive language in inductive papers
2. **Register check** (this section): Catches papers that pass language checks but don't *sound like* their target journal

A paper can avoid every hypo-deductive red flag and still read like a quant report dressed up for ASQ. Register = citation density + opening moves + theory-empirics balance + abstract structure.

### Steps for Register Check

6. **Check Abstract Register**
   - Does it open with research question, theoretical claim, or puzzle? (ASQ/OrgSci)
   - Or does it open with sample sizes and data description? (acceptable for ManSci, red flag for ASQ)
   - Is the core concept/contribution named?
   - Is method stated concisely (one clause) or does it dominate?

7. **Check Introduction Citation Density**
   - Count citations per paragraph after the opening hook
   - ASQ/OrgSci target: ≥2 substantive citations per paragraph (averaged over post-hook paragraphs)
   - ManSci/AMJ: Lower density acceptable, but still expect literature engagement by paragraph 3
   - Flag if >3 consecutive paragraphs have zero citations

8. **Check Cold-Open-With-Data (if used)**
   - Is it ≤2 paragraphs of empirical punch before literature pivot?
   - Does paragraph 3 (latest) engage literature with 2+ substantive citations?
   - Does the cold open earn its keep by making theory engagement feel urgent?
   - ✗ Five paragraphs of data description, then "Prior literature suggests..."
   - ✓ Striking empirical fact (1-2 paragraphs), then "This pattern challenges Author's (Year) claim that..."

9. **Check Theory-Empirics Balance**
   - In ASQ/OrgSci: Does the introduction sound like a theoretical contribution illustrated with evidence?
   - Or does it sound like an evidence report decorated with theory?
   - Compare against exemplar papers: How many paragraphs pass before substantive literature engagement?

### Register Output (add to GENRE_EVAL.md)

```markdown
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

## Argument Construction Check

Genre and register checks catch framing problems. This section catches **structural argument failures** — the mechanical construction errors that make even well-framed papers hard to follow. See `docs/ARGUMENT_CONSTRUCTION_RULES.md` for the full rule set.

### Steps for Argument Construction Check

10. **Check paragraph openings**
    - Sample 10+ paragraphs across all sections
    - Does each open with a CLAIM (contestable statement)?
    - Flag citation-first openings: "Author (Year) argued..." or "(Author, Year) found..."
    - Flag narration openings: "In this section, we..."
    - Flag vague openings: "Several scholars have studied..."
    - Exception: Cold opens (max 1-2 paragraphs) may lead with data/quotes

11. **Check transitions between paragraphs**
    - Sample 5+ paragraph boundaries
    - Does the last key concept of paragraph N appear in the first sentence of paragraph N+1?
    - Flag topic jumps where consecutive paragraphs introduce unconnected concepts
    - Check for "The Turn": Is there exactly ONE adversative pivot (However/But/Yet) from consensus to complication?

12. **Check introduction arc**
    - Does it follow WORLD → PROBLEM → GAP → QUESTION → PREVIEW?
    - Is the gap about a missing process/mechanism (not "more research needed")?
    - Does citation function shift across the arc (consensus → steelman → absence → tension)?

13. **Check discussion structure**
    - Does it open by reconnecting to the introduction's puzzle?
    - Does each contribution paragraph follow: literature anchor → contrast → mechanism → implication?
    - Does the final paragraph zoom out or restate paradox (NOT summarize)?
    - Is the final sentence quotable?

14. **Check citation deployment**
    - Are consensus claims backed by parenthetical stacks (3-6 citations)?
    - Are key works engaged in prose (2-5 sentences), not just cited?
    - Are gap claims typically uncited (author's own assertion)?
    - Are direct quotes reserved for definitions, with page numbers?

### Argument Construction Output (add to GENRE_EVAL.md)

```markdown
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

---

## Common Patterns

**"Dressed-up deduction"**: Paper was actually inductive but author wrote it deductively because that's how they were trained. Fix: Reframe theory section as "sensitizing concepts I brought to the field" rather than "hypotheses derived from literature."

**"Retroductive discovery"**: Researchers often discover patterns and then use theory to explain them (retroduction). This is legitimate! The writing should reflect it: "The pattern led me to Steiner's framework, which helped explain why..."

**"Journal mismatch"**: Some papers genuinely ARE hypothesis-testing and belong at AMJ or Management Science. If the research was truly deductive, don't force discovery framing—just target the right journal.

**"Quant-report register"**: Paper passes all language checks (no deductive terms) but reads like a research report—data-heavy opening, thin literature engagement, abstract leading with sample sizes. Common in mixed-methods papers written by quantitative researchers. Fix: Restructure abstract to lead with question/claim, add literature engagement to introduction within first 3 paragraphs, ensure theory section has substantive (not string) citations.

**"Front-loaded abstract"**: Abstract opens with discoveries presented as premises. E.g., "Managers cannot evaluate skill fit because..." when "managers decide" and "skill fit evaluation" are themselves discoveries. The paper knew its answer before posing its question. Fix: Identify the naive question ("What happens to workers when X?"), open with that, present the puzzle, THEN reveal what you found. Also check theory sections for the same error—sections that present complete mechanisms before findings should be reframed as "theoretical resources" with tentative language.
