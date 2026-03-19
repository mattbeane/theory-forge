## Argument Construction Check

Genre and register checks catch framing problems. This section catches **structural argument failures** — the mechanical construction errors that make even well-framed papers hard to follow. See `docs/ARGUMENT_CONSTRUCTION_RULES.md` for the full rule set.

### Steps for Argument Construction Check

10. **Check paragraph openings**
    - Sample 10+ paragraphs across all sections
    - Does each open with a CLAIM (contestable statement)?
    - Flag citation-first openings: "Author (Year) argued..." or "(Author, Year) found..."
    - Flag narration openings: "In this section, we..."
    - Flag vague openings: "Several scholars have studied..."
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

### Argument Construction Output (add to GENRE_EVAL.md)

```markdown
