# From Dormant Data to Submittable Papers in 3 Weeks
## A Qualitative Researcher's Guide to AI-Assisted Paper Development

**Matt Beane, UC Santa Barbara**
**December 2025**
https://github.com/mattbeane/paper-mining-agent-suite
---

## The Setup

I'm an ethnographer. Most of my work involves fieldwork, interviews, and careful qualitative analysis. But like many qualitative researchers, I also collect quantitative data—and like many of us, I have datasets sitting dormant because the analysis-to-paper pipeline is daunting.

In late November 2025, I saw a tweet from Aniket Panjwani suggesting that coding agents like Claude Code could transform exploratory data analysis for social scientists. I decided to test this claim—not on toy data, but on real research datasets I'd collected years ago and never fully exploited.

**What I had:**

- 351 interviews and 718 hours of observation from 12 sites

*Company X (warehouse automation study):*
- ~59,000 temp worker exit records
- ~1,000 full-time worker exit records
- Daily productivity data across facilities
- Automation project timelines
- 69 interviews with 26 informants

*Company Y (performance incentive study):*
- 68,000+ worker-month observations on a performance incentive program from 4 facilities
- 77 interviews with 47 informants (operations managers, supervisors, HR leaders, senior executives)

*Company Z (AI robotics vendor study):*
- 145 interviews from a 3-year field study
- 17 months of ethnographic observation
- 33 million records of human-robot interaction telemetry

**What I produced in ~3 weeks of part-time work:**

- **Paper 1**: "Wait and See: Why Temporary Workers Don't Flee Impending Automation" (targeting ASQ). Uses Company X data: temp exit records, productivity data, automation timelines, and the full qualitative dataset. Core finding: voluntary resignations *decline* 18-19 pp as automation approaches—workers stay to make sense of uncertainty.

- **Paper 2**: "Learning to Automate: How Multi-Site Firms Distribute Exploration and Exploitation Across Facilities" (targeting Management Science). Uses Company X data: daily operational data, separation records, automation timelines, and interviews focused on network planning. Core finding: firms solve the exploration-exploitation dilemma *spatially*—pilot nodes explore, optimization nodes exploit.

- **Paper 3**: "When Misfit Motivates: Work Orientation and Responses to Performance Pay in Warehouse Work" (targeting ASQ or Management Science). Uses Company Y data: 55K+ worker-month observations and 77 interviews. Core finding: work orientation provides an interpretive lens for understanding when P-E misfit triggers intensified effort rather than withdrawal; firm's inverted incentive allocation suggests management is blind to these orientation-driven patterns.

- **Paper 4**: "Developmental Uncertainty: When Coordination Demands Enable Occupational Mobility Across Status Boundaries" (targeting ASQ). Uses Company Z data: 145 interviews, 17 months observation, 33M telemetry records. Core finding: uncertainty drives cross-boundary coordination that enables skill transfer—76% of early-phase drivers advanced to professional roles; the window closes as uncertainty is consumed.

Each paper went through 5-8 complete reframings. The final versions have expanded literature reviews, quantitative analyses with robustness checks, integrated qualitative evidence, figures, online appendices, and are formatted for target journals. They've been stress-tested by a second AI system acting as adversarial pre-reviewer.

**But that's not all.** The process of developing these papers led me to build infrastructure—reusable tools that formalize the workflow:

- **[paper-mining-agent-suite](https://github.com/mattbeane/paper-mining-agent-suite)**: A structured Claude Code workflow with agents for each phase (explore, patterns, theory, lens, mining, framing, audit, verification, drafting)
- **[Living Paper](https://github.com/mattbeane/living-paper)**: A verification layer that links claims to evidence without exposing protected data—generates reviewer packages that journal reviewers can inspect directly

This document explains how.

---

## Why This Matters for Qualitative Researchers

The tweet that sparked this focused on exploratory data analysis—letting AI run regressions and make graphs. That's useful, but it undersells what's possible.

The real power for qualitative researchers is in the *full pipeline*:
1. Exploring data (maybe you haven't touched it in years)
2. Generating multiple theoretical framings
3. Finding the "sensitizing literature" that explains your patterns
4. Integrating qualitative evidence with quantitative findings
5. Iterating through framings until something robust and novel emerges
6. Producing journal-ready manuscripts
7. **NEW: Creating verifiable claim-evidence links for reviewers**

None of this requires you to be a methods expert. It requires you to be a *domain expert*—which you already are.

---

## The 9-Phase Process (Now Codified as Agents)

Each phase below now has a corresponding slash command in the paper-mining-agent-suite. You can use the workflow manually (as I did initially) or use the structured agents.

### Phase 1: Data Exploration (`/explore-data`)

**What you do**: Point the AI at your data files and ask "what's here?"

**What happens**:
- File inventory (sizes, formats, column names)
- Quick descriptive statistics
- Identification of anomalies and patterns
- Surface-level insights about what's interesting

**Example prompt**:
> "I have data files in [directory]. List what's there, give me basic descriptives, and flag anything unusual or potentially interesting."

**What you're looking for**: Anomalies that trigger your domain expertise. When the AI says "28% of workers logged zero hours before exiting," you think "that's weird—something's happening at recruitment or onboarding." That recognition comes from *you*, not the AI.

**Your role**: Curator. The AI generates; you recognize what matters.

---

### Phase 2: Pattern Hunting (`/hunt-patterns`)

**What you do**: Ask "what patterns exist across these variables?"

**What happens**: The AI looks for relationships, clusters, anomalies that might not be obvious from univariate exploration.

**Critical insight**: Your first framing will almost certainly be wrong. That's fine. The goal is to generate options, not commit.

**Example from this project**:

My first framing for Paper 1 was "Automation causes turnover among temp workers." When we ran robustness checks, the finding didn't survive volume controls. We reframed to "Workers flee approaching automation." But the data showed the *opposite*—turnover *decreased* before automation.

That inversion became the paper: "Why Workers *Stay* in Anticipation of Uncertain Automation."

**Frame shift count across 4 papers**: 23+ total

| Paper | Frame Shifts | Final Title |
|-------|--------------|-------------|
| Paper 1 | 5 | Wait and See: Why Temporary Workers Don't Flee Impending Automation |
| Paper 2 | 8 | Learning to Automate: How Multi-Site Firms Distribute Exploration and Exploitation Across Facilities |
| Paper 3 | 5 | When Misfit Motivates: Work Orientation and Responses to Performance Pay |
| Paper 4 | 5+ | Developmental Uncertainty: When Coordination Demands Enable Occupational Mobility |

**Your role**: Evaluator. Kill framings that don't survive scrutiny. Recognize when an inversion is more interesting than the original hypothesis.

---

### Phase 3: Early Puzzle Check (`/check-puzzle-lite`)

**What you do**: Before investing in theory-building, verify you have something worth pursuing.

**Zuckerman criteria** (adapted for early-stage work):
1. Does the finding violate an established theoretical prediction?
2. Is the empirical pattern robust to obvious confounds?
3. Is there enough "there there" to warrant full development?

This gate prevents sunk-cost theory-building on findings that won't survive review.

---

### Phase 4: Finding the Sensitizing Literature (`/find-theory`, `/find-lens`)

**This is the crucial step that transforms description into contribution.**

You've found a robust empirical pattern that violates an established theoretical prediction. Now you need a *second* literature—a "sensitizing" or "interpretive" lens—that helps to explain the heterogeneity in your data.

**The pattern**:
1. Primary theory makes a prediction (e.g., "misfit leads to withdrawal")
2. Your data violates it (e.g., "some workers intensify effort when misfit")
3. You ask: "What explains *which* workers violate the prediction?"
4. You find a literature on that explanatory factor (e.g., "work orientation")
5. Your contribution *bridges* the two literatures

**Examples from this project**:

**Paper 1**:
- Primary theory: Labor economics predicts workers exit when automation threatens jobs
- Violation: Workers stayed; turnover *decreased* before automation
- Sensitizing question: "Why stay when you can easily leave?"
- Sensitizing literature: Real options theory + Sensemaking
- Extension: Anticipatory sensemaking—workers stay to understand before acting

**Paper 3**:
- Primary theory: P-E fit theory predicts misfit → withdrawal
- Violation: Seasonal workers responded 2x as strongly to incentives as full-time
- Sensitizing question: "Why do only *some* misfit workers intensify effort?"
- Sensitizing literature: Work orientation (Wrzesniewski) + Career anchors (Schein)
- Extension: Orientation moderates the misfit-response relationship

**Paper 4**:
- Primary theory: Status boundaries are defended; cross-status contact rarely benefits nonprofessionals
- Violation: 76% of early drivers advanced to professional roles; 19% to roles requiring credentials they lacked
- Sensitizing question: "Why did early workers develop but later workers didn't?"
- Sensitizing literature: Contingency theory (Thompson, Galbraith, Lawrence & Lorsch)
- Extension: Developmental uncertainty—uncertainty forces cross-boundary coordination that enables skill transfer

**How to prompt for this**:

> "We have a finding that violates [primary theory]. The theory predicts X, but we observe Y—but only for some people. What individual or situational factor might explain who responds which way? What literature addresses that factor?"

**Your role**: Theorist. You recognize what makes a good bridging contribution. The AI can search literature, but you evaluate fit.

---

### Phase 5: Qualitative Mining (`/mine-qual`)

**What you do**: Search your interview data for specific mechanisms.

**Example prompt** (actual prompt I used for Paper 3):

```
### HIGH PRIORITY: Why Do Seasonal Workers Respond More?

1. **Income salience**: Do seasonal workers talk about money differently? More stressed about bills?
2. **Bonus significance**: Is a $50 bonus life-changing for seasonal but trivial for FT?
3. **Proving themselves**: Are seasonal workers trying to get noticed for promotion?
4. **No ceiling effect**: Have FT workers already hit their effort max?

### MEDIUM PRIORITY: Why Is Pay Inverted?

5. **Bonus caps**: Are there explicit or implicit caps on what seasonal workers can earn?
6. **Manager discretion**: Do managers direct bonuses to FT workers preferentially?

### Look for disconfirming evidence. What quotes challenge the interpretation?

### Organize output as:
1. Evidence by claim (for each quant claim, provide supporting/challenging evidence)
2. Key quotes (10-15 most compelling, with context)
3. Disconfirming evidence
4. Suggestions for integration
```

**The payoff**: This prompt, applied to 77 interviews, produced the insight that became Paper 3's core contribution: the "seasonal" category blends three distinct worker types (career-oriented, flexibility-seeking, income-targeting), each responding differently to the same incentive system.

**Your role**: Mechanism detective. You hypothesize what's going on; the AI finds the evidence.

---

### Phase 6: Claim Framing (`/smith-frames`)

**What you do**: Iterate on how to frame your contribution.

Each paper needs:
- A clear violation of established theory
- An explanation of why the violation occurs
- Theoretical mechanisms connecting evidence to claims
- Boundary conditions

---

### Phase 7: Claim Audit (`/audit-claims`)

**What you do**: Systematically search your raw data for supporting AND challenging evidence for each claim.

**This is new and critical.** The biggest risk of AI-assisted paper development is that you (and the AI) convince yourselves of a story that isn't grounded in the data.

The audit phase:
1. Takes each claim in your manuscript
2. Searches the raw data for evidence
3. Documents supporting evidence with quotes/data
4. **Actively searches for challenging evidence**
5. Flags high-concern claims

Output: Living Paper-compatible files (claims.jsonl, evidence.jsonl, links.csv)

---

### Phase 8: External Verification (`/verify-claims`)

**What you do**: Send verification packages to a *different* AI system for adversarial review.

**Why this matters**: The AI that helped you build the paper has seen your reasoning. A different system—with different strengths—provides fresh eyes.

**My approach**: I used Claude Code (Opus) for generation and analysis. I sent verification briefs to ChatGPT Pro (reasoning mode) for deep adversarial review.

**NEW: Automated Living Paper Integration**

When you run `/verify-claims`, it now automatically:
1. Ingests your claims/evidence into the Living Paper database
2. Runs verification checks
3. Generates a reviewer package

The reviewer package is a folder with standalone HTML files. Reviewers can double-click to open—no CLI needed on their end. They see:
- Your claims
- The evidence supporting each claim
- Any challenging evidence
- Contradiction badges highlighting tensions

This creates a "trustless verification" mechanism: reviewers can audit the structure of your argument without seeing raw PII.

---

### Phase 9: Drafting (`/draft-paper`)

**What you do**: Generate journal-formatted manuscripts.

**What a submission-ready paper needs**:

1. **Online Appendix** with:
   - Full robustness check tables (not just prose summaries)
   - Detailed variable definitions
   - Interview sample composition
   - Coding protocols for qualitative data
   - Event-study or pre-trend figures
   - Any analysis mentioned but not shown in main text

2. **Replication Package** with:
   - All analysis scripts
   - Requirements file (dependencies)
   - README with instructions
   - Generated outputs (figures, tables)
   - Data availability statement

3. **Living Paper verification package** (new):
   - claims.jsonl, evidence.jsonl, links.csv
   - Reviewer HTML interface
   - Can be submitted as supplementary materials or shared with reviewers

---

## The Professional Wisdom

Over 3 weeks, I made dozens of judgment calls that shaped these papers. Here's what I was doing, distilled:

### 1. "What interpretive lens helps explain the variation?"

This is the sensitizing literature move. It transforms "here's a pattern" into "here's a contribution."

### 2. "Show me what survives controls"

Every exciting finding got stress-tested. Findings that died got reframed around what *did* survive.

### 3. "What established prediction are we violating?"

The contribution comes from showing something the literature wouldn't expect—and explaining why.

### 4. "Find the heterogeneity"

All four papers benefited from looking *within* categories to find subgroups that behave differently. The aggregate effect often obscures the real story.

### 5. "We don't have data on that"

I caught multiple overclaims—places where we were asserting something (e.g., "what workers want") that we hadn't actually measured. Revealed preferences ≠ stated preferences.

### 6. "This has to fit [journal] format"

Genre awareness. Different journals want different things. I internalized those expectations from years of reading and reviewing.

### 7. "Send it to [expensive AI] for review"

Using a different AI system as adversarial pre-reviewer catches errors and forces precision. It's like asking a skeptical colleague to read your draft—except available at 2am.

### 8. "Can we verify this?" (NEW)

With Living Paper integration, every claim now traces to specific evidence. This isn't just for reviewers—it forces me to be honest with myself about what the data actually show.

---

## What You Need to Make This Work

### 1. Domain expertise

The AI can search literature, run analyses, and draft text. It cannot recognize when a finding is theoretically interesting or when a framing doesn't fit your field. That's you.

### 2. Existing data

This approach works best when you already have data—especially mixed-methods data. The AI dramatically accelerates analysis and writing, but it doesn't collect data for you.

### 3. Tolerance for iteration

23+ frame shifts across 4 papers. You have to be willing to kill your darlings repeatedly when the evidence doesn't support them.

### 4. Quality control instincts

You need to know what reviewers will catch. The AI helps, but you're the gatekeeper.

### 5. A second AI for verification

Using the same system for generation and review has blind spots. A different system provides genuinely fresh perspective.

---

## What This Doesn't Replace

- Fieldwork
- Data collection
- Domain expertise
- Theoretical intuition
- Quality judgment
- Understanding what makes a contribution

What it *dramatically accelerates*:
- Exploratory data analysis
- Literature searching and synthesis
- Draft generation
- Robustness checking
- Qualitative-quantitative integration
- Revision cycles
- **Verification and audit trails**

---

## The Bottom Line

I had data from three field studies that had been sitting dormant for 2-5 years. I hadn't touched them because the analysis-to-paper pipeline felt overwhelming. In ~3 weeks of part-time work, I produced four submission-ready papers with full online appendices:

1. **Paper 1: "Wait and See"** (targeting ASQ) - Workers stay to make sense of uncertain automation. Uses Company X data. Complete with event-study figures, robustness checks, and verification package.

2. **Paper 2: "Learning to Automate"** (targeting Management Science) - Firms distribute exploration and exploitation across facilities. Uses Company X data. Complete with 9 alternative threshold robustness checks, pre-trend analysis, placebo tests, and replication code.

3. **Paper 3: "When Misfit Motivates"** (targeting ASQ or Management Science) - Work orientation provides interpretive lens for when misfit motivates vs. demotivates; misallocation as evidence of firm blindness. Uses Company Y data. Complete with worker fixed effects robustness, lead-lag tests, engagement distribution analysis, and sensitivity analysis across specifications.

4. **Paper 4: "Developmental Uncertainty"** (targeting ASQ) - Uncertainty enables cross-status skill transfer—until it closes. Uses Company Z data. Complete with phase transition analysis using 33M telemetry records and career outcome tracking.

**And I built tools for others to use:**

- **paper-mining-agent-suite**: The workflow as structured agents
- **Living Paper**: Verification infrastructure for qualitative research

This isn't magic. It's leverage. The AI amplifies what you already know how to do. If you're a skilled qualitative researcher with dormant data, you can probably do something similar.

The key insight: Don't think of AI as a replacement for your expertise. Think of it as a very fast, very patient research assistant that never gets tired and can search the literature at 3am. You're still the one making the judgment calls.

Those judgment calls—what framing to pursue, what sensitizing literature to use, what claims to kill, what evidence is compelling—are exactly what your PhD trained you for.

---

## Appendix: Full Frame Shift Log

### Paper 1: Wait and See

| # | Frame | Fate |
|---|-------|------|
| 1 | "Automation causes turnover among temp workers" | Killed: didn't survive volume controls |
| 2 | "Workers flee approaching automation" | Killed: data showed opposite pattern |
| 3 | "The Anticipation Paradox: Turnover declines before automation" | Evolved: too descriptive |
| 4 | "Option Cultivation: Why Workers Stay" | Evolved: real options alone didn't explain mechanism |
| 5 | **"Wait and See: Why Temporary Workers Don't Flee Impending Automation"** | Final: anticipatory sensemaking + real options, explains both staying AND technology moderation |

### Paper 2: Learning to Automate

| # | Frame | Why It Shifted |
|---|-------|----------------|
| 1 | "Seasonal staffing and facility productivity" | Purely descriptive—no theoretical mechanism |
| 2 | "Turnover contagion in warehouse operations" | One finding, not full story of what's happening |
| 3 | "The Seasonal Paradox" | Staffing isn't the main story; automation is |
| 4 | "Automation Architectures" | Documents heterogeneity but still descriptive |
| 5 | Tested Thompson (1967) buffering | **Rejected by data**: Volume variance test showed expansion and efficiency nodes have identical CV (~0.59) |
| 6 | Searched qual data for intentional role differentiation | **Evidence found**: "Gallatin develops, Fresno perfects" |
| 7 | Tested facility size × automation interaction | **Statistically significant (p=0.001)** |
| 8 | **"Learning to Automate"** | **Final**: Spatial ambidexterity—firms solve exploration-exploitation dilemma across geography |
| 9 | Post-adversarial review feedback (Jan 2026) | Minor refinements: n=1 optimization facility acknowledged; role terminology footnote added; pre-trend narrative nuanced; seasonality controls with analysis; outlier sign flip made explicit; winsorizing added to event study |

### Paper 3: When Misfit Motivates

| # | Frame | Fate |
|---|-------|------|
| 1 | "Incentive Misallocation: Why High-Responders Get Low Pay" | Killed: allocation isn't the puzzle |
| 2 | "Motivational Leverage" | Evolved: leverage is property of what? |
| 3 | "Signaling to Escape" | Evolved: only explains one subgroup |
| 4 | "When Misfit Motivates" (draft 1) | Evolved: too broad |
| 5 | "When Misfit Motivates: Work Orientation Moderates Misfit Response" | Killed: reviewer feedback—orientation is never directly observed; "moderator" overstates causal claim |
| 6 | **"When Misfit Motivates: Work Orientation as Interpretive Lens"** | Final (Jan 2026): Primary = misfit can motivate (P-E fit extension); orientation = interpretive lens for heterogeneity; misallocation = evidence firm is blind to patterns. Softened causal language throughout; "Propositions" → "Expected Patterns" |

### Paper 4: Developmental Uncertainty

| # | Frame | Fate |
|---|-------|------|
| 1 | "Ghost work and hidden AI labor" | Evolved: our case showed opposite—visibility and advancement |
| 2 | "Cross-status learning in tech development" | Evolved: too generic |
| 3 | "The closing window: Why timing matters for nonprofessional advancement" | Evolved: needed theoretical anchor |
| 4 | "Uncertainty as enabler" | Evolved: needed to connect to contingency theory |
| 5 | **"Developmental Uncertainty: When Coordination Demands Enable Occupational Mobility"** | Final: extends contingency theory to skill transfer and career mobility |

---

## Appendix: The Tools That Emerged

### paper-mining-agent-suite

**What it is**: A structured Claude Code workflow with slash commands for each phase.

**Key features**:
- Quality gates (warns if out of sequence)
- Frame management (archive old frames, compare alternatives)
- Style enforcement (ASQ/OrgSci/ManSci register)
- State tracking (knows where you are in the pipeline)
- Seamless Living Paper integration

**Repo**: https://github.com/mattbeane/paper-mining-agent-suite

### Living Paper

**What it is**: A verification layer that links claims to evidence.

**Key features**:
- Bidirectional claim-evidence traceability
- Three-tier access control (PUBLIC, CONTROLLED, WITNESS_ONLY)
- Entity redaction for IRB compliance
- Standalone HTML reviewer packages
- No cloud dependencies—runs locally

**Repo**: https://github.com/mattbeane/living-paper

---

*Document updated December 2025. For questions: mattbeane@ucsb.edu*
