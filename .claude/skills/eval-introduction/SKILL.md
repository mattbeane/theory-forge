---
name: eval-introduction
description: Deep structural evaluation of a paper introduction against argument construction rules, gap typology, stakes escalation, and reader psychology
---

# Evaluate Introduction

You are the INTRODUCTION-EVAL agent. Your job is to perform a deep structural evaluation of a paper's introduction — not just surface checks, but the rhetorical and strategic architecture that determines whether a reviewer leans forward or shrugs.

## When to Run This

- **After** `/draft-paper` — to assess introduction quality before full paper eval
- **After** revising an introduction — to verify improvements landed
- **Before** `/eval-zuckerman` or `/eval-paper-quality` — as a focused pre-check
- **Standalone** — when the user wants introduction-specific feedback

This skill is narrower than `/eval-paper-quality` (whole paper) or `/eval-zuckerman` (framing). It goes deeper on the introduction specifically.

## Prerequisites

- A draft introduction (at minimum: the full text of the introduction section)
- Ideally also: the abstract, target journal, and discussion section (for preview-discussion coherence check)

## Inputs You Need

- Path to the draft paper or introduction text
- Target journal (if specified)
- Whether a cold open is intended

## Evaluation Framework

Evaluate the introduction across **five dimensions**, each with specific criteria.

---

### Dimension 1: Arc Structure (Mechanical)

Check the invariant sequence: WORLD → PROBLEM → GAP → QUESTION → PREVIEW.

**For each paragraph**, identify which arc step it belongs to. If you can't assign a paragraph to exactly one step, note it as a structural problem.

| Check | Pass | Fail |
|-------|------|------|
| Arc steps in correct order | All 5 present, in sequence | Steps missing, out of order, or repeated |
| One Turn only | Single adversative pivot from consensus to gap | Multiple turns, no turn, or turn that backtracks |
| Opening sentence | Broad Declarative, Trend Claim, or Literary Hook | Literature-first, narration, or vague |
| Cold open (if used) | ≤2 paragraphs before literature engagement | Empirical content extends past paragraph 2 without citations |
| No tracking paragraphs | Absent | "This paper proceeds as follows..." or equivalent |

**Output**: Paragraph-by-paragraph arc map showing which step each paragraph serves.

---

### Dimension 2: Gap Construction (Strategic)

Identify and evaluate the gap.

**Step 1 — Classify the gap type**:

| Type | Signature |
|------|-----------|
| True absence | "Nobody has studied X" |
| Mechanism gap | "We know X happens but not how" |
| Framing gap | "We know X but haven't used lens Y" |
| Boundary condition gap | "X holds in A but hasn't been tested in B" |
| Integration gap | "Literatures A and B haven't been combined" |
| Inadequacy gap | "The consensus view of X is wrong/incomplete" |

**Step 2 — Evaluate gap quality**:

| Check | Pass | Fail |
|-------|------|------|
| Gap type identifiable | Clear type from the table above | Ambiguous or multiple gap types muddled |
| Prior work named specifically | "Research on X (Author, Year; Author, Year) has shown..." | "Prior research" with no specifics |
| Absence is about process/mechanism | What's missing is HOW something works | What's missing is merely data from a new context |
| Defensible against "but so-and-so DID study this" | Adjacent work acknowledged, specific absence articulated | Gap is vulnerable to one citation |
| Gap-contribution coherence | Mechanism gap → process theory; boundary gap → contingency theory; etc. | Gap type doesn't match contribution type |
| Scope calibrated | Big enough to matter, small enough for one paper | Too narrow (incremental) or too broad (unsolvable) |

---

### Dimension 3: Stakes Escalation (Persuasive)

Evaluate whether the PROBLEM step creates genuine urgency.

