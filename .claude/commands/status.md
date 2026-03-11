# Workflow Status

You are the STATUS agent. Your job is to give a quick overview of project progress and suggest next steps.

## Your Task

Read project state, display a clear status report, and generate an HTML dashboard.

## Steps

1. **Detect project mode**

   Check for:
   - `workspace.json` → multi-project mode (show active project)
   - `state.json` → single-project mode
   - Neither → not initialized (suggest /init-project)

2. **Read state.json**

   Load current project state, including consensus configuration.

3. **Check consensus results**

   If consensus mode is enabled and stages have been run:
   - Read `workflow.<stage>.consensus_result` for stability summaries
   - Display HIGH/MEDIUM/LOW counts
   - Flag any LOW stability items with ⚠️

4. **Generate status report** (terminal output)

5. **Generate HTML dashboard**

   Write `dashboard.html` to project root with visual status.
   Tell user: "Dashboard updated: open dashboard.html in your browser"

## Output Format

```
╔══════════════════════════════════════════════════════════════════╗
║  PAPER MINING STATUS                                             ║
╚══════════════════════════════════════════════════════════════════╝

Project: [name]
Frame: [N] of [total] | [theory name if set]
Updated: [relative time, e.g., "2 hours ago"]

─────────────────────────────────────────────────────────────────────
PIPELINE PROGRESS (use /run-pipeline for guided execution)
─────────────────────────────────────────────────────────────────────

  [✓] explore-data      Data inventory complete (15 files, 3,421 obs)
  [✓] hunt-patterns     3 robust patterns identified
  [✓] GATE A            Pattern confirmed by user
  [✓] find-theory       Process losses (Steiner 1972)
  [✓] find-lens         Technology affordances (Leonardi 2011)
  [✓] mine-qual         5 key quotes, 11 field notes mined
  [✓] GATE B            Mechanism STRONG, disconfirming documented
  [✓] smith-frames      5 framings generated
  [✓] GATE C            "Technology-Enabled Role Structure" selected
  [→] eval-zuckerman    IN PROGRESS
  [ ] eval-becker       Waiting
  [ ] eval-genre        Waiting
  [⛔] GATE D           Evaluations must all pass
  [ ] audit-claims
  [ ] verify-claims
  [ ] GATE E            Verification gate
  [ ] draft-paper
  [ ] eval-paper-quality
  [ ] eval-limitations
  [ ] GATE F            Quality gate (score + limitations)
  [ ] package-verification

Progress: ████████████░░░░░░░░ 45% (9/20 steps)

⚠️  GATE D PENDING: All evaluations must pass before drafting

─────────────────────────────────────────────────────────────────────
EVALUATION RESULTS (Frame [N])
─────────────────────────────────────────────────────────────────────

  Test                    Score       Stability    Status
  ────                    ─────       ─────────    ──────
  Zuckerman               39/50       🟢 HIGH      ✓ PASS
  Paper Quality           37/50       🟢 HIGH      ✓ PASS
  Becker                  PASS        🟡 MED       ✓ PASS
  Counter-Evidence        PASS        🟢 HIGH      ✓ PASS
  Alt Interpretations     —           —            ○ Not run
  Boundary Conditions     PASS        🟢 HIGH      ⚠ STALE (frame changed)

  Submission Readiness:   CONDITIONAL (last run: 2 days ago)
  └─ 1 test stale, 1 not run — run /check-submission to update

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
CONSENSUS MODE
─────────────────────────────────────────────────────────────────────

  Status: [ENABLED / DISABLED]

  Stage Settings:
    hunt-patterns:   n=25, enabled ✓
    mine-qual:       n=15, enabled ✓
    verify-claims:   n=10, enabled ✓

  Last Run Stability (if available):
    PATTERN_REPORT:   4 HIGH, 1 MEDIUM, 0 LOW
    QUAL_EVIDENCE:    12 HIGH, 5 MEDIUM, 2 LOW ⚠️
    VERIFICATION:     3 DEFENSIBLE, 1 MOSTLY DEF.

  Run /consensus-config to modify settings.

─────────────────────────────────────────────────────────────────────
QUICK COMMANDS
─────────────────────────────────────────────────────────────────────

  /new-frame          Start fresh theoretical iteration
  /new-frame list     See all frame attempts
  /new-frame compare  Compare frames side-by-side
  /switch-project     Switch to different paper (multi-project)
  /export             Generate manuscript in different formats
  /consensus-config   Configure consensus mode settings

```

