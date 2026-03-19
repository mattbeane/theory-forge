# Paper 1 Journey: From "Automation Causes Turnover" to "Hedging with Talent"

**Timeline**: November 21, 2025 → January 12, 2026 (52 days)
**Frame Shifts**: 7
**Final Title**: "Hedging with Talent: How Managers Use Selection to Navigate Novel Technology"
**Target Journal**: ASQ

---

## 2025-11-21: Initial Draft — "Automation's Hidden Labor Churn"

**Framing**: Automation causes turnover among temp workers (H1-H5)
**Mechanism**: Direct causal effect — automation → job threat → exit
**Register**: Hypothesis-testing ("We predict...", "H1-H5")

Nine section drafts created in a single day. The paper proposed five hypotheses testing whether automation increases turnover among temporary workers. Core claim: automation displaces workers, who flee approaching job threats.

*Data*: 59,021 temp exit records, 21 automation projects across 12 facilities.

---

## 2025-12-08: Zip Critique — External Model Review

**Category Changed**: Validation (Zip Critique)

Packaged paper + data + code into `option_cultivation_FULL_PACKAGE_20251126.zip` and sent to powerful external AI model for rigorous adversarial review.

**Process**: Model received manuscript, full data files, analysis scripts, and explicit REVIEW_PROMPT.md asking for:
- Verification that quantitative claims survive robustness checks
- Stress-testing of qualitative evidence
- Identification of vulnerabilities in theory positioning

---

## 2025-12-09: External Review Devastates Core Claims

**Category Changed**: Evidence, Claims, Validation, Robustness

The adversarial "friendly review" delivered devastating feedback.

**Key finding killed**: "Automation increases turnover by 40-50%" collapses with volume control.
- Without volume control: +50% exits (p=0.003)
- WITH volume control: +4-5% exits (p=0.63) — *statistically dead*

The reviewer's verdict: "Sites with more volume have more exits AND are more likely to automate. Once you control for volume, the apparent 'automation causes turnover' effect disappears."

**What survived**: Pre-treatment anticipation pattern. Voluntary resignations decrease 18-19 percentage points as automation approaches.

Verdict: "Expect a hard reject at ASQ/ManSci in current form."

---

## 2025-12-09: Reframe #3 — "The Anticipation Paradox"

**Framing**: Workers don't flee approaching automation—they stay. The puzzle is why.
**Mechanism**: Multiple candidates explored:
  1. Option value—stay to see outcomes
  2. Reduced hiring pipeline
  3. Selection—fearful workers already left
  4. Job lock
  5. Curiosity/attachment

Immediate pivot after external review. Dropped the "automation causes turnover" claim entirely. Built paper around the robust pre-treatment pattern.

*Key evidence*:
- Sorter facilities: Voluntary resignations drop from 22.4% to 3.3% (-19.1pp)
- Robot facilities: Voluntary resignations drop from 40.0% to 21.7% (-18.3pp)

---

## 2025-12-13: Living Paper Infrastructure Built

**Category Changed**: Validation, Replication, Automation Added

Built Living Paper system to handle verification of IRB-protected qualitative data. System creates bidirectional links between claims and hashed evidence—reviewers can see verification status without accessing raw transcripts.

**Tools created**: `/audit-claims` command, claim-evidence traceability, reviewer HTML exports.

*Trigger*: Needed to verify claims without exposing protected data to journal reviewers.

---

## 2026-01-06: Mosio Survey Evidence Integrated

**Category Changed**: Evidence, Mechanism, Boundaries

Integrated SMS survey data from 156 temp workers at Bloomington facility.

**Key finding**: Workers framed changes operationally (hours, pay), not technologically—only 6% mentioned automation explicitly. Job search intentions actually *declined* during implementation (29.8% → 24.0%).

**New concept**: "Intuitive awareness" vs explicit knowledge. Workers respond to uncertainty holistically, not to labeled information.

**New limitation acknowledged**: 92% opt-out rate on survey (survivorship bias); single facility; COVID confound.

---

## 2025-12-13: HALLUCINATION DISCOVERED — "Wait and See" Evidence Never Existed

**Category Changed**: Validation (Hallucination/Error Discovery), Evidence, Mechanism

The adversarial audit of 69 interview transcripts revealed a critical failure: **the qualitative evidence for "wait and see" sensemaking had never existed.**

**What the audit searched for**:
- First-person worker accounts of "waiting to see" how automation would affect them
- Worker quotes expressing curiosity about robots/automation
- Evidence of anticipatory sensemaking among frontline workers

**What the audit found**:
> "Searched 69 transcripts for 'wait and see', 'curious', 'want to know', 'find out' patterns. Found 12 matches across 11 files. Most were researcher statements or tangential mentions. **NO clear first-person worker quotes expressing curiosity about automation.**"

**The devastating implication**: The paper's mechanism—that workers stay because they're "making sense" of uncertain technology—was built on evidence that didn't exist in the data. The earlier AI-assisted drafting had either fabricated quotes or assumed worker attitudes that the transcripts don't support.

