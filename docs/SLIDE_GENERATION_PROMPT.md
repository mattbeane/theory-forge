# Slide Generation Prompt: AI-Assisted Qualitative Research

**Purpose**: Generate a 15-20 slide presentation for PhD students about using AI to accelerate qualitative research paper development.

**Audience**: PhD students in management, sociology, organizational behavior—people who collect qualitative data (interviews, ethnography) and struggle with the analysis-to-paper pipeline.

**Tone**: Conversational but substantive. Not hype, not fear. Practical, grounded in real experience.

---

## PRESENTATION STRUCTURE

### Section 1: The Origin Story (Slides 1-4)

**Slide 1: Title**
- Title: "From Dormant Data to Submittable Papers: How I Used AI to Write 4 Papers in 3 Weeks"
- Subtitle: "...and Built Tools So You Can Too"
- Matt Beane, UC Santa Barbara
- December 2025

**Slide 2: The Problem**
- Show the "file drawer problem" for qualitative researchers
- Key stats to include:
  - Many researchers have 2-5 years of untouched data
  - The analysis-to-paper pipeline is overwhelming
  - Mixed-methods work is especially daunting
- Visual suggestion: An overflowing filing cabinet or hard drive icon with dust

**Slide 3: The Spark**
- A tweet from Aniket Panjwani about coding agents for social science
- Key quote: "If you're a social scientist you can save 100s of hours using coding agents like Claude Code for all your exploratory data analysis"
- My reaction: "This undersells it. What about the FULL pipeline?"
- Visual: Screenshot of tweet or simplified version

**Slide 4: What I Actually Had**
- Company X data: 59K temp worker exits, daily productivity, automation timelines, 351 interviews
- Company Y data: 68K worker-month observations, 77 interviews
- Company Z data: 145 interviews, 17 months ethnography, 33M telemetry records
- All sitting dormant for 2-5 years
- Visual: Data inventory table

---

### Section 2: What I Produced (Slides 5-8)

**Slide 5: The Output—4 Papers**
- Paper 1: "Wait and See" (workers STAY when automation approaches—voluntary resignations drop 18-19 pp)
- Paper 2: "Learning to Automate" (firms solve exploration/exploitation spatially—pilot nodes vs optimization nodes)
- Paper 3: "When Misfit Motivates" (work orientation moderates P-E fit—seasonal workers respond 2x)
- Paper 4: "Developmental Uncertainty" (uncertainty enables cross-status skill transfer—76% advanced, window closes)

**Slide 6: The Plot Twists**
- Every paper started with a wrong hypothesis
- 23+ total frame shifts across 4 papers
- Example: "Workers flee automation" → data showed OPPOSITE → became Paper 1
- Key insight: The AI helped me find what the data actually showed, not what I expected

**Slide 7: What Made This Possible**
- Not magic—leverage
- AI as "very fast, very patient research assistant that never gets tired"
- Still needed: domain expertise, theoretical intuition, quality judgment
- Visual: Researcher + AI = accelerated output (not AI alone)

**Slide 8: ...And I Built Infrastructure**
Two repos emerged from the process:
- **paper-mining-agent-suite**: Structured workflow with quality gates
- **Living Paper**: Verification layer for reviewers
- These are now available for others to use
- Visual: Two repo logos/icons

---

### Section 3: The Workflow (Slides 9-14)

**Slide 9: The 9-Phase Pipeline**
Show the full workflow as a diagram:
1. `/explore-data` - What's here?
2. `/hunt-patterns` - What relationships exist?
3. `/check-puzzle-lite` - Is this worth pursuing?
4. `/find-theory` - What does the literature predict?
5. `/find-lens` - What explains the heterogeneity?
6. `/mine-qual` - What do informants say about this?
7. `/smith-frames` - How do we frame the contribution?
8. `/audit-claims` - What evidence supports/challenges each claim?
9. `/verify-claims` - External adversarial review + Living Paper export

**Slide 10: The Key Move—Finding Sensitizing Literature**
The pattern that makes contributions:
1. Primary theory predicts X
2. Your data shows Y (violation!)
3. You find a SECOND literature that explains WHO violates
4. Your contribution BRIDGES the two literatures

Example from Paper 3:
- P-E fit theory predicts misfit → withdrawal
- Data: seasonal workers respond 2x to incentives (OPPOSITE)
- Sensitizing lit: Work orientation (Wrzesniewski, Schein)
- Contribution: Orientation moderates the misfit-response relationship

**Slide 11: Frame Shifts Are The Process**
- Show example frame shift table (Paper 1):
  1. "Automation causes turnover" → Killed: didn't survive controls
  2. "Workers flee automation" → Killed: data showed opposite
  3. "Anticipation Paradox" → Evolved: too descriptive
  4. "Option Cultivation" → Evolved: needed mechanism
  5. **"Wait and See"** → Final: sensemaking + real options

- Key lesson: Be willing to kill your darlings. The FIRST framing is almost never right.

**Slide 12: Qualitative-Quantitative Integration**
- This is where qual researchers have an advantage
- Don't ask for summaries—ask for SPECIFIC evidence for SPECIFIC mechanisms
- Example prompt structure (show simplified version):
  - "Why do seasonal workers respond more?"
    - Income salience?
    - Proving themselves for promotion?
    - No ceiling effect?
  - "Look for DISCONFIRMING evidence"

