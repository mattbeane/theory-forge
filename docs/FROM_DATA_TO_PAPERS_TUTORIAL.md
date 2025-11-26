# From Dormant Data to Submittable Papers in 5 Days
## A Qualitative Researcher's Guide to AI-Assisted Paper Development

**Matt Beane, UC Santa Barbara**
**November 2025**

---

## The Setup

I'm an ethnographer. Most of my work involves fieldwork, interviews, and careful qualitative analysis. But like many qualitative researchers, I also collect quantitative data—and like many of us, I have datasets sitting dormant because the analysis-to-paper pipeline is daunting.

In late November 2025, I saw a tweet from Aniket Panjwani suggesting that coding agents like Claude Code could transform exploratory data analysis for social scientists. I decided to test this claim—not on toy data, but on real research datasets I'd collected years ago and never fully exploited.

**What I had:**
- **Dataset 1**: ~60,000 worker exit records + daily productivity data + project timelines + 300+ interviews and 700+ hours of observation from multiple sites
- **Dataset 2**: ~70,000 worker-month observations on a performance program + 77 interviews with 47 informants from multiple facilities

**What I produced in 5 days of part-time work:**
- 3 distinct papers, each targeting a different journal
- Each paper went through 3-5 complete reframings
- Final versions have expanded literature reviews, quantitative analyses with robustness checks, integrated qualitative evidence, figures, and journal-appropriate formatting
- Each was stress-tested by a second AI system acting as adversarial pre-reviewer

This document explains the process—without revealing the specific content of papers still under development.

---

## Why This Matters for Qualitative Researchers

The tweet that sparked this focused on exploratory data analysis—letting AI run regressions and make graphs. That's useful, but it undersells what's possible.

The real power for qualitative researchers is in the *full pipeline*:
1. Exploring data you haven't touched in years
2. Generating multiple theoretical framings
3. Finding the "sensitizing literature" that explains your patterns
4. Integrating qualitative evidence with quantitative findings
5. Iterating through framings until something robust and novel emerges
6. Producing journal-ready manuscripts

None of this requires you to be a methods expert. It requires you to be a *domain expert*—which you already are.

---

## The 8-Phase Process

### Phase 1: Data Exploration

**What you do**: Point the AI at your data files and ask "what's here?"

**What happens**:
- File inventory (sizes, formats, column names)
- Quick descriptive statistics
- Identification of anomalies and patterns
- Surface-level insights about what's interesting

**Example prompt**:
> "I have data files in [directory]. List what's there, give me basic descriptives, and flag anything unusual or potentially interesting."

**What you're looking for**: Anomalies that trigger your domain expertise. When the AI flags something unexpected in your data, you think "that's weird—something's happening here." That recognition comes from *you*, not the AI.

**Your role**: Curator. The AI generates; you recognize what matters.

---

### Phase 2: Hypothesis Generation & Initial Framing

**What you do**: Ask "what paper could we write with this?"

**What happens**: The AI proposes multiple possible framings. You evaluate them based on:
- Is the finding robust to obvious confounds?
- Is it theoretically interesting?
- Does it violate an established prediction?

**Critical insight**: Your first framing will almost certainly be wrong. That's fine. The goal is to generate options, not commit.

**The frame shift pattern**:

Across 3 papers, I went through 13 total frame shifts. A typical sequence looks like:

| Stage | What Happened |
|-------|---------------|
| Frame 1 | Initial hypothesis based on obvious pattern |
| Frame 2 | Reframe after robustness check kills original finding |
| Frame 3 | Reframe when data shows opposite of expected pattern |
| Frame 4 | Evolve framing to be more theoretical (not just descriptive) |
| Frame 5 | Final framing with active mechanism and clear contribution |

**Your role**: Evaluator. Kill framings that don't survive scrutiny. Recognize when an inversion is more interesting than the original hypothesis.

---

### Phase 3: Finding the Sensitizing Literature

**This is the crucial step that transforms description into contribution.**

You've found a robust empirical pattern that violates an established theoretical prediction. Now you need a *second* literature—a "sensitizing" or "interpretive" lens—that explains the heterogeneity in your data.

**The pattern**:
1. Primary theory makes a prediction (e.g., "X leads to Y")
2. Your data violates it (e.g., "sometimes X leads to NOT-Y")
3. You ask: "What explains *which* cases violate the prediction?"
4. You find a literature on that explanatory factor
5. Your contribution *bridges* the two literatures

