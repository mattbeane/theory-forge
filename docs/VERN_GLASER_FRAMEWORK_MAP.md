# Mapping Glaser & First Loan's Framework to Theory-Forge

**Reference**: Glaser, V. & First Loan, J. (forthcoming). "Generative AI as Abductive Partner in Qualitative Research." *Strategic Organization*.

Glaser and First Loan propose four analytical moves for using GenAI as an abductive partner, plus a governing principle of interpretive vigilance. This document maps their framework to theory-forge commands, showing how each conceptual move is operationalized.

---

## The Four Moves

### 1. Multiplying Lenses

**Glaser's definition**: Interpret the same empirical moment through multiple theoretical frames. Deepen engagement with one frame while deliberately holding others in view. Coherent contradictions across frames expose each lens's reach and limits.

**Theory-forge operationalization**:

| Command | How It Implements This Move |
|---------|---------------------------|
| `/smith-frames` (style engine) | **Primary implementation.** Generates 3-5 theoretical framings of the same finding, each varying the lead, theory, contribution, and audience. Evaluates each on novelty, robustness, coherence, and journal fit. |
| `/find-theory` | Identifies the primary theory being violated — the first lens. |
| `/find-lens` | Finds the sensitizing literature — a second lens that explains heterogeneity. |
| `/compare-frames` | Side-by-side comparison of 2+ framings after multiple `/new-frame` iterations. |
| `/eval-contribution` | Checks whether you're looking through the right KIND of lens (theory violation vs. elaboration vs. phenomenon description). |

**What Glaser emphasizes that theory-forge should preserve**: The lenses must come from the researcher's theoretical knowledge, not from the LLM. Jen First Loan chose institutional, practice, and temporal lenses based on her training. The tool generates framings WITHIN researcher-specified theoretical space; it should not generate the theoretical space itself.

---

### 2. Surfacing Absences

**Glaser's definition**: Inventory what is not done, not said, not considered despite apparent relevance. Treat patterned omissions as analyzable data. The absence itself can become the finding.

**Theory-forge operationalization**:

| Command | How It Implements This Move |
|---------|---------------------------|
| `/surface-absences` | **Primary implementation (NEW).** Systematically scans data for conspicuous omissions, categorizes them (normalized, political, structural, temporal, actor, conceptual), and assesses analytical significance. |
| `/audit-claims` | Partial implementation — searches for evidence that CHALLENGES claims, which can reveal what's missing from the current interpretation. |
| `/mine-qual` | Disconfirming evidence section touches on absences, but from the perspective of "what contradicts" rather than "what's missing entirely." |

**Key example from Glaser**: In Jen's dissertation, the GenAI noted that nobody discussed replacing the ERP system — despite it being the obvious solution. This normalized absence became analytically productive, leading to the concept of "temporal drift."

**What `/surface-absences` adds that existing commands don't**: A dedicated focus on "what SHOULD be here but isn't?" — distinct from "what contradicts my claims?" (audit-claims) or "what challenges my interpretation?" (mine-qual disconfirming evidence).

---

### 3. Bridging Levels

**Glaser's definition**: Explore how micro traces index to macro patterns, and how macro configurations reframe micro events. Make surfacing connections between different concepts and levels of analysis.

**Theory-forge operationalization**:

| Command | How It Implements This Move |
|---------|---------------------------|
| `/integrate-quant-qual` | **Primary implementation.** Maps quantitative patterns (macro) to qualitative mechanisms (micro). Identifies convergence, divergence, and gaps between levels. |
| `/trace-process` | **NEW.** Traces how micro-level events aggregate into macro-level phase transitions and vice versa. |
| `/mine-qual` | Extracts mechanism evidence that bridges individual experience (micro) to organizational patterns (macro). |
| `/hunt-patterns` | Identifies macro-level statistical patterns that qualitative data can then explain at the micro level. |

**Key example from Glaser**: The GenAI connected the IT lead's smoking breaks (micro coping behavior) to a broader organizational pattern of dysfunction and fatigue (macro), which Jen hadn't immediately seen. This led to concepts of predictability and control.

---

### 4. Testing Categories

**Glaser's definition**: Probe boundary cases, track shifts over time, explore where classifications blur or coexist. Treat coexistence as information rather than error.

**Theory-forge operationalization**:

| Command | How It Implements This Move |
|---------|---------------------------|
| `/mine-qual` | Tests mechanism hypotheses against data — supporting AND challenging evidence for each category. |
| `/eval-becker` | Becker's generalization test: checks whether categories are genuinely general or domain-specific. |
| `/smith-frames` | Adversarial check for each framing probes boundary conditions and weakest links. |
| `/audit-claims` | Adversarial evidence search across ALL data for each claim category. |
| `/trace-process` | **NEW.** Tracks how categories evolve over time — blurring, splitting, merging. |
| `/simulate-review` | Tests whether categories survive hostile reviewer scrutiny. |

**Key example from Glaser**: An informant's statement was coded as "doing it right" vs. "doing it fast" — but the GenAI showed it was actually BOTH categories simultaneously. This coexistence led to the concept of "foresight" and eventually revealed hybrid temporal orientations.

---

## The Governing Principle: Interpretive Vigilance

**Glaser's definition**: The researcher must be the author of meaning. Outputs are proposals, not proofs. Dissonance is generative. Conclusions must be anchored in evidence and theory. Maintain a reflexive audit trail.

**Theory-forge operationalization**:

| Principle | Theory-Forge Implementation |
|-----------|---------------------------|
| "Outputs are proposals, not proofs" | Hard gates require user confirmation at every transition. No auto-proceeding. |
| "Dissonance is generative" | Adversarial evidence is standard across `/hunt-patterns`, `/mine-qual`, `/audit-claims`, `/smith-frames`. |
| "Anchored in evidence and theory" | `/verify-claims` + Living Paper create verifiable claim-evidence links. |
| "Reflexive audit trail" | `DECISION_LOG.md` auto-tracks all decisions. `/audit-trail` provides export. `/describe-ai-use` generates methods section disclosure. |
| "Researcher as author of meaning" | Student mode requires manual analysis before AI runs. All theory/lens/framing choices are researcher-directed. |

---

## The "Style Engine" Connection

Reimer & Peter (IS literature) conceptualize GenAI as a **style engine** — a tool that can take the same phenomenon and render it through multiple perspectives. This maps to Glaser's "multiplying lenses" but adds the insight that the power isn't just in seeing multiple perspectives, but in rapidly *generating* them.

Theory-forge's `/smith-frames` (now explicitly a "style engine" for theoretical framing) operationalizes this: same finding, same data, multiple theoretical renderings — each evaluated for novelty, robustness, and journal fit.

---

## What This Mapping Reveals

1. **Theory-forge already covered most of the framework** — but not by name. Explicit mapping helps researchers who've read Glaser's paper find the corresponding tools.

2. **Surfacing absences was the gap.** Now filled with `/surface-absences`.

3. **Temporal dynamics were underserved.** Now addressed by `/trace-process`.

4. **The "style engine" framing improves communication** about what `/smith-frames` does — it's not just generating options, it's rendering the same empirical reality through different theoretical styles.

5. **Interpretive vigilance maps to infrastructure, not a single command.** It's the gates, the audit trail, the adversarial evidence, the student mode — the whole architecture of the system.
