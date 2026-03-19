# Paper 1: The Making of "Hedging with Talent"
## A Visual Journey Through 52 Days of Theory Development

**For slide generation: 9 slides recommended**
**Tone: Documentary-style, showing the messy reality of research**

---

## SLIDE 1: The Starting Point
### "Automation Causes Turnover" (Nov 21, 2025)

**Visual**: Hypothesis-testing structure diagram (H1-H5 arrows pointing to outcomes)

The paper began with a clear, testable story: automation threatens workers, workers flee. Simple cause and effect.

**The Framing**:
> "Workers are widely expected to flee approaching automation. Using 59,021 separation records from 13 distribution centers... we show that automation increases turnover among temporary workers."

**The Data**:
- 59,021 temp worker exit records
- 2,506 permanent employee separations
- 21 automation projects across 12 facilities
- 69 interviews from 2020-2021 fieldwork

**The Hypotheses**:
- H1: Automation increases turnover
- H2: Substituting technologies (sorters, robots) show stronger effects
- H3: Workers quit before automation arrives (anticipation)
- H4: Productivity-churn trade-off exists
- H5: Exit composition shifts toward resignations

**Method**: Standard hypothesis-testing quant paper targeting Management Science or JLE

**Time invested**: 1 day (9 section drafts)

---

## SLIDE 2: The Zip Critique Process
### Sending Work to External AI for Adversarial Review (Dec 8, 2025)

**Visual**: Diagram showing package contents flowing to external model

Before submission, the full paper was packaged with all data and code for rigorous external review—a "zip critique."

**What Was Sent**:
```
option_cultivation_FULL_PACKAGE_20251126.zip
├── manuscript.tex (full paper)
├── data/
│   ├── temp_exits.csv (59K records)
│   ├── perm_exits.csv (2.5K records)
│   └── automation_timelines.xlsx
├── analysis/
│   ├── main_analysis.py
│   └── robustness_checks.py
└── REVIEW_PROMPT.md
```

**The Review Prompt Asked**:
1. Do quantitative claims survive robustness checks?
2. Is qualitative evidence properly grounded?
3. Where are the theoretical vulnerabilities?

**Why This Matters**: External AI review with fresh eyes catches what internal review misses. The model could run the actual code, not just read the reported results.

---

## SLIDE 3: The First Devastation
### External Review Kills the Headline Finding (Dec 9, 2025)

**Visual**: Before/after comparison showing effect collapse

The adversarial review returned devastating feedback. The core finding was an artifact.

**The Kill Shot**:
| Specification | Effect | p-value | Verdict |
|--------------|--------|---------|---------|
| Without volume control | +50% exits | 0.003 | "Significant!" |
| WITH volume control | +4-5% exits | 0.63 | **Dead** |

**The Reviewer's Explanation**:
> "Sites with more volume have more exits AND are more likely to automate. Once you control for volume, the apparent 'automation causes turnover' effect disappears entirely."

**What Survived**: One robust pattern—voluntary resignations *decrease* 18-19 percentage points as automation approaches.

**The Verdict**: "Expect a hard reject at ASQ/ManSci in current form."

**Categories Changed**: Evidence, Claims, Robustness, Validation

---

## SLIDE 4: The Pivot
### Building Around What Survived (Dec 9-13, 2025)

**Visual**: Puzzle icon with question mark—"Why do workers STAY?"

The paper pivoted entirely. Instead of "automation causes turnover," the new puzzle: workers don't flee—they stay. Why?

**The New Pattern**:
| Facility Type | Voluntary Exit Share (Early) | Voluntary Exit Share (Late) | Change |
|--------------|------------------------------|----------------------------|--------|
| Sorter facilities | 22.4% | 3.3% | -19.1pp |
| Robot facilities | 40.0% | 21.7% | -18.3pp |

**Candidate Mechanisms Explored**:
1. **Option value** — Workers stay to see how automation plays out
2. **Reduced hiring** — Fewer new workers entering means fewer exits
3. **Selection** — Fearful workers already left before the window
4. **Job lock** — Workers can't leave (no alternatives)
5. **Curiosity/attachment** — Workers want to see what happens

**The Leading Theory**: "Wait and See" — Workers engage in anticipatory sensemaking, staying to process uncertain information before acting.

---