## Status Symbols

- `[✓]` - Completed
- `[→]` - In progress
- `[ ]` - Pending
- `[!]` - Blocked (missing prerequisites)

### Evaluation Results Dashboard

If `state.json.eval_results` has any entries for the current frame, display them:

For each eval result:
- Show score (X/Y for scored, PASS/FAIL for verdict-based)
- Show stability rating with emoji:
  - 🟢 HIGH — low coefficient of variation across consensus runs
  - 🟡 MED — moderate variation
  - 🔴 LOW — high variation, result is unstable
- Show status:
  - `✓ PASS` — meets threshold, current
  - `✗ FAIL` — below threshold
  - `⚠ STALE` — upstream changed since eval (e.g., frame shift)
  - `○ Not run` — no results exist

If `/check-submission` has been run, show its overall verdict (PASS/CONDITIONAL/FAIL).
If any results are stale, show a warning: "⚠ [N] eval results are stale. Run /check-submission to re-evaluate."

### Next Step: Submission Readiness

In the NEXT STEP section, add this logic: if all workflow stages are complete (explore_data through draft_paper) but `check_submission` status is not "completed" or its verdict is not "PASS", suggest:

```
→ Run /check-submission to verify submission readiness

All workflow stages are complete. Run the full test suite before exporting.
```

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

---

## HTML Dashboard Generation

After displaying terminal output, generate `dashboard.html` in the project root.

