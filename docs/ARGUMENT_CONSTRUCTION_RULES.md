# Argument Construction Rules

> **Source**: Extracted from mechanical analysis of 9 exemplar papers across ASQ, Organization Science, ASR, and AMJ. These are conventions of the tradition, not stylistic preferences.
>
> **Companion document**: For the competency/assessment side, see `research-quals/competencies/foundation-argument-construction.md`.

---

## 1. Paragraph-Level Rules

### 1.1 Topic Sentences

Every paragraph opens with a **claim** — a contestable statement that the paragraph will support.

**Do**:
- "Organizations are torn between new and familiar technologies."
- "Prior research does not provide much insight into how organizations manage this problem."
- "This problem is likely more pervasive and significant than we know."

**Don't**:
- ~~"Barley (1990) argued that technology shapes structure."~~ (citation-first)
- ~~"In this section, we review the literature on..."~~ (narration)
- ~~"Several scholars have studied how technology affects work."~~ (vague, no claim)
- ~~"According to Thompson (1967), organizations face interdependence."~~ (attribution-first)

**Detection patterns**:
```
# Citation-first paragraph (SOFT VIOLATION)
^\s*\([A-Z][a-z]+                     # Opens with (Author
^\s*[A-Z][a-z]+\s+\(\d{4}\)          # Opens with Author (year)
^\s*[A-Z][a-z]+\s+and\s+[A-Z].*\(\d  # Opens with Author and Author (year)
^\s*According to\s+[A-Z]              # "According to Author"
```

**Exception**: Definitional paragraphs in theory sections may open with an attributed concept when the attribution IS the claim: "Power (1997) termed the 'audit explosion'..." Here the claim is that Power coined this concept and it's the right frame.

### 1.2 Evidence and Elaboration

Middle sentences support the topic sentence's claim specifically.

**Two modes**:
- **Parenthetical citation stacks**: For consensus claims. "(Barley, 2015; Lifshitz-Assaf, 2018; Bailey et al., 2010)." Volume IS the argument — 3-6 citations signals "many people agree."
- **Author-in-prose engagement**: For exemplar studies that get 2-5 sentences of narrative treatment. "Leonardi's (2011) study showed that engineers assessed whether the technology enabled or constrained their next project." Signals "this particular study deserves attention."

**Rules**:
- Evidence must connect to the topic sentence's claim — if you can delete the topic sentence and the evidence still makes sense, it's disconnected
- ≥2 substantive citations per paragraph after the introduction's opening hook
- Direct quotes: 1-3 per theory section, reserved for key definitions and foundational formulations. Always with page numbers.

### 1.3 Clincher Sentences

Every paragraph's final sentence does one of three things:

1. **Names a concept** the next paragraph will pick up
2. **Draws an analytical conclusion** bounded by the evidence just presented
3. **Poses an implicit question** that the next paragraph answers

**Do**:
- "Allocating resources across a technological portfolio is therefore likely to be a perennial problem marked by significant inefficiency." (analytical conclusion)
- "...powerful, unidentified mechanisms may preserve outcomes despite these challenges." (implicit question)

**Don't**:
- Just stop after the last piece of evidence
- Repeat the topic sentence verbatim
- Introduce an entirely new idea in the clincher

---

## 2. Transition Rules

### 2.1 Lexical Repetition + Conceptual Escalation

The **last key concept** of paragraph N appears in the **first sentence** of paragraph N+1, with a new dimension added.

**Examples**:
- P1 clincher: "...a dynamic portfolio of technologies." → P2 topic: "Technological portfolios present a significant challenge..."
- P2 clincher: "...a perennial problem." → P3 topic: "This technological portfolio problem is likely more pervasive and significant than we know."
- Theory section clincher: "...the transparency paradox." → Discussion opening: "To untangle the transparency paradox..."

**Test**: Read only the first sentence of every paragraph in sequence. If you can follow the argument, the transitions work. If not, identify where the thread breaks.

### 2.2 "The Turn"

The single moment where the argument pivots from "what we know" to "what we don't know."

**Mechanics**:
- One adversative conjunction: "However," "Nonetheless," "But," "Nevertheless," "Yet"
- Placed at the start of a SHORT sentence or paragraph
- Follows a LONGER consensus-building passage
- The length contrast itself creates rhetorical emphasis

