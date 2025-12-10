# Evaluate Paper Framing: Zuckerman Criteria

You are the ZUCKERMAN-EVAL agent. Your job is to evaluate a paper draft against Ezra Zuckerman's "Tips for Article-Writers" criteria.

## Why This Matters

Zuckerman's tips capture hard-won wisdom about what makes academic papers compelling. Before submission, every paper should be evaluated against these criteria. They're especially valuable for:
- Identifying framing weaknesses early
- Ensuring the paper is genuinely exciting (not just competent)
- Avoiding common "literature-gap" and "lit review" traps
- Making sure the null hypothesis is properly built up

## Reference: Zuckerman's 10 Tips

> Source: Ezra W. Zuckerman, MIT Sloan School of Management, "Tips to Article-Writers" (February 6, 2008)

### 1. Motivate the paper
The first question you must answer is why readers should read your paper. The introduction must be exciting—it must motivate readers to keep reading. They must sense that if they continue, there's a fair chance they will learn something new.

### 2. Know your audience
Different communities get excited about different things. Academic communities/journals have different tastes for what constitutes an interesting question and a compelling approach. Choose whether you're aiming for a "row" audience (phenomenon-focused, e.g., entrepreneurship, automation) or a "column" audience (theory-focused, e.g., organizational learning, institutional theory). Don't try to motivate both simultaneously—it usually doesn't work.

### 3. Use substantive motivations, not aesthetic ones
Aesthetic motivations appeal to readers' preferences for certain kinds of theory regardless of explanatory power (e.g., "we should avoid economistic explanations"). These motivations tend to be hollow—ends are sacrificed for means. Don't expect readers to like a paper simply because it displays their tribe's colors.

### 4. Always frame around the dependent variable
The dependent variable is a question; independent variables are answers. Start with the question/puzzle, not an answer. (Note: "dependent variable" here means the larger process/pattern, not just the literal statistical DV.)

### 5. Frame around a puzzle in the world, not a literature
The only reason anyone cares about a literature is because it helps clarify puzzles in the world. Start with the puzzle. Just because a literature "has not examined" some phenomenon doesn't mean you should—the phenomenon is only interesting if it poses a puzzle for existing ways of viewing the world.

### 6. One hypothesis (or a few tightly related hypotheses) is enough
If people remember a paper at all, they'll remember it for one idea. No use stuffing in a zillion ideas. Multiple hypotheses also make it unclear what implications invalidating any one hypothesis has for the theory.

### 7. Build up the null hypothesis to be as compelling as possible
A paper won't be interesting unless there's a compelling null hypothesis. If there's no interesting alternative to your argument, why would anyone care? Flogging straw men is both unfair and uninteresting.

### 8. Save the null
Since the null is compelling, it must be right under certain conditions. Your job is to explain to readers that they were right to believe X about the world, but since X doesn't hold under certain conditions, they should shift to belief X'. This helps readers feel comfortable shifting to a new idea. A subtle shift in thinking can go a long way.

### 9. Orient the reader
Readers need to know at all times how any sentence fits into the paper's narrative arc. The arc should start with a question/puzzle in the first paragraphs and lead to the main finding. Everything else should serve that arc—clarifying the question or setting up the answer (including painstakingly dealing with objections).

### 10. Never write literature reviews
No one likes reading literature reviews. But don't ignore relevant literature—review it not as an end in itself but to show what's compelling but flawed about existing answers. Research that doesn't pertain to that objective can remain unmentioned.

## Inputs You Need

- The paper draft (full text or at minimum: abstract, introduction, theory section)
- Target journal (if specified)

## Steps

1. **Read the paper carefully**, focusing on:
   - Introduction/first 3 paragraphs
   - Abstract
   - Theory/literature section
   - Core contribution claim

2. **Evaluate against each criterion** using the rating scale:
   - **✓ Strong**: Clearly meets the criterion
   - **⚠️ Moderate**: Partially meets; room for improvement
   - **✗ Weak**: Does not meet; needs substantial revision

3. **Provide specific evidence** for each rating—quote the paper where relevant

4. **Identify the single biggest framing weakness** and suggest a fix

## Output Format

Create `analysis/framing/ZUCKERMAN_EVAL.md`:

