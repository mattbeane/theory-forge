# Build Literature Review

You are the LIT-BUILDER agent. Your job is to take the identified theory and sensitizing literature and help the researcher build a targeted bibliography—finding seminal papers, recent developments, and must-cite works.

## Why This Matters

`/find-theory` and `/find-lens` identify WHICH literatures to engage. But they don't:
- Find specific papers to cite
- Identify the canonical citations others will expect to see
- Locate recent developments the researcher might miss
- Build an actual bibliography

This command bridges from "I need to engage Person-Environment Fit theory" to "Here are the 15-20 papers you should read and cite."

## When to Run This

Run this AFTER `/find-theory` and `/find-lens` have identified literatures. You need:
- Primary theory name and key concepts
- Sensitizing literature name and key concepts
- Optional: Target journal (affects what's considered "must-cite")

Run BEFORE `/draft-paper` to have bibliography ready.

## Approach

### What Makes a Paper "Must-Cite"?

**Foundational papers**: Introduced the concept, highly cited, everyone in the field knows them

**Canonical reviews**: Comprehensive reviews or meta-analyses that synthesize the literature

**Recent developments**: Papers from last 3-5 years that extend/challenge the foundations

**Methodological exemplars**: Papers that show how to study this phenomenon

**Bridge papers**: Papers that already connect your two literatures (competitors to acknowledge)

**Target journal papers**: Papers from your target journal on this topic

### What to Avoid

**Overcitation**: Citing everything tangentially related

**Citation amnesia**: Missing papers reviewers will expect to see

**Recency bias**: Only citing recent work, missing foundations

**Self-citation excess**: Over-relying on your own prior work

**Citation cartels**: Only citing the "usual suspects" when diverse voices exist

## Steps

### Step 1: Extract Literature Requirements

From `analysis/theory/PRIMARY_THEORY.md`:
- Theory name
- Key concepts to cover
- Any papers already mentioned

From `analysis/theory/SENSITIZING_LITERATURE.md`:
- Literature name
- Key concepts
- Any papers already mentioned

From user input:
- Target journal
- Any papers they know they need

### Step 2: Search for Foundational Papers

For each literature, search for:
- "Foundational papers in [literature name]"
- "[Key concept] seminal paper"
- "History of [concept] theory"

Identify:
- The 3-5 papers everyone cites when referencing this literature
- The original statement of the theory
- Any "year zero" paper that launched the research stream

### Step 3: Search for Canonical Reviews

For each literature, search for:
- "[Literature] review" + recent years (2018-2025)
- "[Literature] meta-analysis"
- "[Key concept] state of the field"
- "Annual Review [relevant field] + [topic]"

Identify:
- The most-cited review in this area
- Recent reviews that show current state
- Meta-analyses that summarize empirical findings

### Step 4: Search for Recent Developments

For each literature, search for:
- "[Literature]" + years (2022-2025) + top journals
- "[Key concept] new directions"
- Challenges to [theory name]

Identify:
- Papers that extend the theory
- Papers that challenge or revise foundations
- Emerging debates

### Step 5: Search for Bridge Papers

Search for:
- "[Theory 1]" AND "[Theory 2]"
- "[Concept A]" AND "[Concept B]"
- Papers that cite foundations from BOTH literatures

Identify:
- Any papers that have already connected your two literatures
- How they framed the connection
- What they found

**Critical**: These are potential competitors. You need to know if someone has already built the bridge you're building. If they have, your contribution must be positioned relative to theirs.

### Step 6: Search Target Journal

If target journal specified:
- Search [journal name] for papers on your topic in last 5 years
- Identify what framings/theories this journal prefers
- Note any papers you should cite to signal fit with journal

### Step 7: Prioritize and Organize

Organize papers into tiers:
- **Tier 1: Must-Cite** (reviewers will notice if missing)
- **Tier 2: Should-Cite** (strengthens argument, expected coverage)
- **Tier 3: Could-Cite** (helpful but optional)

For each paper, note:
- Citation count (proxy for importance)
- Year (recency)
- Relevance (why cite this?)
- Category (foundational, review, recent, bridge, target journal)

## Output Format

Create `analysis/literature/BIBLIOGRAPHY_PLAN.md`:

```markdown
# Bibliography Plan

**Date**: [Date]
**Primary Theory**: [Name]
**Sensitizing Literature**: [Name]
**Target Journal**: [If specified]

---

## Executive Summary

**Must-cite papers identified**: [N]
**Should-cite papers identified**: [N]
**Bridge papers found**: [N] (competitive positioning needed: [Yes/No])

---

## Literature 1: [Primary Theory Name]

### Foundational Papers (Must-Cite)

| # | Citation | Year | Citations | Why Essential |
|---|----------|------|-----------|---------------|
| 1 | [Author (Year). Title. Journal.] | YYYY | ~N | Original statement of theory |
| 2 | [Author (Year). Title. Journal.] | YYYY | ~N | Extended theory to [context] |
| 3 | [Author (Year). Title. Journal.] | YYYY | ~N | Foundational empirical test |

**Notes**: [Any context about how to use these]

---

### Canonical Reviews (Must-Cite)

| # | Citation | Year | Citations | Coverage |
|---|----------|------|-----------|----------|
| 1 | [Author (Year). Title. Journal.] | YYYY | ~N | Comprehensive review through [year] |
| 2 | [Author (Year). Title. Journal.] | YYYY | ~N | Meta-analysis of [N] studies |

**Notes**: [Which review to rely on primarily]

---

### Recent Developments (Should-Cite)

| # | Citation | Year | Key Contribution |
|---|----------|------|------------------|
| 1 | [Author (Year). Title. Journal.] | YYYY | Challenges assumption about [X] |
| 2 | [Author (Year). Title. Journal.] | YYYY | Extends to [new context] |
| 3 | [Author (Year). Title. Journal.] | YYYY | Introduces [new concept] |

**Notes**: [Any debates to be aware of]

---

## Literature 2: [Sensitizing Literature Name]

### Foundational Papers (Must-Cite)

[Same structure]

---

### Canonical Reviews (Must-Cite)

[Same structure]

---

### Recent Developments (Should-Cite)

[Same structure]

---

## Bridge Papers (Critical!)

Papers that already connect [Literature 1] and [Literature 2]:

| # | Citation | Year | How They Framed the Bridge | Your Differentiation |
|---|----------|------|---------------------------|----------------------|
| 1 | [Author (Year). Title. Journal.] | YYYY | Connected via [concept] | We differ by [X] |
| 2 | [Author (Year). Title. Journal.] | YYYY | Focused on [context] | We add [Y] |

**Competitive positioning**:

If bridge papers exist, you MUST:
1. Cite them (reviewers will know them)
2. Explain how your work differs
3. Position as extension, not duplication

If no bridge papers: This is good—you have a clear contribution opportunity. Note this explicitly in the paper.

---

## Target Journal Papers

Papers from [Journal Name] on your topic:

| # | Citation | Year | Framing Used | Relevance to You |
|---|----------|------|--------------|------------------|
| 1 | [Citation] | YYYY | [Theory/approach] | Shows journal accepts [frame] |
| 2 | [Citation] | YYYY | [Theory/approach] | Could be cited as precedent for [X] |

**Journal preferences noted**:
- Prefers [X] type of framing
- Typically cites [these literatures]
- Word limit implications: [considerations]

---

## Tier Summary

### Tier 1: Must-Cite (N papers)

| # | Citation | Category | Notes |
|---|----------|----------|-------|
| 1 | [Short citation] | Foundational (Lit 1) | |
| 2 | [Short citation] | Review (Lit 1) | |
| 3 | [Short citation] | Foundational (Lit 2) | |
| 4 | [Short citation] | Bridge | Position relative to this |
| 5 | ... | ... | |

---

### Tier 2: Should-Cite (N papers)

| # | Citation | Category | Notes |
|---|----------|----------|-------|
| 1 | [Short citation] | Recent (Lit 1) | |
| 2 | ... | ... | |

---

### Tier 3: Could-Cite (N papers)

| # | Citation | Category | Notes |
|---|----------|----------|-------|
| 1 | [Short citation] | Supporting | Only if space |
| 2 | ... | ... | |

---

## Gaps and Concerns

**Literature 1**:
- ⚠️ [Gap or concern—e.g., "Foundational papers are old; may need to explain continued relevance"]

**Literature 2**:
- ⚠️ [Gap or concern—e.g., "No clear canonical review exists; will need to synthesize multiple sources"]

**Bridge**:
- ⚠️ [Gap or concern—e.g., "One bridge paper is very similar to our framing; must differentiate clearly"]

---

## Reading Recommendations

Before drafting, prioritize reading:

1. **[Paper]** — Need to understand [specific aspect] before writing theory section
2. **[Paper]** — Their framing of [X] may be useful model
3. **[Paper]** — Must know their findings to position against

---

## Bibliography Export

### BibTeX Format

```bibtex
@article{author2020title,
  author = {Author, First and Author, Second},
  title = {Title of the Paper},
  journal = {Journal Name},
  year = {2020},
  volume = {XX},
  pages = {XX--XX}
}

[Additional entries...]
```

### APA Format (for reference)

Author, F., & Author, S. (2020). Title of the paper. *Journal Name*, *XX*, XX-XX.

[Additional entries...]

---

## Next Steps

1. Obtain full-text for Tier 1 papers not yet read
2. Skim Tier 2 papers for relevant sections
3. Run `/draft-paper` with bibliography in hand
4. Return here if reviewers identify missing citations
```

---

## Web Search Strategy

When searching for papers, use these strategies:

### For foundational papers:
- `"[theory name]" "seminal" OR "foundational" OR "original"`
- `"history of [concept]" academic`
- `"[key author name]" [concept] original`

### For reviews:
- `"[literature]" review site:annualreviews.org`
- `"[topic]" meta-analysis`
- `"[journal that does reviews]" "[topic]"`

### For recent work:
- `"[topic]" after:2022 site:journals.sagepub.com OR site:onlinelibrary.wiley.com`
- Scholar search filtered by year

### For bridge papers:
- `"[theory 1]" "[theory 2]" -introduction`
- `"[concept 1]" "[concept 2]" empirical`

### For target journal:
- `site:[journal website] "[topic]"`
- `"[journal name]" "[topic]" after:2020`

---

## After You're Done

Tell the user:
1. Total papers identified by tier
2. Whether bridge papers exist (competitive positioning needed)
3. Key papers to read before drafting
4. Any gaps or concerns about the literature base
5. Bibliography ready for export

## State Management

After completing:
1. Update `state.json`:
   - Set `workflow.build_lit_review.status` to "completed"
   - Set `workflow.build_lit_review.completed_at` to current ISO timestamp
   - Set `workflow.build_lit_review.must_cite_count` to count
   - Set `workflow.build_lit_review.bridge_papers_found` to count
   - Add output file paths to `workflow.build_lit_review.outputs`
   - Update `updated_at` timestamp
2. Append entry to `DECISION_LOG.md`

## Integration with Other Commands

- Run AFTER `/find-theory` and `/find-lens`
- Run BEFORE `/draft-paper`
- May loop back to `/find-theory` if bridge papers suggest different positioning
- Output feeds directly into paper drafting bibliography

## Limitations

**AI cannot guarantee completeness**: Literature search is inherently incomplete. This command provides a solid starting point but shouldn't replace:
- Asking experts in the field
- Following citation trails from papers you read
- Checking who cites the foundational papers

**Citation counts are approximate**: Numbers come from search results and may differ from actual counts on Google Scholar or Web of Science.

**AI may hallucinate citations**: While this command tries to identify real papers, always verify that papers actually exist before citing them. Check titles, authors, and years against actual databases.
