# Evaluate Paper Quality

You are the PAPER-QUALITY-EVAL agent. Your job is to evaluate a draft paper using the paper_quality rubric with rubric-eval.

## When to Run This

Run this AFTER `/draft-paper` to get systematic quality assessment. This provides:
- Objective scores across 5 key quality dimensions
- Confidence-weighted aggregation (multiple evaluation runs)
- Identification of areas needing improvement
- Flagging of criteria with high variance (needs human review)

This is complementary to `/eval-zuckerman` which focuses on framing. This command focuses on overall execution quality.

## Prerequisites

- A draft paper in PDF or markdown format

### Required: rubric-eval

This command requires rubric-eval. Check if installed:
```bash
which rubric-eval
```

**If not found**, install it:
```bash
pip install rubric-eval
```

Also requires `ANTHROPIC_API_KEY` in environment for API calls.

## Inputs You Need

- Path to the draft paper (PDF or markdown)
- Number of evaluation runs per criterion (default: 5)
- Whether to use batch mode (50% cost reduction but slower)

## Steps

1. **Locate the rubric**

   The paper quality rubric is at:
   ```
   rubrics/paper_quality.json
   ```

2. **Prepare the paper**

   If paper is in markdown, you may want to convert to PDF first for better rubric-eval compatibility:
   ```bash
   # Using pandoc (if available)
   pandoc output/manuscript.md -o output/manuscript.pdf
   ```

   Or use the markdown file directly with the `text` loader.

3. **Run rubric-eval**

   Choose between real-time or batch mode:

   **Real-time mode** (faster, shows progress):
   ```bash
   rubric-eval eval output/manuscript.pdf rubrics/paper_quality.json \
     --type paper_draft \
     --loader pdf \
     --runs 5 \
     --model claude-3-5-haiku-20241022 \
     --db paper_evals.db
   ```

   **Batch mode** (50% cheaper, async):
   ```bash
   rubric-eval batch output/manuscript.pdf rubrics/paper_quality.json \
     --type paper_draft \
     --loader pdf \
     --runs 5 \
     --model claude-3-5-haiku-20241022 \
     --db paper_evals.db

   # Monitor batch status
   rubric-eval batch-status --db paper_evals.db

   # Retrieve results when complete
   rubric-eval batch-retrieve --db paper_evals.db
   ```

4. **View results**

   ```bash
   # Get the session ID from the eval output, then:
   rubric-eval results <session_id> --db paper_evals.db

   # See criteria flagged for human review
   rubric-eval flagged <session_id> --db paper_evals.db

   # Export to CSV for analysis
   rubric-eval export <session_id> --output paper_quality_scores.csv --db paper_evals.db
   ```

5. **Interpret the results**

   For each criterion, rubric-eval provides:
   - **Final score**: Confidence-weighted median across runs
   - **Variance**: How much evaluators disagreed
   - **Flagged**: True if high variance or split decisions

   **Score interpretation**:
   - **45-50**: Excellent - ready for submission with minor polish
   - **35-44**: Good - solid draft, some improvements needed
   - **25-34**: Adequate - substantial revision required
   - **15-24**: Weak - major problems to address
   - **0-14**: Unacceptable - needs fundamental rework

## Output Format

Create `analysis/quality/QUALITY_EVAL_REPORT.md`:

```markdown
# Paper Quality Evaluation

**Paper**: [Title]
**Evaluated**: [Date]
**Model**: claude-3-5-haiku-20241022
**Runs per criterion**: 5

---

## Overall Score

**Total**: X / 50 points

**Rating**: [Excellent/Good/Adequate/Weak/Unacceptable]

---

## Criterion Scores

| Criterion | Score | Max | Rating | Flagged |
|-----------|-------|-----|--------|---------|
| Argument Clarity | X/10 | 10 | [Level] | [Yes/No] |
| Evidence Quality | X/10 | 10 | [Level] | [Yes/No] |
| Theoretical Grounding | X/10 | 10 | [Level] | [Yes/No] |
| Contribution Significance | X/10 | 10 | [Level] | [Yes/No] |
| Prose Quality | X/10 | 10 | [Level] | [Yes/No] |

---

## Detailed Feedback

### Argument Clarity [X/10]

**Score explanation**: [Why this score? What evidence?]

**Specific issues**:
- [Issue 1 with quote/example]
- [Issue 2 with quote/example]

**Recommendations**:
- [Specific action to improve]
- [Specific action to improve]

**Flagged for human review?**: [Yes/No - why?]

---

[Repeat for each criterion]

---

## Top 3 Priorities for Revision

1. **[Lowest scoring criterion]**: [Specific action plan]

2. **[Second lowest or high-variance criterion]**: [Specific action plan]

3. **[Third priority]**: [Specific action plan]

---

## Key Strengths

- [What the paper does well]
- [Another strength]
- [Another strength]

---

## Evaluation Reliability

**Criteria flagged for human review**: [Number]
- [Criterion name]: [Why flagged - high variance/split decision]

**Confidence notes**:
- [Any criteria with consistently low confidence across runs]
- [Any patterns in evaluator disagreement]

---

## Recommended Next Steps

1. [Immediate action based on results]
2. [Second action]
3. [Third action]

---

## Cost Summary

- **API calls**: [Number]
- **Estimated cost**: $[Amount]
- **Mode**: [Real-time/Batch]
```

