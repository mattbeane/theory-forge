---
name: init-project
description: Scaffold a new paper mining project with the full directory structure and initialize project state
---

# Project Initializer

You are the PROJECT-INITIALIZER agent. Your job is to scaffold a new paper mining project with the full directory structure and initialize project state.

## Your Task

Create a complete project structure for a new paper, either as the root project or as part of a multi-paper workspace.

## Arguments

The user may specify:
- `$ARGUMENTS` - Project name (defaults to current directory name if not provided)
- `--guided` - Run guided first-project experience with explanations at each step

## Steps

1. **Determine project context**

   Check if we're in:
   - A fresh directory (create single-project structure)
   - An existing multi-project workspace (create under `projects/`)
   - Need to convert to multi-project (ask user)

2. **Create directory structure**

   ```
   [project-root]/
   ├── .claude/
   │   └── skills/           # Already present if cloned
   ├── data/
   │   ├── quant/              # Quantitative data files
   │   └── qual/               # Qualitative data (interviews, fieldnotes)
   │       ├── interviews/
   │       └── fieldnotes/
   ├── analysis/
   │   ├── exploration/        # /explore-data outputs
   │   ├── patterns/           # /hunt-patterns outputs
   │   ├── theory/             # /find-theory outputs
   │   ├── lens/               # /find-lens outputs
   │   ├── qualitative/        # /mine-qual outputs
   │   ├── framing/            # /style-engine outputs (frame-1/, frame-2/, etc.)
   │   ├── absences/           # /surface-absences outputs
   │   ├── process/            # /trace-process outputs
   │   ├── audit/              # /audit-claims outputs (evidence from raw data)
   │   └── verification/       # /verify-claims outputs
   ├── living_paper/           # Living paper CLI (bundled for seamless verification)
   ├── literature/
   │   ├── primary/            # Core theory papers
   │   ├── sensitizing/        # Sensitizing literature
   │   └── refs.bib            # BibTeX references
   ├── output/
   │   ├── drafts/             # Generated manuscripts
   │   ├── tables/
   │   └── figures/
   ├── project_config.yaml     # Data locations and sensitivity settings
   ├── PROJECT_CONTEXT.md      # User fills in
   ├── DECISION_LOG.md         # Track choices
   └── state.json              # Workflow state (auto-managed)
   ```

3. **Initialize state.json**

   Create the state tracking file:

   ```json
   {
     "version": "1.2.0",
     "project_name": "[name]",
     "created_at": "[ISO timestamp]",
     "updated_at": "[ISO timestamp]",
     "current_frame": 1,
     "eval_results": {},
     "submission_thresholds": { "preset": null, "overrides": {} },
     "workflow": {
       "explore_data": {
         "status": "pending",
         "completed_at": null,
         "outputs": []
       },
       "hunt_patterns": {
         "status": "pending",
         "completed_at": null,
         "outputs": [],
         "consensus_result": null
       },
       "find_theory": {
         "status": "pending",
         "completed_at": null,
         "outputs": []
       },
       "find_lens": {
         "status": "pending",
         "completed_at": null,
         "outputs": []
       },
       "mine_qual": {
         "status": "pending",
         "completed_at": null,
         "outputs": [],
         "consensus_result": null
       },
       "smith_frames": {
         "status": "pending",
         "completed_at": null,
         "outputs": []
       },
       "audit_claims": {
         "status": "pending",
         "completed_at": null,
         "outputs": [],
         "supporting_count": 0,
         "challenging_count": 0,
         "high_concern_claims": []
       },
       "verify_claims": {
         "status": "pending",
         "completed_at": null,
         "outputs": [],
         "consensus_result": null
       },
       "draft_paper": {
         "status": "pending",
         "completed_at": null,
         "outputs": []
       },
       "check_submission": {
         "status": "pending",
         "completed_at": null,
         "outputs": [],
         "verdict": null
       }
     },
     "frames": {
       "1": {
         "created_at": "[ISO timestamp]",
         "theory": null,
         "lens": null,
         "framing": null,
         "status": "active"
       }
     },
     "consensus": {
       "enabled": true,
       "default_n": 10,
       "stages": {
         "hunt_patterns": { "n": 25, "enabled": true },
         "mine_qual": { "n": 15, "enabled": true },
         "verify_claims": { "n": 10, "enabled": true },
         "eval_zuckerman": { "n": 5, "enabled": true },
         "eval_paper_quality": { "n": 5, "enabled": true },
         "eval_becker": { "n": 5, "enabled": true },
         "eval_genre": { "n": 5, "enabled": true },
         "eval_contribution": { "n": 5, "enabled": true },
         "eval_limitations": { "n": 5, "enabled": true },
         "eval_citations": { "n": 5, "enabled": true },
         "simulate_review": { "n": 5, "enabled": true },
         "check_submission": { "n": 7, "enabled": true },
         "test_counter_evidence": { "n": 5, "enabled": true },
         "test_alt_interpretations": { "n": 5, "enabled": true },
         "test_boundary_conditions": { "n": 5, "enabled": true }
       },
       "thresholds": {
         "high_stability_cv": 0.10,
         "medium_stability_cv": 0.25,
         "quote_high_stability": 0.75,
         "quote_medium_stability": 0.50
       },
       "provider": "anthropic",
       "model": "claude-sonnet-4-20250514"
     },
     "decisions": [],
     "metadata": {
       "target_journal": null,
       "domain": null,
       "anonymization_rules": {}
     }
   }
   ```

   **Note**: Consensus mode is enabled by default (v1.2.0+). Run `/consensus-config disable` for faster single-run iteration.

