# Credits & Acknowledgments

Theory-forge draws on ideas and tools from many sources. This document acknowledges the scholarly and technical work that shaped its design.

---

## Intellectual Foundations

### Evaluation Frameworks

**Ezra Zuckerman** — "Tips for Article-Writers" provides the 10-criteria framework that powers `/eval-zuckerman` and `/eval-zuckerman-lite`. The puzzle-null-contribution structure is arguably the dominant framing template for top management and organization journals. Theory-forge's suggested path is essentially a Zuckerman workflow with verification bolted on.

**Fisher & Aguinis** — Theory elaboration criteria used in `/eval-contribution` for papers that add precision to existing theory rather than violating it.

**Weick** — Phenomenon description criteria for papers where rich description IS the contribution. Used in `/eval-contribution`.

**Abbott** — Methodological contribution heuristics for papers where the method is the main offering. Used in `/eval-contribution`.

**Corley & Gioia** — Practical insight criteria for practitioner-facing contributions. Used in `/eval-contribution`.

**Palmatier et al.** — Literature integration criteria for synthesis papers. Used in `/eval-contribution`.

### AI-Augmented Qualitative Research

Several scholars have articulated frameworks for how AI can participate in qualitative analysis without replacing researcher judgment. Theory-forge draws on this emerging literature:

**Glaser & First Loan** (forthcoming, *Strategic Organization*) — Propose four "abductive moves" for using GenAI in qualitative research: multiplying lenses, surfacing absences, bridging levels, and testing categories. Their emphasis on *interpretive vigilance* — the researcher as author of meaning — resonates with theory-forge's design. The `/surface-absences` and `/style-engine` commands were informed by their articulation of these moves, though the analytical operations themselves are not unique to their framework.

**Reimer & Peter** (IS research) — Conceptualize GenAI as a "style engine" that renders the same empirical reality through multiple theoretical styles. This metaphor helped clarify what `/style-engine` does, and the name stuck. The underlying idea — that the same data yields different insights through different theoretical lenses — is a standard move in qualitative research that predates GenAI.

**Nguyen & Welch** (2025) — Their critique of autonomous AI coding in qualitative research identifies real failure modes. Theory-forge's response is documented in `nguyen-welch-comparison.md`. Their concerns motivated several design choices: hypothesis-driven mining rather than open-ended coding, adversarial evidence as default, consensus mode for stability, and external verification via living paper.

**Beckman, Gibbs, and colleagues** — Contributions to the emerging consensus around transparency norms for AI use in research. Informed the `/describe-ai-use` command.

### Argument Construction

**Nine exemplar papers** from ASQ, Organization Science, ASR, AMJ — The argument construction rules in `docs/ARGUMENT_CONSTRUCTION_RULES.md` were extracted from close reading of published papers in these journals. These conventions (topic-sentence-as-claim, evidence-clincher structure, transition patterns) are taught informally in doctoral programs but rarely codified.

### Approach to Theory-Building Language

**The inductive/abductive genre distinction** — `/eval-genre` and `docs/THEORY_BUILDING_STYLE.md` encode the distinction between theory-building and theory-testing language that journals increasingly police. This draws on widespread methodological norms rather than any single source.

---

## Technical Foundations

### GABRIEL (Asirvatham, Mokski & Shleifer, 2026)

**"GPT as a Measurement Tool"**, NBER Working Paper 34834. Introduces GABRIEL (Generalized Attribute Based Ratings Information Extraction Library), a toolkit for using LLMs as systematic measurement instruments. Their validation across 1,000+ human-annotated tasks demonstrates that LLM measurement can be "generally indistinguishable from human evaluators."

Theory-forge's `/measure-at-scale` command generates GABRIEL-compatible measurement specifications. GABRIEL addresses a different problem than theory-forge (measurement vs. discovery), but the two systems compose naturally: discover constructs with theory-forge, measure them exhaustively with GABRIEL.

- Paper: https://www.nber.org/papers/w34834
- Code: https://github.com/openai/GABRIEL
- License: Apache 2.0

### Living Paper

The verification layer bundled in `living_paper/` creates auditable claim-evidence links. Developed alongside theory-forge. See https://github.com/mattbeane/living-paper.

### Claude Code

Theory-forge is built as Claude Code slash commands. The entire architecture depends on Claude Code's command system, context management, and file operations. https://claude.ai/claude-code

---

## Design Influences

**Paul Leonardi** — The pedagogical insight behind `/create-agent` and student mode: building your own analytical tool forces you to articulate what you're looking for, which is itself a form of theoretical work. "Show me your machine and we'll debrief about what you thought you knew about the scholarly process that led you to build it that way."

**Matt Beane** — AI attribution approach in `/describe-ai-use` is based on the method used in "Developmental Uncertainty" (submitted to *Organization Science*).

---

## A Note on Attribution

Several of the analytical moves encoded in theory-forge — interpreting data through multiple theoretical frames, looking for what's conspicuously absent, connecting micro and macro, testing emerging categories adversarially — are standard practices in qualitative research. They have long histories across ethnography, grounded theory, case study methodology, and interpretive sociology.

Recent scholarship (Glaser & First Loan; Reimer & Peter; others) has usefully articulated how GenAI can *accelerate* these moves. Theory-forge benefited from these articulations. But the moves themselves belong to the qualitative research tradition, not to any particular paper or framework. Credit where due: to the tradition first, to the recent articulators second.

---

## License

Theory-forge is MIT licensed. The referenced works retain their own copyright and licensing.

---

*Last updated: 2026-02-20*
