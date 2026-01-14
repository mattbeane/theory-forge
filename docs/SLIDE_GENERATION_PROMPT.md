# Slide Generation Prompt: AI-Assisted Qualitative Research

**Purpose**: Generate a ~22 slide presentation for PhD students about using AI to accelerate qualitative research paper development.

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
- Paper 1: "Hedging with Talent" (managers select temps on reliability under novel-tech uncertainty—tenure 4x at robot facility, +74h diff-in-diff)
- Paper 2: "Learning to Automate" (firms solve exploration/exploitation spatially—pilot nodes vs optimization nodes)
- Paper 3: "When Misfit Motivates" (work orientation moderates P-E fit—seasonal workers respond 2x)
- Paper 4: "Developmental Uncertainty" (uncertainty enables cross-status skill transfer—76% advanced, window closes)

**Slide 6: The Plot Twists**
- Every paper started with a wrong hypothesis
- 23+ total frame shifts across 4 papers
- Example: "Workers flee automation" → data showed OPPOSITE → "Wait and See" (workers making sense) → BUT validation revealed managers withheld info, so workers *couldn't* be sensemaking → **Final**: "Hedging with Talent" (manager-side selection mechanism)
- Key insight: The AI helped me find what the data actually showed, not what I expected—AND validation caught a plausible-but-wrong mechanism

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

**Slide 10: The Foundation—Zuckerman's Framework + Optional Moves**

**The foundation (Zuckerman):**
Every compelling paper needs:
1. A puzzle in the world (not a lit gap)
2. Build up and save the null (make the conventional view compelling before breaking it)
3. Your resolution (the contribution)

**One powerful gambit—Sensitizing Literature:**
When your data shows heterogeneity (only SOME violate):
1. Primary theory predicts X
2. Your data shows Y (violation!)
3. You find a SECOND literature that explains WHO violates
4. Your contribution BRIDGES the two literatures

Example from Paper 3:
- P-E fit theory predicts misfit → withdrawal
- Data: seasonal workers respond 2x to incentives (OPPOSITE)
- Sensitizing lit: Work orientation (Wrzesniewski, Schein)
- Contribution: Orientation moderates the misfit-response relationship

**But it's not the only move:**
- Sometimes your contribution is a new mechanism, not a moderator
- Sometimes the finding is uniform (everyone violates)
- The sensitizing literature gambit is one tool, not the whole toolkit

**Slide 11: Frame Shifts Are The Process**
- Show example frame shift table (Paper 1):
  1. "Automation causes turnover" → Killed: didn't survive controls
  2. "Workers flee automation" → Killed: data showed opposite
  3. "Anticipation Paradox" → Evolved: too descriptive
  4. "Option Cultivation" → Evolved: needed mechanism
  5. "Wait and See" → Killed (Jan 2026): validation revealed workers couldn't be sensemaking if managers withheld info
  6. **"Hedging with Talent"** → Final: manager-side selection on reliability + information asymmetry

- Key lesson: Be willing to kill your darlings. Even a LATER framing can be wrong—validation matters.

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

**Slide 14b: Theory-Building vs Theory-Testing Language (Optional Style)**

**Know your paper's genre:**
- **Theory-building**: Discovers patterns, proposes mechanisms, develops frameworks
- **Theory-testing**: Tests pre-specified hypotheses against data

**A single paper can't do both.** If you're discovering patterns AND claiming to test them, something's wrong.

**Language matters:**
| Theory-Building | Theory-Testing |
|-----------------|----------------|
| "The data suggest..." | "The data confirm..." |
| "is consistent with..." | "supports the hypothesis..." |
| "the pattern indicates..." | "validates the prediction..." |

**Red flags for theory-building papers:**
- Numbered hypotheses (H1, H2, H3)
- "The data support Hypothesis 1"
- "As predicted..."
- Tables with "Supported/Not Supported" columns

**This is a style choice**—some papers legitimately test hypotheses. Use the theory-building rubric in `docs/THEORY_BUILDING_STYLE.md` when your paper is building, not testing.

---

### Section 4: Addressing the Critique (Slides 15-16)

**Slide 15: "But What About Nguyen & Welch?"**

Context: PhD students have been discussing the Nguyen & Welch paper critiquing AI in qualitative research. Address it directly.

