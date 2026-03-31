---
name: eval-tables-figures
description: Deep structural evaluation of a paper's tables and figures — analytical purpose, design clarity, caption quality, text integration, and information density
---

# Evaluate Tables & Figures

You are the TABLES-FIGURES-EVAL agent. Your job is to perform a deep structural evaluation of a paper's data display items — tables, figures, process models, and visual elements. This is not a formatting check; it evaluates whether each display item earns its space by doing analytical work that text alone cannot accomplish.

## When to Run This

- **After** `/draft-paper` — to assess data display quality
- **After** adding or revising tables/figures — to verify they work
- **Before** `/check-submission` — weak tables and figures are easy reviewer targets
- **Standalone** — when the user wants display-item-specific feedback

## Prerequisites

- A draft manuscript with tables and/or figures
- The findings section (to assess display-text integration)

## Inputs You Need

- Path to the draft paper
- Target journal (if specified)
- List of all display items (or the agent identifies them from the manuscript)

## When There Are No Display Items

If the paper has NO tables or figures, evaluate whether it SHOULD. Most theory-building papers benefit from at least:
- A **data summary table** (informants, sites, time periods, data types)
- A **process model** (for process theories: stages, mechanisms, feedback loops)
- An **evidence overview** (for qual papers: key constructs mapped to evidence types)

If the paper genuinely doesn't need display items (rare), note this and score Dimension 5 only.

## Evaluation Framework

Evaluate display items across **five dimensions**, each with specific criteria.

---

### Dimension 1: Analytical Purpose (Strategic)

Check whether each display item does analytical work that text alone cannot do.

For each table/figure:

| Check | Pass | Fail |
|-------|------|------|
| Earns its space | Communicates relationships, patterns, or structures that would require 200+ words of prose | Merely restates what the text already says |
| Analytical, not decorative | Shows patterns, comparisons, processes, or structures | Decorative illustration or generic stock diagram |
| Appropriate type chosen | Tables for comparisons and structured data; figures for processes, relationships, and visual evidence | Table where a figure would be clearer, or vice versa |
| Contributes to argument | Removing this display item would weaken the paper's argument | Removing it would lose nothing |

**The Tufte test**: Every element in a display item should present data or aid comprehension. Remove any element that doesn't. If the display item can be replaced by a sentence, it should be.

**Expected display items by paper type**:

| Paper Type | Minimum Expected | Common Display Items |
|-----------|-----------------|---------------------|
| Qual/ethnographic | 2-4 | Data overview table, process model, evidence mapping table, key quotes table |
| Mixed-methods | 4-6 | Data table, statistical results, process model, evidence mapping, comparison table |
| Comparative case | 3-5 | Case comparison table, within-case evidence, cross-case patterns, process model |

---

### Dimension 2: Design Clarity (Visual)

Check whether each display item is visually clear and immediately interpretable.

| Check | Pass | Fail |
|-------|------|------|
| Self-contained | Display item is interpretable WITHOUT reading surrounding text | Requires extensive text context to understand |
| Visual hierarchy clear | Most important information is visually prominent | Everything at same visual weight; reader doesn't know where to look |
| Not cluttered | Appropriate information density; white space used well | Overloaded with data, rows, or labels |
| Consistent formatting | All display items follow the same design conventions | Mixed conventions (some tables with headers, some without; inconsistent alignment) |
| Accessible | Would be legible in black and white or grayscale; not color-dependent | Color-dependent encoding with no alternative |

**For tables specifically**:
- Column headers should be clear and unambiguous
- Row/column organization should follow analytical logic (not alphabetical or arbitrary)
- Alignment: numbers right-aligned; text left-aligned; headers centered
- No excessive gridlines — use whitespace to separate, not lines

**For figures specifically**:
- Labels on all axes, nodes, or components
- Arrow directions and meanings are clear
- Legend present if multiple categories/series
- Resolution sufficient for print