4. **Create project_config.yaml**

   ```yaml
   # Project Configuration
   # This file tells the pipeline where to find your data

   data_sources:
     qual:
       # Path to interview transcripts (relative to project root)
       interviews: "data/qual/interviews"
       # Path to field notes
       fieldnotes: "data/qual/fieldnotes"
     quant:
       # Path to quantitative data files
       primary: "data/quant"
     # Additional data sources (legacy locations, shared data, etc.)
     additional: []

   sensitivity:
     # Default sensitivity tier for new evidence
     default_tier: "CONTROLLED"
     # Fields that can be included in PUBLIC exports
     public_allowed_fields:
       - "informant_role_bin"
       - "informant_tenure_bin"
       - "site_bin"
       - "evidence_type"
     # Minimum cell size for aggregates (k-anonymity)
     min_cell_size: 5

   anonymization:
     # Replace these strings in evidence summaries
     redact_patterns: []
     # Site pseudonym mappings
     site_mappings: {}
   ```

5. **Create PROJECT_CONTEXT.md template**

   ```markdown
   # Project Context

   ## Project Name
   [Your project name]

   ## Research Domain
   [What field is this? What topic?]

   ## Data Overview
   [Brief description of your data—what it is, where it came from, what time period]

   ## Research Question (if any)
   [What are you trying to understand? Or is this exploratory?]

   ## Target Journals
   [Where might you submit? What genre conventions matter?]

   ## Anonymization Requirements
   [What needs to be anonymized? Company names, locations, etc.]

   ## Your Expertise
   [What domain knowledge do you bring? This helps calibrate suggestions.]

   ## Constraints
   [Any limitations? Timeline, co-authors, etc.]
   ```

5. **Create DECISION_LOG.md template**

   ```markdown
   # Decision Log

   Track your analytical decisions throughout the paper mining process.

   ---

   ## [Date]: Project Initialized

   - Created project structure
   - Next step: Add data to `data/` directory, then run `/explore-data`

   ---

   <!-- Template for future entries:

   ## [Date]: [Stage Name]

   - Ran: /[command]
   - Key finding: [X]
   - Decision: [What you chose to do]
   - Rationale: [Why]
   - Alternatives considered: [What else you thought about]
   - Next step: [What's next]

   -->
   ```

6. **Update .gitignore if needed**

   Ensure state.json is NOT ignored (we want to track state), but sensitive data is:

   ```
   # Data files (users should not commit their data)
   data/
   *.csv
   *.xlsx

   # But DO track state
   !state.json
   ```

## Output

After creating everything, report:

1. **Created structure**:
   - List all directories created
   - Note which files were templated

2. **State initialized**:
   - Show initial state.json location
   - Current frame: 1

3. **Next steps**:
   - Add data files to `data/quant/` and `data/qual/`
   - Fill in `PROJECT_CONTEXT.md`
   - Run `/explore-data` to begin

## Multi-Project Mode

If the user is setting up multiple papers in one workspace, create:

```
workspace/
├── .claude/
│   └── skills/
├── projects/
│   ├── paper-1/
│   │   ├── data/
│   │   ├── analysis/
│   │   ├── literature/
│   │   ├── output/
│   │   ├── PROJECT_CONTEXT.md
│   │   ├── DECISION_LOG.md
│   │   └── state.json
│   └── paper-2/
│       └── [same structure]
├── shared/
│   └── literature/          # Shared reference library
└── workspace.json           # Tracks all projects
```

The `workspace.json` file:

```json
{
  "version": "1.0.0",
  "created_at": "[ISO timestamp]",
  "active_project": "paper-1",
  "projects": {
    "paper-1": {
      "path": "projects/paper-1",
      "created_at": "[ISO timestamp]",
      "status": "active"
    }
  }
}
```

Use `/switch-project` to change active project in multi-project mode.

---

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
