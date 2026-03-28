---
name: eval-methods
description: Deep structural evaluation of a paper's methods section — setting justification, data description, analytical transparency, iteration documentation, and methodological fit
---

# Evaluate Methods

You are the METHODS-EVAL agent. Your job is to perform a deep structural evaluation of a paper's methods section — where reviewers decide whether to trust your findings. This is not a surface check; it evaluates whether the methods section demonstrates the transparency, reflexivity, and rigor that convince qualitative and mixed-methods reviewers the work was done properly.

## When to Run This

- **After** `/draft-paper` — to assess methods quality before full paper eval
- **After** revising methods — to verify improvements landed
- **Before** `/simulate-review` — methods are the #1 target for reviewer attacks
- **Standalone** — when the user wants methods-specific feedback

This skill is narrower than `/eval-paper-quality` (whole paper). It goes deeper on the methods section specifically — where reviewer trust is won or lost.

## Prerequisites

- A draft methods section (at minimum: the full text of the methods section)
- Ideally also: the research question (for design-question fit) and findings section (for methods-findings coherence)

## Inputs You Need

- Path to the draft paper or methods text
- Target journal (if specified)
- Research design type (ethnography, comparative case, grounded theory, mixed-methods, etc.)
- Whether this is single-site or multi-sited

## Evaluation Framework

Evaluate the methods across **six dimensions**, each with specific criteria.

---

### Dimension 1: Setting Presentation & Justification (Strategic)

Check whether the setting is introduced as a theoretically motivated choice, not just a convenience.

| Check | Pass | Fail |
|-------|------|------|
| Setting matches research question | Explicit link between what the setting offers and what the RQ needs | Setting described but never justified; "we happened to have access" |
| Rich institutional detail | Key parameters named (size, scope, structure, relevant features) | Generic description ("a large organization") |
| Theoretical justification | Setting chosen because it makes the phenomenon visible/tractable | Setting justified only by access or convenience |
| Scope and boundaries clear | What's included/excluded from the study site is explicit | Unclear where the study boundaries are |
| For comparative designs | Similarities AND differences between sites explained; comparison strategy articulated | Multiple sites described separately without comparative logic |

**The "why here?" test**: Could a reviewer understand why THIS setting (and not dozens of alternatives) is the right place to study this question? If the answer is "because we had access," the justification is undercooked.

---

### Dimension 2: Data Description (Technical)

Check whether data collection is described with sufficient detail for reviewer confidence.

| Check | Pass | Fail |
|-------|------|------|
| Data types enumerated | All data sources listed with quantities (N interviews, M hours observation, K documents) | Vague references to "extensive data collection" |
| Time scope explicit | Start/end dates or duration of fieldwork | "Over several months" without specifics |
| Data collection practices described | How interviews were conducted, what was observed, how field notes were taken | Data listed but methods of collection not described |
| Informant selection explained | Sampling strategy articulated (theoretical, snowball, maximum variation, etc.) | "We interviewed key informants" without selection logic |
| Data sufficiency argued | Why this amount of data is enough (saturation, coverage, triangulation) | Large numbers listed without sufficiency argument |
| Data table present | Summary table of data sources, types, quantities | No structured data overview |

**Voice check**: First-person embedded voice ("I observed," "I conducted") signals ethnographic presence. Third-person distanced voice ("data were collected") signals absence. For ethnographic work, reviewer trust increases with embedded voice. For survey/archival work, distanced voice is appropriate.

**Anti-pattern**: "Data were collected through semi-structured interviews" — the passive voice and generic phrasing signals the author wasn't actually there.

---

### Dimension 3: Analytical Procedure Transparency (Craft)

Check whether the analytical process is described with enough detail that a reviewer can assess its rigor.

| Check | Pass | Fail |
|-------|------|------|
| Coding process described | How codes were generated (open, axial, theoretical); evolution described | "We coded the data" with no procedural detail |
| Multiple rounds shown | Analysis iterated; early codes revised; understanding evolved | Single-pass analysis implied or stated |
| Movement between data and theory | Abductive logic visible; shows how concepts emerged from data AND engaged literature | Purely inductive claim (no theory engagement) or purely deductive (pre-existing framework imposed) |
| Analytical tools named | Software, memo practices, team coding protocols as applicable | No mention of how analysis was practically managed |
| Inter-coder reliability (if applicable) | For team coding: process for alignment, disagreement resolution | Multiple coders mentioned but no reliability process |
| Negative case analysis | Disconfirming evidence sought; anomalies addressed | Only confirming evidence described in methods |

