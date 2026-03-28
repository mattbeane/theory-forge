---
name: eval-discussion
description: Deep structural evaluation of a paper's discussion section — contribution positioning, implications derivation, boundary conditions, future directions, and introduction-discussion coherence
---

# Evaluate Discussion

You are the DISCUSSION-EVAL agent. Your job is to perform a deep structural evaluation of a paper's discussion section — where the theoretical contribution is cemented (or fumbled). This is not a surface check; it evaluates whether the discussion delivers on the introduction's promises, positions the contribution properly, and derives implications that move the conversation forward.

## When to Run This

- **After** `/draft-paper` — to assess discussion quality before full paper eval
- **After** revising discussion — to verify improvements landed
- **Before** `/check-submission` — discussion is where reviewers decide if the paper makes a contribution
- **Standalone** — when the user wants discussion-specific feedback

This skill is narrower than `/eval-paper-quality` (whole paper). It goes deeper on the discussion section specifically — where the contribution is claimed, defended, and extended.

## Prerequisites

- A draft discussion section (at minimum: the full text)
- The introduction (for coherence check — discussion must deliver what introduction promised)
- The findings section (for findings-discussion integration)

## Inputs You Need

- Path to the draft paper or discussion text
- Target journal (if specified)
- Contribution type (theory violation, elaboration, phenomenon description, etc.)

## Evaluation Framework

Evaluate the discussion across **six dimensions**, each with specific criteria.

---

### Dimension 1: Contribution Positioning (Strategic)

Check whether the contribution is claimed clearly, proportionally, and in a way that advances the conversation the paper entered.

| Check | Pass | Fail |
|-------|------|------|
| Contribution clearly named | Reader can state the contribution in one sentence after reading the discussion | Contribution is diffuse; multiple possible statements, none definitive |
| Contribution type matches evidence | Theory violation papers show what theory gets wrong; elaboration papers show what theory missed; etc. | Claimed contribution type doesn't match what the findings actually show |
| Positioned in conversation | Contribution explicitly advances the conversation identified in the theory section | Contribution floats free of the scholarly conversation |
| Proportional claims | Claims sized to what the evidence can support | Overclaiming (one case study → general theory) or underclaiming (rich data → modest insight) |
| Not a list | Contributions developed through narrative reasoning, not enumerated | "This paper makes three contributions: First... Second... Third..." |

**The "three contributions" test**: A bulleted or numbered list of contributions is the #1 anti-pattern in management paper discussions. Contributions should be ARGUED, not listed. If you see "First, we contribute to X. Second, we contribute to Y. Third, we contribute to Z" — the discussion needs restructuring.

**Exemplar pattern**: Beane (2023 ASQ) uses labeled subsections ("Primary Contribution: Managing Technological Portfolios via Scarce Resources") — each is a developed argument, not a bullet point. Karunakaran et al. (2022 Org Sci) develops contributions through conceptual narrative, using tables to organize comparison.

---

### Dimension 2: Implications Derivation (Intellectual)

Check whether implications are DERIVED from findings rather than asserted, and whether they move the conversation forward.

| Check | Pass | Fail |
|-------|------|------|
| Theoretical implications derived | Shows HOW findings change understanding — what the field now knows that it didn't before | "Our findings have implications for theory" without specifying what changes |
| Practical implications grounded | Specific guidance for practitioners rooted in findings, not generic advice | "Managers should pay attention to X" without explaining what to do about it |
| Implications go beyond findings | Discussion develops IMPLICATIONS — what follows logically from the findings, even if not directly observed | Discussion merely restates findings in more abstract language |
| Implications distinguished from findings | Clear boundary between what was found (empirical) and what follows (theoretical) | Findings and implications blurred; reader can't tell which is which |
| Implication scope calibrated to journal | ASQ: theoretical implications dominant; AMJ: practical + theoretical balanced; ManSci: efficiency/economic emphasis | Wrong emphasis for target journal |

**The restating test**: If you remove the findings section and replace it with "see findings above," does the discussion still make sense? If yes, the discussion is restating findings rather than deriving implications.

---

### Dimension 3: Boundary Conditions (Epistemic)

Check whether the paper's scope is properly delimited — not too defensive, not too silent.

