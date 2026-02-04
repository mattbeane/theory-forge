# /eval-citations - Citation Coverage Check

Evaluate whether the paper has adequate citation coverage for its claimed literatures and target journal.

## Why This Matters

A paper can have perfect framing (Zuckerman PASS), generalizable theory (Becker PASS), and appropriate genre (Genre PASS)—yet still fail review because it lacks sufficient scholarly grounding. Reviewers expect:
- Engagement with canonical works in claimed literatures
- Coverage proportional to theoretical claims
- Citation counts appropriate for the target journal

This check catches papers that are well-argued but under-cited.

## When to Run

- After `/draft-paper`
- Before submission
- Whenever you invoke a literature you haven't deeply engaged with

## Benchmarks by Journal

Based on exemplar papers:

| Journal | Typical Range | Minimum | Notes |
|---------|---------------|---------|-------|
| ASQ | 80-150 | 60 | Theory-heavy, expects deep engagement |
| Organization Science | 60-100 | 50 | Phenomenon + theory balance |
| AMJ | 70-120 | 50 | Empirical focus, still needs grounding |
| AMD | 50-80 | 40 | Phenomenon-forward, lighter theory |
| ASR | 80-150 | 60 | Sociology expects comprehensive coverage |
| ILR Review | 40-70 | 35 | Applied focus, lighter requirements |

## Evaluation Steps

### Step 1: Count Raw Citations

```bash
grep -o '\\cite[tp]*{[^}]*}' main.tex | sed 's/.*{\(.*\)}/\1/' | tr ',' '\n' | sed 's/^ *//' | sort -u | wc -l
```

**Verdict:**
- Below minimum for target journal → FAIL
- Within range → PASS
- Above range → Check for padding (CONDITIONAL)

### Step 2: Identify Claimed Literatures

Scan the paper for literature claims. Look for phrases like:
- "Drawing on [X] theory..."
- "[X] research has shown..."
- "The literature on [X]..."
- "Prior work on [X]..."

List each claimed literature and its canonical citations.

### Step 3: Check Canonical Coverage

For each claimed literature, verify presence of:

**Must-have for any literature claim:**
- Foundational paper(s) that introduced the concept
- At least one recent review or meta-analysis (if exists)
- 2-3 empirical papers showing the literature is active

**Red flags:**
- Claiming a literature but only citing 1-2 papers from it
- Missing the "obvious" canonical cite everyone knows
- Only citing old papers (nothing in last 10 years)
- Only citing recent papers (missing foundations)

### Step 4: Calculate Coverage Ratio

For each major theoretical claim, count supporting citations:

| Section | Claims Made | Citations | Ratio |
|---------|-------------|-----------|-------|
| Work Orientation | 3 | 8 | 2.7 |
| P-E Fit | 4 | 12 | 3.0 |
| Signaling | 2 | 3 | 1.5 |
| Contingent Work | 2 | 6 | 3.0 |

**Target:** 2-4 citations per major claim
**Red flag:** <2 citations for a central theoretical claim

### Step 5: Check Bib Utilization

```bash
# Citations in paper
grep -o '\\cite[tp]*{[^}]*}' main.tex | sed 's/.*{\(.*\)}/\1/' | tr ',' '\n' | sed 's/^ *//' | sort -u > /tmp/used.txt

# Entries in bib
grep -o '@[a-z]*{[^,]*' references.bib | sed 's/.*{//' | sort -u > /tmp/bib.txt

# Unused entries
comm -23 /tmp/bib.txt /tmp/used.txt
```

**If many unused entries:** You have citations available but didn't use them—probably an oversight.

### Step 6: Literature-Specific Canonical Checks

For common literatures, verify these citations are present (if the literature is invoked):

**Person-Environment Fit:**
- Kristof (1996) - foundational review
- Kristof-Brown et al. (2005) - meta-analysis
- Edwards (1991/1998) - conceptual integration

**Work Orientation:**
- Wrzesniewski et al. (1997) - jobs/careers/callings
- Schein (1978, 1990) - career anchors
- Recent: Schabram et al. (2023) - dynamics

