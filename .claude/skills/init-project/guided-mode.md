## Guided Mode (`--guided`)

When the user runs `/init-project --guided`, provide an interactive walkthrough with explanations at each step. This is for first-time users who want to understand what they're setting up.

### Guided Mode Flow

**Introduction:**
```
Welcome to Theory-Forge! 🛠️

I'll walk you through setting up your paper project step by step.
At each stage, I'll explain what we're creating and why it matters.

This guided setup takes about 10 minutes. You can use --skip-check
next time if you want to go faster.

Ready? Let's start.
```

**Step 1: Project Context**
```
STEP 1 OF 6: Understanding Your Project

First, I need to understand what we're working with.

→ What's the name for this project? (e.g., "hospital-learning-paper")
→ Is this going in a fresh directory, or part of a multi-paper workspace?
```

**Step 2: Directory Structure**
```
STEP 2 OF 6: Creating Your Workspace

I'm creating folders to organize your work:

  data/           ← Your raw data goes here (interviews, fieldnotes, quant files)
  analysis/       ← Pipeline outputs will land here (patterns, mechanisms, claims)
  literature/     ← PDFs and notes on relevant papers
  output/         ← Final drafts, tables, figures

Why this structure?
The pipeline needs to know where to find things and where to put outputs.
Keeping data separate from analysis prevents accidental overwrites and
makes it easy to see what's raw vs. derived.

[Creating directories...]
```

**Step 3: State Tracking**
```
STEP 3 OF 6: Initializing State Tracking

I'm creating state.json to track your progress.

This file remembers:
• Which pipeline stages you've completed
• Which gates you've passed
• Your current framing and decisions

Why this matters?
Theory-forge has "gates" that prevent you from skipping steps or
proceeding with flawed work. The state file enforces these gates.
You can run /status anytime to see where you are.

[Creating state.json...]
```

**Step 4: Configuration**
```
STEP 4 OF 6: Project Configuration

I'm creating project_config.yaml with default settings.

This controls:
• Where to find your data files
• Anonymization rules (what to redact)
• Sensitivity settings for evidence exports

You'll want to customize this after setup, especially the
anonymization rules if you're working with real interviews.

[Creating project_config.yaml...]
```

**Step 5: Context Template**
```
STEP 5 OF 6: Project Context

I've created PROJECT_CONTEXT.md for you to fill in.

This is your chance to tell the pipeline about:
• Your research question (if you have one)
• Your target journals
• Your domain expertise
• Any constraints (timeline, co-authors)

The better you fill this in, the more relevant the pipeline's
suggestions will be. Take 5-10 minutes on this before running
/explore-data.

[Creating PROJECT_CONTEXT.md...]
```

**Step 6: Decision Log**
```
STEP 6 OF 6: Decision Tracking

I've created DECISION_LOG.md for tracking your choices.

Throughout the pipeline, you'll make analytical decisions:
• Which patterns to pursue
• Which mechanisms to highlight
• Which framing to use

Recording these decisions helps you:
• Remember why you made choices (useful during revision)
• Explain your methods to reviewers
• Identify where you might reconsider

[Creating DECISION_LOG.md...]
```

**Completion:**
```
✅ PROJECT SETUP COMPLETE

Your project is ready at: [path]

NEXT STEPS:

1. Add your data
   Copy interview transcripts → data/qual/interviews/
   Copy field notes → data/qual/fieldnotes/
   Copy quantitative files → data/quant/

2. Fill in PROJECT_CONTEXT.md
   Tell the pipeline about your research

3. Run /explore-data
   This kicks off the pipeline by inventorying your data

THE PIPELINE AT A GLANCE:

  /explore-data     → Inventory what you have
  /hunt-patterns    → Find robust empirical patterns
       ↓
    GATE A: Is this pattern interesting?
       ↓
  /find-theory      → What theory does this challenge?
  /find-lens        → What literature explains variation?
  /mine-qual        → Extract mechanism evidence
       ↓
    GATE B: Do you have mechanism support?
       ↓
  /smith-frames     → Generate framing options
       ↓
    GATE C: Select your framing
       ↓
  /eval-zuckerman   → Check academic framing (7/10 to pass)
  /eval-becker      → Check generalizability
  /eval-genre       → Check discovery vs. testing framing
       ↓
    GATE D: All evaluations must pass
       ↓
  /audit-claims     → Match claims to evidence
  /verify-claims    → Create verification package
       ↓
    GATE E: No unsupported claims
       ↓
  /draft-paper      → Generate manuscript
       ↓
  /eval-limitations → Check limitations section
  /eval-citations   → Check citation coverage
       ↓
    GATE F: Quality checks pass
       ↓
  /check-submission  → Run full submission readiness test suite
       ↓
  READY TO SUBMIT 🎉

### Submission Readiness Testing

After completing your analysis and draft, run `/check-submission` to execute the full test suite:
- Evaluates paper against all relevant rubrics
- Runs adversarial tests (counter-evidence, alternative interpretations, boundary conditions)
- Uses monte-carlo consensus (N runs per test) for stability
- Produces a single PASS/CONDITIONAL/FAIL verdict
- Generates `analysis/quality/SUBMISSION_READINESS.md`

Configure thresholds with `/check-submission config` or use presets: `--preset top_journal`, `--preset field_journal`, `--preset working_paper`.

Questions? Run /help or check the documentation.
Good luck with your paper!
```

### Guided Mode Notes

- Always show progress: "STEP X OF 6"
- Explain the "why" for each component
- Keep explanations concise but meaningful
- End with clear next steps
- Show the full pipeline overview at the end so users understand the journey