**Slide 13: The Verification Problem (Why Living Paper Exists)**
- Biggest risk of AI-assisted work: convincing yourself of a story not grounded in data
- Solution: Systematic audit of claims against raw evidence
- Living Paper creates:
  - Bidirectional claim-evidence links
  - Explicitly searches for challenging evidence
  - Reviewer packages that don't expose protected data
- Visual: Claim → Evidence diagram with contradiction badges

**Slide 14: The Anti-Hallucination Design**
- Built-in skepticism:
  - `/audit-claims` searches for CHALLENGING evidence
  - `/verify-claims` goes to a DIFFERENT AI system
  - Living Paper forces explicit evidence links
  - Zuckerman criteria at two checkpoints
- Key quote: "The system that built the analysis should NOT be the only verifier"

---

### Section 4: How to Use This (Slides 15-17)

**Slide 15: What You Need**
1. **Domain expertise** - AI can't recognize when a finding is theoretically interesting
2. **Existing data** - This accelerates analysis, not collection
3. **Tolerance for iteration** - 23+ frame shifts means killing darlings repeatedly
4. **Quality control instincts** - You know what reviewers will catch
5. **A second AI for verification** - Different strengths, fresh eyes

**Slide 16: Getting Started**
```bash
# Clone the repo
git clone https://github.com/mattbeane/paper-mining-agent-suite.git
cd paper-mining-agent-suite

# Open in Claude Code
claude .

# Initialize a project
/init-project

# Start exploring
/explore-data
```

Key commands to learn:
- `/status` - Where am I in the pipeline?
- `/new-frame` - Archive current frame, start fresh
- `/verify-claims` - Generate reviewer package

**Slide 17: What This Doesn't Replace**
- Fieldwork
- Data collection
- Domain expertise
- Theoretical intuition
- Quality judgment
- Understanding what makes a contribution

What it dramatically accelerates:
- Exploratory analysis
- Literature synthesis
- Draft generation
- Robustness checking
- Qual-quant integration
- Verification trails

---

### Section 5: Closing (Slides 18-20)

**Slide 18: The Honest Assessment**
What worked:
- 4 papers from 3 weeks of part-time work
- Each stress-tested by adversarial AI review
- Verification packages for reviewers

What's still hard:
- Requires Claude Code (CLI comfort needed for now)
- No model abstraction yet (Claude-specific)
- Learning curve for the workflow

What's next (roadmap):
- Docker/web UI for non-CLI users
- Model agnosticism
- More examples and demos

**Slide 19: The Bottom Line**
- If you're a skilled qualitative researcher with dormant data, you can probably do something similar
- The AI amplifies what you already know how to do
- Your PhD trained you for exactly the judgment calls that matter
- The tools are free and open source

Links:
- paper-mining-agent-suite: github.com/mattbeane/paper-mining-agent-suite
- Living Paper: github.com/mattbeane/living-paper
- Tutorial doc: FROM_DATA_TO_PAPERS_TUTORIAL_W_DETAIL.md

**Slide 20: Discussion / Q&A**
- What datasets do YOU have sitting dormant?
- What's blocking you from the analysis-to-paper pipeline?
- Questions about the workflow?

---

## VISUAL STYLE NOTES

- Clean, academic aesthetic—not startup-y or flashy
- Use diagrams to show workflows
- Include actual code snippets for technical slides
- Show data: frame shift tables, statistics from papers
- Avoid stock photos; prefer diagrams and data visualizations
- Color scheme: muted, professional (blues, grays, occasional accent)

## KEY QUOTES TO INCLUDE

1. "Don't think of AI as a replacement for your expertise. Think of it as a very fast, very patient research assistant that never gets tired."

2. "Those judgment calls—what framing to pursue, what sensitizing literature to use, what claims to kill, what evidence is compelling—are exactly what your PhD trained you for."

3. "The system that built the analysis should NOT be the only verifier."

4. "We'll see. I want to see what happens. If it doesn't work out, I can always leave." (from Paper 1, capturing anticipatory sensemaking)

5. "Money was not the answer." (from Paper 3, the 1,300 workers who didn't quit)

6. "Gallatin develops, Fresno perfects." (from Paper 2, deliberate facility role differentiation)

## STATS TO HIGHLIGHT

- 4 papers in ~3 weeks of part-time work
- 23+ frame shifts across papers
- 59,000 temp worker exit records
- 33 million telemetry records
- 351 interviews, 718 hours observation
- 76% of early-phase drivers advanced to professional roles
- 18-19 pp decline in voluntary resignations before automation
- 2x incentive response for seasonal vs full-time workers

---

## GENERATING THE SLIDES

Use this prompt to generate slides with any presentation-capable LLM:

> Create a 15-20 slide presentation following this structure and content. Use a clean academic visual style. Include the specific statistics and quotes mentioned. Each slide should be information-dense but not cluttered—this audience is PhD students who can handle complexity. Include code snippets where noted. Make sure the narrative arc goes from "origin story" to "what I produced" to "how it works" to "how you can use it."