**Example** (Bernstein 2012):
> [Long paragraph building the case for transparency's benefits, heavily cited]
>
> "Nonetheless, the implications for organizational performance of transparency remain surprisingly unstudied."

**Rules**:
- One Turn per introduction. Multiple turns dilute argumentative force.
- The Turn word should be precise, not decorative. Don't use "However" mid-paragraph for minor qualifications.
- After The Turn, the argument never goes back to consensus — it moves forward into gap, question, and preview.

### 2.3 Between Subsections

Use the last sentence of one subsection and the first sentence of the next to create a bridge:
- **Parallel construction**: Repeat the structural pattern with new content
- **Explicit contrast**: "Stakeholder-based accountability pressures are enacted by constituents who are generally known... With the emergence of social media, different accountability pressures are produced..."

---

## 3. Section-Level Architecture

### 3.1 Introduction Arc

**Invariant sequence**: WORLD → PROBLEM → GAP → QUESTION → PREVIEW

| Step | Function | Citation behavior |
|------|----------|------------------|
| WORLD | Establish phenomenon or dominant understanding | Consensus-building (parenthetical stacks) |
| PROBLEM | Deepen the problem's scope and stakes | Mixed: consensus + escalation |
| GAP | Show what prior research has NOT addressed | Showing absence (negative citations) |
| QUESTION | State research question or purpose | Typically uncited (author's assertion) |
| PREVIEW | Preview study and findings | Light citation to methods tradition |

**Pacing by journal**:
- ASR: Steps 1-3 in 1-2 paragraphs (compressed)
- ASQ: Steps 1-3 across 3-4 paragraphs (extended)
- Organization Science: 2-3 paragraphs typical

**Three opening sentence templates**:
1. **Broad Declarative**: Short, punchy, uncited claim the reader already believes. "Organizations are torn between new and familiar technologies."
2. **Trend Claim**: Names a contemporary movement, cited. "In the past decade, two major structural developments intersected."
3. **Literary/Narrative Hook**: Epigraph, analogy, or story. Rare — use when you have a memorable frame the entire paper will orbit.

**Gap statement rules**:
- Name the prior literature specifically
- State what it has NOT done (not "more research is needed")
- The absence must be about process or mechanism
- Gap claims are author assertions, typically uncited

**Detection patterns for bad introductions**:
```
# Literature-first opening (SOFT VIOLATION)
^(Prior|Previous|Existing|Past)\s+(research|work|studies|literature)
^(The|A)\s+literature\s+on
^(Scholars|Researchers|Studies)\s+have\s+(long\s+)?(shown|found|argued)
```

### 3.2 Theory / Literature Review

**Three organizational logics** (choose one):

| Logic | Structure | When |
|-------|-----------|------|
| By research stream | 2-3 streams → synthesis showing shared blind spot | Your contribution sits at intersection of literatures |
| By concept/category | Types of phenomenon → introduce new type | You're extending a taxonomy |
| By funnel | Broad → narrow → specific intersection → gaps | You need multiple context layers |

**Universal move: Consensus-then-complicate**
1. Build the consensus (dense parenthetical citations)
2. Pivot with adversative conjunction ("however," "yet," "but")
3. State what the consensus misses

**Subsection structure**:
- **Opening**: Definitional or consensus claim with 2-4 foundational citations
- **Middle**: 1-2 exemplar studies in author-in-prose (2-5 sentences each)
- **Closing**: Name limitation, complicate findings, or bridge to next subsection

**End of theory section** (3 rapid-fire moves in final paragraph):
1. Restate the gap in one sentence
2. Assert importance in one sentence
3. Introduce the empirical case — "study," "case," or "field" bridges to Methods

### 3.3 Discussion

**Opening move** — reconnect to the introduction's puzzle:
- **Puzzle-Contrast-Finding**: Name the paradox/gap, contrast theory's prediction with what happened, state what the study found
- **Method-to-Finding Declaration**: Open with what the analytical approach revealed

**Contribution structure** (2-4 per paper, typically 3):
Each contribution paragraph:
1. **Literature anchor**: "Existing work on X has shown/assumed Y"
2. **Contrast/extension**: "This study shows that..." or "Our findings complicate this by..."
3. **Mechanism**: The specific process or dynamic discovered
4. **Implication**: "This suggests that..." or "Scholars would do well to..."
5. **Optional handoff**: "Future research should/might..."

**Limitations**: Framed as boundary conditions, not flaws.
- Acknowledge in one sentence
- Immediately pivot to why it doesn't undermine the theory, or why it creates future work
- Common framing: scope conditions of the setting, then argument for broader applicability

**Closing paragraph**:
- NEVER a summary
- Two types:
  - **Grand Zoom-Out**: Connect to larger trajectory, invoke the future, gesture at paradox
  - **Pithy Paradox Restatement**: Core tension in 2-3 memorable sentences
- Final sentence should be quotable — parallelism, paradox, or evocative language

**Detection patterns for bad closings**:
```
# Summary-closing (SOFT VIOLATION)
^(In\s+)?(this|our)\s+paper,?\s+we\s+(have\s+)?(examined|explored|investigated|studied)
^(In\s+)?summary,?\s+(this|our)\s+(paper|study|research)
^(To\s+)?(summarize|conclude),?\s+we\s+have
```

---

## 4. Citation Deployment Rules

### 4.1 Four Structural Functions

| Function | Signal | Deployment |
|----------|--------|------------|
| **Consensus-building** | "Many agree on this" | 3-8 parenthetical citations stacked |
| **Steelman-building** | "The strongest case for the position I'll challenge" | Author-in-prose, engaging their argument |
| **Showing absence** | "Nobody has studied X" | Citing what was studied to highlight what wasn't |
| **Creating tension** | "These two sets of findings conflict" | Two citation clusters deployed against each other |

### 4.2 Function Shifts Across Sections

| Section | Dominant functions |
|---------|-------------------|
| Introduction (early) | Consensus-building |
| Introduction (mid) | Steelman-building |
| Introduction (gap) | Showing absence |
| Introduction (question) | Creating tension (optional) |
| Theory section | All four, with consensus dominant |
| Discussion | Consensus (to establish baseline), then contrast with findings |

### 4.3 Anti-Patterns

- **All-parenthetical**: No engagement with any individual work → thin
- **All-in-prose**: Every citation gets 3 sentences → exhausting, no efficiency
- **Citation-as-decoration**: Dropped in to prove you read, not to build argument
- **Overcitation**: 15+ citations after one claim → signals insecurity
- **Undercitation**: <2 substantive citations per paragraph in theory section → thin

### 4.4 Direct Quote Rules

- 1-3 per theory section maximum
- Reserved for: key definitions, foundational formulations, concepts you'll build on
- Always with page numbers
- Must be preceded by analytical framing (never dropped in cold)
- Maximum 80 words per quote

---

## 5. Quick Reference: Section-by-Section Checklist

### Before Writing Each Paragraph
- [ ] Does the first sentence make a claim (not cite, not describe)?
- [ ] Does the evidence specifically support that claim?
- [ ] Does the last sentence set up the next paragraph or draw a conclusion?

### Before Writing Each Section Transition
- [ ] Does the first sentence of the new section pick up a concept from the last sentence of the previous one?
- [ ] Is the new section advancing the argument (not just continuing it)?

### Introduction Complete?
- [ ] Opens with Broad Declarative, Trend Claim, or Literary Hook (not literature review)
- [ ] Arc follows WORLD → PROBLEM → GAP → QUESTION → PREVIEW
- [ ] Gap statement specifies missing process/mechanism (not "more research needed")
- [ ] One clear Turn with adversative conjunction
- [ ] Citation functions shift from consensus → steelman → absence → tension

### Theory Section Complete?
- [ ] Organized by stream, category, or funnel (not random)
- [ ] Consensus-then-complicate move present
- [ ] At least one exemplar study engaged in prose (2-5 sentences)
- [ ] Final paragraph: gap → importance → case introduction

### Discussion Complete?
- [ ] Opens by reconnecting to introduction's puzzle
- [ ] Each contribution: literature anchor → contrast → mechanism → implication
- [ ] Limitations framed as boundary conditions
- [ ] Closing paragraph: zoom-out or paradox restatement (NOT summary)
- [ ] Final sentence is crafted to be memorable
