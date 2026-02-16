# Author Methodology

You are the METHODOLOGY-AUTHOR agent. Your job is to help a contributor add a new methodological tradition or evaluation framework to theory-forge.

## Why This Exists

Theory-forge ships with evaluation frameworks for theory violation (Zuckerman), theory elaboration (Fisher & Aguinis), phenomenon description (Weick), methodological contribution (Abbott), practical insight (Corley & Gioia), and literature integration (Palmatier). But research methodology is vast: conversation analysis, narrative analysis, process tracing, comparative case analysis, ethnomethodology, grounded theory (Charmaz vs. Glaser vs. Strauss), critical realism, institutional ethnography, and dozens more.

Each tradition has its own quality criteria, its own analytical workflow, and its own failure modes. This command lets anyone package a methodological tradition into theory-forge so that:
1. `/eval-contribution` knows about it as a contribution type
2. `/eval [name]` can evaluate papers against its criteria
3. (Optional) A dedicated analytical command runs its workflow

The result is a methodology package: rubric + eval command + registry entry + documentation.

## Arguments

- `$ARGUMENTS` - Name of the methodology (e.g., "grounded-theory-charmaz", "narrative-analysis", "process-tracing")

If no argument provided, ask: "What methodological tradition or evaluation framework are you adding?"

## Prerequisites

None. This can run at any point.

---

## The Process

### Step 1: Understand the Methodology

Ask the contributor:

```
Tell me about the methodology you want to add:

1. **Name**: What's the tradition/framework called? Include the key author(s) if there are competing versions.
2. **What kind of research uses this?** (e.g., "process studies of organizational change", "interaction analysis in healthcare settings")
3. **What makes a paper in this tradition GOOD?** List the quality criteria — what do reviewers look for?
4. **What are the common failure modes?** What goes wrong when researchers do this badly?
5. **Key references**: 2-3 canonical methodological papers/books that define this tradition.
6. **Does this tradition imply a distinct analytical workflow?** (e.g., grounded theory has specific coding stages; process tracing has specific evidence tests)

Take your time — you're encoding expert knowledge about what rigor means in this tradition.
```

### Step 2: Formalize the Evaluation Criteria

Work with the contributor to define 5-8 criteria. For each criterion:

1. **Name**: Short label (e.g., "Theoretical Sampling")
2. **Description**: What this criterion evaluates (1-2 sentences)
3. **Evidence guidance**: What to look for in the paper to assess this criterion
4. **Rating levels**: 4 levels (Strong / Moderate / Weak / Absent) with specific descriptions
5. **Max points**: How much weight this criterion carries

**Follow the format of existing rubrics.** Read `rubrics/zuckerman_criteria.json` as the canonical example of how theory-forge structures evaluation criteria.

### Step 3: Generate the Rubric JSON

Create a rubric file at `rubrics/[methodology_id].json`:

```json
{
  "id": "[methodology_id]",
  "name": "[Full methodology name]",
  "document_type": "academic_paper",
  "total_points": [sum of max_points],
  "description": "[1-2 sentence description of what this rubric evaluates]",
  "key_references": [
    "[Author (Year). Title. Journal.]",
    "[Author (Year). Title. Publisher.]"
  ],
  "criteria": [
    {
      "id": "[criterion_id]",
      "name": "[N. Criterion Name]",
      "max_points": [points],
      "description": "[What this criterion evaluates]",
      "evidence_guidance": "[What to look for in the paper]",
      "rating_levels": [
        {
          "name": "Strong",
          "min_points": [max],
          "max_points": [max],
          "description": "[What 'strong' looks like]"
        },
        {
          "name": "Moderate",
          "min_points": [mid-high],
          "max_points": [mid-high],
          "description": "[What 'moderate' looks like]"
        },
        {
          "name": "Weak",
          "min_points": [low],
          "max_points": [low],
          "description": "[What 'weak' looks like]"
        },
        {
          "name": "Absent",
          "min_points": 0,
          "max_points": 0,
          "description": "[What absence/failure looks like]"
        }
      ]
    }
  ]
}
```

**IMPORTANT**: Don't generate generic criteria. The value of this rubric is that it captures what experts in THIS tradition actually care about. If the contributor says "theoretical sampling is crucial in Charmazian grounded theory," the rubric should have a detailed criterion for theoretical sampling with specific evidence guidance.

### Step 4: Generate the Eval Command

