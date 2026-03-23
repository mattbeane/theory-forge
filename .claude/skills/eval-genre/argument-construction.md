## Argument Construction Check

Genre and register checks catch framing problems. This section catches **structural argument failures** — the mechanical construction errors that make even well-framed papers hard to follow. See `docs/ARGUMENT_CONSTRUCTION_RULES.md` for the full rule set.

### Steps for Argument Construction Check

10. **Check paragraph openings**
    - Sample 10+ paragraphs across all sections
    - Does each open with a CLAIM (contestable statement)?
    - Flag citation-first openings: "Author (Year) argued..." or "(Author, Year) found..."
    - Flag narration openings: "In this section, we..." / "Before presenting X, we establish Y" / "We now turn to..."
    - Flag vague openings: "Several scholars have studied..."
    - **Findings section specific:** Opening sentences of findings subsections must state the finding directly, not narrate the paper's structure
    - BAD: "Before presenting quantitative patterns, we establish that role differentiation is deliberate"
    - BAD: "We now present evidence that managers assign roles"
    - GOOD: "Facility role differentiation was deliberate rather than emergent"
    - GOOD: "Managers explicitly coordinated facility learning roles"
    - Rationale: Meta-narration ("we establish," "we present evidence") puts the author's process center stage instead of the finding itself. The reader should encounter claims about the world, not descriptions of what the paper does.
    - Exception: Cold opens (max 1-2 paragraphs) may lead with data/quotes

11. **Check transitions between paragraphs**
    - Sample 5+ paragraph boundaries
    - Does the last key concept of paragraph N appear in the first sentence of paragraph N+1?
    - Flag topic jumps where consecutive paragraphs introduce unconnected concepts
    - Check for "The Turn": Is there exactly ONE adversative pivot (However/But/Yet) from consensus to complication?

12. **Check introduction arc**
    - Does it follow WORLD → PROBLEM → GAP → QUESTION → PREVIEW?
    - Is the gap about a missing process/mechanism (not "more research needed")?
    - Does citation function shift across the arc (consensus → steelman → absence → tension)?

13. **Check discussion structure**
    - Does it open by reconnecting to the introduction's puzzle?
    - Does each contribution paragraph follow: literature anchor → contrast → mechanism → implication?
    - Does the final paragraph zoom out or restate paradox (NOT summarize)?
    - Is the final sentence quotable?

14. **Check citation deployment**
    - Are consensus claims backed by parenthetical stacks (3-6 citations)?
    - Are key works engaged in prose (2-5 sentences), not just cited?
    - Are gap claims typically uncited (author's own assertion)?
    - Are direct quotes reserved for definitions, with page numbers?

15. **Check paragraph granularity**
    - Sample paragraphs across all sections (intro, theory, methods, findings, discussion)
    - Flag any single-sentence paragraphs (except block quotes or table/figure notes)
    - Flag two-sentence paragraphs that lack substantive development
    - OrgSci / ASQ style: Every paragraph should develop an idea across at minimum 3 sentences (claim, evidence/reasoning, implication or transition)
    - Exception: A single short transitional sentence between major sections is acceptable if it serves as a signpost, but should be folded into the preceding or following paragraph where possible
    - Rationale: Short paragraphs signal underdeveloped ideas and read as listicle-style prose, which is inappropriate for top organizational journals

16. **Check section titles for argument-advancing quality**
    - Theory/lit review section title should name **the existing scholarly conversation** the paper enters — the research area or problem space the literature addresses — NOT the paper's contribution or finding
    - BAD: "Theoretical Background," "Literature Review," "Theory" (generic containers)
    - BAD: "Distributed Learning Across Sites" (names the contribution, not the conversation)
    - GOOD: "Managing Exploration and Exploitation in Multi-Unit Organizations" (names the problem space)
    - GOOD: "Alignment of Technology and Structure" (Barley 1990 — names the scholarly conversation)
    - GOOD: "Relevant Perspectives on Careers" (O'Mahoney & Bechky 2006 — names the literature streams)
    - Findings/results section title should **describe the empirical terrain or phenomenon** without revealing the theoretical punchline
    - BAD: "Findings," "Results" (generic containers — acceptable but signals missed opportunity)
    - BAD: "How Firms Distribute Learning" (front-loads the contribution)
    - GOOD: "Facility Roles in Automation Implementation" (names what's covered without stating the conclusion)
    - GOOD: "Types of Virtual Work" (Bailey/Barley/Leonardi — descriptive, not conclusory)
    - GOOD: "Problem Construction" (Leonardi 2011 — names the phenomenon)
    - **Findings subsection titles** should be **declarative findings**, not meta-narration about what kind of evidence follows
    - BAD: "Evidence of deliberate role assignment" (describes the evidence type, not the finding)
    - BAD: "Quantitative patterns in facility outcomes" (describes what the section contains)
    - GOOD: "Facilities were deliberately assigned roles" (states what was found)
    - GOOD: "Three facility role clusters emerged" (declarative)
    - Rationale: Subsection titles in findings are micro-claims. Each one should tell the reader what the paper discovered, not what kind of evidence they're about to see. "Evidence of X" is a container; "X happened" is a finding.
    - Rationale: In top OrgSci/ASQ papers, section titles are argument-advancing, not containers. They compress the paper's intellectual terrain into a phrase. Generic titles ("Theoretical Background," "Findings") waste the reader's attention and signal boilerplate structure rather than directed argumentation.
    - Exception: "Theoretical Background" is used occasionally (Leonardi 2011) — flag as WEAK rather than FAIL

### Argument Construction Output (add to GENRE_EVAL.md)

```markdown
