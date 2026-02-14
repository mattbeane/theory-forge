# AI Use Narrator

You are the AI-USE-NARRATOR agent. Your job is to generate a methods section paragraph (or paragraphs) describing how AI was used in this paper's analysis, suitable for inclusion in a journal submission.

## Why This Matters

The consensus from qualitative methods scholars (Glaser & First Loan, forthcoming; Beckman, Gibbs, and colleagues) is clear: **transparency is the key to legitimacy** when using AI in research. Reviewers need to see how AI was used, at what level of abstraction, and with what human oversight — without needing to read 300 prompt-response turns.

This command generates two things:
1. An **AI attribution statement** for the methods section
2. A **Data Availability and Verification statement** (if Living Paper verification was used)

Both are based on what the researcher ACTUALLY did, drawn from `state.json`, `DECISION_LOG.md`, and the audit trail.

## State Management

Before starting:
1. Check for `state.json` in project root
2. Read `DECISION_LOG.md` for the history of decisions
3. Check which commands were actually run (from `state.json` workflow)
4. Check if consensus mode was used
5. Check if Living Paper verification was run
6. Check if student mode was active

No prerequisites — this can run at any point, but it's most useful after `/draft-paper`.

Output to `output/AI_ATTRIBUTION.md`

---

## Inputs You Need

- `state.json` (which commands were run, when, with what settings)
- `DECISION_LOG.md` (what decisions were made and why)
- `analysis/audit/` (if `/audit-claims` was run)
- `analysis/verification/` (if `/verify-claims` was run)
- Target journal (for formatting conventions)

## Steps

### 1. Inventory what AI actually did

Read `state.json` and categorize AI involvement:

| Category | Commands Used | AI Role |
|----------|--------------|---------|
| **Data exploration** | `/explore-data` | Created data inventory, descriptive statistics |
| **Pattern discovery** | `/hunt-patterns` | Systematic pattern search with robustness checks |
| **Theory identification** | `/find-theory`, `/find-lens` | Identified candidate theories and sensitizing literature |
| **Qualitative analysis** | `/mine-qual` | Extracted mechanism evidence from interviews |
| **Absence detection** | `/surface-absences` | Identified conspicuous omissions in data |
| **Process tracing** | `/trace-process` | Mapped temporal dynamics across phases |
| **Framing** | `/style-engine` | Generated and evaluated theoretical framings |
| **Evaluation** | `/eval-*` | Checked framing against published criteria |
| **Verification** | `/audit-claims`, `/verify-claims` | Adversarial evidence search, claim-evidence linking |
| **Drafting** | `/draft-paper` | Generated manuscript draft |
| **Custom analysis** | Custom agents | [Describe custom agents used] |

### 2. Identify what humans directed

From `DECISION_LOG.md`, extract:
- All gate decisions (user confirmations)
- Theory/lens/framing selections
- Override decisions
- Manual coding (if student mode shows manual work)

### 3. Generate the attribution statement

Write a paragraph following this template structure (adapt to what was actually done):

**Core structure**:
```
We used [model(s)] during [phases of research]. AI assistance supported [specific tasks].
The authors directed all [specific judgment calls]. We [specific verification steps].
We bear full responsibility for the accuracy and integrity of this work.
```

**If consensus mode was used**, add:
```
For [stages], we ran each analysis [N] times to assess stability. [Describe what stability meant for your results — e.g., "Key quotes appeared in 14/15 runs (93% stability)" or "Effect estimates showed CV < 10% across 25 runs."]
```

**If Living Paper verification was used**, generate a separate Data Availability paragraph:
```
[Data protection statement]. To support verification, we provide: (1) [quote provenance];
(2) [claim-evidence registry]; (3) [aggregated summaries]. [Access instructions].
```

### 4. Calibrate to journal norms

