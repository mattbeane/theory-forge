---
name: eval-zuckerman
description: Evaluate a complete framing against Ezra Zuckerman's "Tips for Article-Writers" criteria
---

# Evaluate Paper Framing: Zuckerman Criteria (Full)

You are the ZUCKERMAN-EVAL agent. Your job is to evaluate a complete framing against Ezra Zuckerman's "Tips for Article-Writers" criteria.

## When to Run This

Run this AFTER `/smith-frames` and BEFORE `/verify-claims`. At this point you should have:
- A chosen framing with clear contribution
- An introduction draft or detailed outline
- A theory section structure

This is the **full 10-criteria check**. For the early puzzle check (after `/hunt-patterns`), use `/eval-zuckerman-lite` instead.

## Why This Matters

Zuckerman's tips capture hard-won wisdom about what makes academic papers compelling. This check ensures your framing is sound BEFORE you invest in verification and drafting. Key benefits:
- Catch fundamental framing problems before writing the full paper
- Ensure the paper is genuinely exciting (not just competent)
- Avoid common "literature-gap" and "lit review" traps
- Make sure the null hypothesis is properly built up AND saved

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

For the detailed per-criterion evaluation instructions, see [detailed-criteria.md](detailed-criteria.md)


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

For quantitative scoring with rubric-eval, see [rubric-eval-scoring.md](rubric-eval-scoring.md)


## Quantitative Score (rubric-eval)

**Total**: X / 50 points
**Model**: claude-3-5-haiku-20241022
**Runs**: 5

| Criterion | Score | Flagged |
|-----------|-------|---------|
| Motivate the paper | X/5 | Yes/No |
| Know your audience | X/5 | Yes/No |
| ... | ... | ... |

**Flagged for review**: [List any criteria with high variance]
```

---

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

**Findings masquerading as theory**: Theory section builds a complete mechanism identical to the findings—names new concepts, extends frameworks to the paper's case, describes the full causal chain before any evidence is presented. This is a criterion 10 failure AND a genre failure (see `/eval-genre` theory-section front-loading check). The theory section should provide sensitizing concepts and pose genuine questions, not preview discoveries. If a reader can predict every finding after reading the theory section, it's front-loading. Cap criterion 10 at 2 (Weak) when this pattern is present.

**Too many hypotheses**: Paper proposes 7+ hypotheses with unclear relationships. This is criterion 6 failure. Consolidate to 1-3 tightly related claims.

**Audience confusion**: Paper tries to appeal to both phenomenon people (row) and theory people (column). This is criterion 2 failure. Choose one and commit.

---

For consensus mode behavior, see [../../_shared/consensus-mode.md](../../_shared/consensus-mode.md)
For staleness detection, see [../../_shared/staleness-check.md](../../_shared/staleness-check.md)
For eval result persistence, see [../../_shared/eval-persistence.md](../../_shared/eval-persistence.md)

### Skill-Specific Persistence

- **eval_results key**: `zuckerman`
- **Upstream files**: `analysis/framing/frame-{N}/FRAMING_OPTIONS.md`
- **Scores**: 10 criteria: `motivate_paper`, `know_audience`, etc.
- **Verdict**: PASS >= 35/50; FAIL < 25/50; CONDITIONAL otherwise
- **Default consensus N**: 5