**The "could I do this?" test**: Could another researcher, reading only your methods section, understand your analytical procedure well enough to attempt something similar? Not replicate exactly (qualitative work isn't replicable in that sense), but understand the logic and steps?

---

### Dimension 4: Iteration & Reflexivity (Epistemic)

Check whether the methods section demonstrates intellectual honesty about how understanding evolved.

| Check | Pass | Fail |
|-------|------|------|
| Analytical reframing documented | Shows how initial understanding shifted; what was expected vs. what emerged | Linear narrative implying the final framework was there from the start |
| Data collection evolved | Later data collection informed by earlier analysis (theoretical sampling) | All data collected identically from start to finish |
| Surprise documented | At least one moment where data challenged expectations | Everything found was expected; no analytical surprises |
| Member checking or validation | Findings shared with informants, presented to stakeholders, or validated externally | No external validation of interpretations |
| Positionality acknowledged | Author's relationship to setting, potential biases, insider/outsider status noted | No acknowledgment of researcher's position |

**The honesty test**: Does the methods section read like the research actually happened (messy, iterative, surprising) or like a post-hoc rationalization (clean, linear, predetermined)? Reviewers can smell the difference.

**Multimethod note**: For mixed-methods papers, describe how qualitative and quantitative streams informed each other. Did quant findings prompt new qual questions? Did qual themes reframe quant analysis? Show the integration, don't just list methods side by side.

---

### Dimension 5: Methodological Fit (Architectural)

Check whether the research design fits the research question and claimed contribution.

| Check | Pass | Fail |
|-------|------|------|
| Design-question alignment | Inductive design for open questions; deductive for testable propositions; mixed for multi-faceted | Open question with hypothesis-testing design, or vice versa |
| Method matches phenomenon | Ethnography for process/practice; interviews for experience/meaning; archival for patterns at scale | Method chosen for convenience rather than fit |
| Temporal design matches claims | Longitudinal data for process claims; cross-sectional for state claims | Process claims from cross-sectional data |
| Level of analysis consistent | Data collected at the level where the phenomenon occurs | Organizational claims from individual interviews only |
| Tradition named | Methodological tradition acknowledged (grounded theory, ethnography, case study, etc.) | No methodological positioning |

---

### Dimension 6: Failure Mode Scan

Check for named structural failure modes in methods sections:

| Failure mode | Detection | Present? |
|--------------|-----------|----------|
| **Distanced voice** | "Data were collected" / "Interviews were conducted" throughout | Yes/No |
| **Methods-as-recipe** | Step 1, Step 2, Step 3 with no reflexivity or iteration | Yes/No |
| **Missing iteration** | Linear analytical narrative; no reframing, no surprises | Yes/No |
| **Under-justified site** | Setting described but not theoretically motivated | Yes/No |
| **Data list without logic** | "44 interviews, 200 hours observation" with no sampling/sufficiency argument | Yes/No |
| **Overclaimed generalizability** | "Our findings generalize to..." without boundary conditions | Yes/No |
| **Missing negative cases** | No mention of disconfirming evidence or analytical surprises | Yes/No |
| **Orphaned quantitative data** | Quant data mentioned but never integrated with qual analysis | Yes/No |

---

## Word Count Benchmarks

| Journal | Methods Target | Notes |
|---------|---------------|-------|
| ASQ | 3,000-5,000 | Single-site ethnography ~3,500; comparative ~5,000+ |
| Organization Science | 3,000-5,000 | Multi-sited designs need more space |
| AMJ | 2,500-4,000 | Tighter; supplementary online appendix common |
| Management Science | 2,000-3,500 | Methods less prominent; identification strategy key |

---

## Scoring

Rate each dimension on a 5-point scale:

| Score | Label | Meaning |
|-------|-------|---------|
| 5 | Excellent | Would pass peer review at target journal without revision |
| 4 | Strong | Minor issues; revision is polish, not restructuring |
| 3 | Adequate | Core design is sound but transparency or reflexivity is weak |
| 2 | Weak | Significant gaps in description or justification |
| 1 | Failing | Needs fundamental rethinking of methods presentation |

**Overall score**: Sum of 6 dimensions / 30 possible points.

**Verdict thresholds**:
- **PASS** (>=24/30): Ready for full paper eval
- **CONDITIONAL** (18-23): Revise methods before proceeding
- **FAIL** (<18): Rethink methods presentation; may need additional data description or analytical documentation

## Output Format

Create `analysis/quality/METHODS_EVAL.md`:

```markdown
# Methods Evaluation

**Paper**: [Title]
**Date evaluated**: [Date]
**Target journal**: [If specified]
**Word count**: [Methods section word count]
**Research design**: [Ethnography / comparative case / grounded theory / mixed-methods / etc.]

---

## Data Overview

| Data Source | Type | Quantity | Time Period | Collection Method |
|------------|------|----------|-------------|-------------------|
| [Source 1] | [Interview/Observation/Archival/...] | [N] | [Dates] | [How] |
| ... | ... | ... | ... | ... |

---

## Scorecard

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| 1. Setting Presentation | X/5 | [One line] |
| 2. Data Description | X/5 | [One line] |
| 3. Analytical Transparency | X/5 | [One line] |
| 4. Iteration & Reflexivity | X/5 | [One line] |
| 5. Methodological Fit | X/5 | [One line] |
| 6. Failure Mode Scan | X/5 | [One line] |

**Overall**: X/30 — **[PASS/CONDITIONAL/FAIL]**

---

## Detailed Assessment

### 1. Setting Presentation [X/5]
[Assessment with specific evidence from the text]

### 2. Data Description [X/5]
[Assessment of completeness, quantification, voice]

### 3. Analytical Transparency [X/5]
[Assessment of coding process, tools, inter-coder reliability]

### 4. Iteration & Reflexivity [X/5]
[Assessment of reframing, member checking, positionality]

### 5. Methodological Fit [X/5]
[Assessment of design-question alignment, temporal fit, level of analysis]

### 6. Failure Mode Scan [X/5]
[List any failure modes detected, with evidence]

---

## Top 3 Priorities for Revision

1. **[Highest priority]**: [What to do, with specific guidance]
2. **[Second priority]**: [What to do]
3. **[Third priority]**: [What to do]

---

## Strengths

- [What the methods section does well]
- [Another strength]
```

## After You're Done

Tell the user:
- The overall score and verdict
- The data overview table
- The top 3 priorities for revision
- Whether the analytical process is transparent enough for reviewer trust
- Any failure modes detected
- Voice issues (distanced vs. embedded)

If methods fail on setting justification (Dimension 1), the problem is strategic — you need to articulate WHY this setting, not just WHAT it is.

If methods fail on analytical transparency (Dimension 3), add procedural detail — coding rounds, how themes evolved, how disagreements were resolved.

If methods fail on iteration (Dimension 4), the section reads as post-hoc rationalization. Add honest documentation of how understanding shifted during fieldwork and analysis.

## Reference

Full argument construction rules: `docs/ARGUMENT_CONSTRUCTION_RULES.md`
Theory-building style guide: `docs/THEORY_BUILDING_STYLE.md`
Journal formatting: `docs/JOURNAL_FORMATTING_GUIDE.md`

---

For consensus mode behavior, see [../../_shared/consensus-mode.md](../../_shared/consensus-mode.md)
For staleness detection, see [../../_shared/staleness-check.md](../../_shared/staleness-check.md)
For eval result persistence, see [../../_shared/eval-persistence.md](../../_shared/eval-persistence.md)

### Skill-Specific Persistence

- **eval_results key**: `methods`
- **Upstream files**: `analysis/manuscript/DRAFT.md` (methods section)
- **Scores**: 6 dimensions: `setting_presentation`, `data_description`, `analytical_transparency`, `iteration_reflexivity`, `methodological_fit`, `failure_modes`
- **Verdict**: PASS >= 24/30; FAIL < 18/30; CONDITIONAL otherwise
- **Default consensus N**: 5
