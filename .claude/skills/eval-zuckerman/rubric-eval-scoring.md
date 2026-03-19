## Quantitative Scoring with rubric-eval

For systematic scoring with statistical confidence, use rubric-eval.

### Step 1: Check for rubric-eval

```bash
which rubric-eval
```

**If not found**: Fall back to qualitative ratings (✓/⚠️/✗) above, and note to user:
> "Install rubric-eval for quantitative scoring: `pip install rubric-eval`"

### Step 2: Run rubric-eval

```bash
rubric-eval eval output/manuscript.pdf rubrics/zuckerman_criteria.json \
  --type academic_paper \
  --loader pdf \
  --runs 5 \
  --model claude-3-5-haiku-20241022
```

For markdown files:
```bash
rubric-eval eval output/manuscript.md rubrics/zuckerman_criteria.json \
  --type academic_paper \
  --loader text \
  --runs 5 \
  --model claude-3-5-haiku-20241022
```

### Step 3: Interpret scores

The rubric produces 50 points total (10 criteria × 5 points each):

| Score Range | Interpretation |
|-------------|----------------|
| 45-50 | Excellent framing - ready for submission |
| 35-44 | Good framing - minor adjustments needed |
| 25-34 | Adequate - some criteria need work |
| 15-24 | Weak - significant reframing required |
| 0-14 | Major issues - consider `/smith-frames` again |

### Step 4: Flag weak criteria

Any criterion scoring 0-2 (Absent or Weak) should be prioritized:

```bash
rubric-eval flagged <session_id>
```

Common patterns:
- **Low puzzle_in_world + Low frame_around_dv**: Literature-gap framing problem
- **Low compelling_null + Low save_null**: Not engaging with alternatives
- **Low motivate_paper + Low orient_reader**: Structural/narrative issues
- **Low know_audience**: Trying to please everyone

### Step 5: Add to evaluation report

Include quantitative scores in `ZUCKERMAN_EVAL.md`:

```markdown
