# Argument Construction Rules

> **Source**: Extracted from mechanical analysis of 9 exemplar papers across ASQ, Organization Science, ASR, and AMJ. These are conventions of the tradition, not stylistic preferences.
>
> **Related**: The separate [ResearchKit Quals](https://github.com/mattbeane/research-quals) project includes a draft competency definition for argument construction (`competencies/foundation-argument-construction.md`). That project is evolving independently.

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

#### 3.1.1 Reader Psychology: The Emotional Arc

The introduction's structural moves (WORLD → PROBLEM → GAP → QUESTION → PREVIEW) have corresponding persuasive functions. Each step should produce a specific cognitive-emotional response in the reader:

| Step | Structural function | Reader should feel | Test question |
|------|--------------------|--------------------|---------------|
| WORLD | Establish phenomenon | **Recognition**: "Yes, I know this" | Would my reader nod along? |
| PROBLEM | Deepen stakes | **Concern**: "Hmm, that IS a problem" | Does this feel consequential? |
| GAP | Show what's missing | **Surprise/frustration**: "Wait, we really DON'T know this?" | Would my reader be startled by the absence? |
| QUESTION | State the research question | **Curiosity**: "How DOES this work?" | Is the reader now hooked? |
| PREVIEW | Foreshadow contribution | **Anticipation**: "Tell me what you found" | Has the reader committed to the paper? |

**The inevitability principle**: By the end of the introduction, the reader should feel that OF COURSE this study needed to be done. If the reader shrugs at the gap, the introduction has failed — even if structurally correct.

**The Davis test** (Davis 1971, "That's Interesting!"): The most compelling papers challenge assumptions the audience didn't know they held. The WORLD step establishes the assumption. The PROBLEM step destabilizes it. The GAP shows nobody has resolved the destabilization. A competent introduction presents a gap; a great introduction makes the reader realize they've been wrong about something.

**The Locke & Golden-Biddle test** (1997): The introduction must construct an "opportunity for contribution" — not merely identify a topic that hasn't been studied, but show that the absence matters for how we understand the world. The gap must feel like a wound in our collective understanding, not a blank spot on a map.

#### 3.1.2 Stakes Escalation

The PROBLEM step must deepen stakes progressively. Three layers, deployed in order:

1. **Practical stakes**: Real organizations/people are affected. "Workers face displacement." "Hospitals adopt technology without understanding its effects on training." Grounds the problem in lived experience.

2. **Theoretical stakes**: Our theories can't explain what's happening. "Existing frameworks predict X, but we observe Y." "The dominant account assumes conditions that no longer hold." Shows the problem isn't just practical — it reveals a gap in how we think.

3. **Broader scholarly stakes**: The problem challenges assumptions across multiple literatures or reframes a foundational question. "If this assumption fails here, it likely fails in other domains too." Optional — not every paper needs this layer, but the strongest introductions reach it.

**Calibration by journal**:

| Journal | Practical stakes | Theoretical stakes | Broader stakes |
|---------|-----------------|-------------------|---------------|
| ASQ | Brief (1-2 sentences) | Dominant | Optional but valued |
| Organization Science | Moderate | Dominant | Valued |
| AMJ | Substantial (equal weight) | Required | Light |
| ManSci | Economic/efficiency framing | Brief | Rare |

**The scope-credibility tradeoff**: Bigger stakes are more persuasive but harder to deliver. The gap must be big enough that filling it matters, but small enough that one paper can credibly address it. If the stakes paragraph promises to revolutionize organizational theory, the paper had better deliver. If it promises to extend one concept to a new context, the reader will expect modest but solid contribution.

**Anti-pattern: The defensive introduction**: An introduction that spends 500+ words justifying why the study matters before saying what it IS. This signals that the author knows the stakes are weak and is compensating. If the problem is genuinely important, stating it clearly is sufficient.

#### 3.1.3 Gap Construction Typology

Not all gaps are the same. Each type requires different construction and has different vulnerabilities.

**Based on Locke & Golden-Biddle (1997), operationalized for practice:**

| Gap type | Logic | Construction | Vulnerability | Defense |
|----------|-------|-------------|---------------|---------|
| **True absence** | "Nobody has studied X" | Show that adjacent work exists, but the specific phenomenon/process is unstudied | Reviewer cites a paper you missed | Acknowledge adjacent work explicitly; show why it doesn't address your specific question |
| **Mechanism gap** | "We know X happens but not HOW" | Cite outcome studies, show the process is a black box | "The mechanism is obvious" | Show competing plausible mechanisms; demonstrate that the outcome literature assumes rather than demonstrates mechanism |
| **Framing gap** | "We know X but haven't looked through lens Y" | Engage lens Y seriously, show it predicts different things | "Why does the new lens matter?" | Demonstrate that lens Y generates different predictions or reveals dynamics invisible under prior lenses |
| **Boundary condition gap** | "X holds in context A but not B" | Establish X's domain, show B differs on theoretically relevant dimensions | "B is just a minor variant" | Argue that the difference between A and B is theoretically generative, not just empirically different |
| **Integration gap** | "Literatures A and B both address X but haven't been combined" | Engage both literatures, show each has a blind spot the other fills | "This is just a lit review mashup" | Demonstrate that the combination produces novel insight neither literature alone generates |
| **Inadequacy gap** | "The consensus view of X is wrong or incomplete" | Build up the consensus (steelman), then show the crack | "You're misrepresenting the literature" | Engage the strongest version of the view you're challenging; concede what it gets right |

**Which gap type to use**:
- **Mechanism gap** is the bread and butter of ASQ and OrgSci process papers
- **Boundary condition gap** is common in AMJ
- **True absence** is strongest when genuine, but rarest — most "absences" turn out to be mechanism or framing gaps on closer inspection
- **Integration gap** requires genuine synthesis, not just "these two literatures exist" — the combination must produce something neither generates alone
- **Inadequacy gap** is the hardest to execute because you must steelman the view you're challenging (Zuckerman criteria 7-8: build up and save the null)

**Gap statement rules**:
- Name the prior literature specifically
- State what it has NOT done (not "more research is needed")
- The absence must be about process or mechanism
- Gap claims are author assertions, typically uncited
- **Match the gap type to the contribution**: A mechanism gap promises process theory. A boundary condition gap promises contingency. An integration gap promises synthesis. If the gap and contribution don't match, the introduction will feel incoherent.

#### 3.1.4 Paragraph Budget

The 1500-2000 word introduction needs deliberate allocation. These are guidelines, not rigid prescriptions — but substantial deviations signal structural problems.

| Arc step | Typical paragraphs | Word budget | Function |
|----------|-------------------|-------------|----------|
| WORLD | 1-2 | 200-400 | Establish shared understanding |
| PROBLEM | 1-2 | 300-500 | Escalate stakes (practical → theoretical) |
| GAP | 1 | 150-300 | Name what's missing (gap typology) |
| QUESTION | 0.5-1 | 100-200 | State research question |
| PREVIEW | 1-2 | 300-500 | Foreshadow contributions and study |

**Budget shifts by journal**:
- **ASQ**: WORLD and PROBLEM get more space (up to 900 words); PREVIEW is brief (200-300). Theory leads.
- **Organization Science**: Roughly even distribution. Theoretical novelty emphasized in PREVIEW.
- **AMJ**: PROBLEM gets substantial space (practical + theoretical motivation); PREVIEW includes practical implications.
- **ManSci**: Compressed WORLD and PROBLEM (400-500 total); longer PREVIEW with identification strategy hint (300-400).

**Budget diagnostic**: If WORLD exceeds 500 words, you're probably doing a literature review in the introduction. If GAP exceeds 300 words, you're being defensive. If PREVIEW exceeds 600 words, you're writing the abstract again.

#### 3.1.5 Research Question Formulation

The research question bridges GAP and PREVIEW. It constrains the paper's scope and signals methodology.

**Open vs. closed form**:
- **Open**: "How do organizations manage X?" — signals inductive/qual. Appropriate for ASQ, OrgSci theory-building papers. Admits you don't know the answer.
- **Closed**: "Does X affect Y?" or "Under what conditions does X lead to Y?" — signals deductive/quant. Appropriate for AMJ, ManSci hypothesis-testing papers. Admits you have a prediction.
- **Mixed**: "How and when does X shape Y?" — signals mixed-methods. Combines process and contingency.

**Rules**:
- One research question is ideal. Two is acceptable if they're sequential (descriptive + explanatory: "What happens? And why?"). Three signals unfocused thinking.
- The RQ must be answerable by the study described in the PREVIEW. If the RQ implies a population study but the PREVIEW describes an ethnography, something is wrong.
- The RQ should make the paper's scope obvious. If the RQ could generate 10 different papers, it's too broad.
- The RQ is typically uncited — it's the author's assertion of what matters. But it should be clearly motivated by the GAP that precedes it.

**The constraint test**: A good research question, read alone, should tell a colleague in your field roughly what kind of paper to expect (topic, method family, contribution type). If it doesn't, tighten it.

#### 3.1.6 Contribution Preview (PREVIEW Step)

The PREVIEW foreshadows what the paper delivers. It must be precise enough to create anticipation but not so detailed that it spoils the findings.

**What to include**:
1. **Study description** (1-2 sentences): Setting, method family, scale. "Drawing on a two-year ethnography of..." or "Using 59,000 separation records across six facilities..."
2. **Core finding or concept** (1-2 sentences): Tease the mechanism or name the concept. "We find that..." or "I identify a process I call..."
3. **Contributions** (2-4 sentences): Which scholarly conversations does this paper advance, and how?

**How much to reveal**:
- **Tease, don't spoil**: "We show how X unfolds through Y" previews the contribution type without giving away the full mechanism. "We find that X causes Y through Z mediated by W" is a spoiler — save it for the findings.
- **Name the concept** if you're coining one: "I call this process 'shadow learning'" in the introduction is powerful — it gives the reader a handle.
- **Don't pre-argue**: The PREVIEW states contributions; it doesn't defend them. Defense is for the discussion.

**Number of contributions**:
- ASQ/OrgSci: 2-3 contributions typical. More than 3 signals unfocused.
- AMJ: 2-3 theoretical + 1 practical implication.
- ManSci: 1-2 contributions, precisely stated.

**The formula and its variants**:
- "This paper contributes to X by showing Y" — standard, clear
- "We advance understanding of X by..." — slightly more assertive
- "This study extends X to show..." — signals extension, not challenge
- "Our findings challenge the assumption that..." — signals an inadequacy gap contribution

**Preview-discussion coherence rule**: Every contribution previewed in the introduction MUST be claimed in the discussion, and vice versa. This is a mechanical check: list the PREVIEW contributions and the discussion contributions side by side. They should map 1:1. Mismatches mean the paper drifted during drafting.

**Detection patterns for bad introductions**:
```
# Literature-first opening (SOFT VIOLATION)
^(Prior|Previous|Existing|Past)\s+(research|work|studies|literature)
^(The|A)\s+literature\s+on
^(Scholars|Researchers|Studies)\s+have\s+(long\s+)?(shown|found|argued)
```

#### 3.1.7 Common Structural Failure Modes

Beyond surface detection patterns, these are the structural problems that sink introductions. Each is named for diagnosis.

**The Premature Contribution List**
> "This paper makes three contributions. First, we extend... Second, we show... Third, we document..."

Appears in paragraph 2-3, before the reader cares. Contributions should be EARNED by the argument, not announced at the door. The PREVIEW may gesture at contributions, but the bulleted contribution list is a discussion move, never an introduction move.

**The Everything Introduction**
> Engages 5+ literatures in the introduction, each for one paragraph, with no throughline.

The introduction should join ONE scholarly conversation (Zuckerman criterion 2). Engaging multiple literatures is for the theory section. If the introduction needs five literatures to motivate the gap, the gap is probably unfocused.

**The Defensive Introduction**
> Spends 500+ words justifying why the topic matters before saying what the study IS.

Signals that the author knows the stakes are weak. If the problem is genuinely important, a brief, clear statement of stakes is more persuasive than a long defense. When you catch yourself writing "it is important to study X because...", ask whether a stronger opening would make the justification unnecessary.

**The Methods-Forward Introduction**
> "We conducted a two-year ethnographic study of six hospitals..." in paragraph 2, before the theoretical puzzle exists.

The empirical setting serves the theoretical question, not the other way around. The reader must understand WHY the study was done before they care HOW it was done. Exception: the cold-open-with-data offramp (max 2 paragraphs), which uses empirical surprise to motivate the question.

**The Too-Narrow Gap**
> "While studies have examined X in context A, none have examined X in context B."

If the contribution is "we did the same thing somewhere else," the gap is too narrow. The move to context B must be theoretically motivated — B must differ from A on dimensions that generate new insight, not just new data points.

**The Too-Broad Gap**
> "Organizations face unprecedented change, yet we lack a comprehensive theory of adaptation."

No single paper can fill a gap this large. The reader will wonder which corner of this enormous gap the paper actually addresses, and will expect the answer to be modest relative to the promise. Narrow the gap to the specific process/mechanism the paper actually illuminates.

**The Contribution-First Introduction**
> Opens with "We contribute to X by showing Y" before establishing why X matters.

The contribution only has meaning in the context of the gap. If the reader doesn't feel the gap, the contribution lands flat. Build the world, deepen the problem, reveal the gap, THEN preview the contribution.

**Detection heuristic**: Read only the first sentence of each paragraph. If the throughline is unclear, there's a structural problem. If you can't identify which arc step each paragraph belongs to (WORLD, PROBLEM, GAP, QUESTION, PREVIEW), the introduction needs restructuring.

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

**Structure**:
- [ ] Opens with Broad Declarative, Trend Claim, or Literary Hook (not literature review)
- [ ] Arc follows WORLD → PROBLEM → GAP → QUESTION → PREVIEW
- [ ] One clear Turn with adversative conjunction
- [ ] Citation functions shift from consensus → steelman → absence → tension

**Gap & Question**:
- [ ] Gap type identified (absence, mechanism, framing, boundary, integration, or inadequacy)
- [ ] Gap statement specifies missing process/mechanism (not "more research needed")
- [ ] Gap is defensible — adjacent work acknowledged, specific absence articulated
- [ ] Research question is answerable by the study described in PREVIEW
- [ ] Research question form matches methodology (open → inductive; closed → deductive)

**Stakes & Persuasion**:
- [ ] Stakes escalate: practical → theoretical (→ broader, if warranted)
- [ ] Stakes calibrated to journal (ASQ: theory-dominant; AMJ: practical + theoretical)
- [ ] Reader would feel surprise/frustration at the gap, not just acknowledge it
- [ ] No defensive over-justification (>500 words of "why this matters")

**Preview**:
- [ ] Study described concisely (setting, method family, scale)
- [ ] Core finding/concept teased without spoiling mechanism
- [ ] Contributions previewed (2-3 for ASQ/OrgSci, 1-2 for ManSci)
- [ ] Preview contributions will map 1:1 to discussion contributions

**Failure mode scan**:
- [ ] No premature contribution list (bulleted "three contributions" before gap is earned)
- [ ] No everything introduction (5+ literatures engaged without throughline)
- [ ] No methods-forward framing (study described before theoretical puzzle)
- [ ] Gap is neither too narrow (same thing, new context) nor too broad (solve all of X)

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