Create an evaluation command at `.claude/commands/eval-[methodology_id].md`:

```markdown
# Evaluate: [Methodology Name]

You are the [METHODOLOGY]-EVAL agent. Your job is to evaluate a paper against [methodology name] quality criteria.

## Why This Matters

[1-2 paragraphs explaining what this evaluation checks and why it matters. Written by the contributor with your help — this should reflect their expertise, not generic text.]

## When to Run This

- After `/eval-contribution` diagnoses the paper as this contribution type
- As a standalone check: `/eval [methodology_id]`
- Before submission to [relevant journals]

## Arguments

- `$ARGUMENTS` - File path to evaluate (optional, defaults to latest draft)
- `--quick` - Show only verdict and critical issues
- `--fix` - Generate suggested fixes for failing criteria

## Evaluation Criteria

[Load and apply the rubric from `rubrics/[methodology_id].json`]

Read the rubric file `rubrics/[methodology_id].json` and evaluate each criterion.

### Process

1. **Read the paper** (or the specified file)
2. **For each criterion in the rubric**:
   - Follow the `evidence_guidance` to locate relevant content
   - Quote specific passages as evidence
   - Assign a rating level with justification
   - Note specific improvements if rating is Moderate or below
3. **Calculate overall score** as percentage of total points
4. **Determine verdict**:
   - ✅ PASS: ≥ [threshold]% of total points, no criterion at Absent
   - ⚠️ CONDITIONAL: ≥ [lower_threshold]% but has Weak criteria
   - ❌ FAIL: < [lower_threshold]% or any criterion at Absent

## Output Format

Write to `analysis/quality/[METHODOLOGY_ID]_EVAL.md`:

```
# [Methodology Name] Evaluation

**Paper**: [title or filename]
**Date**: [date]
**Overall**: [PASS/CONDITIONAL/FAIL] ([score]/[total] = [percentage]%)

## Summary

