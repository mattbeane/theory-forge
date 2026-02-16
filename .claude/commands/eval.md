# /eval - Run Individual Evaluations

Run any evaluation independently, outside the full pipeline. Useful for:
- Quick spot-checks during revision
- Re-running a single eval after making changes
- Iterative improvement on specific framing issues

## Usage

```
/eval [evaluation-name] [--file path/to/paper.md]
```

## Available Evaluations

### Built-in Evaluations

| Name | What It Checks | Typical Use |
|------|----------------|-------------|
| `zuckerman` | Full 10-criteria framing check | Before submission, after major intro/theory changes |
| `zuckerman-lite` | Quick puzzle check (criteria 4-7) | Early framing sanity check |
| `becker` | Generalizability test | After framing selection |
| `genre` | Inductive vs. deductive framing | After any revision (LLM skews deductive) |
| `limitations` | Limitations section quality | After draft, before submission |
| `citations` | Reference coverage | Before submission |
| `contribution` | Contribution clarity | After framing work |

### Contributed Evaluations (from registry)

Check `registry.json` in the project root for additional methodologies that have `eval_command` entries. Any methodology registered with an `eval_command` can be run via `/eval [name]`.

To add a new evaluation framework: `/author-methodology`

## Arguments

- `$ARGUMENTS` - The evaluation name (required)
- `--file` - Path to paper file (optional, defaults to latest in output/drafts/)
- `--quick` - Suppress verbose output, show only verdict and critical issues
- `--fix` - Attempt to generate fixes for failing criteria

## Examples

```
/eval genre                           # Check genre on latest draft
/eval zuckerman --file paper_v2.md    # Full Zuckerman on specific file
/eval becker --quick                  # Quick generalizability check
/eval genre --fix                     # Check genre and suggest fixes
```

## Behavior

### Step 1: Parse Arguments

Extract:
- Evaluation name (required)
- File path (optional)
- Flags (--quick, --fix)

If no file specified, find the most recent file in `output/drafts/` or look for `submission/main.tex`.

### Step 2: Validate

Check that the file exists and is readable. If not found:

```
⚠️ No paper found. Specify a file with --file or run /draft-paper first.
```

### Step 3: Run the Evaluation

First, check the built-in dispatch table:

| Input | Runs |
|-------|------|
| `zuckerman` | `/eval-zuckerman` |
| `zuckerman-lite` | `/eval-zuckerman-lite` |
| `becker` | `/eval-becker` |
| `genre` | `/eval-genre` |
| `limitations` | `/eval-limitations` |
| `citations` | `/eval-citations` |
| `contribution` | `/eval-contribution` |

**If the evaluation name doesn't match a built-in**, check `registry.json` in the project root:

1. Read `registry.json`
2. Search `methodologies` array for an entry where `id` or `eval_command` matches the requested name
3. If found and an `eval_command` exists, dispatch to `/[eval_command]`
4. If found but no `eval_command`, check if a rubric file exists at the `rubric` path — if so, run a generic rubric-based evaluation using that JSON rubric
5. If not found anywhere:
   ```
   ❌ Unknown evaluation: "[name]"

   Available evaluations:
   [list built-in table + any registered methodologies with eval_commands]

   To add a new evaluation framework: /author-methodology
   ```

### Step 4: Report Results

**Standard output:**
- Show full evaluation report
- Write to `analysis/quality/[EVAL_NAME]_EVAL.md`

**With `--quick`:**
```
/eval genre --quick

Genre Check: ✓ PASS
  - Structure: Inductive framing ✓
  - Language: No red flags ✓
  - Temporal logic: Discovery narrative ✓
```

Or if issues found:
```
/eval genre --quick

Genre Check: ✗ FAIL
  Critical issues:
  - Line 56: "derive observable implications" ← hypo-deductive
  - Line 23: "we hypothesize that..." ← explicit hypothesis

  Run without --quick for full report and suggested fixes.
```

**With `--fix`:**

After showing issues, generate specific fixes:

```
/eval genre --fix

Genre Check: ✗ FAIL

Issues found:
1. Line 56: "We derive observable implications from this framework"
   Fix → "This framework helps make sense of the patterns we observed"

2. Line 23: "We hypothesize that technology-mediated work reduces..."
   Fix → "Our observations suggest that technology-mediated work reduces..."

Apply these fixes? [Y/n]
```

If user confirms, apply the edits directly.

## Re-Run After Revisions

**IMPORTANT**: Passing an evaluation once doesn't mean it stays passed.

LLM-generated prose (including revisions) tends to drift toward hypo-deductive framing. After ANY substantive revision to:
- Introduction
- Abstract
- Theory section

Re-run `/eval genre` before submission.

Common symptoms of drift:
- "develop and test" → should be "develop this argument from"
- "derive implications" → should be "this framework illuminates"
- "we predict" → should be "we observed"

## Evaluation Quick Reference

### Zuckerman (7/10 to pass)

1. Motivate the paper
2. Know your audience
3. Substantive motivation
4. Frame around DV
5. Puzzle in world
6. Few hypotheses
7. Compelling null
8. Save the null
9. Orient the reader
10. No lit reviews

### Becker (PASS/CONDITIONAL/FAIL)

- Can you state your finding without domain-specific nouns?
- Does the abstracted claim transfer to 3+ other domains?
- Does it connect to existing middle-range theory?

### Genre (PASS/FAIL)

- Is the paper framed as discovery (inductive) or testing (deductive)?
- Does the framing match what you actually did?
- Does the framing match the target journal?

### Limitations (PASS/FAIL)

- ≤400 words
- Not enumerated confessions
- Includes generalizability discussion
- No over-disclosure

### Citations (threshold varies by journal)

- ASQ: 60-120
- Org Science: 50-100
- AMJ: 80-150
- Management Science: 40-80
- Missing canonical works flagged

## Integration with Pipeline

These evaluations are also run as part of `/run-pipeline`:
- Stage 6 runs zuckerman, becker, genre (Gate D)
- Stage 9 runs limitations, citations (Gate F)

Use `/eval` for spot-checks; use `/run-pipeline` for full workflow enforcement.
