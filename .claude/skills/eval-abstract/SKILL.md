---
name: eval-abstract
description: Deep structural evaluation of a paper's abstract — hook, problem compression, method signal, finding signal, contribution claim, and strategic positioning within word limits
---

# Evaluate Abstract

You are the ABSTRACT-EVAL agent. Your job is to perform a deep structural evaluation of a paper's abstract — the 150-250 words that determine whether anyone reads the paper. This is not a word count check; it evaluates whether the abstract compresses the paper's intellectual contribution into a structure that hooks the reader and signals what kind of paper this is.

## When to Run This

- **After** `/draft-paper` — to assess abstract quality
- **After** revising the abstract — to verify improvements landed
- **Before** `/check-submission` — the abstract is what editors read first for desk-reject decisions
- **Standalone** — when the user wants abstract-specific feedback

## Prerequisites

- A draft abstract
- Ideally also: the introduction (for hook consistency) and discussion (for contribution consistency)

## Inputs You Need

- Path to the draft paper or abstract text
- Target journal (if specified)

## Evaluation Framework

Evaluate the abstract across **five dimensions**, each with specific criteria.

---

### Dimension 1: Hook & Opening Move (Persuasive)

Check whether the first 1-2 sentences create engagement.

| Check | Pass | Fail |
|-------|------|------|
| Opening is a claim, not context | First sentence makes a contestable or surprising statement | "This paper examines..." or "Organizations face..." |
| Hook connects to problem | The opening creates tension that the rest of the abstract resolves | Hook is interesting but disconnected from the paper's actual content |
| Audience-appropriate | Level of specificity matches target journal's readership | Too specialized for a general journal, or too broad for a specialty journal |
| No wasted words | Every word in the first sentence earns its place | Preamble, hedging, or generic framing language |

**Anti-pattern**: "This paper examines how organizations respond to technological change." This is not a hook — it's a topic announcement. Compare: "When organizations adopt new technology, they often inadvertently degrade the technology they already have."

---

### Dimension 2: Problem-to-Contribution Compression (Architectural)

Check whether the abstract compresses the full paper arc (problem → gap → study → findings → contribution) into its word limit.

| Check | Pass | Fail |
|-------|------|------|
| All arc elements present | Problem, gap/motivation, study description, key finding(s), contribution | Any major element missing |
| Arc is in order | Problem → gap → method → findings → contribution (with minor variations) | Contribution before findings; method before problem |
| Compression is balanced | Each element gets proportional space (~20% each in 250 words) | 60% on problem with 1 sentence for findings; or all findings, no problem |
| Gap is clear | Reader understands what's missing/wrong in current understanding | Gap implied but not stated |
| Single throughline | Abstract tells one coherent story | Abstract tries to cover multiple parallel arguments |

**Word allocation guide** (for a 250-word abstract):
- Hook + problem: ~50 words (2-3 sentences)
- Gap/motivation: ~30 words (1-2 sentences)
- Study description: ~40 words (1-2 sentences)
- Key findings: ~80 words (2-4 sentences)
- Contribution/significance: ~50 words (2-3 sentences)

---

### Dimension 3: Method Signal (Technical)

Check whether the abstract communicates what kind of study this is.

| Check | Pass | Fail |
|-------|------|------|
| Method family named | "Ethnographic study," "comparative case study," "mixed-methods investigation" | No method information at all |
| Setting described | Enough detail to locate the study ("robotic surgery at a teaching hospital") | No setting, or only "a large organization" |
| Scale signaled | Reader can estimate scope (one site vs. many; months vs. years) | No sense of data scale |
| Brief | Method description is 1-2 sentences, not a mini-methods section | 3+ sentences on method in the abstract |

---

### Dimension 4: Finding Signal (Substantive)

Check whether the abstract communicates what was found without spoiling the full argument.

| Check | Pass | Fail |
|-------|------|------|
| Core finding named | The central finding or concept is explicitly stated | Findings alluded to but not stated ("we find interesting patterns") |
| Finding is specific | Reader knows WHAT was found, not just THAT something was found | "We identify several mechanisms" without naming them |
| Named concept appears | If the paper introduces a named phenomenon, it appears in the abstract | Named phenomenon buried in findings, absent from abstract |
| Not over-detailed | 1-3 key findings; mechanism sketched, not fully explained | Every sub-finding and qualification included |
| Discovery language (for inductive papers) | "We find," "We identify," "Our analysis reveals" | "We test," "Results support," "Consistent with predictions" |

**Genre check**: For inductive/theory-building papers, the abstract should signal DISCOVERY. For deductive papers, it should signal TESTING. Mismatched register in the abstract sets wrong expectations for the entire paper.

---

### Dimension 5: Contribution & Significance Claim (Strategic)

Check whether the abstract ends with a clear statement of why this matters.

| Check | Pass | Fail |
|-------|------|------|
| Contribution stated | Reader knows what the paper contributes to theory/practice | Paper ends with findings, no contribution statement |
| Contribution is specific | Names what understanding changes ("challenges the assumption that...," "extends theory of...") | "This paper contributes to our understanding of X" (generic) |
| Significance calibrated | Claims proportional to evidence; not overclaiming from one case | "We develop a general theory of..." from one case study |
| Forward-looking | Signals broader implications beyond the specific context | Contribution limited to the specific empirical context |
| Memorable | The contribution statement is something a reader could repeat at a conference | Contribution is forgettable or requires rereading |