---

### Dimension 3: Caption Quality (Technical)

Check whether captions do proper work.

| Check | Pass | Fail |
|-------|------|------|
| Caption is complete | Reader can understand the display item from caption + display alone | Caption is a bare title ("Table 1: Interview Data") |
| Caption describes content | States what the table/figure shows, not just what it is | "Figure 2: Process Model" (what is the process? what does it model?) |
| Notes explain conventions | Abbreviations, coding schemes, or selection criteria are noted | Abbreviations used without explanation |
| Source noted (if applicable) | Data source identified for tables based on external data | Source unclear |
| Numbered sequentially | Tables and figures numbered separately in order of first mention | Misnumbered or referenced out of sequence |

**Good caption pattern**: "Table 2. Comparison of Coordination Practices Across Technology Conditions. Practices are grouped by phase (preparation, performance, recovery). Evidence types are coded: I = interview, O = observation, A = archival. N = number of incidents observed."

**Bad caption pattern**: "Table 2. Coordination Practices"

---

### Dimension 4: Text Integration (Craft)

Check whether display items are integrated into the narrative flow.

| Check | Pass | Fail |
|-------|------|------|
| Referenced at point of need | Text references the display item at the moment the reader needs it | Display item appears pages before or after its textual reference |
| Reference is substantive | "As Table 2 shows, coordination practices differed markedly across conditions" | "See Table 2" with no interpretive frame |
| Text doesn't duplicate display | Text highlights key patterns; display provides full detail | Text restates every row of the table |
| Display items placed near reference | Within one page of the textual reference (or per journal convention) | Display items collected at the end with no clear placement logic |
| Cross-references between displays | When relevant, figures and tables reference each other | Related display items exist independently |

---

### Dimension 5: Information Density (Analytical)

Check whether the collection of display items has the right overall density.

| Check | Pass | Fail |
|-------|------|------|
| Sufficient display items | Paper has enough visual/tabular elements to support its claims | Claims made entirely through prose when tables/figures would strengthen them |
| No redundant items | Each display item shows something unique | Two tables showing essentially the same comparison from different angles |
| Process model present (if needed) | *(strongly recommended but not required)* For process theories: a figure showing the model with stages and mechanisms — often excellent when present | Process theory claimed with no visual representation AND no stated rationale for omitting one |
| Data overview present | *(recommended but not required)* Summary of data sources, informants, or analytical categories — many excellent papers embed this in prose | Absent AND data scope is genuinely unclear from reading the methods section |
| Total count appropriate | Consistent with journal conventions | Too many (every finding has its own table) or too few (no visual support) |

**Journal conventions**:

| Journal | Typical Display Items | Notes |
|---------|---------------------|-------|
| ASQ | 3-6 | Figures often inline; tables at end or inline |
| Organization Science | 3-7 | More liberal with display items |
| AMJ | 4-8 | Tables expected for statistical results + qual evidence |
| Management Science | 3-6 | Heavy on statistical tables |

---

### Failure Mode Scan

| Failure mode | Detection | Present? |
|--------------|-----------|----------|
| **Decorative display** | Table/figure that adds nothing prose doesn't already say | Yes/No |
| **Missing captions** | Bare title without descriptive information | Yes/No |
| **Data dump table** | Raw data in table form without analytical organization | Yes/No |
| **Orphaned display** | Table/figure not referenced in text, or referenced far from placement | Yes/No |
| **Missing process model** | Process theory claimed but no visual model | Yes/No |
| **Missing data overview** | No structured summary of data sources/scope | Yes/No |
| **Inconsistent formatting** | Different conventions across display items | Yes/No |
| **Color-dependent encoding** | Information lost in grayscale/print | Yes/No |

---

## Scoring

Rate each dimension on a 5-point scale:

| Score | Label | Meaning |
|-------|-------|---------|
| 5 | Excellent | Display items are a strength; would impress reviewers |
| 4 | Strong | Minor issues; formatting or caption polish needed |
| 3 | Adequate | Display items present but don't do full analytical work |
| 2 | Weak | Key display items missing or poorly designed |
| 1 | Failing | Display strategy needs fundamental rethinking |

**Overall score**: Sum of 5 dimensions / 25 possible points.

**Verdict thresholds**:
- **PASS** (>=20/25): Display items are ready
- **CONDITIONAL** (15-19): Revise display items before submission
- **FAIL** (<15): Rethink display strategy; may need to add, remove, or redesign tables/figures

## Output Format

Create `analysis/quality/TABLES_FIGURES_EVAL.md`:

```markdown
# Tables & Figures Evaluation

**Paper**: [Title]
**Date evaluated**: [Date]
**Target journal**: [If specified]
**Total display items**: [N tables, M figures]

---

## Display Item Inventory

| # | Type | Caption/Title | Purpose | Earns Space? | Text Reference |
|---|------|--------------|---------|-------------|----------------|
| Table 1 | Data overview | [...] | [Summarize data] | Yes/No | [Page/section] |
| Figure 1 | Process model | [...] | [Show mechanism] | Yes/No | [...] |
| ... | ... | ... | ... | ... | ... |

---

## Missing Display Items

| Suggested Item | Type | Why Needed |
|---------------|------|-----------|
| [Data summary] | Table | [No structured data overview in paper] |
| [Process model] | Figure | [Process theory without visual model] |

---

## Scorecard

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| 1. Analytical Purpose | X/5 | [One line] |
| 2. Design Clarity | X/5 | [One line] |
| 3. Caption Quality | X/5 | [One line] |
| 4. Text Integration | X/5 | [One line] |
| 5. Information Density | X/5 | [One line] |

**Overall**: X/25 — **[PASS/CONDITIONAL/FAIL]**

---

## Detailed Assessment

### 1. Analytical Purpose [X/5]
[Assessment per display item]

### 2. Design Clarity [X/5]
[Assessment of visual quality]

### 3. Caption Quality [X/5]
[Assessment of caption completeness]

### 4. Text Integration [X/5]
[Assessment of narrative integration]

### 5. Information Density [X/5]
[Assessment of overall display strategy]

---

## Top 3 Priorities for Revision

1. **[Highest priority]**: [What to do, with specific guidance]
2. **[Second priority]**: [What to do]
3. **[Third priority]**: [What to do]

---

## Strengths

- [What the display items do well]
- [Another strength]
```

## After You're Done

Tell the user:
- The overall score and verdict
- The display item inventory
- Any missing display items that should be added
- The top 3 priorities for revision
- Any failure modes detected

If the paper has no display items, recommend starting with a data overview table and a process model (if applicable).

If display items fail on analytical purpose (Dimension 1), the issue is usually that tables were created to organize data rather than to make an analytical point. Redesign each table/figure around the analytical claim it should support.

If display items fail on integration (Dimension 4), add substantive text references and move display items closer to their first reference.

## Reference

Journal formatting: `docs/JOURNAL_FORMATTING_GUIDE.md` (table/figure placement rules)

---

For consensus mode behavior, see [../../_shared/consensus-mode.md](../../_shared/consensus-mode.md)
For staleness detection, see [../../_shared/staleness-check.md](../../_shared/staleness-check.md)
For eval result persistence, see [../../_shared/eval-persistence.md](../../_shared/eval-persistence.md)

### Skill-Specific Persistence

- **eval_results key**: `tables_figures`
- **Upstream files**: `analysis/manuscript/DRAFT.md`
- **Scores**: 5 dimensions: `analytical_purpose`, `design_clarity`, `caption_quality`, `text_integration`, `information_density`
- **Verdict**: PASS >= 20/25; FAIL < 15/25; CONDITIONAL otherwise
- **Default consensus N**: 5
