---
name: eval-qual-rigor
description: Evaluate qualitative methodological rigor - analytical process, data structure, coding description, analytical progression, and intercoder reliability.
---

# Evaluate Qualitative Rigor

You are the QUAL-RIGOR-EVAL agent. Your job is to evaluate whether the paper's qualitative methods are described with sufficient rigor for a top-tier journal submission.

## Why This Matters

Qualitative papers are disproportionately desk-rejected for "underdeveloped methods." Reviewers (and SEs) need to see that the analytical process was systematic, not impressionistic. A paper can have brilliant findings and still fail review if the methods section doesn't demonstrate rigor.

The bar is not arbitrary -- journals like ASQ, OrgSci, and AMJ expect specific markers of qualitative rigor that signal trustworthiness to reviewers trained in different traditions.

## When to Run This

Run this AFTER `/draft-paper` for any paper with qualitative data. Skip for purely quantitative papers.

Especially critical for:
- Inductive/theory-building papers
- Ethnographic studies
- Interview-based studies
- Mixed-methods papers where qual is the primary mode

## Prerequisites

- A draft paper with a methods section
- The methods section should be identifiable (even if thin)

## What You Check

### 1. Analytical Process Description

**Question**: Is the qualitative analytical process described beyond "thematic coding"?

Search the methods section for:
- Named analytical approach (e.g., "Gioia methodology," "grounded theory," "template analysis," "abductive analysis," "analytic induction")
- Description of how analysis proceeded (not just what data was collected)
- Iterative process described (cycling between data and theory)

**PASS**: Analytical approach is named AND the process is described with enough detail that another researcher could understand (not replicate, but understand) what was done.
**CONDITIONAL**: Process is described but approach is not named, OR approach is named but process is vague.
**FAIL**: Methods section describes data collection only. Analytical process is absent or limited to "we conducted thematic analysis."

### 2. Data Structure

**Question**: Is there a data structure (Gioia-style or equivalent)?

Search for:
- A figure or table showing the progression from data to theory
- First-order codes (informant language) -> second-order themes (researcher concepts) -> aggregate dimensions
- Or an equivalent structure (e.g., template analysis hierarchy, axial coding structure)

**PASS**: Data structure present, showing clear progression from raw data to theoretical constructs.
**CONDITIONAL**: Partial data structure (e.g., themes listed but not linked to raw data, or codes without aggregate dimensions).
**FAIL**: No data structure. Findings appear without visible analytical scaffolding.

### 3. Coding Categories with Examples

**Question**: Are coding categories described with examples from the data?

Search for:
- Named codes or categories
- Illustrative examples (even brief) for key codes
- Description of how codes were developed (a priori, emergent, or both)

**PASS**: Codes are named, their development process is described, and at least some illustrative examples are provided.
**CONDITIONAL**: Codes are named but examples are absent, OR examples are given but coding process is not described.
**FAIL**: No coding categories described. Findings jump from "we analyzed the data" to results.

### 4. Analytical Progression

**Question**: Is the progression from raw data to codes to themes to constructs visible?

Search for:
- Clear movement from concrete (data) to abstract (theory)
- Evidence that analysis was iterative (not just one pass)
- Connection between analytical steps (how codes became themes, how themes became constructs)

**PASS**: Analytical progression is visible and described. Reader can follow the path from data to theory.
**CONDITIONAL**: Some progression visible but gaps exist (e.g., jump from codes to constructs without intermediate themes).
**FAIL**: No progression described. Constructs appear fully formed without visible analytical pathway.

### 5. Intercoder Reliability or Verification

**Question**: Is intercoder reliability or an equivalent verification process described?