**Additional challenges found**:
- EV-008: Manager reports 75% of workforce shows "really no care" about automation
- EV-007: Manager explicitly states immigrant workers "don't wait"
- Direct evidence of exodus at some facilities contradicting retention narrative

*This hallucination discovery, combined with the seasonality confound, killed the "Wait and See" framing entirely.*

---

## 2026-01-08: Frame Shift #6 — "Wait and See" Killed, "Hedging with Talent" Emerges

**Framing**: KILLED: "Wait and See" (sensemaking mechanism unsupported). NEW: "Hedging with Talent"—manager-side selection mechanism
**Mechanism**: KILLED: Workers making sense of uncertainty. NEW: Managers select on reliability + withhold job-threat info → reliable (low-turnover) workers stay longer

**The debunking**: Discovered seasonality confound—the 18-19pp drop in voluntary exits exists company-wide in 2019 with NO automation. More critically: the Dec 13 audit had already revealed workers couldn't be "making sense" because (1) no evidence of curiosity in transcripts and (2) managers deliberately withheld information.

**The pivot**: Shifted from worker-side mechanism to manager-side mechanism. Under technological uncertainty, managers select temps on reliability and withhold job-threat info, creating a workforce "hedge."

*Key evidence*:
- Robot facilities: +66h tenure increase (22h → 76h median)
- Sorter facilities: -12h tenure (34h → 22h)
- 95% CI: [56h, 79h], Mann-Whitney p < 0.001

**Boundary condition**: Novel tech (robots) = high uncertainty → tenure 4x increase. Mature tech (sorters) = low uncertainty → no change.

---

## 2026-01-08: Theory Formalized via /find-theory and /find-lens

**Category Changed**: Mechanism, Boundaries

Ran theory-forge workflow to ground the new mechanism.

**Primary theory violated**: Job Insecurity and Displacement Theory
**Sensitizing literature**: Organizational Learning Under Uncertainty + Labor Market Sorting
**Key bridge**: Technological novelty → uncertainty → selection based on reliability → retention effect

**Zuckerman check**:
- Puzzle in the world? YES
- Compelling null? YES
- Clear audience? NEEDS WORK

---

## 2026-01-09: Theory-Building Language Scrub

**Category Changed**: Register, Claims

Systematic replacement of hypothesis-testing language with theory-building alternatives.

- "tests confirm" → "tests indicate"
- "data support the prediction" → "data are consistent with the expectation"
- "validates" → "indicates"

*Rationale*: Theory-building papers discover patterns; they don't test hypotheses.

---

## 2026-01-12: Frame Shift #7 — Qual-Inductive Restructure (FINAL)

**Architecture**: MAJOR restructure to ASQ/OrgSci inductive theory-building genre
**Mechanism**: Named phenomena introduced:
  - "Reliability Hedging" (selection)
  - "Information Shielding" (withholding implications)
  - "The Compositional Shift" (resulting tenure patterns)

**Structural changes**:
- Introduction: Now puzzle-only (removed mechanism preview)
- Theory section: Renamed to "Prior Work and the Displacement Puzzle" with "What Prior Work Assumes" subsection—ends with research question, NOT answer
- Findings: Restructured around named phenomena. Quantitative patterns integrated AFTER qualitative discovery.
- Discussion: Uses named phenomena consistently throughout

**Expansion**: 6,895 → 11,037 words. Quotes: 5 → 8.

*Quality score*: Prior ~24/50 on qual-inductive criteria → estimated ~40-45/50 post-restructure.

**Automation built**: Qual-inductive rubric (10 criteria, 50 pts) for genre-specific validation.

---

## Summary: The Arc

| Version | Title | Fate |
|---------|-------|------|
| 1 | "Automation causes turnover among temp workers" | Killed: didn't survive volume controls |
| 2 | "Workers flee approaching automation" | Killed: data showed opposite pattern |
| 3 | "The Anticipation Paradox" | Evolved: too descriptive |
| 4 | "Option Cultivation" | Evolved: real options alone didn't explain mechanism |
| 5 | "Wait and See" | Killed: **HALLUCINATION** — audit found no worker quotes supporting sensemaking; workers couldn't "make sense" because managers withheld info |
| 6 | "Hedging with Talent" | Reframed: manager-side mechanism discovered |
| 7 | "Hedging with Talent" — Qual-Inductive | **FINAL**: Restructured to inductive genre with named phenomena |

**Key insight**: The paper required a complete shift in protagonist—from workers (who supposedly "made sense" of uncertainty) to managers (who selected on reliability and withheld information). This only emerged when validation revealed the original mechanism was unsupported by the data.

**Critical lesson about AI-assisted research**: The "Wait and See" framing was built on evidence that never existed in the transcripts. The AI had either fabricated quotes or inferred worker attitudes that weren't documented. Only adversarial audit against raw data revealed this—highlighting why external validation against source data is essential when using AI for qualitative analysis.

**Automation built during this journey**:
- `/eval-zuckerman-lite`: Early puzzle check
- Living Paper: Claim-evidence traceability
- Qual-inductive rubric: Genre-specific validation
