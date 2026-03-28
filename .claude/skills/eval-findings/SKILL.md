---
name: eval-findings
description: Deep structural evaluation of a paper's findings section — concept organization, evidence-theory interleaving, progressive theory building, quote handling, and narrative arc
---

# Evaluate Findings

You are the FINDINGS-EVAL agent. Your job is to perform a deep structural evaluation of a paper's findings section — the section where theory gets BUILT in inductive papers. This is not a surface check; it evaluates whether findings progressively construct a theoretical contribution through named concepts, well-integrated evidence, and narrative momentum.

## When to Run This

- **After** `/draft-paper` — to assess findings quality before full paper eval
- **After** revising findings — to verify improvements landed
- **Before** `/eval-paper-quality` — as a focused pre-check on the section that carries the theoretical weight
- **Standalone** — when the user wants findings-specific feedback

This skill is narrower than `/eval-paper-quality` (whole paper). It goes deeper on the findings section specifically — where inductive theory papers live or die.

## Prerequisites

- A draft findings section (at minimum: the full text of the findings/results section)
- Ideally also: the introduction (for finding-promise coherence) and framing options (for concept alignment)

## Inputs You Need

- Path to the draft paper or findings text
- Target journal (if specified)
- Contribution type (theory violation, elaboration, phenomenon description — affects expectations)
- Whether the paper is qual-only, quant-only, or mixed-methods

## Evaluation Framework

Evaluate the findings across **six dimensions**, each with specific criteria.

---

### Dimension 1: Concept Organization (Structural)

Check whether findings are organized around emergent concepts rather than imposed categories.

| Check | Pass | Fail |
|-------|------|------|
| Organized by named concepts | Findings sections headed by concept names (e.g., "Shadow Learning," "Premature Specialization") | Headed by H1/H2/H3, chronological periods without conceptual framing, or "Theme 1" |
| Concepts are emergent | Concepts appear to arise from data; not front-loaded from theory section | All major findings are derivable from the theory section (front-loading) |
| Progressive development | Each concept builds on the previous; order matters | Concepts are interchangeable; reordering wouldn't matter |
| Concept count calibrated | 3-5 major concepts for a full paper; 2-3 for a shorter piece | 1 (underdeveloped) or 7+ (fragmented) |
| Naming quality | Names are evocative, memorable, capture the essence of what was observed | Generic labels ("coordination challenges"), purely descriptive names, or no names at all |

**The front-loading test**: Could a reader predict ALL major findings from the theory section alone? If yes, the findings are front-loaded and the paper reads as deductive, regardless of claimed methodology. Check eval-genre's front-loading diagnostic.

**Output**: Concept map showing the named concepts, their sequence, and how each builds on the prior.

---

### Dimension 2: Evidence-Theory Interleaving (Craft)

Check whether evidence (quotes, observations, data) is woven into analytical prose rather than separated from it.

| Check | Pass | Fail |
|-------|------|------|
| Claim-evidence-development cycle | Each finding unit follows: analytical claim → evidence → further development | Evidence dumped then interpreted in bulk; or claims without evidence |
| No naked quotes | Every block quote followed by interpretive text before next quote or section break | Quote → section break, or quote → next quote |
| Post-quote text does work | Names mechanism, links to theory, synthesizes with other data, explicates logic, contrasts, or traces consequences | Pure restatement ("She said she felt overwhelmed") |
| Evidence quantity calibrated | Sufficient evidence to convince but not overwhelm; multiple evidence types per major finding | One illustrative quote per finding (thin) or 5+ quotes per finding (quote dump) |
| Analytical voice maintained | Author's interpretive voice present throughout | Findings read like a data report with author absent |

**The two-move pattern**: Most effective post-quote sequences follow: (1) NAME what the quote exemplifies (mechanism, process, concept), then (2) SITUATE it within the larger argument (consequences, pattern, theory).

---

### Dimension 3: Quote Selection & Handling (Technical)

Check the quality and deployment of qualitative evidence.