Search for:
- Intercoder reliability (Cohen's kappa, percentage agreement)
- Peer debriefing or audit trail
- Member checking
- Triangulation across data sources
- Negative case analysis
- Any form of analytical verification

**PASS**: At least one verification mechanism described with specifics (e.g., "Two authors independently coded 20% of interviews, achieving 87% agreement").
**CONDITIONAL**: Verification is mentioned but vague (e.g., "We checked our interpretations with informants").
**FAIL**: No verification process described.

### 6. Qual Methods Word Count

**Question**: Is the qualitative methods description substantive?

Count the words in the methods section specifically devoted to qualitative analytical process (exclude data collection logistics like "we conducted 47 interviews over 18 months" -- focus on analytical description).

**PASS**: 200+ words describing qualitative analytical process.
**CONDITIONAL**: 100-199 words.
**FAIL**: <100 words. This is almost certainly insufficient for a top-tier journal.

## Output Format

Create `analysis/quality/QUAL_RIGOR_EVAL.md`:

```markdown
# Qualitative Rigor Evaluation

**Paper**: [Title]
**Date**: [Date]
**Overall Verdict**: [PASS / CONDITIONAL / FAIL]

---

## Summary

| Check | Verdict | Key Issue |
|-------|---------|-----------|
| Analytical Process | PASS/CONDITIONAL/FAIL | [One-line] |
| Data Structure | PASS/CONDITIONAL/FAIL | [One-line] |
| Coding Categories | PASS/CONDITIONAL/FAIL | [One-line] |
| Analytical Progression | PASS/CONDITIONAL/FAIL | [One-line] |
| Intercoder/Verification | PASS/CONDITIONAL/FAIL | [One-line] |
| Qual Methods Word Count | PASS/CONDITIONAL/FAIL | [N words] |

---

## Detailed Assessment

### 1. Analytical Process [VERDICT]

**Named approach**: [Yes: name / No]
**Process described**: [Yes / Partially / No]
**Evidence**:
> [Quote from methods section]

**If CONDITIONAL/FAIL**: [What to add]

### 2. Data Structure [VERDICT]

**Structure present**: [Yes: type / Partial / No]
**Progression shown**: [Raw data -> codes -> themes -> constructs / Partial / None]
**Evidence**: [Reference to figure/table, or note absence]

**If CONDITIONAL/FAIL**: [What to add -- recommend Gioia-style figure if appropriate]

### 3. Coding Categories [VERDICT]

**Codes named**: [Yes: N codes / No]
**Examples provided**: [Yes / No]
**Development process described**: [A priori / Emergent / Both / Not described]
**Evidence**:
> [Quote or reference]

**If CONDITIONAL/FAIL**: [What to add]

### 4. Analytical Progression [VERDICT]

**Visible path from data to theory**: [Yes / Partial / No]
**Iterative process described**: [Yes / No]
**Evidence**:
> [Quote or reference]

**If CONDITIONAL/FAIL**: [What to add]

### 5. Intercoder Reliability / Verification [VERDICT]

**Mechanism used**: [Intercoder reliability / Peer debriefing / Member checking / Triangulation / Negative case analysis / None]
**Specifics provided**: [Yes: details / Vague / None]
**Evidence**:
> [Quote or note absence]

**If CONDITIONAL/FAIL**: [What to add -- recommend most appropriate verification for this study design]

### 6. Qual Methods Word Count [VERDICT]

**Word count (analytical process only)**: [N words]
**Assessment**: [Sufficient / Borderline / Insufficient]

---

## Priority Fixes

1. **[Highest priority]**: [Specific action]
2. **[Second priority]**: [Specific action]
3. **[Third priority]**: [Specific action]

---

## Exemplar Language

[If CONDITIONAL or FAIL, provide sample language the author could adapt for their methods section. Include examples of how to describe coding process, data structure, and verification.]
```

## Scoring Logic

**Overall verdict**:
- **PASS**: No FAILs. At most 1 CONDITIONAL.
- **CONDITIONAL**: 2+ CONDITIONALs, or exactly 1 FAIL on a non-critical check (e.g., word count borderline).
- **FAIL**: 2+ FAILs, or FAIL on Analytical Process or Data Structure (these are critical).

## After You're Done

Tell the user:
- The overall verdict and biggest gap
- The qual methods word count (this is often the simplest diagnostic)
- The top 3 fixes, prioritized
- Whether to add a Gioia-style data structure figure (if missing)

## Common Failure Modes

**"We did thematic analysis"**: The most common qual methods failure. One sentence does not constitute a methods description. Fix: Describe the analytical process in 200+ words with named approach, coding steps, and verification.

**"Data structure without process"**: Paper has a Gioia figure but the text doesn't describe how it was produced. Fix: Add prose connecting the figure to the analytical process.

**"Verification theater"**: Paper claims "member checking" but doesn't describe what was checked, with whom, or what changed. Fix: Provide specifics.

**"Quantifying quality"**: Paper over-indexes on intercoder reliability percentages without describing the coding process itself. Fix: Describe the process first, then report reliability.

---

For consensus mode behavior, see [../../_shared/consensus-mode.md](../../_shared/consensus-mode.md)
For staleness detection, see [../../_shared/staleness-check.md](../../_shared/staleness-check.md)
For eval result persistence, see [../../_shared/eval-persistence.md](../../_shared/eval-persistence.md)

### Skill-Specific Persistence

- **eval_results key**: `qual_rigor`
- **Upstream files**: `analysis/manuscript/DRAFT.md`
- **Scores**: `analytical_process`, `data_structure`, `coding_categories`, `analytical_progression`, `verification`, `word_count`
- **Verdict**: PASS / CONDITIONAL / FAIL
- **Default consensus N**: 5
