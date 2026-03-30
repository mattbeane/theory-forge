---
name: eval-citations
description: /eval-citations - Citation Coverage Check
---

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

### Step 6: Check Venue Quality (Peer-Review Gate)

For each citation that appears in the **theory section's core argument** (not just parenthetical background cites), verify it is from a peer-reviewed venue.

**Peer-reviewed (OK for core theory scaffolding):**
- Top-tier journals (ASQ, OrgSci, AMJ, AMR, ASR, ManSci, SMJ, etc.)
- Specialty journals (ILR Review, Research Policy, JOM, etc.)
- Annual Reviews series
- Peer-reviewed conference proceedings (if clearly marked)

**NOT peer-reviewed (flag if used as core theoretical foundation):**
- Harvard Business Review, Sloan Management Review, California Management Review (practitioner outlets)
- Working papers / NBER working papers (not yet through review)
- Book chapters (varies — check if the volume was peer-reviewed)
- Edited volumes without peer review
- Reports, white papers, policy briefs

**How to check:**
1. Identify the 5-10 citations that do the heaviest theoretical lifting (i.e., the ones the argument couldn't stand without)
2. For each, verify the venue is peer-reviewed
3. Flag any non-peer-reviewed source used as core scaffolding

**What to flag:**
- A theory section that rests on an HBR article as its primary framework
- A mechanism derived from a working paper
- A "canonical" citation that's actually a practitioner piece

**What's OK:**
- Non-peer-reviewed sources as supplementary context ("as Ferdows (1997) noted in HBR...")
- Practitioner sources cited for empirical facts or industry context in the Methods section
- Working papers cited alongside published versions of the same work
- Classic books (March & Simon 1958, Thompson 1967) that predate modern peer review norms

**Verdict:**
- If any core theoretical citation is non-peer-reviewed with no peer-reviewed substitute available → FLAG
- Suggest peer-reviewed alternatives or reframe the citation as supplementary rather than foundational

### Step 7: Literature-Specific Canonical Checks

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

### Step 8: Literature Depth Check (Discussion)

For each literature *named* in the discussion section, verify that the paper cites canonical works from that literature's core.

**Why this matters**: Papers often name literatures in the discussion ("our findings contribute to the literature on organizational learning") without citing the canonical works that define those literatures. Reviewers who work in those literatures will notice immediately.

**Process**:
1. Identify every literature stream explicitly named in the discussion (e.g., "organizational learning," "ambidexterity," "knowledge transfer")
2. For each named literature, check whether the paper cites at least 3 canonical works from that literature's core
3. Use the canonical works reference below, plus domain knowledge

**Canonical Works by Major Literature Stream**:

| Literature | Canonical Works (minimum expectations) |
|-----------|---------------------------------------|
| Organizational Learning | March (1991); Levitt & March (1988); Argote (2013); Huber (1991) |
| Ambidexterity | March (1991); Tushman & O'Reilly (1996); Gibson & Birkinshaw (2004); Raisch & Birkinshaw (2008) |
| Productivity Paradox | Solow (1987); Brynjolfsson (1993); Brynjolfsson & Hitt (1998) |
| Knowledge Transfer | Argote & Ingram (2000); Szulanski (1996); Hansen (1999); Reagans & McEvily (2003) |
| Routines | Nelson & Winter (1982); Feldman & Pentland (2003); Pentland & Rueter (1994) |
| Institutional Theory | DiMaggio & Powell (1983); Meyer & Rowan (1977); Scott (2014); Thornton et al. (2012) |
| Sensemaking | Weick (1995); Weick et al. (2005); Maitlis & Christianson (2014) |
| Identity (Organizational) | Albert & Whetten (1985); Gioia et al. (2000); Ravasi & Schultz (2006) |
| Identity (Individual/Work) | Ibarra (1999); Pratt et al. (2006); Caza et al. (2018) |
| Technology & Work | Orlikowski (1992, 2007); Barley (1986); Zuboff (1988); Bailey & Barley (2020) |
| Expertise & Skill | Dreyfus & Dreyfus (1986); Ericsson et al. (1993); Lave & Wenger (1991); Beane (2019) |
| Occupations & Professions | Abbott (1988); Anteby et al. (2016); Bechky (2003) |

**Note**: This list is not exhaustive. Use domain knowledge to identify canonical works for literatures not listed. When uncertain, check whether the cited works are foundational (introduced the concept), landmark (shaped the field), or recent-canonical (major reviews/meta-analyses).

**Scoring**:
- **PASS**: Every literature named in the discussion cites 3+ canonical works from its core
- **CONDITIONAL**: Any named literature has <3 citations from its canon
- **FAIL**: A literature is named in the discussion with zero canonical citations

**Output for this step**: Add a "Discussion Literature Depth" section to the report:

```markdown
## Discussion Literature Depth

| Literature Named in Discussion | Canonical Cites Found | Count | Status |
|-------------------------------|----------------------|-------|--------|
| [Literature 1] | [Author Year], [Author Year], [Author Year] | 3 | PASS |
| [Literature 2] | [Author Year] | 1 | CONDITIONAL |
| [Literature 3] | None | 0 | FAIL |

**Verdict**: [PASS / CONDITIONAL / FAIL]

**Missing canonical cites to add**:
- [Literature]: Add [Author Year] — [Why canonical]
- [Literature]: Add [Author Year] — [Why canonical]
```

Incorporate this verdict into the overall citation evaluation. If the literature depth check is CONDITIONAL, the overall citation eval cannot be higher than CONDITIONAL.

---

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
| Core theory cites from peer-reviewed venues | N/N | 100% | ✓/✗ |
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

## Venue Quality: Core Theory Citations

| Citation | Role in Argument | Venue | Peer-Reviewed? | Status |
|----------|-----------------|-------|----------------|--------|
| [Author Year] | [Core scaffolding / Supporting] | [Journal/Outlet] | Yes/No | ✓/FLAG |

**Flagged non-peer-reviewed core citations:**
- [Author Year] — [Venue] — [Why it's core] — [Peer-reviewed alternative if available]

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
       - Paper quality score ≥40/50 OR user override
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

---

For consensus mode behavior, see [../../_shared/consensus-mode.md](../../_shared/consensus-mode.md)
For staleness detection, see [../../_shared/staleness-check.md](../../_shared/staleness-check.md)
For eval result persistence, see [../../_shared/eval-persistence.md](../../_shared/eval-persistence.md)

### Skill-Specific Persistence

- **eval_results key**: `citations`
- **Upstream files**: `analysis/manuscript/DRAFT.md`, `analysis/framing/frame-{N}/FRAMING_OPTIONS.md`
- **Scores**: `total_cited`, `missing_critical`, `coverage_score`
- **Verdict**: PASS if coverage_score >= threshold; FAIL otherwise
- **Default consensus N**: 5