**Template:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Paper Mining Dashboard - [PROJECT_NAME]</title>
  <style>
    :root {
      --bg: #1a1a2e;
      --card: #16213e;
      --accent: #0f3460;
      --text: #eee;
      --muted: #888;
      --success: #4ecca3;
      --warning: #ffc107;
      --danger: #e74c3c;
      --info: #3498db;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: var(--bg);
      color: var(--text);
      padding: 2rem;
      min-height: 100vh;
    }
    .container { max-width: 900px; margin: 0 auto; }
    h1 { margin-bottom: 0.5rem; }
    .subtitle { color: var(--muted); margin-bottom: 2rem; }
    .card {
      background: var(--card);
      border-radius: 12px;
      padding: 1.5rem;
      margin-bottom: 1.5rem;
    }
    .card h2 {
      font-size: 1rem;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--muted);
      margin-bottom: 1rem;
      border-bottom: 1px solid var(--accent);
      padding-bottom: 0.5rem;
    }
    .progress-bar {
      background: var(--accent);
      border-radius: 8px;
      height: 12px;
      overflow: hidden;
      margin-bottom: 0.5rem;
    }
    .progress-fill {
      background: linear-gradient(90deg, var(--info), var(--success));
      height: 100%;
      transition: width 0.3s ease;
    }
    .progress-text { color: var(--muted); font-size: 0.9rem; }
    .stages { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem; }
    .stage {
      background: var(--accent);
      border-radius: 8px;
      padding: 1rem;
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }
    .stage-icon {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1rem;
    }
    .stage-icon.completed { background: var(--success); }
    .stage-icon.in-progress { background: var(--info); }
    .stage-icon.pending { background: var(--muted); opacity: 0.5; }
    .stage-icon.blocked { background: var(--danger); }
    .stage-name { font-weight: 500; }
    .stage-status { font-size: 0.8rem; color: var(--muted); }
    .frame-info { display: flex; gap: 2rem; flex-wrap: wrap; }
    .frame-item { }
    .frame-label { color: var(--muted); font-size: 0.8rem; }
    .frame-value { font-size: 1.1rem; margin-top: 0.25rem; }
    .consensus-badge {
      display: inline-block;
      padding: 0.25rem 0.75rem;
      border-radius: 12px;
      font-size: 0.85rem;
      font-weight: 500;
    }
    .consensus-badge.enabled { background: var(--success); color: #000; }
    .consensus-badge.disabled { background: var(--muted); }
    .stability-row { display: flex; gap: 1rem; margin-top: 0.5rem; }
    .stability-item { font-size: 0.9rem; }
    .stability-item.high { color: var(--success); }
    .stability-item.medium { color: var(--warning); }
    .stability-item.low { color: var(--danger); }
    .next-step {
      background: linear-gradient(135deg, var(--info), var(--accent));
      border-radius: 8px;
      padding: 1rem 1.5rem;
      font-size: 1.1rem;
    }
    .next-step code {
      background: rgba(0,0,0,0.3);
      padding: 0.2rem 0.5rem;
      border-radius: 4px;
      font-family: monospace;
    }
    .updated { color: var(--muted); font-size: 0.8rem; text-align: center; margin-top: 2rem; }
  </style>
</head>
<body>
  <div class="container">
    <h1>📄 [PROJECT_NAME]</h1>
    <p class="subtitle">Frame [FRAME_NUM] · Updated [UPDATED_TIME]</p>

    <div class="card">
      <h2>Workflow Progress</h2>
      <div class="progress-bar">
        <div class="progress-fill" style="width: [PROGRESS_PCT]%;"></div>
      </div>
      <p class="progress-text">[COMPLETED_COUNT]/8 stages complete ([PROGRESS_PCT]%)</p>

      <div class="stages" style="margin-top: 1rem;">
        <!-- Repeat for each stage -->
        <div class="stage">
          <div class="stage-icon [STATUS_CLASS]">[ICON]</div>
          <div>
            <div class="stage-name">[STAGE_NAME]</div>
            <div class="stage-status">[STATUS_TEXT]</div>
          </div>
        </div>
        <!-- End repeat -->
      </div>
    </div>

    <div class="card">
      <h2>Current Frame</h2>
      <div class="frame-info">
        <div class="frame-item">
          <div class="frame-label">Theory</div>
          <div class="frame-value">[THEORY_NAME]</div>
        </div>
        <div class="frame-item">
          <div class="frame-label">Lens</div>
          <div class="frame-value">[LENS_NAME]</div>
        </div>
        <div class="frame-item">
          <div class="frame-label">Framing</div>
          <div class="frame-value">[FRAMING_NAME]</div>
        </div>
      </div>
    </div>

    <div class="card">
      <h2>Consensus Mode</h2>
      <span class="consensus-badge [CONSENSUS_CLASS]">[CONSENSUS_STATUS]</span>
      <!-- If enabled, show stability summary -->
      <div class="stability-row">
        <span class="stability-item high">✓ [HIGH_COUNT] HIGH</span>
        <span class="stability-item medium">~ [MED_COUNT] MEDIUM</span>
        <span class="stability-item low">⚠ [LOW_COUNT] LOW</span>
      </div>
    </div>

    <div class="card">
      <h2>Next Step</h2>
      <div class="next-step">
        → Run <code>[NEXT_COMMAND]</code> [NEXT_DESCRIPTION]
      </div>
    </div>

    <p class="updated">Refresh this page after running commands in Claude Code</p>
  </div>
</body>
</html>
```

**Generation instructions:**

1. Read `state.json` and extract all values
2. Replace placeholders in template:
   - `[PROJECT_NAME]` → `state.project_name`
   - `[FRAME_NUM]` → `state.current_frame`
   - `[UPDATED_TIME]` → relative time from `state.updated_at`
   - `[PROGRESS_PCT]` → (completed stages / 8) × 100
   - `[COMPLETED_COUNT]` → count of completed stages
   - For each stage: `[STATUS_CLASS]`, `[ICON]`, `[STAGE_NAME]`, `[STATUS_TEXT]`
   - `[THEORY_NAME]`, `[LENS_NAME]`, `[FRAMING_NAME]` → from current frame
   - `[CONSENSUS_CLASS]` → "enabled" or "disabled"
   - `[CONSENSUS_STATUS]` → "ENABLED" or "DISABLED"
   - `[HIGH_COUNT]`, `[MED_COUNT]`, `[LOW_COUNT]` → from consensus results
   - `[NEXT_COMMAND]`, `[NEXT_DESCRIPTION]` → next uncompleted stage
3. Write to `dashboard.html` in project root
4. Tell user: "Dashboard updated → open dashboard.html in browser"

**Stage icons:**
- completed: ✓
- in_progress: →
- pending: ○
- blocked: !