## After You're Done

Tell the user:
- The overall score (X/50) and rating
- The top 3 priorities for revision
- Which criteria were flagged for human review (if any)
- Specific, actionable recommendations for the weakest areas
- Whether the paper appears ready for submission or needs substantial work

## Integration with Other Commands

- Run **after** `/draft-paper` for systematic quality check
- Run **before** final submission to catch issues
- Compare with `/eval-zuckerman` for comprehensive assessment:
  - Zuckerman eval: Framing, puzzle, audience fit
  - Quality eval: Execution, evidence, prose, contribution
- Use alongside `/verify-claims` to ensure claims are both verified AND well-presented

## Cost Estimation

Using Claude 3.5 Haiku with 5 runs on a 12,000-word paper:
- **Real-time**: ~$0.10-0.15 per paper
- **Batch**: ~$0.05-0.08 per paper (50% savings)

Increase runs to 10 for higher confidence (~2x cost).

## Pre-Check: Argument Construction

**Before running rubric-eval, scan for argument construction violations.**

These are structural issues that affect how the argument lands, independent of content quality:

1. **Citation-first paragraphs**: Search for paragraphs opening with "Author (Year)" or "(Author, Year)" or "According to Author". Count violations. Exception: definitional paragraphs in theory sections ("Power (1997) termed...").

2. **Introduction opening**: Check if the first paragraph of the introduction opens with "Prior research..." or "The literature on..." instead of a phenomenon/puzzle. Flag if so.

3. **Discussion closing**: Check if the final paragraph of the discussion opens with "In this paper, we examined..." or "In summary..." Flag if so — the closing should zoom out or restate the paradox, never summarize.

4. **Transition quality**: Spot-check 3 paragraph boundaries (one in intro, one in theory, one in discussion). For each, check whether the first sentence of paragraph N+1 picks up a concept from the last sentence of paragraph N. Note gaps.

5. **Citation function variety**: In the theory section, check whether all citations are parenthetical stacks or whether at least 1-2 exemplar studies are engaged in prose (2+ sentences). All-parenthetical = thin engagement.

**Report these as structural issues** in the quality eval output, separate from rubric-eval scores. Reference `docs/ARGUMENT_CONSTRUCTION_RULES.md` for the full rule set.

---

## Pre-Check: Tracking Paragraphs

**Before running rubric-eval, scan for and flag tracking paragraphs.**

Search the manuscript for:
- "In this paper, we..."
- "This paper proceeds as follows..."
- "We organize the remainder..."
- "In the next section, we..."
- "We then present our..."
- "The paper is structured as follows..."

**If found**: Flag in the report as a prose quality issue. These are throat-clearing that breaks flow. A good paper is self-guiding - readers don't need a roadmap if the structure is clear.

**Action**: Delete tracking paragraphs before final submission. If structure isn't clear without them, fix the structure.

---

## Common Patterns

**Low argument_clarity + Low theoretical_grounding**: Paper needs conceptual tightening before prose work.

**Low evidence_quality**: Go back to `/verify-claims` - may need stronger support.

**Low contribution_significance**: May need reframing - consider `/smith-frames` again.

**Low prose_quality only**: Good news! Just needs editing, not rethinking.

**High variance on theoretical_grounding**: Edge case - get human expert review.

**Tracking paragraphs found**: Delete them. They signal author insecurity and break narrative momentum.

## Troubleshooting

**"No documents found"**: Check file path and loader type match (use `pdf` for .pdf, `text` for .md/.txt)

**High variance across all criteria**: Paper may have inconsistent quality - some sections strong, others weak. Drill down to specific sections.

**All scores excellent but paper feels off**: Consider Zuckerman criteria (framing, audience, motivation) which this rubric doesn't directly measure.
