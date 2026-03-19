# Paper Revision Change Categories

This document defines the typology of changes that can occur during paper development. Each revision event is classified across these categories—multiple categories can change simultaneously.

---

## Substantive/Content Categories

### Framing
**What it is**: The core theoretical argument—what puzzle you're solving, what theory you're violating, what contribution you're making.

**Examples from Paper 1**:
- "Automation causes turnover among temp workers" → Killed (didn't survive volume controls)
- "Workers flee approaching automation" → Killed (data showed opposite)
- "Workers stay to wait and see" → Killed (sensemaking mechanism unsupported)
- "Managers hedge with talent selection" → Final

**Signals a framing change**: New title, new abstract, different "violation" of theory, different contribution claim.

---

### Mechanism
**What it is**: The causal story explaining *why* the pattern exists—the theoretical engine.

**Examples from Paper 1**:
- Direct causal effect (automation → job threat → exit)
- Sensemaking under uncertainty (workers process information before acting)
- Real options (workers preserve option value by staying)
- Selection under uncertainty (managers select reliable workers when tech is novel)

**Signals a mechanism change**: New "because" statement, different mediating variable, shift in who the actor is (workers vs managers).

---

### Evidence
**What it is**: Which quantitative findings, qualitative quotes, and robustness checks are included in the manuscript.

**Examples**:
- Added Mosio SMS survey data (156 workers, Oct 2020 - Aug 2021)
- Dropped the "40% turnover increase" finding (didn't survive volume controls)
- Added diff-in-diff tenure analysis (+74h, 95% CI: 62-92h)
- Increased quote count from 5 to 8

**Signals an evidence change**: New tables, new figures, new quotes, dropped analyses, added robustness checks.

---

### Claims
**What it is**: The specific assertions the paper makes—can be strengthened, softened, or killed entirely.

**Examples**:
- Killed: "Automation increases turnover by 40-50%"
- Softened: "validates" → "indicates"; "confirms" → "suggests"
- Added: "Tenure increases 4x at novel-tech facilities"
- Bounded: "N=1 robot facility acknowledged as limitation"

**Signals a claims change**: Language precision shifts, assertions added/removed, confidence levels adjusted.

---

### Boundaries
**What it is**: Where the argument applies and where it doesn't—scope conditions and limitations.

**Examples from Paper 1**:
- Added: "Novel vs mature technology" as moderator
- Added: "N=1 robot facility" limitation
- Added: "Temp workers only—permanents show different pattern"

**Signals a boundaries change**: New "when does this apply" discussion, new limitations section content, scope narrowing/expanding.

---

## Structural/Genre Categories

### Architecture
**What it is**: Section ordering, where different content lives, how the paper is organized.

**Examples from Paper 1**:
- Moved mechanism from Theory section to Findings section (inductive restructure)
- Renamed "Theoretical Development" → "Prior Work and the Displacement Puzzle"
- Added "What Prior Work Assumes" subsection
- Restructured Findings around named phenomena: "Reliability Hedging," "Information Shielding," "The Compositional Shift"

**Signals an architecture change**: Section renaming, content relocation, new subsections, structural reorganization.

---

### Register
**What it is**: The linguistic style—theory-testing vs theory-building language, passive vs active voice, hedging patterns.

**Examples**:
- "validates this framework by testing" → "checked whether...aligned"
- "confirms that" → "indicates that"
- "Lead-lag tests confirm" → "Lead-lag analyses suggest"
- Reduced passive voice from 40% to <30%

**Signals a register change**: Systematic word substitutions, voice changes, hedging adjustments.

---

### Length
**What it is**: Word count, quote count, table count—hitting journal norms.

**Examples from Paper 1**:
- Introduction: 366 → 1,021 words
- Total: 6,895 → 11,037 words
- Quotes: 5 → 8 (meets ASQ 8-15 requirement)

**Signals a length change**: Expansion or compression of sections, quote additions/removals.

---

## Verification/Quality Categories

### Robustness
**What it is**: Adding controls, alternative specifications, placebo tests, sensitivity analyses.

**Examples**:
- Added volume controls (finding survived)
- Added seasonality controls
- Fixed broken placebo test (Paper 2)
- Added 9 alternative threshold robustness checks (Paper 2)

**Signals a robustness change**: New appendix tables, new robustness discussion, new controls in specifications.

---

### Validation
**What it is**: External review, adversarial testing, claim audits—checking the work.

**Examples**:
- Dec 9, 2025: External "friendly review" delivered devastating feedback
- Dec 13, 2025: Comprehensive audit (3,949 evidence items linked to claims)
- Jan 2026: Adversarial review revealed sensemaking mechanism unsupported

**Signals a validation change**: Review received, audit completed, verification package created.

---

### Zip Critique (External Model Review)
**What it is**: Packaging the full paper + data + code into a zip file and sending to a powerful external AI model for rigorous, adversarial review. Different from internal validation because it uses a separate system with fresh eyes.

**Examples**:
- Dec 8, 2025: Sent option_cultivation_FULL_PACKAGE_20251126.zip to external model
- Dec 8, 2025: Sent learning_to_automate_FULL_PACKAGE_20251126.zip for critique
- External model verified reviewer claims against actual code/data
- External model ran replication checks and found placebo test bug (Paper 2)

**Process**:
1. Package manuscript.tex + data files + analysis code + prior reviews into .zip
2. Write REVIEW_PROMPT.md with specific verification requests
3. Send to powerful external model (e.g., o1, Opus) for rigorous critique
4. Model runs code, checks claims against data, stress-tests theory
5. Receive point-by-point critique with specific line-number citations

**Signals a zip critique**: New *_REVIEW_*.zip file created, REVIEW_PROMPT.md written, detailed critique document returned.

---

### Hallucination/Error Discovery
**What it is**: Discovery that AI-generated content (quotes, statistics, claims) was fabricated or incorrect. A critical validation failure that often triggers major reframing.

**Types of hallucination**:
- **Qualitative**: AI fabricates interview quotes that don't exist in transcripts
- **Quantitative**: AI invents statistics, p-values, or effect sizes
- **Mechanism**: AI claims a causal story the data doesn't support

**Examples from Paper 1**:
- "Wait and see" mechanism was built on assumption workers expressed curiosity about automation
- Adversarial audit of 69 transcripts found: "No worker first-person accounts of 'waiting to see'"
- The paper had described workers as "making sense" of automation—but search found NO quotes of workers expressing curiosity
- Entire framing had to be killed when evidence base proved fabricated/unfound

**Examples from Paper 2**:
- Placebo test appeared valid but was broken (all 1,000 iterations produced identical result)
- Verification revealed variance = 0 due to merge bug returning same dates

**Signals hallucination discovery**: Audit finds "NO EVIDENCE FOUND," quote search returns empty, replication reveals broken code, mechanism proves unsupported by actual data.

---

### Replication
**What it is**: Code, data availability statements, reproducibility infrastructure.

**Examples**:
- Created replication package with Python scripts
- Added DATA_DESCRIPTOR.md
- Created validation_package.zip
- Built living_paper infrastructure for claim-evidence traceability

**Signals a replication change**: New code files, new documentation, new packages.

---

## Meta/Tooling Categories

### Automation Added
**What it is**: New slash commands, scripts, prompts, or infrastructure built to solve a problem encountered during paper development.

**Examples**:
- `/eval-zuckerman-lite` built after wasting weeks on non-puzzles
- Style enforcer built after Claude defaulted to wrong genre register
- Living Paper built to handle IRB-protected data verification
- Consensus mode built after single-run reproducibility concerns
- Qual-inductive rubric built after generic rubrics failed qual papers

**Signals automation added**: New tool in theory-forge, new script in analysis folder, new prompt file.

---

### Workflow Refinement
**What it is**: Changes to how the human-AI collaboration works—not the paper itself, but how papers get made.

**Examples**:
- Added early puzzle check (Zuckerman-lite) BEFORE theory investment
- Added external verification step (send to different AI system)
- Added claim audit step BEFORE drafting
- Restructured pipeline: exploration → patterns → puzzle check → theory → lens → mining → framing → verification → drafting

**Signals workflow refinement**: New step in the process, reordered steps, new quality gate.

---

## Using This Typology

When classifying a revision event:

1. **Identify what changed** — read the commit message, diff, or document
2. **Check each category** — did this change affect framing? mechanism? evidence? etc.
3. **Write brief description** — for each affected category, describe what changed
4. **Assign hierarchy level** — is this a major version shift, a session-level change, or a commit-level detail?

Multiple categories often change together. A "major version" typically involves framing + mechanism + architecture changes. A "commit" might only touch register or length.