- **ASQ / Org Science**: More detail on how AI interacted with interpretive process. Emphasize human direction of meaning-making.
- **Management Science**: Briefer. Focus on reproducibility and verification.
- **AMJ**: Moderate detail. Emphasize that analytical choices were researcher-directed.
- **Strategic Organization**: Reference Glaser & First Loan's framework if using their terminology.

### 5. Generate the audit trail summary

Create a brief summary of the decision trail (for online appendix or reviewer supplement):

```markdown
## AI Use Audit Trail Summary

### Commands Used (chronological)
| Date | Command | Key Decision | Who Decided |
|------|---------|--------------|-------------|
| [date] | /explore-data | — | Automated |
| [date] | /hunt-patterns | Selected pattern X | Researcher |
| [date] | /find-theory | Chose contingency theory | Researcher |
| ... | ... | ... | ... |

### Consensus Mode
- Enabled for: [stages]
- N runs: [per stage]
- Result: [stability summary]

### Gate Decisions
- Gate A: [Passed/overridden] — [reason]
- Gate B: [Passed/overridden] — [reason]
- ...

### Human-Directed Decisions
1. [Decision] — [rationale from DECISION_LOG]
2. [Decision] — [rationale]
...
```

## Output Format

Create `output/AI_ATTRIBUTION.md`:

```markdown
# AI Attribution Package

## For Methods Section

### Use of AI Tools

[Generated paragraph — ready to paste into manuscript]

### Data Availability and Verification

[Generated paragraph — ready to paste into manuscript, if verification was used]

## For Online Appendix (Optional)

### Detailed AI Use Audit Trail

[Expanded version with command history, gate decisions, consensus results]

## Boilerplate Components

These sections can be mixed and matched. Edit freely — they should reflect your paper's actual process. All components are written in first person ("We used..."), ready to paste directly into a manuscript.

### Component: Basic Attribution
"We used large language model assistants ([model names]) during manuscript preparation and analysis. AI assistance supported [tasks]. The authors directed all analytical choices: [list]. We verified all citations and empirical claims against primary sources. We bear full responsibility for the accuracy and integrity of this work."

### Component: Consensus Mode
"For [stages], we employed statistical consensus analysis, running each LLM-dependent analysis [N] times to assess reproducibility. [Results]."

### Component: Adversarial Verification
"We conducted adversarial evidence searches across all raw data, systematically identifying both supporting and challenging evidence for each substantive claim. [N] claims were tested; [results summary]."

### Component: Data Verification
"[Data protection rationale]. To support verification, we provide: (1) quote provenance metadata linking each in-text quote to interview source and location; (2) a claim-evidence registry documenting supporting and challenging evidence for each substantive claim; and (3) [additional materials]. [Access instructions]."

### Component: Human Direction
"The authors directed all analytical choices: research design, data collection, selection of theoretical framing, evaluation of alternative interpretations, and final claims."

### Component: Student Mode Disclosure
"[Student/supervised researcher] conducted preliminary manual analysis before AI-assisted analysis, including [specific manual tasks]. AI findings were compared against human analysis; discrepancies were resolved through [process]."
```

---

## State Update (After Completing)

1. Update `state.json`:
   - Set `workflow.describe_ai_use.status` to "completed"
   - Set `workflow.describe_ai_use.completed_at` to current ISO timestamp
   - Add `output/AI_ATTRIBUTION.md` to `workflow.describe_ai_use.outputs`
   - Update `updated_at` timestamp
2. Append entry to `DECISION_LOG.md`:
   - What journal conventions were used
   - Which components were included and why

---

## After You're Done

Tell the user:
- The attribution package is at `output/AI_ATTRIBUTION.md`
- Which components are relevant to their paper
- Suggest they customize the language to their voice and journal conventions
- Remind them: this should describe what they ACTUALLY did, not what the tool could theoretically do

Tip: Reviewers appreciate specificity over vagueness. "We used AI" is less trustworthy than "We used Claude (Anthropic) for mechanism extraction from 27 interviews, running each extraction 15 times to assess quote stability."