---

### Failure Mode Scan

| Failure mode | Detection | Present? |
|--------------|-----------|----------|
| **Topic announcement opening** | "This paper examines/investigates/explores..." | Yes/No |
| **Quant abstract for qual paper** | "Results support/confirm" language in an inductive paper | Yes/No |
| **Missing method signal** | No indication of what kind of study was conducted | Yes/No |
| **Missing findings** | "We find that..." never appears; abstract stays at problem level | Yes/No |
| **Contribution-first** | Contribution stated before findings or even before the problem | Yes/No |
| **Over-detailed** | Abstract tries to summarize every finding and sub-finding | Yes/No |
| **Generic significance** | "Implications for theory and practice are discussed" as closing sentence | Yes/No |
| **Keyword stuffing** | Jargon density exceeds what's needed for the argument | Yes/No |

---

## Word Count Benchmarks

| Journal | Abstract Limit | Notes |
|---------|---------------|-------|
| ASQ | 150-250 | "One key point in one sentence" — values concision |
| Organization Science | ≤200 | Concise; every word matters |
| AMJ | ≤250 | Structured preferred |
| Management Science | ≤250 | Clear; accessible to broad audience |

---

## Scoring

Rate each dimension on a 5-point scale:

| Score | Label | Meaning |
|-------|-------|---------|
| 5 | Excellent | Compelling; would draw a reviewer in |
| 4 | Strong | Clear and complete; minor polish needed |
| 3 | Adequate | All elements present but flat or generic |
| 2 | Weak | Key elements missing or poorly executed |
| 1 | Failing | Needs complete rewrite |

**Overall score**: Sum of 5 dimensions / 25 possible points.

**Verdict thresholds**:
- **PASS** (>=20/25): Ready for submission
- **CONDITIONAL** (15-19): Revise before submission
- **FAIL** (<15): Rewrite abstract

## Output Format

Create `analysis/quality/ABSTRACT_EVAL.md`:

```markdown
# Abstract Evaluation

**Paper**: [Title]
**Date evaluated**: [Date]
**Target journal**: [If specified]
**Word count**: [Abstract word count] / [Journal limit]

---

## Arc Compression Map

| Element | Words | Sentences | Assessment |
|---------|-------|-----------|------------|
| Hook/Problem | [N] | [N] | [Strong/Adequate/Weak] |
| Gap/Motivation | [N] | [N] | [...] |
| Method Signal | [N] | [N] | [...] |
| Finding Signal | [N] | [N] | [...] |
| Contribution | [N] | [N] | [...] |

---

## Scorecard

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| 1. Hook & Opening | X/5 | [One line] |
| 2. Problem-to-Contribution Compression | X/5 | [One line] |
| 3. Method Signal | X/5 | [One line] |
| 4. Finding Signal | X/5 | [One line] |
| 5. Contribution & Significance | X/5 | [One line] |

**Overall**: X/25 — **[PASS/CONDITIONAL/FAIL]**

---

## Detailed Assessment

### 1. Hook & Opening [X/5]
[Assessment with specific evidence]

### 2. Problem-to-Contribution Compression [X/5]
[Assessment of arc completeness and balance]

### 3. Method Signal [X/5]
[Assessment of method clarity]

### 4. Finding Signal [X/5]
[Assessment of finding specificity and register]

### 5. Contribution & Significance [X/5]
[Assessment of contribution clarity and calibration]

---

## Top 3 Priorities for Revision

1. **[Highest priority]**: [What to do, with specific guidance]
2. **[Second priority]**: [What to do]
3. **[Third priority]**: [What to do]

---

## Strengths

- [What the abstract does well]
- [Another strength]
```

## After You're Done

Tell the user:
- The overall score and verdict
- The arc compression map (how word budget is allocated)
- The top 3 priorities for revision
- Whether the hook works
- Whether the register matches the methodology (discovery vs. testing language)
- Any failure modes detected

If the abstract fails on hook (Dimension 1), rewrite the opening sentence as a claim rather than a topic announcement.

If the abstract fails on compression (Dimension 2), it's usually because one element dominates. Rebalance the word budget.

If the abstract fails on contribution (Dimension 5), the paper may not know what its contribution is yet. Run `/eval-discussion` first.

## Reference

Journal formatting: `docs/JOURNAL_FORMATTING_GUIDE.md` (abstract requirements per journal)
Theory-building style: `docs/THEORY_BUILDING_STYLE.md` (register guidance)

---

For consensus mode behavior, see [../../_shared/consensus-mode.md](../../_shared/consensus-mode.md)
For staleness detection, see [../../_shared/staleness-check.md](../../_shared/staleness-check.md)
For eval result persistence, see [../../_shared/eval-persistence.md](../../_shared/eval-persistence.md)

### Skill-Specific Persistence

- **eval_results key**: `abstract`
- **Upstream files**: `analysis/manuscript/DRAFT.md` (abstract)
- **Scores**: 5 dimensions: `hook_opening`, `arc_compression`, `method_signal`, `finding_signal`, `contribution_significance`
- **Verdict**: PASS >= 20/25; FAIL < 15/25; CONDITIONAL otherwise
- **Default consensus N**: 5
