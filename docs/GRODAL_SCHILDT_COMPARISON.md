# Grodal & Schildt vs. Theory-Forge: A Comparison

*Analysis of the "How to Use AI in Qualitative Research" webinar (Stine Grodal, Northeastern) against Theory-Forge*

---

## The Core Agreement

Both Grodal/Schildt and theory-forge share the same fundamental premise: **AI should augment qualitative researchers, not automate them**. The webinar's central distinction—automated vs. augmented use of AI—maps almost perfectly onto theory-forge's design philosophy.

| Grodal/Schildt Principle | Theory-Forge Implementation |
|--------------------------|----------------------------|
| "Legitimacy resides with the human" | Hard gates require explicit user approval at each stage |
| "Always go back to the data yourself" | `/verify-claims` creates packages linking claims to exact quotes |
| "AI as tool, not substitute" | Commands are prompts you invoke; you make judgment calls at transitions |
| "Use for summarizing, identifying patterns" | `/explore-data`, `/hunt-patterns` do exactly this |
| "Challenge confirmation bias" | `/eval-zuckerman`, `/eval-becker`, `/eval-genre` run as adversarial checks |

---

## Where Theory-Forge Goes Further

### 1. Abduction-First Design

Grodal emphasizes abduction (finding puzzles that violate existing theory) but treats it as one approach among many. Theory-forge makes it the *only* path—the entire pipeline is structured around:
- Finding patterns → checking if they're puzzling → identifying *which theory* is violated → finding sensitizing literature that explains heterogeneity

The `/eval-zuckerman-lite` early check explicitly asks: "Is this a puzzle in the world (not a lit gap)? Is the null hypothesis compelling?"

### 2. Hard Gates vs. Soft Warnings

Grodal: "We need to develop good practices as a community"
Theory-forge: "Here are 6 blocking gates that won't let you proceed until conditions are met"

The system doesn't trust researchers to self-regulate. Gate D requires ALL THREE evaluations (Zuckerman, Becker, Genre) to pass before verification. This is more paternalistic than anything Grodal proposes—by design.

### 3. Frame Management

Grodal mentions that following the data leads to "puddle jumping" and identity challenges. Theory-forge operationalizes this:
- `/new-frame` archives your current theoretical framing while preserving empirical work
- `/new-frame list` and `/new-frame compare` let you compare iterations
- The system *expects* 3-5 complete reframings per paper

### 4. External Verification

Grodal: "You should always double-check AI output"
Theory-forge: "Send the verification package to a *different* AI or colleague"

The `/verify-claims` and `/package-verification` commands create self-contained HTML packages that external reviewers can audit independently. This goes beyond "trust but verify" to "verify with a different verifier."

### 5. Journal-Specific Genre Enforcement

Grodal mentions that qualitative papers for ASQ/OrgSci need "theory-building language" not hypothesis-testing. Theory-forge has an entire `/eval-genre` check for this:
- "Here's what I observed" NOT "Here's what I predicted"
- "The data suggest" NOT "The data confirm"
- "Hypothesis Development" sections are flagged as red flags

Plus a style enforcer that bans bullets, numbered lists, and enforces narrative prose.

---

## Where Grodal/Schildt Go Further

### 1. Sociological Context

The webinar situates AI in qualitative research within broader professional changes—lawyers using AI, translators, copy editors displaced. Theory-forge assumes you've already decided to use AI; it doesn't address whether you *should*.

### 2. Junior Scholar Concerns

Grodal explicitly addresses deskilling risks for junior scholars:
> "Maybe as a junior scholar if you have not been through the hardship of criticality and working through very difficult data sets for a long time, it's easier to fall victim to this form of laziness"

Theory-forge has a `PHD_STUDENT_CURRICULUM.md` doc but doesn't build in graduated scaffolding—it's the same pipeline for novices and experts.

### 3. Data Collection Integration

Schildt mentions using AI *during* data collection:
> "Should we be analyzing the interviews after every day of data collection to already map out what the topics were... so we could more quickly adapt the questions we ask?"

Theory-forge assumes you already have your data. There's no `/during-fieldwork` agent.

### 4. The "Microwave Oven" Pragmatism

Grodal repeatedly uses the microwave metaphor—we thought it would replace ovens, but it's just good for heating things. This pragmatic humility is less present in theory-forge, which positions itself as a comprehensive pipeline rather than a collection of small conveniences.

### 5. Community Norm Development

Grodal: "We need to develop these practices *together* as a community"
Theory-forge: "Here are the practices" (already codified)

The webinar emphasizes that good AI practices should emerge from collective discussion. Theory-forge is one person's (your) crystallized view of what those practices should be.

---

## Philosophical Tensions

### On Trust

Grodal: "I wouldn't trust it... the same way I wouldn't trust an untrained undergraduate RA"
Theory-forge: Actually encodes this distrust into the system architecture (hard gates, external verification packages)

### On Journal Policies

Grodal: "I haven't used AI on any papers I've submitted because it's against journal policies"
Theory-forge: Built specifically to produce papers for AMJ, ASQ, OrgSci—implicitly assumes journals will come around

### On Quantitative Methods Encroachment

Grodal worries about quant researchers using AI to "take over" qualitative territory with computational text analysis. Theory-forge explicitly supports mixed-methods designs but maintains qual primacy:
> "When qual contradicts quant, reclassify as mistaken beliefs"

This is a stronger stance than Grodal takes.

---

## Specific Feature Gaps

### In Grodal/Schildt but not Theory-Forge:
- Iterative summarization during data collection
- Teaching/curriculum design beyond documentation
- Explicit GDPR/privacy compliance tooling (Schildt's tool runs data in Sweden)
- Addressing the "drinking from a fire hose" problem of AI output overload

### In Theory-Forge but not Grodal/Schildt:
- Consensus mode (run analyses N times, compute statistical aggregates)
- Adaptive robustness testing (RASC protocol)
- Claim-evidence verification packages with checksums
- Multi-project workspace management
- Export to LaTeX/Word/PDF
- The Becker generalizability test ("can you state your finding without domain-specific nouns?")

---

## Bottom Line

Grodal and Schildt are having the *conversation* about how qualitative researchers should use AI. Theory-forge is an *answer* to that conversation—one that's more structured, more opinionated, and more operationally specific than anything they propose.

The webinar represents **consensus-building discourse** among senior scholars navigating uncertainty.
Theory-forge represents **codified practice** by someone who already decided what works.

Both are valuable. The webinar legitimizes experimentation; theory-forge provides a concrete starting point for that experimentation. If you wanted to cite the webinar in theory-forge's documentation, you could position it as "here's the community conversation we're contributing to."