What Nguyen & Welch critique (and they're right about):
- **Type A usage**: "AI, analyze my data and tell me what it means"
- Automated thematic coding ("upload transcripts, get themes")
- LLMs as autonomous interpretation tools
- Their point: LLMs don't "understand" meaning—they produce plausible word sequences

Key quote from their critique: LLMs generate text that *looks like* coding output but isn't grounded in data the way human coding is.

**Slide 16: Why This Workflow Is Different**

This workflow is **Type B** (not what they critique):

| Type A (what they critique) | Type B (what this workflow does) |
|---------------------------|--------------------------------|
| "AI, analyze my data" | "I hypothesize X. Find evidence for/against." |
| LLM generates themes | Human generates hypotheses, LLM searches |
| LLM interprets meaning | LLM is turbo-charged CTRL+F |
| Single system, no audit | External verification, frame versioning |

The key distinction:
- **Human stays the theorist and interpreter**
- **LLM accelerates search, not interpretation**
- `/mine-qual` explicitly forbids: "Read interviews and tell me what's interesting"
- `/mine-qual` requires: "Here are 5 mechanisms. Find evidence for/against each."

Where their critique still lands (and how we address it):
- **Hallucination risk** → `/verify-claims` + external AI verification
- **Priming effects** → Frame versioning makes evolution auditable
- **Opacity** → Living Paper creates explicit claim-evidence links

Bottom line: The workflow *itself* is the audit trail. More transparent than typical qualitative work, not less.

---

### Section 5: How to Use This (Slides 17-19)

**Slide 17: What You Need**
1. **Domain expertise** - AI can't recognize when a finding is theoretically interesting
2. **Existing data** - This accelerates analysis, not collection
3. **Tolerance for iteration** - 23+ frame shifts means killing darlings repeatedly
4. **Quality control instincts** - You know what reviewers will catch
5. **A second AI for verification** - Different strengths, fresh eyes

**Slide 18: Getting Started**
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

**Slide 19: What This Doesn't Replace**
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

### Section 6: Closing (Slides 20-22)

**Slide 20: The Honest Assessment**
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

**Slide 21: The Bottom Line**
- If you're a skilled qualitative researcher with dormant data, you can probably do something similar
- The AI amplifies what you already know how to do
- Your PhD trained you for exactly the judgment calls that matter
- The tools are free and open source

Links:
- paper-mining-agent-suite: github.com/mattbeane/paper-mining-agent-suite
- Living Paper: github.com/mattbeane/living-paper
- Tutorial doc: FROM_DATA_TO_PAPERS_TUTORIAL_W_DETAIL.md

**Slide 22: Discussion Launch — Critique**

Frame this as genuine inquiry, not defense:

- **Where does this break down?** (They just saw failure modes in the workflow)
- **What can't it do?** (Theoretical taste, knowing what's interesting, field knowledge)
- **Nguyen & Welch's concerns—are they right? When?**
- **What would happen if you used this mindlessly?**

**Slide 23: Discussion — Extrapolation**

- **What else could this approach do?** (Literature reviews, proposal writing, data exploration, R&R responses)
- **What would a "good" versus "bad" use of this look like?**
- **How would you know if the output was wrong?**

**Slide 24: The Meta-Skill**

Key insight for their careers:

- **The skill isn't using the tool—it's supervising it**
- Calibration comes from doing things the hard way first
- Taste can't be automated; developing taste IS the job
- You need to know what good looks like before you can judge AI output

This is why their PhD training still matters—maybe more than ever.

---

### Section 7: The Practical Move (Slides 25-26)

**Slide 25: "Got Any Data Lying Around?"**

The immediate opportunity: **Go ask faculty about dormant data and dormant access.**

What professors accumulate:
- Data that never became a paper
- Relationships with field sites they haven't used in years
- Old qualifying exam data, failed projects, side explorations
- Access that could yield complementary data for another paper

**The pitch to faculty**:
> "Do you have data that never became a paper? Or could we go back to your field sites and collect something new to complement what you've got?"

**Slide 26: Your Next Steps**

1. **Identify 2-3 faculty** whose work interests you
2. **Ask**: "Do you have datasets that never became papers—or field site relationships we could use to collect more?"
3. **Propose a collaboration**: their data/access + their guidance + your time with these tools
4. **Learn by doing**—on real stakes, with real supervision

Why this works:
- **Low-risk for them** (data exists, or access already established)
- **High-learning for you** (real data, real stakes, possibly real fieldwork)
- **Relationship-building** (you're offering value, not asking for it)
- **Practice supervising the tool** on something that matters

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

4. "The first thing I did is I verified attendance across first and second shift, but it's probably the most important thing, right? You need to show up to work." (from Paper 1, capturing reliability-based selection)

5. "The ultimate goal here is to reduce labor costs... But I'm not going to go ahead and deliver that message." (from Paper 1, capturing deliberate information withholding)

6. "Money was not the answer." (from Paper 3, the 1,300 workers who didn't quit)

7. "Gallatin develops, Fresno perfects." (from Paper 2, deliberate facility role differentiation)

## STATS TO HIGHLIGHT

- 4 papers in ~3 weeks of part-time work
- 23+ frame shifts across papers (6 for Paper 1 alone: through "Wait and See" to final "Hedging with Talent")
- 59,000 temp worker exit records
- 33 million telemetry records
- 351 interviews, 718 hours observation
- 76% of early-phase drivers advanced to professional roles
- +74h diff-in-diff tenure increase at robot vs sorter facilities [95% CI: 62-92h]
- 4x tenure increase at robot facility (21h → 84h median)
- 2x incentive response for seasonal vs full-time workers

---

## OPTIONAL: Source Material for Deeper Technical Detail

If you can fetch URLs, pull from these for accurate technical details:

- **Command definitions**: https://github.com/mattbeane/paper-mining-agent-suite/tree/main/.claude/commands
- **ROADMAP**: https://github.com/mattbeane/paper-mining-agent-suite/blob/main/ROADMAP.md
- **Living Paper README**: https://github.com/mattbeane/living-paper/blob/main/README.md
- **State schema**: https://github.com/mattbeane/paper-mining-agent-suite/blob/main/docs/STATE_SCHEMA.md
- **Nguyen-Welch comparison**: https://github.com/mattbeane/paper-mining-agent-suite/blob/main/nguyen-welch-comparison.md (addresses the AI-in-qualitative-research critique)

Use these to enrich technical slides (9, 13, 15-16, 18) with actual command syntax, feature lists, and the Nguyen-Welch response. The narrative structure above is the primary source.

---

## GENERATING THE SLIDES

Use this prompt to generate slides with any presentation-capable LLM:

> Create a ~22 slide presentation following this structure and content. Use a clean academic visual style. Include the specific statistics and quotes mentioned. Each slide should be information-dense but not cluttered—this audience is PhD students who can handle complexity. Include code snippets where noted. Make sure the narrative arc goes from "origin story" to "what I produced" to "how it works" to "addressing the critique" to "how you can use it."