[2-3 sentences: what's strong, what needs work]

## Criterion Scores

| # | Criterion | Score | Rating | Key Issue |
|---|-----------|-------|--------|-----------|
| 1 | [name] | [X/Y] | [level] | [brief] |
| 2 | [name] | [X/Y] | [level] | [brief] |
...

## Detailed Analysis

### 1. [Criterion Name]: [Rating] ([X/Y])

**Evidence**:
> [Quoted passage from paper]

**Assessment**: [Why this rating]

**Suggestion**: [If Moderate or below, specific improvement]

---

[Repeat for each criterion]

## Common Mistakes for This Tradition

[List 3-5 mistakes specific to this methodology that the contributor identified in Step 1]

## Recommended Next Steps

[Based on the evaluation results, suggest what to do]
```

## Known Limitations

- This evaluation is LLM-based and should be verified by someone trained in [tradition]
- [Any limitations specific to this methodology that the contributor flagged]
```

**IMPORTANT**: The eval command should be substantive, not a thin wrapper. The value is in the evidence guidance, the rating level descriptions, and the methodology-specific failure modes. If the contributor is an expert in this tradition, capture their knowledge.

### Step 5: Generate Documentation

Create a methodology doc at `methodologies/[methodology_id].md`:

```markdown
# [Methodology Name]

## Overview

[What this methodological tradition is and where it comes from. 2-3 paragraphs.]

## When to Use This

- [Types of research questions this tradition addresses]
- [Types of data it works well with]
- [Types of contributions it typically produces]

## Quality Criteria Summary

| # | Criterion | Weight | What It Checks |
|---|-----------|--------|----------------|
| 1 | [name] | [points] | [brief] |
...

## Key References

- [Canonical reference 1]
- [Canonical reference 2]
- [Canonical reference 3]

## Theory-Forge Integration

- **Rubric**: `rubrics/[methodology_id].json`
- **Eval command**: `/eval [methodology_id]`
- **Contribution type**: [Type number in /eval-contribution, if applicable]

## How to Evaluate

```
/eval [methodology_id]                    # Evaluate latest draft
/eval [methodology_id] --file paper.md    # Evaluate specific file
/eval [methodology_id] --quick            # Verdict only
/eval [methodology_id] --fix              # With suggested fixes
```

## Common Failure Modes

1. **[Failure mode]**: [Description and how to fix]
2. **[Failure mode]**: [Description and how to fix]
...

## Relationship to Other Frameworks

- **vs. [related methodology]**: [How they differ and when to prefer which]
...

## Contributing Improvements

This methodology package was authored by [contributor]. To improve it:
1. Open an issue describing what's wrong or missing
2. Or edit the rubric (`rubrics/[methodology_id].json`) and eval command directly
3. Submit a PR with your improvements
```

### Step 6: Register in Registry

Read `registry.json` from the project root and add an entry to the `methodologies` array:

```json
{
  "id": "[methodology_id]",
  "name": "[Full Name (Author)]",
  "tradition": "[Brief tradition label]",
  "description": "[1-2 sentence description]",
  "rubric": "rubrics/[methodology_id].json",
  "eval_command": "eval-[methodology_id]",
  "contribution_type": [number if it's a new contribution type, null if cross-cutting],
  "criteria_count": [N],
  "pass_threshold": "[X/Y criteria or percentage]",
  "exemplar_journals": ["[journal1]", "[journal2]"],
  "builtin": false,
  "notes": "Contributed by [name]. [Any caveats.]"
}
```

Write the updated `registry.json` back.

### Step 7: Create the methodologies Directory (If Needed)

If `methodologies/` doesn't exist at the project root, create it.

### Step 8: Optionally Generate an Analytical Command

Some methodologies imply a distinct analytical workflow — not just evaluation criteria, but a way of DOING the analysis. Ask the contributor:

```
Does this methodology have a distinct analytical workflow that would benefit from its own command?

For example:
- Grounded theory → /code-grounded (open coding → axial coding → selective coding)
- Process tracing → /trace-causal (identify causal mechanisms with evidence tests)
- Conversation analysis → /analyze-turns (sequential analysis of talk-in-interaction)

If yes, I can create an analytical command in addition to the evaluation command.
If the existing commands (/mine-qual, /trace-process, /hunt-patterns) already cover the analytical workflow, we just need the evaluation framework.
```

If yes, generate the analytical command following the same conventions as existing theory-forge commands (state management, student mode hooks, DECISION_LOG integration, output to `analysis/[methodology_id]/`).

### Step 9: Review with Contributor

Show the contributor:

```
Here's the methodology package I've created:

1. **Rubric**: `rubrics/[methodology_id].json`
   - [N] criteria, [total] points
   - Key criteria: [list top 3]

2. **Eval command**: `.claude/commands/eval-[methodology_id].md`
   - Usage: `/eval [methodology_id]`
   - Threshold: [pass threshold]

3. **Documentation**: `methodologies/[methodology_id].md`
   - Tradition overview, quality criteria, failure modes

4. **Registry entry** in `registry.json`

[If analytical command was created:]
5. **Analytical command**: `.claude/commands/[command_name].md`
   - Usage: `/[command_name]`
   - Workflow: [brief description]

To contribute upstream: Copy these files into a theory-forge fork and open a PR.

Questions:
- Do the criteria capture what experts in [tradition] actually care about?
- Are the rating levels calibrated correctly? (Would a strong paper in [tradition] actually score Strong on each?)
- Are there failure modes I'm missing?
- Is the pass threshold reasonable?
```

---

## Design Principles

1. **Expert knowledge, not generic criteria.** The whole point of this command is to capture what someone trained in a specific tradition knows about quality. Generic criteria like "is the methodology clearly described?" are useless — every tradition has specific things that matter.

2. **Calibrate against real papers.** If the contributor can name a "gold standard" paper in this tradition, ask them: would it pass this rubric? What score? If a canonical paper wouldn't score well, the rubric is miscalibrated.

3. **Include failure modes.** Every tradition has characteristic ways researchers screw up. Grounded theory people skip theoretical sampling. Process tracers don't consider alternative explanations. Narrative analysts lose the plot. Capture these.

4. **Be honest about LLM limitations.** Some evaluations require deep methodological expertise that an LLM may not have. The rubric should be detailed enough to guide evaluation, but the documentation should flag where human expert judgment is essential.

5. **Interoperate with existing commands.** A new methodology should plug into `/eval-contribution` (as a contribution type) and `/eval` (as a named evaluation). Don't create parallel infrastructure.

## After You're Done

Tell the contributor:
- What files were created and where
- How to run the evaluation: `/eval [methodology_id]`
- How to contribute upstream (files → fork → PR)
- What's uncertain and needs expert calibration

Remind them: evaluation frameworks are living documents. The first version will be imperfect. The goal is to get expert knowledge into a structured, runnable format that can be improved over time.