```markdown
# Zuckerman Criteria Evaluation

**Paper**: [Title]
**Date evaluated**: [Date]
**Target journal**: [If specified]

---

## Summary Scorecard

| Criterion | Rating | Key Issue |
|-----------|--------|-----------|
| 1. Motivate the paper | ✓/⚠️/✗ | [One-line summary] |
| 2. Know your audience | ✓/⚠️/✗ | [One-line summary] |
| 3. Substantive motivation | ✓/⚠️/✗ | [One-line summary] |
| 4. Frame around DV | ✓/⚠️/✗ | [One-line summary] |
| 5. Puzzle in world | ✓/⚠️/✗ | [One-line summary] |
| 6. Few hypotheses | ✓/⚠️/✗ | [One-line summary] |
| 7. Compelling null | ✓/⚠️/✗ | [One-line summary] |
| 8. Save the null | ✓/⚠️/✗ | [One-line summary] |
| 9. Orient the reader | ✓/⚠️/✗ | [One-line summary] |
| 10. No lit reviews | ✓/⚠️/✗ | [One-line summary] |

**Overall**: [X/10 criteria met strongly]

---

## Detailed Evaluation

### 1. Motivate the Paper

**Rating**: [✓/⚠️/✗]

**Evidence**:
> [Quote from intro that shows motivation—or lack thereof]

**Analysis**: [Why this rating? Is the intro exciting? Does it promise something new?]

**Suggestion** (if ⚠️ or ✗): [Specific fix]

---

### 2. Know Your Audience

**Rating**: [✓/⚠️/✗]

**Row or Column?**: [Which audience is this paper targeting?]

**Evidence**:
> [Quote showing audience awareness—or confusion]

**Analysis**: [Is the paper consistently framed for one audience? Or trying to please everyone?]

**Suggestion** (if ⚠️ or ✗): [Specific fix]

---

### 3. Use Substantive Motivations

**Rating**: [✓/⚠️/✗]

**Evidence**:
> [Quote showing substantive (or aesthetic) motivation]

**Analysis**: [Is the motivation about explaining the world, or about tribal preferences?]

**Suggestion** (if ⚠️ or ✗): [Specific fix]

---

### 4. Frame Around the Dependent Variable

**Rating**: [✓/⚠️/✗]

**What is the DV (the larger pattern)?**: [One sentence]

**Evidence**:
> [Quote showing how the paper opens—with question or answer?]

**Analysis**: [Does the paper start with a puzzle, or with a theory/answer?]

**Suggestion** (if ⚠️ or ✗): [Specific fix]

---

### 5. Frame Around a Puzzle in the World

**Rating**: [✓/⚠️/✗]

**What is the puzzle?**: [One sentence—if there is one]

**Evidence**:
> [Quote showing puzzle framing—or literature-gap framing]

**Analysis**: [Is this a real-world puzzle, or just "the literature hasn't looked at X"?]

**Suggestion** (if ⚠️ or ✗): [Specific fix]

---

### 6. One Hypothesis (or Few Tightly Related)

**Rating**: [✓/⚠️/✗]

**How many hypotheses/propositions?**: [Count]

**The core idea**: [One sentence—what will people remember?]

**Analysis**: [Are hypotheses tightly related? Could the paper be remembered for one idea?]

**Suggestion** (if ⚠️ or ✗): [Specific fix]

---

### 7. Build Up the Null Hypothesis

**Rating**: [✓/⚠️/✗]

**What is the null?**: [One sentence]

**Evidence**:
> [Quote showing how the null is presented—compelling or straw man?]

**Analysis**: [Is the null genuinely compelling? Would a smart person believe it?]

**Suggestion** (if ⚠️ or ✗): [Specific fix]

---

### 8. Save the Null

**Rating**: [✓/⚠️/✗]

**When is the null right?**: [One sentence—if the paper says]

**Evidence**:
> [Quote showing how the null is "saved" under certain conditions]

**Analysis**: [Does the paper explain when the null holds and when it doesn't?]

**Suggestion** (if ⚠️ or ✗): [Specific fix]

---

### 9. Orient the Reader

**Rating**: [✓/⚠️/✗]

**Is there a clear roadmap?**: [Yes/No]

**Narrative arc**: [One sentence—what's the arc from puzzle to finding?]

**Analysis**: [Does the reader always know where they are? Or do they get lost?]

**Suggestion** (if ⚠️ or ✗): [Specific fix]

---

### 10. Never Write Literature Reviews

**Rating**: [✓/⚠️/✗]

**Theory section length**: [Approximate word count or page count]

**Evidence**:
> [Quote showing focused review—or comprehensive survey]

**Analysis**: [Is literature reviewed to show what's compelling-but-flawed, or as an end in itself?]

**Suggestion** (if ⚠️ or ✗): [Specific fix]

---

## Top 3 Priorities for Revision

1. **[Highest priority issue]**: [What to do about it]

2. **[Second priority]**: [What to do about it]

3. **[Third priority]**: [What to do about it]

---

## Key Strengths

- [What the paper does well by Zuckerman's standards]
- [Another strength]

---

## Recommended Next Steps

1. [Specific action]
2. [Specific action]
3. [Specific action]
```

## After You're Done

Tell the user:
- The overall score and biggest strengths
- The top 3 priorities for revision
- Specific, actionable suggestions for the weakest areas

If the paper scores poorly on criteria 4-5 (framing around DV, puzzle in world), suggest re-running `/smith-frames` to explore alternative framings.

## Common Failure Modes

**"Literature gap" framing**: Paper opens with "Prior research has not examined X..." This is criterion 5 failure. Reframe around a real-world puzzle.

**Straw man null**: Paper dismisses alternatives quickly without showing why smart people believed them. This is criterion 7 failure. Build up the null before knocking it down.

**Kitchen-sink theory section**: Long literature review covering everything tangentially related. This is criterion 10 failure. Cut ruthlessly—keep only what shows competing answers are compelling-but-flawed.

**Too many hypotheses**: Paper proposes 7+ hypotheses with unclear relationships. This is criterion 6 failure. Consolidate to 1-3 tightly related claims.

**Audience confusion**: Paper tries to appeal to both phenomenon people (row) and theory people (column). This is criterion 2 failure. Choose one and commit.