**Incentive Pay:**
- Lazear (2000) - performance pay and productivity
- Prendergast (1999) - JEL review
- At least one meta-analysis (Gubler et al. 2016 or similar)

**Contingent Work:**
- Kalleberg (2000) - Annual Review
- Connelly & Gallagher (2007) - meta-analysis
- Recent empirical work

**Signaling Theory:**
- Spence (1973) - foundational
- Applications in labor/org context

## Output Format

Create `analysis/quality/CITATIONS_EVAL.md`:

```markdown
# Citation Coverage Evaluation

**Paper**: [Title]
**Target Journal**: [Journal]
**Date**: [Date]

---

## Summary

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Total unique citations | X | 50-80 | ✓/✗ |
| Claimed literatures | N | — | — |
| Literatures with adequate coverage | N/N | 100% | ✓/✗ |
| Unused bib entries | X | <10 | ✓/✗ |

**Overall**: [PASS / CONDITIONAL / FAIL]

---

## Claimed Literatures

### 1. [Literature Name]

**Canonical citations expected:**
- [Author Year] - [Why essential]
- [Author Year] - [Why essential]

**Found in paper:**
- ✓ [Author Year]
- ✓ [Author Year]
- ✗ [Author Year] - MISSING

**Coverage**: [Adequate / Thin / Missing canonical]

---

### 2. [Literature Name]
...

---

## Coverage Ratios by Section

| Section | Major Claims | Citations | Ratio | Status |
|---------|--------------|-----------|-------|--------|
| Introduction | X | Y | Z | ✓/✗ |
| Theory | X | Y | Z | ✓/✗ |
| Methods | X | Y | Z | ✓/✗ |
| Discussion | X | Y | Z | ✓/✗ |

---

## Unused Bib Entries

[List of bib keys not cited in paper]

**Recommendation**: [Which should be added where]

---

## Missing Citations to Add

| Literature | Missing Cite | Suggested Location |
|------------|--------------|-------------------|
| [Lit] | [Author Year] | [Section/paragraph] |

---

## Verdict

**Status**: [PASS / CONDITIONAL / FAIL]

**If CONDITIONAL/FAIL:**
- [Specific action 1]
- [Specific action 2]
```

## Integration with Pipeline

Add to Gate F alongside `/eval-limitations`:

```
STAGE 9: QUALITY CHECKS
  ├─ /eval-paper-quality (if rubric-eval available)
  ├─ /eval-limitations (REQUIRED)
  └─ /eval-citations (REQUIRED)
       ↓
     GATE F: Quality gate
       - Paper quality score ≥35/50 OR user override
       - Limitations section: PASS
       - Citations: ≥ minimum for target journal, no missing canonicals
```

## Common Failure Modes

**"Thin literature"**: Paper claims to engage a literature but only cites 2-3 papers. Fix: Add foundational papers and recent work.

**"Missing canonical"**: Paper engages P-E fit but doesn't cite Kristof-Brown et al. (2005) meta-analysis. Reviewers will notice. Fix: Add the obvious cites.

**"Orphan bib"**: References.bib has 50 entries but paper only uses 20. Fix: You already have the citations—use them.

**"Stale literature"**: All citations are 15+ years old. Fix: Add recent papers showing the literature is still active.

**"Citation padding"**: 150 citations but most are tangential. Fix: Cut padding, ensure depth on claimed literatures.

## After You're Done

Tell the user:
- Total citation count vs. target
- Which literatures have adequate vs. thin coverage
- Specific missing canonical cites to add
- Whether unused bib entries should be incorporated

## Why This Wasn't Caught Before

The other theory-forge evaluations focus on:
- **Zuckerman**: Is the framing compelling? (Says nothing about citation depth)
- **Becker**: Is the theory generalizable? (Tests abstraction, not grounding)
- **Genre**: Is the epistemology appropriate? (Checks framing style, not coverage)
- **Paper Quality**: Is the argument clear? (Execution, not scholarly apparatus)

None of these explicitly check whether the paper has *enough* citations or whether claimed literatures are *adequately covered*. A paper can score well on all four and still be under-cited.

This check fills that gap.