| Check | Pass | Fail |
|-------|------|------|
| Quotes are extended and voicey | 60-120+ words, colorful, informant's personality visible | 15-word fragments that could be anyone |
| Analytical setup precedes each quote | "As one resident explained, describing the tension between..." | Quote appears with no framing context |
| Quote-to-analysis ratio | Interpretation shorter than or equal to quote length | 50 words of analysis after 150-word quote (underdeveloped) |
| Quotes do argumentative work | Each quote advances the argument, not just illustrates it | Quotes are decorative; removing them wouldn't weaken the argument |
| Evidence type diversity | Quotes, field observations, archival data, quantitative patterns as appropriate | One evidence type only (all interview quotes, no triangulation) |

**Multimethod note**: Mixed-methods papers may have fewer quotes. Score based on how well the qualitative evidence that IS present is handled. A paper can score 4-5 with fewer quotes if they're well-integrated and quantitative evidence also builds theory inductively.

---

### Dimension 4: Narrative Progression (Persuasive)

Check whether the findings section tells a story with momentum.

| Check | Pass | Fail |
|-------|------|------|
| Findings build | Later findings depend on earlier ones; removing Finding 1 would make Finding 3 incoherent | Findings are parallel/interchangeable |
| Transitions are narrative bridges | "Having established X, we now turn to..." or causal/contrastive connectors | Section breaks with no bridging; or mechanical "Next we discuss..." |
| Complexity escalates | Early findings are more descriptive; later findings are more analytical/theoretical | Constant abstraction level throughout |
| Model emerges by section end | By the final finding, a coherent theoretical model is visible | Findings end without synthesis; model is deferred entirely to discussion |
| Pace is managed | Flagship findings get more space; supporting findings are tighter | All findings receive equal treatment regardless of importance |

**The inevitability test**: By the end of findings, does the theoretical contribution feel like the only possible interpretation of this evidence? Or does it feel like one of several plausible readings?

---

### Dimension 5: Data Display Integration (Visual)

Check how tables, figures, and other visual elements support the findings.

| Check | Pass | Fail |
|-------|------|------|
| Display items earn their space | Each table/figure communicates something text alone cannot | Tables that merely repeat what prose already states |
| Integrated with text | Text refers to display items at the moment they're needed | Tables/figures appear with no textual reference, or referenced pages away |
| Process models present | For process theories: a figure showing the model, stages, or mechanism | Process theory with no visual model |
| Data summary table | Overview table showing key data characteristics (informants, sites, time periods) | No summary of the data used |
| Display items do analytical work | Tables organize analytical categories, not just raw data | Raw data dumps in table form |

**Note**: This dimension applies primarily when tables/figures are present. If the paper has no display items, evaluate whether it SHOULD — most theory-building papers benefit from at least a process model and a data summary.

---

### Dimension 6: Failure Mode Scan

Check for named structural failure modes in findings sections:

| Failure mode | Detection | Present? |
|--------------|-----------|----------|
| **H1/H2/H3 structure** | Findings organized as hypothesis tests with support/non-support | Yes/No |
| **Pattern reporting** | Patterns described but not developed into concepts | Yes/No |
| **Quote dump** | Multiple quotes strung together without analytical framing between them | Yes/No |
| **Missing post-quote analysis** | Block quotes followed by section breaks or next quotes | Yes/No |
| **Front-loaded findings** | All major findings derivable from theory section | Yes/No |
| **Deductive register** | "Consistent with predictions," "supports our hypothesis" in an inductive paper | Yes/No |
| **Flat structure** | All findings at same abstraction level; no progressive building | Yes/No |
| **Everything findings** | 6+ major findings that fragment the contribution | Yes/No |

---

## Language Register Check

For inductive/theory-building papers, findings should use discovery language:

| Use | Avoid |
|-----|-------|
| reveal, uncover, identify, document, observe, find, discover | validate, test, confirm, verify, prove |
| pattern, theme, mechanism, process, dynamic | hypothesis, prediction |
| suggests, indicates, is consistent with, may, appears to | demonstrates that, establishes that, proves that |
| "the data reveal," "we observe," "informants described" | "as predicted," "consistent with our prediction" |

**Section header**: Use "Findings" not "Results" for inductive papers (subtle but signals discovery vs. testing).

---

## Scoring

Rate each dimension on a 5-point scale:

| Score | Label | Meaning |
|-------|-------|---------|
| 5 | Excellent | Would pass peer review at target journal without revision |
| 4 | Strong | Minor issues; revision is polish, not restructuring |
| 3 | Adequate | Structure is sound but concept development or evidence handling is weak |
| 2 | Weak | Significant structural or evidence problems |
| 1 | Failing | Needs fundamental rethinking of findings organization |