**Generic example**:
- Primary theory: Theory A predicts that workers in situation X will behave in way Y
- Violation: Your data shows some workers behave in way NOT-Y
- Sensitizing question: "Why do only *some* workers violate the prediction?"
- Sensitizing literature: A body of work on individual differences, orientations, or situational factors
- Extension: That factor moderates the Theory A prediction

**From my own prior work** (published, so I can share):
- Primary theory: Skill development through deliberate practice
- Violation: Some surgical trainees skilled up fast despite no formal practice time
- Sensitizing question: "How are they learning without practice?"
- Sensitizing literature: Deviance / workarounds
- Extension: "Shadow learning"—unsanctioned practice explains skill variance

**How to prompt for this**:

> "We have a finding that violates [primary theory]. The theory predicts X, but we observe Y—but only for some people. What individual or situational factor might explain who responds which way? What literature addresses that factor?"

**Your role**: Theorist. You recognize what makes a good bridging contribution. The AI can search literature, but you evaluate fit.

---

### Phase 4: Literature Positioning & Genre Requirements

**What you do**: Ensure the literature review positions your contribution properly and meets journal expectations.

**Two problems to solve**:

**Problem 1: The "two scholars" trap**

Early drafts often anchor on a small number of foundational papers. Reviewers will notice. You need to show you know the field is vibrant and ongoing.

**Example prompt**:
> "The lit review is anchored on just [Foundational Author 1] and [Foundational Author 2]. We need to show this is a vibrant, long-standing field. Find recent work—especially anything from the last 5 years that updates or challenges these frameworks."

**Problem 2: Genre requirements**

Different journals have different expectations:
- **Management Science**: ~10,000 words, heavy quantitative emphasis
- **ASQ**: Mixed-methods welcome, theory-building expected
- **AMJ**: Clear hypotheses, robustness checks, practical implications

**Example prompt**:
> "Expand this to full [Journal] length. That means ~X words, detailed methods section, multiple robustness checks, and extended discussion of boundary conditions."

**Your role**: Editor. You know what top journals expect because you've published in them (or read enough to internalize the genre).

---

### Phase 5: Quantitative-Qualitative Integration

**This is where qualitative researchers have a massive advantage.**

Most AI-assisted data analysis stops at quantitative patterns. But if you have interview data, you can do something more powerful: show the *mechanisms* behind the patterns.

**The key**: Don't ask for summaries. Ask for *specific evidence* for *specific mechanisms*.

**Example prompt structure**:

```
### HIGH PRIORITY: Why does [Pattern from Quant Data] occur?

1. **Mechanism A**: [Specific observable evidence you'd expect]
2. **Mechanism B**: [Specific observable evidence you'd expect]
3. **Mechanism C**: [Specific observable evidence you'd expect]

### MEDIUM PRIORITY: Why does [Secondary Pattern]?

4. **Explanation A**: [What to look for]
5. **Explanation B**: [What to look for]

### Look for disconfirming evidence. What quotes challenge the interpretation?

### Organize output as:
1. Evidence by claim (for each quant claim, provide supporting/challenging evidence)
2. Key quotes (10-15 most compelling, with context)
3. Disconfirming evidence
4. Suggestions for integration
```

**The payoff**: This structured approach, applied to my interviews, produced insights that became core contributions—revealing heterogeneity within categories that the quantitative data alone couldn't explain.

**Your role**: Mechanism detective. You hypothesize what's going on; the AI finds the evidence.

---

### Phase 6: External Verification

**What you do**: Send verification packages to a *different* AI system for adversarial review.

**Why this matters**: The AI that helped you build the paper has seen your reasoning. A different system—with different strengths—provides fresh eyes.

**My approach**: I used Claude Code (Opus) for generation and analysis. I sent verification briefs to ChatGPT Pro (o1/reasoning mode) for deep adversarial review.

**What goes in a verification brief**:

```markdown
### Claim 1: [Description]

**Statement**: "[Exact claim as it will appear in paper]"

**Expected results**: [Specific numbers]

**Data files**: [Which files]

**Verification code**: [Full script that reproduces the analysis]

**Questions for verification**:
1. Do these numbers replicate?
2. Is the statistical approach appropriate?
3. What confounds might we be missing?
4. Does the theoretical interpretation fit the empirical pattern?
```

**Your role**: Quality control. You're simulating peer review before submission.

---

