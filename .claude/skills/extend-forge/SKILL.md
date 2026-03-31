---
name: extend-forge
description: Add a new capability to theory-forge — triggered when a gap in the pipeline is discovered mid-research. Handles the full build-and-wire workflow, then returns you to research.
---

# Extend Theory-Forge

You are the FORGE-ENGINEER agent. Your job is to systematically extend theory-forge by building a new skill from scratch and wiring it into the pipeline correctly — so nothing is left half-connected.

This skill exists because building new capabilities should be a named, confirmable workflow, not an ad-hoc detour. When you discover mid-research that the forge is missing something, you pause, build it right, and return.

## When to Run This

- You've discovered a gap in theory-forge mid-research (missing eval, missing analysis tool, missing output format)
- You want to encode a new methodological tradition or evaluation framework
- You're adding a project-specific capability that should persist across sessions
- A previous `/create-agent` was too lightweight and you want to formalize it

**This is a framework development moment — not a research moment.** The skill puts research on hold, extends the forge, commits the new capability, then hands control back.

## Mode Confirmation (MANDATORY)

Before doing anything, state clearly:

> "This is a forge-extension session. I'll build `/[skill-name]` and wire it into check-submission, README, staleness-check, and submission_thresholds.json, then commit to main. **Confirm to proceed.**"

Wait for explicit confirmation. Do not begin building until confirmed.

If the user hasn't specified a skill name, gather enough information to name it first (see Step 1).

---

## Step 1: Define the Capability

Ask (or infer from context) the following. Most of these can be answered from the conversation that prompted this skill:

| Question | Why it matters |
|----------|---------------|
| What capability is missing? | Defines scope |
| What prompted the discovery? | Usually reveals the exact gap |
| Where does it fit in the pipeline? | Determines skill type and check-submission placement |
| What section/property/output does it address? | Determines naming and upstream files |
| Is this eval, analysis, output, or management? | Determines wiring scope |
| What would PASS look like? | Seeds the scoring framework |
| What are the 3 most common ways this goes wrong? | Seeds the failure mode scan |

**Skill type classification:**

| Type | Description | Examples |
|------|-------------|---------|
| **Eval skill** | Scores a section or property with a dimensional rubric | `eval-introduction`, `eval-findings` |
| **Analysis skill** | Extracts, synthesizes, or tests something | `mine-qual`, `hunt-patterns`, `test-counter-evidence` |
| **Output skill** | Produces a deliverable file | `draft-paper`, `build-lit-review` |
| **Management skill** | Project state, configuration, repair | `status`, `repair-state` |

---

## Step 2: Scaffold the SKILL.md

Load and follow: [`../../_shared/skill-authoring-pattern.md`](../../_shared/skill-authoring-pattern.md)

Use the appropriate template (eval vs. non-eval). Write the full SKILL.md — don't stub it. A half-written skill is worse than no skill because it gives false confidence.

**For eval skills specifically:**

1. Start by naming the dimensions. Aim for 5-7. Each dimension should be independently scorable and address a distinct failure mode.
2. Write the failure mode scan last — it should name the anti-patterns you've already implicitly described in the dimensional checks.
3. Set thresholds using the convention table in skill-authoring-pattern.md. When in doubt, use PASS ≥ 80% of max.
4. Write the output file template — the eval is only useful if the output is structured consistently.

**Quality bar**: The SKILL.md should be good enough that someone who has never seen this section before could run the eval and get a reliable, actionable result. If you're being vague, you're not done.

---

## Step 3: Run the Wiring Checklist

Work through all four wiring targets in order. Don't skip any.

### 3a. `check-submission/SKILL.md`

Determine the right suite:
- **Core Suite** if this eval applies to every paper after `/draft-paper`
- **Contribution-Type Conditional** if it only applies to certain paper types
- **Workflow-State Conditional** if it only makes sense after a specific earlier skill

Add the row. Verify the table still renders correctly.

### 3b. `README.md`

Add to the appropriate skills table section. For eval skills, also add to the Quality Checks table with score format (`Score /[max]`).

### 3c. `_shared/staleness-check.md`

Add upstream file entry. For manuscript-section evals, upstream is always `analysis/manuscript/DRAFT.md`. For framing evals, also add `analysis/framing/frame-{N}/FRAMING_OPTIONS.md`.

### 3d. `rubrics/submission_thresholds.json`

Add the threshold entry. Confirm the JSON parses cleanly (no trailing commas on last entry).

---

## Step 4: Verify

Before committing, spot-check:

1. Read back the new SKILL.md — does it make sense to someone encountering it cold?
2. Open `check-submission/SKILL.md` — is the new skill in the right suite?
3. Open `staleness-check.md` — is the upstream file correct?
4. Run `python3 -c "import json; json.load(open('rubrics/submission_thresholds.json'))"` — does JSON parse?
5. Check `README.md` — does the new row appear in the right table?

---

## Step 5: Commit and Push

Stage all affected files specifically (don't `git add .`):

```bash
git add .claude/skills/[skill-name]/ \
        .claude/skills/check-submission/SKILL.md \
        README.md \
        .claude/skills/_shared/staleness-check.md \
        rubrics/submission_thresholds.json
git commit -m "Add [skill-name]: [one-line description of what it does]"
git push origin main
```

---

## Step 6: Return to Research

Tell the user:

> "Done. `/[skill-name]` is live and wired. Here's what was built: [2-3 sentence summary of what the skill does, its scoring, and where it sits in the pipeline]. You can run it now with `/[skill-name]` or continue with what you were doing."

If the user was mid-research when they triggered this skill, briefly recall where they were:
> "You were working on [X] — want to continue there?"

---

## After You're Done

Confirm explicitly:
- New skill path (`.claude/skills/[name]/SKILL.md`)
- Score range and PASS threshold (if eval)
- Which check-submission suite it's in
- Commit hash and push status

---

## Reference

Skill authoring pattern: [`../../_shared/skill-authoring-pattern.md`](../../_shared/skill-authoring-pattern.md)
DAAF framework-engineer pattern: inspiration for this skill
Existing eval skills as examples: `eval-introduction`, `eval-findings`, `eval-methods`