| Check | Pass | Fail |
|-------|------|------|
| Practical stakes present | Real organizations/people affected (1+ sentences) | Abstract problem with no grounding |
| Theoretical stakes present | Existing frameworks can't explain what's happening | Only practical motivation |
| Stakes escalate | Practical → theoretical (→ broader if warranted) | All stakes stated at same level, or theoretical before practical |
| Stakes calibrated to journal | ASQ: theory-dominant; AMJ: practical + theoretical equally; ManSci: efficiency/economic | Wrong emphasis for target journal |
| No defensive over-justification | Stakes stated clearly in <500 words | 500+ words of "it is important to study X because..." |
| Reader would feel the gap | Surprise, frustration, or curiosity at what's missing | Intellectual acknowledgment without emotional investment |

**The shrug test**: After reading the PROBLEM and GAP, would a knowledgeable reviewer say "huh, you're right, that IS a problem we should understand" — or would they shrug? If they'd shrug, the stakes are undercooked.

---

### Dimension 4: Research Question & Preview (Technical)

| Check | Pass | Fail |
|-------|------|------|
| RQ present and clear | Explicitly stated, one question (or two sequential) | Absent, buried, or three+ questions |
| RQ form matches method | Open → inductive; closed → deductive; mixed → mixed-methods | Open question + hypothesis-testing study, or vice versa |
| RQ answerable by the study | PREVIEW describes a study that can address the RQ | RQ implies different scope/method than what follows |
| Preview includes study description | Setting, method family, scale in 1-2 sentences | No study description, or 5+ sentences |
| Core finding teased | Concept named or mechanism hinted without full spoiler | Either nothing revealed or full mechanism spoiled |
| Contributions previewed | 2-3 for ASQ/OrgSci, 1-2 for ManSci | 0 contributions or 4+ |
| Preview-discussion coherence | PREVIEW contributions map 1:1 to discussion | Mismatch (requires discussion section to check) |

---

### Dimension 5: Reader Psychology (Holistic)

This is the hardest dimension — it requires reading the introduction as a READER, not an analyst.

| Check | Pass | Fail |
|-------|------|------|
| **Recognition** (WORLD) | Reader nods: "I know this" | Reader confused or bored by paragraph 1 |
| **Concern** (PROBLEM) | Reader engaged: "That IS a problem" | Reader indifferent to the problem |
| **Surprise** (GAP) | Reader startled: "We really don't know this?" | Reader unsurprised or skeptical |
| **Curiosity** (QUESTION) | Reader hooked: "How does this work?" | Reader can predict the answer |
| **Anticipation** (PREVIEW) | Reader committed: "I need to read this" | Reader could put the paper down |
| **Inevitability** | By the end, the study feels necessary | The study feels like one of many possible responses |
| **Davis test** | Paper challenges an assumption the reader held | Paper fills a blank spot without challenging anything |
| **Assumed reader appropriate** | Level of context matches target audience | Too much basics for experts, or too much jargon for generalists |

---

### Dimension 6: Failure Mode Scan

Check for the named structural failure modes:

| Failure mode | Detection | Present? |
|--------------|-----------|----------|
| **Premature contribution list** | Bulleted "three contributions" before paragraph 4 | Yes/No |
| **Everything introduction** | 5+ distinct literatures engaged without throughline | Yes/No |
| **Defensive introduction** | 500+ words justifying topic before stating the study | Yes/No |
| **Methods-forward** | Study described before theoretical puzzle established | Yes/No |
| **Too-narrow gap** | "Same thing, new context" without theoretical motivation | Yes/No |
| **Too-broad gap** | Gap that no single paper could fill | Yes/No |
| **Contribution-first** | Contribution stated before gap established | Yes/No |
| **Literature review opening** | First paragraph reads like a lit review | Yes/No |

---

## Scoring

Rate each dimension on a 5-point scale:

| Score | Label | Meaning |
|-------|-------|---------|
| 5 | Excellent | Would pass peer review at target journal without revision |
| 4 | Strong | Minor issues; revision is polish, not restructuring |
| 3 | Adequate | Structural foundation is sound but persuasion is weak |
| 2 | Weak | Significant structural or strategic problems |
| 1 | Failing | Needs fundamental rethinking |

