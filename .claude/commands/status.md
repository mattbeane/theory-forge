# Workflow Status

You are the STATUS agent. Your job is to give a quick overview of project progress and suggest next steps.

## Your Task

Read project state and display a clear status report.

## Steps

1. **Detect project mode**

   Check for:
   - `workspace.json` → multi-project mode (show active project)
   - `state.json` → single-project mode
   - Neither → not initialized (suggest /init-project)

2. **Read state.json**

   Load current project state.

3. **Generate status report**

## Output Format

```
╔══════════════════════════════════════════════════════════════════╗
║  PAPER MINING STATUS                                             ║
╚══════════════════════════════════════════════════════════════════╝

Project: [name]
Frame: [N] of [total] | [theory name if set]
Updated: [relative time, e.g., "2 hours ago"]

─────────────────────────────────────────────────────────────────────
WORKFLOW PROGRESS
─────────────────────────────────────────────────────────────────────

  [✓] explore-data      Data inventory complete (15 files, 3,421 obs)
  [✓] hunt-patterns     3 robust patterns identified
  [→] find-theory       IN PROGRESS
  [ ] find-lens         Waiting for theory selection
  [ ] mine-qual
  [ ] smith-frames
  [ ] verify-claims
  [ ] draft-paper

Progress: ████████░░░░░░░░░░░░ 25% (2/8 steps)

─────────────────────────────────────────────────────────────────────
CURRENT FRAME (#2)
─────────────────────────────────────────────────────────────────────

Theory:      Learning curves (Argote & Epple, 1990)
Lens:        [not yet selected]
Framing:     [not yet selected]

Previous frames: 1 archived
  └─ Frame 1: TCE approach (abandoned - poor heterogeneity fit)

─────────────────────────────────────────────────────────────────────
KEY OUTPUTS
─────────────────────────────────────────────────────────────────────

  analysis/exploration/DATA_INVENTORY.md      ✓ exists
  analysis/patterns/PATTERN_REPORT.md         ✓ exists
  analysis/framing/frame-2/PRIMARY_THEORY.md  ✗ missing

─────────────────────────────────────────────────────────────────────
NEXT STEP
─────────────────────────────────────────────────────────────────────

→ Run /find-theory to select your theoretical anchor

After that: /find-lens → /mine-qual → /smith-frames → /verify-claims → /draft-paper

─────────────────────────────────────────────────────────────────────
QUICK COMMANDS
─────────────────────────────────────────────────────────────────────

  /new-frame          Start fresh theoretical iteration
  /new-frame list     See all frame attempts
  /new-frame compare  Compare frames side-by-side
  /switch-project     Switch to different paper (multi-project)
  /export             Generate manuscript in different formats

```

## Status Symbols

- `[✓]` - Completed
- `[→]` - In progress
- `[ ]` - Pending
- `[!]` - Blocked (missing prerequisites)

## Not Initialized

If no state.json found:

```
╔══════════════════════════════════════════════════════════════════╗
║  PROJECT NOT INITIALIZED                                         ║
╚══════════════════════════════════════════════════════════════════╝

No state.json found in this directory.

To get started:
  /init-project              Initialize single paper project
  /init-project [name]       Initialize named project (multi-project mode)

Need help? See templates/PROJECT_SETUP.md for manual setup.
```

## Multi-Project Summary

If in workspace with multiple projects:

```
╔══════════════════════════════════════════════════════════════════╗
║  WORKSPACE OVERVIEW                                              ║
╚══════════════════════════════════════════════════════════════════╝

Active: paper-1 (Surgical Learning)

─────────────────────────────────────────────────────────────────────
ALL PROJECTS
─────────────────────────────────────────────────────────────────────

  → paper-1    Surgical Learning       Frame 2   ████████░░ 40%
    paper-2    Shadow Learning         Frame 1   ████░░░░░░ 20%
    paper-3    Network Effects         Frame 1   ██░░░░░░░░ 10%

Use /switch-project [name] to change active project.

─────────────────────────────────────────────────────────────────────

[Then show full status for active project as above]
```

## Blocked States

If a step can't proceed due to missing prerequisites:

```
  [!] find-theory       BLOCKED - requires hunt-patterns output
      └─ Missing: analysis/patterns/PATTERN_REPORT.md
      └─ Run /hunt-patterns first
```

## Stale Detection

If outputs exist but are older than their inputs:

```
  [⚠] hunt-patterns     May be stale (data changed since last run)
      └─ PATTERN_REPORT.md: 3 days old
      └─ data/quant/: modified 1 day ago
      └─ Consider re-running /hunt-patterns
```