**Overall score**: Sum of 6 dimensions / 30 possible points.

**Verdict thresholds**:
- **PASS** (>=24/30): Ready for full paper eval
- **CONDITIONAL** (18-23): Revise findings before proceeding
- **FAIL** (<18): Rethink findings organization; consider re-running `/hunt-patterns` or `/mine-qual`

## Output Format

Create `analysis/quality/FINDINGS_EVAL.md`:

```markdown
# Findings Evaluation

**Paper**: [Title]
**Date evaluated**: [Date]
**Target journal**: [If specified]
**Word count**: [Findings section word count]
**Contribution type**: [Theory violation / elaboration / phenomenon / etc.]

---

## Concept Map

| # | Concept Name | Builds On | Key Evidence Types | Approx. Words |
|---|-------------|-----------|-------------------|---------------|
| 1 | [Name] | — | [Quote, observation, table...] | [N] |
| 2 | [Name] | Concept 1 | [...] | [N] |
| 3 | [Name] | Concepts 1+2 | [...] | [N] |

---

## Scorecard

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| 1. Concept Organization | X/5 | [One line] |
| 2. Evidence-Theory Interleaving | X/5 | [One line] |
| 3. Quote Selection & Handling | X/5 | [One line] |
| 4. Narrative Progression | X/5 | [One line] |
| 5. Data Display Integration | X/5 | [One line] |
| 6. Failure Mode Scan | X/5 | [One line] |

**Overall**: X/30 — **[PASS/CONDITIONAL/FAIL]**

---

## Detailed Assessment

### 1. Concept Organization [X/5]
[Assessment with specific evidence from the text]

### 2. Evidence-Theory Interleaving [X/5]
[Assessment of claim-evidence-development cycle]

### 3. Quote Selection & Handling [X/5]
[Assessment of quote quality, framing, and analytical follow-through]

### 4. Narrative Progression [X/5]
[Assessment of building momentum, transitions, complexity escalation]

### 5. Data Display Integration [X/5]
[Assessment of tables/figures or their absence]

### 6. Failure Mode Scan [X/5]
[List any failure modes detected, with evidence]

---

## Top 3 Priorities for Revision

1. **[Highest priority]**: [What to do, with specific guidance]
2. **[Second priority]**: [What to do]
3. **[Third priority]**: [What to do]

---

## Strengths

- [What the findings section does well]
- [Another strength]
```

## After You're Done

Tell the user:
- The overall score and verdict
- The concept map (named concepts and their sequence)
- The top 3 priorities for revision
- Whether the narrative builds progressively or is flat
- Any failure modes detected
- Register issues (deductive language in inductive paper)

If findings fail on concept organization (Dimension 1), suggest restructuring before addressing other dimensions — concept organization is load-bearing.

If findings fail on evidence-theory interleaving (Dimension 2) but pass concept organization, the issue is usually craft — add analytical framing after quotes, strengthen post-quote interpretation.

If findings fail on narrative progression (Dimension 4) but pass concept organization, consider reordering concepts so each builds on the prior. Look for implicit dependencies that should be made explicit.

## Reference

Full argument construction rules: `docs/ARGUMENT_CONSTRUCTION_RULES.md`
Post-quote interpretation rules: `docs/JOURNAL_FORMATTING_GUIDE.md` (Post-Quote Interpretation Rules section)
Theory-building style guide: `docs/THEORY_BUILDING_STYLE.md`

---

For consensus mode behavior, see [../../_shared/consensus-mode.md](../../_shared/consensus-mode.md)
For staleness detection, see [../../_shared/staleness-check.md](../../_shared/staleness-check.md)
For eval result persistence, see [../../_shared/eval-persistence.md](../../_shared/eval-persistence.md)

### Skill-Specific Persistence

- **eval_results key**: `findings`
- **Upstream files**: `analysis/manuscript/DRAFT.md` (findings section)
- **Scores**: 6 dimensions: `concept_organization`, `evidence_theory_interleaving`, `quote_handling`, `narrative_progression`, `data_display`, `failure_modes`
- **Verdict**: PASS >= 24/30; FAIL < 18/30; CONDITIONAL otherwise
- **Default consensus N**: 5