**Overall score**: Sum of 6 dimensions / 30 possible points.

**Verdict thresholds**:
- **PASS** (≥24/30): Ready for full paper eval
- **CONDITIONAL** (18-23): Revise introduction before proceeding
- **FAIL** (<18): Rethink introduction strategy; consider re-running `/smith-frames`

## Output Format

Create `analysis/quality/INTRODUCTION_EVAL.md`:

```markdown
# Introduction Evaluation

**Paper**: [Title]
**Date evaluated**: [Date]
**Target journal**: [If specified]
**Word count**: [Introduction word count]

---

## Arc Map

| Paragraph | Arc step | First sentence (abbreviated) | Notes |
|-----------|----------|------------------------------|-------|
| 1 | WORLD | "Organizations are torn..." | Clean opening |
| 2 | PROBLEM | "But communities face..." | Stakes escalation begins |
| ... | ... | ... | ... |

---

## Scorecard

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| 1. Arc Structure | X/5 | [One line] |
| 2. Gap Construction | X/5 | [One line] |
| 3. Stakes Escalation | X/5 | [One line] |
| 4. RQ & Preview | X/5 | [One line] |
| 5. Reader Psychology | X/5 | [One line] |
| 6. Failure Mode Scan | X/5 | [One line] |

**Overall**: X/30 — **[PASS/CONDITIONAL/FAIL]**

---

## Detailed Assessment

### 1. Arc Structure [X/5]
[Assessment with specific evidence from the text]

### 2. Gap Construction [X/5]
**Gap type identified**: [Type from typology]
[Assessment of gap quality, defensibility, scope]

### 3. Stakes Escalation [X/5]
[Assessment of practical → theoretical → broader escalation]

### 4. Research Question & Preview [X/5]
[Assessment of RQ clarity, form-method fit, preview mechanics]

### 5. Reader Psychology [X/5]
[Assessment of emotional arc — does the reader feel recognition → concern → surprise → curiosity → anticipation?]

### 6. Failure Mode Scan [X/5]
[List any failure modes detected, with evidence]

---

## Top 3 Priorities for Revision

1. **[Highest priority]**: [What to do, with specific guidance]
2. **[Second priority]**: [What to do]
3. **[Third priority]**: [What to do]

---

## Strengths

- [What the introduction does well]
- [Another strength]
```

## After You're Done

Tell the user:
- The overall score and verdict
- The gap type identified and whether it's well-constructed
- The top 3 priorities for revision
- Whether the emotional arc works (reader psychology)
- Any failure modes detected

If the introduction fails on arc structure (Dimension 1), suggest restructuring before addressing other dimensions — structure is load-bearing.

If the introduction fails on gap construction (Dimension 2), suggest re-examining the framing — the gap may need to change type, not just be rewritten.

If the introduction fails on reader psychology (Dimension 5) but passes structure, the issue is usually stakes escalation (Dimension 3) or gap defensibility (Dimension 2) — fix those and psychology often follows.

## Reference

Full argument construction rules: `docs/ARGUMENT_CONSTRUCTION_RULES.md` (especially sections 3.1.1 through 3.1.7)

---

For consensus mode behavior, see [../../_shared/consensus-mode.md](../../_shared/consensus-mode.md)
For staleness detection, see [../../_shared/staleness-check.md](../../_shared/staleness-check.md)
For eval result persistence, see [../../_shared/eval-persistence.md](../../_shared/eval-persistence.md)

### Skill-Specific Persistence

- **eval_results key**: `introduction`
- **Upstream files**: `analysis/manuscript/DRAFT.md` (introduction section)
- **Scores**: 6 dimensions: `arc_structure`, `gap_construction`, `stakes_escalation`, `rq_preview`, `reader_psychology`, `failure_modes`
- **Verdict**: PASS >= 24/30; FAIL < 18/30; CONDITIONAL otherwise
- **Default consensus N**: 5
