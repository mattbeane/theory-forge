"""
Prompt templates for manuscript generation.

Contains the core prompts injected into section writers and paragraph fixers.
"""

# System prompt for section writer
SECTION_WRITER_SYSTEM = """You are writing a section of an academic paper targeting a top management journal (Organization Science, Management Science, or Administrative Science Quarterly).

## ABSOLUTE RULES (violating these will cause rejection and rewrite)

1. NO BULLET POINTS - Ever. Not for lists, not for contributions, not for anything.
   Convert all lists to flowing prose.

2. NO NUMBERED LISTS - Ever. Not "1. First..." Not "(a) ..." Not "i) ..."
   Weave sequential points into narrative paragraphs.

3. CONTRIBUTIONS AS NARRATIVE - Never "This paper makes three contributions: First..."
   Instead: "This research extends X by showing Y. We demonstrate that..."

4. INTERPRET ALL STATISTICS - Every quantitative result must be followed (within 2 sentences)
   by substantive interpretation. What does it mean? Why does it matter?
   Bad: "β = 0.21, p < .001."
   Good: "β = 0.21, p < .001—nearly twice the response shown by full-time workers.
         This gap reveals that..."

## STYLE GUIDELINES

VOICE:
- Use active voice: "We find" not "It was found"
- Be direct: "We show" not "This may suggest"
- First person plural for coauthored papers
- Confident about empirical claims, humble about theoretical extensions

QUOTES:
- Each quote is a polished gem—use sparingly, make each one count
- Prefer colorful quotes: profanity, bluntness, colloquialisms are assets
- Quotes should sound like a real person said them
- Always precede quotes with analytical claim (EXCEPT at paper/section opening—cold opens permitted sparingly)
- Keep quotes under 80 words; trim to essential content

STRUCTURE:
- Paragraphs flow into each other
- Rhetorical questions can serve as transitions
- Theoretical claims emerge from reasoning, not as numbered propositions

REGISTER:
- Academic but not stiff
- Occasional colloquialism is fine
- Match the target journal's expectations

## PAPER TYPE: {paper_type}

{paper_type_guidance}
"""

QUANT_FORWARD_GUIDANCE = """This is a QUANT-FORWARD paper. The quantitative analysis is the main tentpole; qualitative data illuminates mechanisms.

- Lead with quantitative findings when presenting results
- Tables and figures can be prominent
- Statistical claims can open paragraphs
- BUT: always interpret, always connect to theory
- Qualitative evidence explains WHY the patterns exist
- The "econ-y" feel is appropriate for empirics, but theoretical framing must still read as management theory
"""

QUAL_FORWARD_GUIDANCE = """This is a QUAL-FORWARD paper. Ethnographic evidence is primary; quantitative data (if any) supports.

- Lead with observed patterns and quotes
- Tables are supplementary
- Extended narrative development
- Quotes do heavy lifting as primary evidence
- More space for setting description and observational detail
"""


# Prompt for paragraph fixer
PARAGRAPH_FIXER_PROMPT = """The following paragraph violates a style rule for top management journals.

## PARAGRAPH TO FIX:
{paragraph}

## VIOLATION:
{violation_type}: {violation_message}

{violation_suggestion}

## EXEMPLAR OF CORRECT STYLE:
{exemplar}

## INSTRUCTIONS:
Rewrite the paragraph to fix ONLY this violation.
- Preserve all content and meaning
- Do not introduce new violations
- Do not add content that wasn't there
- Match the style shown in the exemplar

Return ONLY the rewritten paragraph, nothing else.
"""


# Prompt for section-level review
SECTION_REVIEW_PROMPT = """Review this draft section for style compliance with top management journals.

## SECTION: {section_name}

## DRAFT:
{section_text}

## SECTION REQUIREMENTS:
- Word count target: {min_words}-{max_words}
- Quote budget: {quote_min}-{quote_max}
- Required elements: {required_elements}

## CHECK FOR:

1. HARD VIOLATIONS (must fix):
   - Any bullet points
   - Any numbered lists
   - Contribution claims as lists

2. SOFT VIOLATIONS (flag):
   - Excessive passive voice
   - Quotes without setup (except cold opens)
   - Orphaned statistics (no interpretation)
   - Long quotes (>80 words)
   - Missing required elements

3. COHERENCE:
   - Does the section flow?
   - Are transitions smooth?
   - Is the argument clear?

## OUTPUT FORMAT:

HARD VIOLATIONS: [list any found, or "None"]
SOFT VIOLATIONS: [list any found, or "None"]
MISSING ELEMENTS: [list any, or "None"]
COHERENCE NOTES: [brief assessment]
RECOMMENDED FIXES: [specific, actionable suggestions]
"""


# Prompt for generating alternative openings
OPENING_ALTERNATIVES_PROMPT = """Generate two alternative openings for this paper, one using each hook type.

## PAPER SUMMARY:
{paper_summary}

## KEY FINDING:
{key_finding}

## BEST AVAILABLE QUOTE (for cold open):
{best_quote}

---

## OPTION A: THEORETICAL PUZZLE OPENING

Write an opening paragraph (150-200 words) that:
- Leads with a theoretical tension or gap
- Frames the contribution as extending scholarly understanding
- Does NOT lead with empirical findings
- Positions the paper as joining a conversation

## OPTION B: EMPIRICAL SURPRISE OPENING

Write an opening paragraph (150-200 words) that:
- Leads with the surprising empirical finding
- May use a cold open (quote first) if the quote is perfect
- Establishes "conventional wisdom was wrong"
- Creates immediate engagement through surprise

---

Provide both options. The author will choose which fits the paper better.
"""


# Quote selection guidance (injected into findings prompts)
QUOTE_SELECTION_GUIDANCE = """
## QUOTE SELECTION

When selecting quotes from interview data, prefer:

1. COLORFUL LANGUAGE: Profanity, bluntness, colloquialisms are assets, not liabilities.
   Real humans don't speak in sanitized academic-ese.

2. VOICE: You should be able to hear the speaker. Quotes that could have been
   written by anyone are weak. Quotes that sound like *this specific person* are strong.

3. NORM-VIOLATING: Surprising statements, counterintuitive observations, things that
   make the reader go "wait, really?"

4. COMPRESSED INSIGHT: The quote distills a mechanism or finding into vivid form.
   It does the work of a paragraph in a sentence.

BAD QUOTE: "We found the implementation process to be challenging but ultimately
beneficial for our operational efficiency."

GOOD QUOTE: "Once I hit that threshold, I'm done. So we actually—there's at least
a theory that some of our incentives may actually have made our attendance worse."

Each quote is a polished gem. Fewer, better quotes beat more, adequate quotes.
"""


# Cold open guidance
COLD_OPEN_GUIDANCE = """
## COLD OPEN (use sparingly)

A cold open begins with raw data—a quote that perfectly distills the core phenomenon.
It creates an "oh, this is real life" feeling before any analytical framing.

RULES:
1. The quote must encapsulate the paper's central puzzle or finding
2. Immediately follow (within 1-2 sentences) with analytical framing
3. Maximum: one cold open per paper, maybe one per major section
4. Only use when you have a quote SO perfect it would be a crime to bury it

EXAMPLE:
"Telling them now that you got robotics here, they'll all leave."

This prediction—offered by a warehouse operations manager—reflects conventional
wisdom about worker response to automation. Yet we observed the opposite...

Do NOT use a cold open just because it's permitted. Use it when you have a
quote so striking that it must lead.
"""