## SLIDE 5: THE HALLUCINATION
### Discovering the Evidence Never Existed (Dec 13, 2025)

**Visual**: Red warning icon, transcript search results showing "0 matches"

The Living Paper audit system was built to verify claims against raw interview transcripts. What it found was devastating.

**The Search**:
Searched 69 interview transcripts for evidence of workers "waiting to see" how automation would affect them.

**Search Terms**:
- "wait and see"
- "curious" (about automation)
- "want to know"
- "find out"

**The Result**:
> "Found 12 matches across 11 files. Most were researcher statements or tangential mentions. **NO clear first-person worker quotes expressing curiosity about automation.**"

**The Devastating Implication**: The entire "sensemaking" mechanism was built on evidence that didn't exist. AI had either:
- Fabricated quotes that weren't in the data
- Inferred worker attitudes that weren't documented
- Assumed a mechanism without grounding it in evidence

**Contradicting Evidence Found**:
- EV-008: Manager reports 75% of workforce shows "really no care" about automation
- EV-007: Manager states immigrant workers "don't wait"
- Evidence of exodus at some facilities contradicting retention narrative

**Categories Changed**: Validation (Hallucination Discovery), Evidence, Mechanism

---

## SLIDE 6: The Mechanism Reversal
### From Worker-Side to Manager-Side (Jan 8, 2026)

**Visual**: Two-panel comparison—crossed-out "Workers make sense" vs. highlighted "Managers select"

With the sensemaking mechanism debunked, a completely different story emerged from the data.

**The Old Story** (Killed):
> Workers stay because they're making sense of uncertainty, waiting to see how automation affects them.

**The New Story** (Emerged):
> Managers select temps on reliability and withhold job-threat information. Under technological uncertainty, this creates a workforce "hedge"—reliable workers stay longer because they don't know to leave.

**Key Evidence for New Mechanism**:
| Metric | Robot Facilities | Sorter Facilities |
|--------|-----------------|-------------------|
| Median tenure (before) | 22 hours | 34 hours |
| Median tenure (after) | 76 hours | 22 hours |
| Change | **+66 hours (+4x)** | -12 hours |
| 95% CI | [56h, 79h] | — |
| Mann-Whitney p | <0.001 | — |

**The Boundary Condition**: Novel technology (robots) creates uncertainty → managers hedge. Mature technology (sorters) has known outcomes → no hedging needed.

**The Protagonist Shift**: The paper completely changed who the actor was—from workers (making sense) to managers (selecting).

---

## SLIDE 7: The Genre Transformation
### From Hypothesis-Testing to Qual-Inductive (Jan 12, 2026)

**Visual**: Side-by-side paper structures—old (H1-H5 → Results) vs. new (Puzzle → Named Phenomena)

The paper needed more than a new mechanism—it needed a different genre entirely.

**Structural Changes**:

| Section | Before | After |
|---------|--------|-------|
| Introduction | States mechanism upfront | Puzzle only—no answer |
| Theory | "Theoretical Development" | "Prior Work and the Displacement Puzzle" |
| — | Ends with hypotheses | Ends with research question |
| Findings | Tests hypotheses | Develops theory through named phenomena |
| — | Quant first | Qual first, quant integrated after |

**Named Phenomena Introduced**:
1. **Reliability Hedging** — Selection on low-turnover workers
2. **Information Shielding** — Withholding job-threat implications
3. **The Compositional Shift** — Resulting tenure patterns

**Register Changes** (Theory-Building Language Scrub):
- "validates" → "indicates"
- "confirms" → "suggests"
- "tests confirm" → "tests indicate"
- "data support the prediction" → "data are consistent with the expectation"

**Length Expansion**: 6,895 → 11,037 words (meets ASQ 10K-12K requirement)

**Quote Count**: 5 → 8 (meets ASQ 8-15 requirement)

---

## SLIDE 8: The Final Paper
### "Hedging with Talent" (Jan 12, 2026)

**Visual**: Final paper title with key contribution highlighted

**Final Title**: "Hedging with Talent: How Managers Use Selection to Navigate Novel Technology"

**Target Journal**: Administrative Science Quarterly (ASQ)

**Core Contribution**:
> When facing novel technology with uncertain outcomes, managers hedge by selecting temporary workers on reliability and shielding them from job-threat information. This creates a compositional shift—longer-tenured, more reliable workers remain—that firms can exploit when technology succeeds.

