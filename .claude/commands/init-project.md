# Project Initializer

You are the PROJECT-INITIALIZER agent. Your job is to scaffold a new paper mining project with the full directory structure and initialize project state.

## Your Task

Create a complete project structure for a new paper, either as the root project or as part of a multi-paper workspace.

## Arguments

The user may specify:
- `$ARGUMENTS` - Project name (defaults to current directory name if not provided)

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
   │   └── commands/           # Already present if cloned
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
   │   ├── framing/            # /smith-frames outputs (frame-1/, frame-2/, etc.)
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
     "version": "1.1.0",
     "project_name": "[name]",
     "created_at": "[ISO timestamp]",
     "updated_at": "[ISO timestamp]",
     "current_frame": 1,
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
       "enabled": false,
       "default_n": 10,
       "stages": {
         "hunt_patterns": { "n": 25, "enabled": true },
         "mine_qual": { "n": 15, "enabled": true },
         "verify_claims": { "n": 10, "enabled": true }
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

   **Note**: Consensus mode is disabled by default. Run `/consensus-config enable` when preparing for peer review.

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
│   └── commands/
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
