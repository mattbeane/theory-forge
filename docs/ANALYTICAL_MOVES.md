# Analytical Moves in Theory-Forge

Theory-forge encodes four core analytical moves and a governing principle. These moves have deep roots in qualitative research traditions — ethnography, grounded theory, case study methodology, interpretive sociology. AI accelerates them; it didn't invent them.

Recent scholarship has usefully articulated how GenAI fits into these moves (notably Glaser & First Loan, forthcoming in *Strategic Organization*; Reimer & Peter in IS). Their articulations informed theory-forge's command design. But the moves belong to the qualitative tradition, not to any single paper. See `CREDITS.md` for full acknowledgments.

---

## The Four Moves

### 1. Interpreting Through Multiple Frames

**The move**: Read the same empirical moment through multiple theoretical lenses. Hold multiple interpretations simultaneously. Let contradictions between frames reveal each lens's reach and limits.

**Tradition**: Standard in ethnography, comparative case analysis, and theory-building methodology. Any good qualitative researcher does this — theory-forge just does it faster and more systematically.

**Theory-forge implementation**:

| Command | How It Implements This Move |
|---------|---------------------------|
| `/style-engine` | **Primary.** Generates 3-5 theoretical framings of the same finding, each varying the lead, theory, contribution, and audience. Evaluates on novelty, robustness, coherence, and journal fit. |
| `/find-theory` | Identifies the primary theory being violated — the first lens. |
| `/find-lens` | Finds sensitizing literature — a second lens explaining heterogeneity. |
| `/compare-frames` | Side-by-side comparison after multiple `/new-frame` iterations. |
| `/eval-contribution` | Checks whether you're using the right KIND of lens (violation vs. elaboration vs. phenomenon description). |

**Critical constraint**: The lenses must come from the researcher's theoretical knowledge, not from the LLM. The tool generates framings WITHIN researcher-specified theoretical space; it should not generate the theoretical space itself.

---

### 2. Surfacing Absences

**The move**: Inventory what is not done, not said, not considered — despite apparent relevance. Treat patterned omissions as analyzable data. Sometimes the absence itself is the finding.

**Tradition**: Ethnographic attention to silences and taken-for-granted assumptions. What people don't discuss is often analytically richer than what they do.

**Theory-forge implementation**:

| Command | How It Implements This Move |
|---------|---------------------------|
| `/surface-absences` | **Primary.** Systematically scans data for conspicuous omissions, categorizes them (normalized, political, structural, temporal, actor, conceptual), and assesses analytical significance. |
| `/audit-claims` | Searches for evidence that CHALLENGES claims, which can reveal what's missing from the current interpretation. |
| `/mine-qual` | Disconfirming evidence section touches on absences, but from "what contradicts" rather than "what's missing entirely." |

**Why AI helps here**: Absences are especially hard for embedded researchers to see because familiarity normalizes what's missing. AI brings an outsider's perspective — it knows what's typical in similar settings and can flag what's conspicuously absent.

**What `/surface-absences` adds over existing commands**: Dedicated focus on "what SHOULD be here but isn't?" — distinct from "what contradicts my claims?" (audit-claims) or "what challenges my interpretation?" (mine-qual).

---

### 3. Bridging Levels

**The move**: Explore how micro traces index to macro patterns, and how macro configurations reframe micro events. Connect individual-level experience to organizational or field-level dynamics.

**Tradition**: Multi-level analysis in organizational research, connecting micro and macro in sociology. This is the mixed-methods integration challenge.

**Theory-forge implementation**:

| Command | How It Implements This Move |
|---------|---------------------------|
| `/integrate-quant-qual` | **Primary.** Maps quantitative patterns (macro) to qualitative mechanisms (micro). Identifies convergence, divergence, and gaps between levels. |
| `/trace-process` | Traces how micro-level events aggregate into macro-level phase transitions and vice versa. |
| `/mine-qual` | Extracts mechanism evidence bridging individual experience (micro) to organizational patterns (macro). |
| `/hunt-patterns` | Identifies macro-level statistical patterns that qualitative data can then explain at the micro level. |
| `/measure-at-scale` | Quantifies constructs discovered at micro level across the full corpus, revealing macro distributions. |

---

### 4. Testing Categories Adversarially

**The move**: Probe boundary cases, track shifts over time, explore where classifications blur or coexist. Treat coexistence as information rather than error.

**Tradition**: Disconfirmation logic in case study methodology, negative case analysis in grounded theory, analytical induction. Adversarial testing of emerging concepts is standard practice — it's just laborious by hand.

**Theory-forge implementation**:

| Command | How It Implements This Move |
|---------|---------------------------|
| `/mine-qual` | Tests mechanism hypotheses against data — supporting AND challenging evidence for each category. |
| `/eval-becker` | Becker's generalization test: checks whether categories are genuinely general or domain-specific. |
| `/style-engine` | Adversarial check for each framing probes boundary conditions and weakest links. |
| `/audit-claims` | Adversarial evidence search across ALL data for each claim category. |
| `/trace-process` | Tracks how categories evolve over time — blurring, splitting, merging. |
| `/simulate-review` | Tests whether categories survive hostile reviewer scrutiny. |
| `/measure-at-scale` | Reveals whether categories are pervasive or concentrated — cherry-picking detection. |

---

## The Governing Principle: Interpretive Vigilance

**The principle**: The researcher must be the author of meaning. AI outputs are proposals, not proofs. Dissonance is generative. Conclusions must be anchored in evidence and theory. Maintain a reflexive audit trail.

This isn't a single command — it's the architecture of the system:

| Principle | Theory-Forge Implementation |
|-----------|---------------------------|
| "Outputs are proposals, not proofs" | Hard gates require user confirmation at every transition. No auto-proceeding. |
| "Dissonance is generative" | Adversarial evidence is standard across `/hunt-patterns`, `/mine-qual`, `/audit-claims`, `/style-engine`. |
| "Anchored in evidence and theory" | `/verify-claims` + Living Paper create verifiable claim-evidence links. |
| "Reflexive audit trail" | `DECISION_LOG.md` auto-tracks all decisions. `/audit-trail` provides export. `/describe-ai-use` generates methods section disclosure. |
| "Researcher as author of meaning" | Student mode requires manual analysis before AI runs. All theory/lens/framing choices are researcher-directed. |

---

## Scholarship That Informed This Design

- **Glaser & First Loan** (forthcoming, *Strategic Organization*) — Articulated four "abductive moves" for AI-augmented qualitative analysis that map to theory-forge's command structure. Their emphasis on interpretive vigilance resonates with theory-forge's gate and verification architecture.
- **Reimer & Peter** (IS research) — Conceptualized GenAI as a "style engine" that renders the same empirical reality through multiple theoretical styles. This metaphor clarified what `/style-engine` does.
- **Nguyen & Welch** (2025) — Critique of autonomous AI coding that motivated hypothesis-driven design, adversarial defaults, and external verification.
- The broader qualitative methods tradition — ethnography, grounded theory, case study methodology — where these moves originated.

See [`../CREDITS.md`](../CREDITS.md) for full acknowledgments.