### Phase 7: Iterative Refinement

**What you do**: Kill framings that don't work; evolve those that do.

**The pattern**:
- Robustness check kills a finding → reframe around what *did* survive
- Theory seems shallow → dig for deeper mechanism
- Contribution unclear → sharpen the established prediction you're violating

**Typical evolution**:

| Draft | Issue | Resolution |
|-------|-------|------------|
| 1 | Finding didn't survive controls | Reframe around what DID survive |
| 2 | Data showed opposite of prediction | Make the inversion the story |
| 3 | Framing too descriptive | Add theoretical mechanism |
| 4 | Passive framing | Emphasize active mechanism |
| 5 | Final version | Clear contribution, robust finding |

**Your role**: Intellectual integrity. You kill your darlings when the evidence doesn't support them.

---

### Phase 8: Anonymization & Publishing Prep

**What you do**: Catch what reviewers would catch before they catch it.

**Common issues to watch for**:
- Organization/program names not anonymized
- Site/location names not anonymized
- Claims about preferences when you only have revealed behaviors
- Vague sample sizes (make them precise)

**Example prompt**:
> "Review this paper for anonymization failures, overclaims, and imprecise statistics. Flag anything a reviewer would catch."

**Your role**: Pre-reviewer. You know what gets papers desk-rejected.

---

## The Professional Wisdom

Over 5 days, I made dozens of judgment calls that shaped these papers. Here's what I was doing, distilled:

### 1. "What interpretive lens helps explain the variation?"

This is the sensitizing literature move. It transforms "here's a pattern" into "here's a contribution."

### 2. "Show me what survives controls"

Every exciting finding got stress-tested. Findings that died got reframed around what *did* survive.

### 3. "What established prediction are we violating?"

The contribution comes from showing something the literature wouldn't expect—and explaining why.

### 4. "Find the heterogeneity"

All three papers benefited from looking *within* categories to find subgroups that behave differently. The aggregate effect often obscures the real story.

### 5. "We don't have data on that"

I caught multiple overclaims—places where we were asserting something we hadn't actually measured. Revealed preferences ≠ stated preferences.

### 6. "This has to fit [journal] format"

Genre awareness. Different journals want different things. I internalized those expectations from years of reading and reviewing.

### 7. "Send it to [different AI] for review"

Using a different AI system as adversarial pre-reviewer catches errors and forces precision. It's like asking a skeptical colleague to read your draft—except available at 2am.

---

## What You Need to Make This Work

### 1. Domain expertise

The AI can search literature, run analyses, and draft text. It cannot recognize when a finding is theoretically interesting or when a framing doesn't fit your field. That's you.

### 2. Existing data

This approach works best when you already have data—especially mixed-methods data. The AI dramatically accelerates analysis and writing, but it doesn't collect data for you.

### 3. Tolerance for iteration

13 frame shifts across 3 papers. You have to be willing to kill your darlings repeatedly when the evidence doesn't support them.

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

---

## The Bottom Line

I had two datasets that had been sitting dormant for 2-3 years. I hadn't touched them because the analysis-to-paper pipeline felt overwhelming. In 5 days of part-time work, I produced three papers that are close to submittable.

This isn't magic. It's leverage. The AI amplifies what you already know how to do. If you're a skilled qualitative researcher with dormant data, you can probably do something similar.

The key insight: Don't think of AI as a replacement for your expertise. Think of it as a very fast, very patient research assistant that never gets tired and can search the literature at 3am. You're still the one making the judgment calls.

Those judgment calls—what framing to pursue, what sensitizing literature to use, what claims to kill, what evidence is compelling—are exactly what your PhD trained you for.

---

## Appendix: The Tweet Thread That Started This

Aniket Panjwani (@aniketapanjwani):

> "If you're a social scientist you can save 100s of hours by using coding agents like Claude Code and Codex for all your exploratory data analysis.
>
> Here's a beginner's guide:
>
> 1. Describe your datasets/where they are on your file system
> 2. Describe the research problem you're investigating
> 3. Tell the coding agent what tools to use
> 4. Ask it to create a plan of potential graphs, tables, regressions
> 5. Have it implement each task in turn
> 6. Marvel at the incredible results..."

What I learned: This undersells it. The real power isn't graphs and regressions—it's the full paper development pipeline, especially for researchers with mixed-methods data and dormant datasets.

---

*Document created November 2025. For questions: mattbeane@ucsb.edu*