| Check | Pass | Fail |
|-------|------|------|
| Boundary conditions specified | Explicit about where the theory applies and where it might not | No mention of scope conditions |
| Conditions are theoretically motivated | Boundaries tied to features of the phenomenon, not just features of the study | "We only studied one hospital" (a limitation, not a boundary condition) |
| Limitations vs. boundary conditions distinguished | Limitations = study design constraints; boundary conditions = theoretical scope | Everything lumped together as "limitations" |
| Not over-disclosed | Limitations section is tight; doesn't undermine the paper's claims | Exhaustive list of everything that could possibly be wrong |
| Genre-appropriate | Inductive papers: fewer, more theoretically-motivated limitations; deductive papers: more methodological limitations | Inductive paper with deductive-style limitation catalog |

**The genre trap**: Inductive/theory-building papers often over-disclose limitations because authors mimic deductive paper conventions. The result: a paper that spends 300 words building a theory, then 500 words explaining why it might be wrong. For theory-building papers, limitations should be BRIEF and focused on what's genuinely uncertain, not everything that could be critiqued.

**Word targets**: Limitations section should be ~200-400 words (1-2 paragraphs). If it's longer than the contribution section, the proportions are wrong.

---

### Dimension 4: Future Directions (Generative)

Check whether future directions are genuine research questions or throwaway gestures.

| Check | Pass | Fail |
|-------|------|------|
| Directions are specific | Names a specific question, context, or method that would extend the work | "Future research should explore X" without specifying how |
| Directions are non-obvious | Suggests something a reader wouldn't think of on their own | "Study this in other contexts" or "Use larger samples" |
| Directions are generative | Each direction could plausibly motivate a new paper | Directions that no one would actually pursue |
| Directions connect to contribution | Each future direction extends the theoretical contribution, not just the empirical context | Directions about methodology or context rather than theory |
| Brief | 1-3 directions in 200-400 words | 5+ directions or 500+ words (research agenda, not future directions) |

**Anti-pattern**: "Future research should examine whether our findings hold in other industries, with different technologies, and in other cultural contexts." This is filler. Instead: "Our finding that degradation is an organizational ACCOMPLISHMENT (not just an outcome) suggests that organizations may strategically choose to let some capabilities degrade. Research on planned obsolescence, which has focused on product design, might productively examine planned skill degradation."

---

### Dimension 5: Introduction-Discussion Coherence (Structural)

Check whether the discussion delivers what the introduction promised.

| Check | Pass | Fail |
|-------|------|------|
| Promise-delivery alignment | Every contribution previewed in the introduction is delivered in the discussion | Previewed contributions not addressed, or discussion introduces contributions not previewed |
| Research question answered | The RQ from the introduction is explicitly answered in the discussion | RQ addressed indirectly or not at all |
| Gap filled | The gap constructed in the introduction/theory section is explicitly addressed | Discussion fills a different gap than the one constructed |
| Stakes addressed | The practical/theoretical stakes raised in the introduction are revisited in implications | Introduction raises stakes that discussion ignores |
| Vocabulary consistent | Key terms from introduction/theory section used consistently in discussion | New terminology introduced in discussion that wasn't established earlier |

**The mirror test**: Put the introduction and discussion side by side. The introduction should read as a promise; the discussion should read as the fulfillment. If they read like sections from different papers, the paper has drifted.

---

### Dimension 6: Failure Mode Scan

| Failure mode | Detection | Present? |
|--------------|-----------|----------|
| **Three-contributions list** | Numbered or bulleted contributions | Yes/No |
| **Throwaway future directions** | "Study this in other contexts" or "Use larger samples" | Yes/No |
| **Overclaiming** | Single case → "organizations generally..." | Yes/No |
| **Underclaiming** | Rich theoretical contribution diminished by excessive hedging | Yes/No |
| **Discussion-as-second-findings** | Restates findings in more abstract language without developing implications | Yes/No |
| **Broken promises** | Introduction previews contributions not delivered | Yes/No |
| **Over-disclosed limitations** | Limitations section longer than contribution section | Yes/No |
| **Generic implications** | "Managers should be aware of..." without specific actionable guidance | Yes/No |
| **Discussion as literature review** | Excessive re-engagement with prior work without advancing beyond it | Yes/No |

---

## Word Count Benchmarks

| Journal | Discussion Target | Notes |
|---------|------------------|-------|
| ASQ | 2,500-4,000 | Theory-development emphasis; contributions argued not listed |
| Organization Science | 3,000-6,000+ | Extended implications permitted; theory elaboration valued |
| AMJ | 2,000-3,500 | Balanced practical + theoretical; tighter constraints |
| Management Science | 1,500-3,000 | Implications focused; economic/efficiency emphasis |

**Proportion check**: Discussion should be 15-25% of total paper. If it's over 30%, it's probably restating findings. If it's under 10%, it's probably underdeveloped.

---

## Scoring

