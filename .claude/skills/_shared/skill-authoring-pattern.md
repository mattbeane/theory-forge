# Skill Authoring Pattern

Use this document whenever creating a new skill for theory-forge — whether from `/extend-forge` or manually. It encodes the canonical SKILL.md structure and the four-file wiring checklist every new skill requires.

---

## Step 0: Classify the Skill Type

Before writing anything, determine which type the new skill is:

| Type | Description | Scoring? | Wiring target |
|------|-------------|----------|---------------|
| **Eval skill** | Scores a paper section or property on a rubric | Yes — dimensional, /N total | All 4 wiring files |
| **Analysis skill** | Extracts, mines, or synthesizes from data/manuscript | No | check-submission (conditional), README |
| **Output skill** | Produces a file (draft, export, report) | No | README only |
| **Management skill** | Project state, config, repair | No | README only |

---

## Step 1: Create the SKILL.md

**Path**: `.claude/skills/[skill-name]/SKILL.md`

**Naming convention**:
- Eval skills: `eval-[section]` (e.g., `eval-introduction`, `eval-findings`)
- Analysis skills: verb-noun (e.g., `mine-qual`, `hunt-patterns`)
- Output skills: verb-noun (e.g., `draft-paper`, `build-lit-review`)
- Management skills: noun or verb-noun (e.g., `status`, `repair-state`)

---

### SKILL.md Template: Eval Skill

```markdown
---
name: eval-[section]
description: [One sentence: what it evaluates and why it matters]
---

# Evaluate [Section Name]

You are the [SECTION]-EVAL agent. Your job is to perform a deep structural evaluation of a paper's [section] — [what makes this section matter and what the evaluation is really testing].

## When to Run This

- **After** `/draft-paper` — to assess [section] quality before full paper eval
- **After** revising [section] — to verify improvements landed
- **Before** `/check-submission` — [why this section is a reviewer target]
- **Standalone** — when the user wants [section]-specific feedback

## Prerequisites

- A draft [section] (at minimum: the full text)
- Ideally also: [other sections or files that improve the evaluation]

## Inputs You Need

- Path to the draft paper or [section] text
- Target journal (if specified)
- [Any other inputs specific to this section]

## Evaluation Framework

Evaluate the [section] across **[N] dimensions**, each with specific criteria.

---

### Dimension 1: [Name] ([Type: Strategic/Technical/Craft/Epistemic/Holistic])

[One sentence: what this dimension is checking and why it matters.]

| Check | Pass | Fail |
|-------|------|------|
| [Check name] | [What good looks like] | [What bad looks like] |
| ... | ... | ... |

**[Named test or heuristic]**: [Memorable formulation of what this dimension is really asking.]

---

### Dimension 2: [Name] ([Type])

[Repeat pattern...]

---

### Dimension N: Failure Mode Scan

Check for named structural failure modes:

| Failure mode | Detection | Present? |
|--------------|-----------|----------|
| **[Name]** | [How to detect it] | Yes/No |
| ... | ... | ... |

---

## Scoring

Rate each dimension on a 5-point scale:

| Score | Label | Meaning |
|-------|-------|---------|
| 5 | Excellent | Would pass peer review at target journal without revision |
| 4 | Strong | Minor issues; revision is polish, not restructuring |
| 3 | Adequate | Foundation is sound but persuasion or transparency is weak |
| 2 | Weak | Significant structural or strategic problems |
| 1 | Failing | Needs fundamental rethinking |

**Overall score**: Sum of [N] dimensions / [N×5] possible points.

**Verdict thresholds**:
- **PASS** (>=[N×5 × 0.80]/[N×5]): Ready for full paper eval
- **CONDITIONAL** ([N×5 × 0.60]-[N×5 × 0.79]): Revise [section] before proceeding
- **FAIL** (<[N×5 × 0.60]): Rethink [section] strategy

> **Threshold convention**: PASS = ≥80% of max; FAIL = <60% of max. Adjust for section criticality.

## Output Format

Create `analysis/quality/[SECTION]_EVAL.md`:

[Include a markdown template showing: paper metadata header, scorecard table, detailed assessment per dimension, top 3 revision priorities, strengths]

## After You're Done

Tell the user:
- The overall score and verdict
- [2-3 section-specific highlights the user most needs to know]
- The top 3 priorities for revision
- Any failure modes detected

[Include conditional guidance: "If [section] fails on [dimension], the issue is usually... Fix by..."]

## Reference

[Cite relevant docs in theory-forge/docs/ that inform this evaluation]

---

For consensus mode behavior, see [../../_shared/consensus-mode.md](../../_shared/consensus-mode.md)
For staleness detection, see [../../_shared/staleness-check.md](../../_shared/staleness-check.md)
For eval result persistence, see [../../_shared/eval-persistence.md](../../_shared/eval-persistence.md)

### Skill-Specific Persistence

- **eval_results key**: `[section_key]`
- **Upstream files**: `analysis/manuscript/DRAFT.md` ([section] section)[, plus any other upstream files]
- **Scores**: [N] dimensions: `[dim1_key]`, `[dim2_key]`, ...
- **Verdict**: PASS >= [threshold]/[max]; FAIL < [fail_threshold]/[max]; CONDITIONAL otherwise
- **Default consensus N**: 5
```

