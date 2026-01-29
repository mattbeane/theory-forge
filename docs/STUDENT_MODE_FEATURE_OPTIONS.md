# Student Mode: Feature Options Weighted by Probability of Success

---

## The Core Problem

The risks aren't about AI accuracy. They're about **what students fail to develop** when AI does the work:

| Skill | How It's Normally Built | How AI Bypasses It |
|-------|------------------------|-------------------|
| **Knowing your data** | Hours reading transcripts, noticing patterns | AI summarizes; student never reads raw |
| **Scholarly taste** | Internalizing Zuckerman criteria through failed papers | AI enforces criteria; student never fails |
| **Theory intuition** | Reading 200 papers, feeling what's missing | AI suggests theories; student never struggled |
| **Iteration tolerance** | 15 drafts, each reframed | AI generates 5 frames instantly; no struggle |
| **Qual-quant triangulation** | Noticing something in interviews, checking quant | AI finds supporting quotes for any quant finding |

---

## Feature Options: Ranked by Probability of Actually Working

### TIER 1: HIGH PROBABILITY (80%+)
*These will likely improve outcomes if implemented*

#### 1.1 Mandatory Prediction Prompts
**What**: Before AI runs analysis, student must write what they expect to find.
**How**: Each command shows prompt, waits for text input, logs to `STUDENT_WORK.md`, then runs.
**Why it works**: Forces engagement with the question before seeing the answer. Creates documentation of pre-AI thinking.
**Risk addressed**: #1 (deskilling), #4 (iteration muscle)
**Implementation**: 2-3 hours per command

#### 1.2 Explanation Layers (AI Shows Reasoning)
**What**: Every AI output includes "Why I Did This" section explaining reasoning.
**How**: Append to command prompts: "After output, explain your reasoning: what you looked for, key judgment calls, alternatives you considered."
**Why it works**: Makes the black box transparent. Student learns the process, not just the output.
**Risk addressed**: #2 (automating taste)
**Implementation**: 1-2 hours per command

#### 1.3 Adversarial Evidence Surfacing
**What**: AI actively searches for evidence that contradicts emerging theory.
**How**: Built into `/mine-qual` and `/verify-claims`: "Now find quotes that challenge or contradict this framing."
**Why it works**: Prevents cherry-picking by forcing confrontation with disconfirming data.
**Risk addressed**: #3 (cherry-picking), #7 (hallucination)
**Implementation**: Already partially exists; enhance to be more aggressive

#### 1.4 Audit Trail Documentation
**What**: Auto-log what student did vs. what AI did to `DECISION_LOG.md`.
**How**: Each command appends: timestamp, command run, student input (if any), AI output summary, student decision.
**Why it works**: Creates reviewable record. Advisor can see what happened. Methods section writes itself.
**Risk addressed**: #8 (methods section)
**Implementation**: Already exists; enhance with student-specific fields

---

### TIER 2: MEDIUM PROBABILITY (50-79%)
*These might work but have significant uncertainties*

#### 2.1 Staged Command Unlocking
**What**: Certain commands locked until student demonstrates prior work.
**How**: `/smith-frames` won't run until student has uploaded their own 1-paragraph framing attempt to `analysis/student_framing/`.
**Why it works**: Forces student to try before seeing AI alternatives.
**Risk addressed**: #1 (deskilling), #2 (taste)
**Uncertainty**: Students might write garbage just to unlock. No verification of quality.
**Implementation**: 3-4 hours per gated command

#### 2.2 Advisor Notification at Gates
**What**: Optional email/webhook to advisor when student passes major gates.
**How**: State.json tracks `advisor_email`; hooks fire notification at Gate A, C, F.
**Why it works**: Human accountability without requiring advisor to use the tool.
**Risk addressed**: #1, #3, #8
**Uncertainty**: Depends on advisor actually reading notifications. Many won't.
**Implementation**: 4-6 hours (email/webhook infrastructure)