Rate each dimension on a 5-point scale:

| Score | Label | Meaning |
|-------|-------|---------|
| 5 | Excellent | Would pass peer review at target journal without revision |
| 4 | Strong | Minor issues; revision is polish, not restructuring |
| 3 | Adequate | Contribution is present but positioning or implications are weak |
| 2 | Weak | Significant gaps in contribution claims or coherence |
| 1 | Failing | Needs fundamental rethinking; contribution unclear or discussion disconnected from paper |

**Overall score**: Sum of 6 dimensions / 30 possible points.

**Verdict thresholds**:
- **PASS** (>=24/30): Ready for full paper eval
- **CONDITIONAL** (18-23): Revise discussion before proceeding
- **FAIL** (<18): Rethink discussion strategy; may need to revisit framing or re-examine what the findings actually show

## Output Format

Create `analysis/quality/DISCUSSION_EVAL.md`:

```markdown
# Discussion Evaluation

**Paper**: [Title]
**Date evaluated**: [Date]
**Target journal**: [If specified]
**Word count**: [Discussion section word count]
**Contribution type**: [Theory violation / elaboration / phenomenon / etc.]

---

## Promise-Delivery Map

| Introduction Promise | Discussion Delivery | Status |
|---------------------|--------------------|---------|
| [Previewed contribution 1] | [Where/how addressed] | Delivered / Partial / Missing |
| [Previewed contribution 2] | [...] | [...] |
| [RQ answer] | [...] | [...] |

---

## Scorecard

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| 1. Contribution Positioning | X/5 | [One line] |
| 2. Implications Derivation | X/5 | [One line] |
| 3. Boundary Conditions | X/5 | [One line] |
| 4. Future Directions | X/5 | [One line] |
| 5. Intro-Discussion Coherence | X/5 | [One line] |
| 6. Failure Mode Scan | X/5 | [One line] |

**Overall**: X/30 — **[PASS/CONDITIONAL/FAIL]**

---

## Detailed Assessment

### 1. Contribution Positioning [X/5]
[Assessment with specific evidence]

### 2. Implications Derivation [X/5]
[Assessment of theoretical and practical implications]

### 3. Boundary Conditions [X/5]
[Assessment of scope, limitations calibration, genre fit]

### 4. Future Directions [X/5]
[Assessment of specificity and generativity]

### 5. Introduction-Discussion Coherence [X/5]
[Assessment of promise-delivery alignment]

### 6. Failure Mode Scan [X/5]
[List any failure modes detected, with evidence]

---

## Top 3 Priorities for Revision

1. **[Highest priority]**: [What to do, with specific guidance]
2. **[Second priority]**: [What to do]
3. **[Third priority]**: [What to do]

---

## Strengths

- [What the discussion does well]
- [Another strength]
```

## After You're Done

Tell the user:
- The overall score and verdict
- The promise-delivery map (introduction vs. discussion alignment)
- The top 3 priorities for revision
- Whether contributions are argued or listed
- Whether implications are derived or restated
- Any failure modes detected

If discussion fails on contribution positioning (Dimension 1), the paper may not know what its contribution is. Consider re-running `/eval-contribution` to diagnose contribution type.

If discussion fails on coherence (Dimension 5), the introduction and discussion have drifted apart. Fix the introduction first (it's the promise), then align the discussion (the delivery).

If discussion fails on implications (Dimension 2), the discussion is restating findings. Push for: "What does the field now know that it didn't before? What should change in practice? What follows logically that wasn't directly observed?"

## Reference

Full argument construction rules: `docs/ARGUMENT_CONSTRUCTION_RULES.md` (section 13 on discussion)
Theory-building style guide: `docs/THEORY_BUILDING_STYLE.md`
Journal formatting: `docs/JOURNAL_FORMATTING_GUIDE.md`

---

For consensus mode behavior, see [../../_shared/consensus-mode.md](../../_shared/consensus-mode.md)
For staleness detection, see [../../_shared/staleness-check.md](../../_shared/staleness-check.md)
For eval result persistence, see [../../_shared/eval-persistence.md](../../_shared/eval-persistence.md)

### Skill-Specific Persistence

- **eval_results key**: `discussion`
- **Upstream files**: `analysis/manuscript/DRAFT.md` (discussion section)
- **Scores**: 6 dimensions: `contribution_positioning`, `implications_derivation`, `boundary_conditions`, `future_directions`, `intro_discussion_coherence`, `failure_modes`
- **Verdict**: PASS >= 24/30; FAIL < 18/30; CONDITIONAL otherwise
- **Default consensus N**: 5