---

### SKILL.md Template: Non-Eval Skill

```markdown
---
name: [skill-name]
description: [One sentence: what it does]
---

# [Skill Title]

You are the [SKILL-NAME] agent. [One sentence: job description and what success looks like.]

## When to Run This

- [Trigger condition 1]
- [Trigger condition 2]
- **Standalone** — [when to use directly]

## Prerequisites

- [What must exist before this skill can run]

## Inputs You Need

- [Required input 1]
- [Required input 2]
- [Optional inputs]

## [Step-by-step execution or framework]

[The skill's main logic. Use numbered steps, tables, and named heuristics as appropriate.]

## Output Format

[What file(s) this skill creates, and where. Include a template if the output format is non-obvious.]

## After You're Done

Tell the user:
- [What they most need to know about the output]
- [What to do next]

## Reference

[Relevant docs]
```

---

## Step 2: The Wiring Checklist

Every new skill must be wired into the following files. Run through this checklist completely — partial wiring creates invisible gaps.

### ✅ 2a. `check-submission/SKILL.md` — add to the test suite

For **eval skills**: add a row to the appropriate suite table.
- **Always Run (Core Suite)**: section-level evals that every paper needs
- **Contribution-Type Conditional**: evals that only apply to certain paper types
- **Workflow-State Conditional**: evals that only apply after certain skills have run (e.g., tables/figures after `/draft-paper`)

Format:
```
| [Section] | `[eval_key]` | [One-line description of what it checks] |
```

For **non-eval skills**: no addition needed unless the skill is a quality gate.

### ✅ 2b. `README.md` — add a row to the skills table

Find the appropriate skills section (Discovery, Framing, Quality Checks, Output, Project Management) and add a row:
```
| `/[skill-name]` | [What it does] |
```

For **eval skills**, also add to the Quality Checks table with the score format:
```
| `/eval-[section]` | [What it checks] | Score /[max] |
```

### ✅ 2c. `_shared/staleness-check.md` — add upstream file entry

Add a row to the "Upstream Files by Evaluation" table:
```
| eval-[section] | `analysis/manuscript/DRAFT.md` [, other upstream files] |
```

Only required for **eval skills** (and analysis skills that cache results).

### ✅ 2d. `rubrics/submission_thresholds.json` — add threshold entry

For **eval skills with numeric scores**:
```json
"[section_key]": {
  "min_score": [PASS threshold],
  "max_score": [max possible score]
}
```

Key naming: matches `eval_results key` in the SKILL.md persistence block.

---

## Step 3: Verify the Wiring

After all four files are updated:

1. Open `check-submission/SKILL.md` — does the new eval appear in the right suite?
2. Open `README.md` — does the skill appear in the right table?
3. Open `staleness-check.md` — does the upstream file entry exist?
4. Open `submission_thresholds.json` — does the JSON parse cleanly? (no trailing commas)

---

## Step 4: Commit

```bash
git add .claude/skills/[skill-name]/ \
        .claude/skills/check-submission/SKILL.md \
        README.md \
        .claude/skills/_shared/staleness-check.md \
        rubrics/submission_thresholds.json
git commit -m "Add [skill-name]: [one-line description]"
git push origin main
```

---

## Scoring Threshold Conventions

| Max score | PASS (≥80%) | CONDITIONAL (60-79%) | FAIL (<60%) |
|-----------|-------------|---------------------|-------------|
| /25 | ≥20 | 15-19 | <15 |
| /30 | ≥24 | 18-23 | <18 |
| /35 | ≥28 | 21-27 | <21 |
| /40 | ≥32 | 24-31 | <24 |
| /50 | ≥40 | 30-39 | <30 |

For critical sections (gap-defining, contribution-defining), you can raise the PASS threshold by 1-2 points. For conditional sections (e.g., tables/figures — only relevant after draft), keep standard thresholds.

---

## Common Mistakes to Avoid

- **Missing failure mode dimension**: Every eval skill should end with a Failure Mode Scan dimension that lists named anti-patterns. This is the most actionable output for revision.
- **Vague pass/fail criteria**: Each check should have a concrete observable pass state and a concrete observable fail state — not "good" vs. "bad."
- **Checks that require real readers**: Flag these explicitly as "LLM-proxy required" (see eval-introduction Dimension 5 for the pattern).
- **Over-prescriptive checks**: If a check would fail for papers that are genuinely excellent (e.g., strict single-arc requirement), add an exception note.
- **Forgetting staleness-check.md**: The most commonly missed wiring step.