#### 2.3 Manual Coding Requirement (Partial)
**What**: Before `/mine-qual` processes all interviews, student must code N interviews by hand.
**How**: Student uploads coding to designated folder; AI runs on remainder.
**Why it works**: Ensures student has touched raw data before AI processes it.
**Risk addressed**: #1 (knowing data)
**Uncertainty**: How do we verify student actually coded vs. used AI to code then claimed manual? No good answer.
**Implementation**: 3-4 hours, but verification is unsolved

#### 2.4 Comparison Reports (Student vs. AI)
**What**: After student provides input, AI shows side-by-side: "You found X, I found Y, overlap is Z%."
**How**: Structured comparison output after any student+AI dual analysis.
**Why it works**: Makes learning explicit. Student sees gaps in their own analysis.
**Risk addressed**: #1, #4
**Uncertainty**: Useful only if student engages with the comparison. Many will skip.
**Implementation**: 2-3 hours per command

---

### TIER 3: LOW PROBABILITY (20-49%)
*These sound good but likely won't achieve intended effect*

#### 3.1 Automated Skill Evaluation
**What**: AI evaluates whether student's coding/analysis demonstrates sufficient understanding.
**How**: LLM reviews student work, provides feedback, blocks progression if inadequate.
**Why it doesn't work**:
- "Good coding" is contested; no ground truth
- LLM might reward codes matching its own biases
- Students will learn to game the evaluator
**Risk addressed**: Would address #1 if it worked
**Implementation**: High effort, low confidence

#### 3.2 Time-Based Delays
**What**: Force minimum time between commands (e.g., must wait 2 hours between `/explore-data` and `/hunt-patterns`).
**How**: State.json tracks timestamps; commands check elapsed time.
**Why it doesn't work**:
- Arbitrary; doesn't ensure engagement
- Punishes fast workers and slow workers alike
- Easy to circumvent (just wait, don't think)
**Risk addressed**: None effectively
**Implementation**: Easy but pointless

#### 3.3 Quiz-Based Unlocking
**What**: Student must pass quiz about their data/theory before proceeding.
**How**: AI generates quiz based on project content; student answers; proceeds if correct.
**Why it doesn't work**:
- Trivial to use AI to answer the quiz
- Tests recall, not understanding
- Annoying without being educational
**Risk addressed**: Appearance of addressing #1
**Implementation**: High effort, easily gamed

---

### TIER 4: STRUCTURAL / NON-FEATURE
*These address risks but aren't software features*

#### 4.1 Required Advisor Co-Pilot
**What**: Theory-forge designed for advisor+student pairs, not solo student use.
**How**: Documentation, workshop design, explicit "this tool is for guided use" messaging.
**Why it might work**: Human judgment where AI can't evaluate quality.
**Risk addressed**: All of them, potentially
**Uncertainty**: Depends entirely on advisor engagement and competence.

#### 4.2 Progressive Curriculum Integration
**What**: Theory-forge used only after student has completed traditional qual methods training.
**How**: Documentation recommends: "Use this tool only after you've coded at least one dataset by hand."
**Why it might work**: Ensures baseline skill exists before acceleration.
**Risk addressed**: #1, #2
**Uncertainty**: Honor system; no enforcement.

#### 4.3 Workshop-Based Introduction
**What**: Students learn tool in facilitated workshop, not solo exploration.
**How**: TORS-style sessions where cohort works through tool together with faculty guidance.
**Why it might work**: Collective learning, immediate feedback, norms established.
**Risk addressed**: All of them
**Uncertainty**: Doesn't scale; requires ongoing faculty time.

---

## Recommended Implementation Priority

### Build Now
1. **Prediction prompts** — high impact, low effort
2. **Explanation layers** — makes reasoning visible
3. **Enhanced adversarial evidence** — already partially exists
4. **Better audit trail** — supports methods section writing

### Build If Resources Allow
5. **Staged command unlocking** — forces student attempt first
6. **Advisor notifications** — optional accountability layer
7. **Comparison reports** — makes learning explicit

### Don't Build
- Automated skill evaluation (unsolved problem)
- Time-based delays (annoying, ineffective)
- Quiz-based unlocking (easily gamed)

### Do Instead of Building
- Write clear documentation: "This tool assumes prior qual methods training"
- Design workshop curriculum for TORS-style introduction
- Create advisor guide: "How to supervise students using Theory-Forge"