**Key Findings**:
1. Tenure increases 4x at novel-tech (robot) facilities
2. No change at mature-tech (sorter) facilities
3. Managers deliberately select on reliability under uncertainty
4. Information about automation implications is systematically withheld

**Central Limitation Acknowledged**: N=1 robot facility. The effect is large and robust, but replication needed.

**Theory Violated**: Job Insecurity and Displacement Theory — which predicts workers flee uncertain situations, not stay.

---

## SLIDE 9: The Journey Map
### 52 Days, 7 Frame Shifts, 1 Hallucination

**Visual**: Timeline with key events marked, color-coded by category

| Date | Event | What Changed |
|------|-------|--------------|
| Nov 21 | Initial draft | "Automation causes turnover" (H1-H5) |
| Dec 8 | Zip critique sent | Full package to external AI |
| Dec 9 | Core finding killed | Volume control destroys +50% effect |
| Dec 9 | Pivot to "Anticipation Paradox" | Why do workers STAY? |
| Dec 13 | **HALLUCINATION DISCOVERED** | "Wait and see" evidence never existed |
| Jan 8 | Mechanism reversal | Worker-side → Manager-side |
| Jan 12 | Genre transformation | Hypothesis-testing → Qual-inductive |

**Frame Shift Summary**:
| # | Frame | Fate |
|---|-------|------|
| 1 | "Automation causes turnover" | Killed: volume control |
| 2 | "Workers flee automation" | Killed: opposite pattern |
| 3 | "The Anticipation Paradox" | Evolved: too descriptive |
| 4 | "Option Cultivation" | Evolved: real options insufficient |
| 5 | "Wait and See" | **HALLUCINATION**: No evidence existed |
| 6 | "Hedging with Talent" | Reframed: manager mechanism |
| 7 | "Hedging with Talent" (qual-inductive) | **FINAL** |

**Critical Lessons**:

1. **External validation catches what internal review misses** — The zip critique process found the volume control issue

2. **AI can hallucinate qualitative evidence** — The entire "wait and see" mechanism was built on quotes and worker attitudes that didn't exist in the transcripts

3. **Adversarial audit against source data is essential** — Only by searching the raw transcripts did we discover the fabrication

4. **Major pivots can improve papers** — The final "Hedging with Talent" story is more interesting and better supported than the original "automation causes turnover" claim

**Automation Built During This Journey**:
- `/eval-zuckerman-lite`: Early puzzle check
- Living Paper: Claim-evidence traceability with IRB-protected data
- Qual-inductive rubric: Genre-specific validation (10 criteria, 50 pts)

---

## APPENDIX: Data Snippets for Slides

### For Slide 3 (Volume Control Kill):
```python
# Without volume control
automation_effect = 0.50  # +50% exits
p_value = 0.003

# WITH volume control
automation_effect = 0.045  # +4.5% exits
p_value = 0.63  # Not significant
```

### For Slide 5 (Hallucination Discovery):
```
AUDIT SEARCH: "wait and see", "curious", "want to know", "find out"
TRANSCRIPTS SEARCHED: 69
MATCHES FOUND: 12

BREAKDOWN:
- Researcher statements: 8
- Tangential mentions: 3
- Manager describing workers: 1
- Worker first-person curiosity: 0  ← THE PROBLEM

CONCLUSION: No direct evidence of worker anticipatory sensemaking
```

### For Slide 6 (Tenure Evidence):
```
Robot Facilities (N=1, but robust):
- Pre-automation median tenure: 22 hours
- Post-automation median tenure: 76 hours
- Difference: +54 hours (+245%)
- 95% CI: [56h, 79h]
- Mann-Whitney U test: p < 0.001

Sorter Facilities (N=4):
- Pre-automation median tenure: 34 hours
- Post-automation median tenure: 22 hours
- Difference: -12 hours (-35%)
```

### For Slide 7 (Language Scrub Examples):
```
BEFORE → AFTER

"Our tests confirm that managers..."
→ "Our tests indicate that managers..."

"The data support the prediction that..."
→ "The data are consistent with the expectation that..."

"This validates the hedging mechanism"
→ "This is consistent with a hedging mechanism"

"Lead-lag tests confirm the direction of causality"
→ "Lead-lag analyses suggest the direction of influence"
```
