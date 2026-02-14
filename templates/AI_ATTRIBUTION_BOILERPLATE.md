# AI Attribution Boilerplate

Standard language for disclosing AI use in journal submissions. Based on the attribution statement used in "Developmental Uncertainty" (Beane, submitted to Organization Science).

Customize these components to reflect what you actually did. Do not claim processes you didn't follow.

---

## Full Template (for methods section)

### Use of AI Tools

We used large language model assistants ([MODEL NAMES, e.g., Claude, Anthropic]) during manuscript preparation and analysis. AI assistance supported [SELECT FROM LIST BELOW]:

- literature search and synthesis
- exploratory data analysis
- systematic pattern discovery with robustness checks
- validation of human-coded patterns in qualitative data
- mechanism extraction from interview transcripts
- adversarial evidence search (supporting AND challenging evidence for each claim)
- generation and evaluation of theoretical framings
- prose drafting

[IF CONSENSUS MODE]: For [STAGES, e.g., qualitative mining and pattern discovery], we employed statistical consensus analysis, running each LLM-dependent analysis [N] times to assess reproducibility. [RESULTS, e.g., "Key quotes appeared in 14/15 runs (93% stability); effect estimates showed CV < 10% across 25 runs."]

The authors directed all analytical choices: research design, data collection, selection of theoretical framing, evaluation of alternative interpretations, and final claims. We verified all citations and empirical claims against primary sources. We bear full responsibility for the accuracy and integrity of this work.

### Data Availability and Verification

[DATA PROTECTION RATIONALE, e.g., "Interview transcripts and observational data remain protected under IRB protocol and nondisclosure agreements with our research site."] To support verification, we provide: (1) quote provenance metadata linking each in-text quote to interview source and location; (2) a claim-evidence registry documenting supporting and challenging evidence for each substantive claim; and (3) [ADDITIONAL MATERIALS, e.g., "aggregated quantitative summaries (phase-level statistics, not individual records)"]. [ACCESS INSTRUCTIONS, e.g., "These materials are available upon request from the first author."] [OPTIONAL: link to Living Paper repository or verification interface.]

---

## Minimal Version (2 sentences)

We used large language model assistants (Claude, Anthropic) during manuscript preparation and analysis. The authors directed all analytical choices and verified all empirical claims against primary sources.

---

## Components (mix and match)

### Basic Attribution
"We used large language model assistants ([MODEL]) during manuscript preparation and analysis. AI assistance supported [TASKS]. The authors directed all analytical choices: [LIST]. We bear full responsibility for the accuracy and integrity of this work."

### Human-Coded-First Disclosure
"Qualitative coding was initially conducted manually by the authors. AI-assisted analysis was subsequently used to validate human-coded patterns, identify potential omissions, and surface disconfirming evidence."

### Consensus Mode Disclosure
"For [STAGES], we employed statistical consensus analysis, running each LLM-dependent analysis [N] times to assess reproducibility. Results with coefficient of variation exceeding 25% were flagged for manual review."

### Adversarial Verification Disclosure
"We conducted adversarial evidence searches across all raw data, systematically identifying both supporting and challenging evidence for each substantive claim. [N] claims were tested; [RESULTS]."

### Living Paper Verification Disclosure
"To support verification, we provide: (1) quote provenance metadata linking each in-text quote to interview source and location; (2) a claim-evidence registry documenting supporting and challenging evidence for each substantive claim; and (3) aggregated quantitative summaries. [ACCESS INSTRUCTIONS]."

### Student/Supervised Mode Disclosure
"[RESEARCHER] conducted preliminary manual analysis before AI-assisted analysis, including [TASKS]. AI findings were compared against human analysis to identify areas of convergence and divergence."

---

## Notes

1. **Be specific about what AI did.** "We used AI" is less trustworthy than listing the specific tasks.

2. **The phrase "validation of human-coded patterns" matters.** It establishes that humans coded first, AI validated — not the reverse.

3. **Bridge the attribution to the verification.** The "Use of AI Tools" and "Data Availability" paragraphs are adjacent in the Developmental Uncertainty paper because they're one argument: we used AI, AND here's how you can check our work.

4. **Customize to your actual process.** Don't claim consensus mode if you didn't use it. Don't claim adversarial verification if you didn't run `/audit-claims`.

5. **Journal norms are evolving.** Check your target journal's current AI disclosure policy. This boilerplate is designed to exceed current requirements while remaining concise.
