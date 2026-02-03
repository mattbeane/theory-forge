# Repair Project State

You are the STATE-REPAIR agent. Your job is to diagnose and fix problems with project state, recovering from corrupted, missing, or out-of-sync `state.json` files.

## Why This Matters

`state.json` tracks workflow progress, but things can go wrong:
- File gets accidentally deleted or corrupted
- JSON syntax errors from manual editing
- State gets out of sync with actual output files
- Workflow stages show "pending" but outputs exist
- Frames get mixed up or lost

This command diagnoses the problem and offers recovery options.

## When to Run This

Run this when:
- `/status` errors out or shows strange data
- You see "state.json not found" errors
- State doesn't match reality (outputs exist but state says pending)
- After git operations that might have affected state
- When state seems corrupted (missing keys, bad data)

## Diagnostic Framework

### Problem Type 1: Missing state.json

**Symptoms**: No `state.json` in project root

**Diagnosis**: Check if this is:
- A fresh project (never initialized)
- A project where state was deleted
- Multi-project mode with state in wrong location

**Recovery options**:
- A) Create fresh state.json (if truly new project)
- B) Reconstruct state from existing outputs (if outputs exist)
- C) Check for state.json.backup (if we've been making backups)
- D) Check git history for deleted state.json

---

### Problem Type 2: Corrupted JSON

**Symptoms**: JSON parse errors when reading state.json

**Diagnosis**: Attempt to parse and identify error location

**Recovery options**:
- A) Fix JSON syntax automatically (if minor issue like trailing comma)
- B) Extract what's salvageable, rebuild rest
- C) Restore from backup
- D) Reconstruct from outputs

---

### Problem Type 3: State-Output Desync

**Symptoms**: state.json says "pending" but output files exist (or vice versa)

**Diagnosis**: Compare state.json workflow statuses against actual output files

**Recovery options**:
- A) Update state to match outputs (trust the files)
- B) Clear outputs to match state (trust the state)
- C) Interactive reconciliation (ask user for each mismatch)

---

### Problem Type 4: Schema Mismatch

**Symptoms**: Old state.json missing fields needed by current commands

**Diagnosis**: Check state.json version against expected schema

**Recovery options**:
- A) Migrate state to current schema (preserve data, add missing fields)
- B) Create fresh state (lose progress)

---

### Problem Type 5: Frame Confusion

**Symptoms**: Frame numbers don't match frame directories, or current_frame is invalid

**Diagnosis**: Compare state.json frames against `analysis/framing/frame-*/` directories

**Recovery options**:
- A) Rebuild frames from directories
- B) Clean up orphaned directories
- C) Reset to single frame

---

## Steps

### Step 1: Initial Diagnosis

```python
# Pseudocode for diagnosis

def diagnose_state():
    # 1. Check if state.json exists
    if not exists("state.json"):
        return "MISSING_STATE"

    # 2. Try to parse JSON
    try:
        state = json.load("state.json")
    except JSONDecodeError as e:
        return ("CORRUPTED_JSON", e.lineno, e.colno)

    # 3. Check schema version
    if state.get("version", "0.0.0") < CURRENT_VERSION:
        return ("SCHEMA_MISMATCH", state.get("version"))

    # 4. Check state-output sync
    mismatches = check_output_sync(state)
    if mismatches:
        return ("DESYNC", mismatches)

    # 5. Check frame consistency
    frame_issues = check_frames(state)
    if frame_issues:
        return ("FRAME_ISSUES", frame_issues)

    return "HEALTHY"
```

### Step 2: Report Diagnosis

Show user exactly what's wrong:

```
╔══════════════════════════════════════════════════════════════════╗
║  STATE DIAGNOSIS                                                  ║
╚══════════════════════════════════════════════════════════════════╝

Problem detected: STATE-OUTPUT DESYNC

The following mismatches were found:

  Stage              State Says    Output Files
  ────────────────   ────────────  ────────────────────────
  explore_data       completed ✓   ✓ DATA_INVENTORY.md exists
  hunt_patterns      completed ✓   ✓ PATTERN_REPORT.md exists
  find_theory        pending ✗     ✓ PRIMARY_THEORY.md EXISTS   ← MISMATCH
  find_lens          pending ✓     ✗ No output (matches)
  smith_frames       pending ✗     ✓ FRAMING_OPTIONS.md EXISTS  ← MISMATCH

2 stages have outputs but state shows "pending"

Recovery options:
  [A] Update state to match outputs (recommended)
  [B] Interactive reconciliation
  [C] Manual inspection first
```

### Step 3: Execute Recovery

Based on user choice, execute the appropriate recovery strategy.

### Step 4: Validate Recovery

After any repair, validate:
1. state.json is valid JSON
2. All workflow stages have valid status values
3. Outputs mentioned in state actually exist
4. Frame references are consistent
5. Timestamps are reasonable

### Step 5: Create Backup

Before any repair that modifies state:
1. Copy current state.json to state.json.backup (if parseable)
2. Or copy corrupted file to state.json.corrupted for inspection

## Output Format

Create `analysis/REPAIR_LOG.md` (append if exists):

```markdown
# State Repair Log

---

## Repair: [ISO Timestamp]

### Diagnosis

**Problem type**: [MISSING_STATE / CORRUPTED_JSON / DESYNC / SCHEMA_MISMATCH / FRAME_ISSUES]

**Details**:
[Specific description of what was wrong]

### Recovery Action

**Strategy chosen**: [A/B/C/D with description]

**Changes made**:
- [Change 1]
- [Change 2]
- [Change 3]

### Before State (if available)

```json
[Relevant portions of old state]
```

### After State

```json
[Relevant portions of new state]
```

### Validation

- [x] state.json is valid JSON
- [x] All workflow stages have valid status
- [x] Output files match state
- [x] Frame references are consistent
- [ ] Timestamps verified

### Notes

[Any additional context or warnings for the user]

---
```

## Repair Strategies

### Strategy: Reconstruct from Outputs

If state.json is missing or corrupted beyond repair, reconstruct by scanning outputs:

```python
def reconstruct_state_from_outputs():
    state = create_fresh_state()

    # Check each stage's expected outputs
    stages_to_check = [
        ("explore_data", "analysis/exploration/DATA_INVENTORY.md"),
        ("hunt_patterns", "analysis/patterns/PATTERN_REPORT.md"),
        ("find_theory", "analysis/theory/PRIMARY_THEORY.md"),
        ("find_lens", "analysis/theory/SENSITIZING_LITERATURE.md"),
        ("mine_qual", "analysis/qualitative/MECHANISM_REPORT.md"),
        ("smith_frames", "analysis/framing/FRAMING_OPTIONS.md"),
        ("audit_claims", "analysis/audit/AUDIT_REPORT.md"),
        ("verify_claims", "analysis/verification/VERIFICATION_BRIEF.md"),
        ("draft_paper", "output/drafts/manuscript.md"),
    ]

    for stage, output_path in stages_to_check:
        if exists(output_path):
            state["workflow"][stage]["status"] = "completed"
            state["workflow"][stage]["outputs"] = [output_path]
            # Use file modification time as completion timestamp
            state["workflow"][stage]["completed_at"] = file_mtime(output_path)

    # Check for frames
    frame_dirs = glob("analysis/framing/frame-*/")
    for i, frame_dir in enumerate(sorted(frame_dirs), 1):
        state["frames"][str(i)] = reconstruct_frame(frame_dir)

    state["current_frame"] = len(frame_dirs) or 1

    return state
```

### Strategy: Migrate Schema

When state.json exists but is outdated:

```python
def migrate_state(old_state, from_version):
    new_state = copy(old_state)

    if from_version < "1.1.0":
        # Add consensus fields (introduced in 1.1.0)
        new_state["consensus"] = {
            "enabled": False,
            "default_n": 10,
            "stages": {
                "hunt_patterns": {"n": 25, "enabled": True},
                "mine_qual": {"n": 15, "enabled": True},
                "verify_claims": {"n": 10, "enabled": True}
            },
            "thresholds": {
                "high_stability_cv": 0.10,
                "medium_stability_cv": 0.25,
                "quote_high_stability": 0.75,
                "quote_medium_stability": 0.50
            },
            "provider": "anthropic",
            "model": "claude-sonnet-4-20250514"
        }

    # Add any missing workflow stages
    expected_stages = ["explore_data", "hunt_patterns", "find_theory",
                       "find_lens", "mine_qual", "smith_frames",
                       "audit_claims", "verify_claims", "draft_paper",
                       # New stages added over time
                       "integrate_quant_qual", "compare_frames",
                       "simulate_review", "build_lit_review", "eval_contribution"]

    for stage in expected_stages:
        if stage not in new_state["workflow"]:
            new_state["workflow"][stage] = {
                "status": "pending",
                "completed_at": None,
                "outputs": []
            }

    new_state["version"] = CURRENT_VERSION
    return new_state
```

### Strategy: Fix JSON Syntax

Common JSON errors and fixes:

| Error | Fix |
|-------|-----|
| Trailing comma | Remove the comma |
| Missing closing brace | Add the brace |
| Unquoted key | Add quotes |
| Single quotes | Replace with double quotes |
| Unescaped newline in string | Escape or remove |

Attempt automatic fix for simple errors; prompt user for complex ones.

### Strategy: Interactive Reconciliation

For desync issues, walk through each mismatch:

```
Mismatch 1 of 3: find_theory

  State says:     pending
  Output exists:  analysis/theory/PRIMARY_THEORY.md (modified 2 days ago)

  What should we do?

  [T] Trust the output → mark find_theory as "completed"
  [S] Trust the state → this output must be from another project, ignore it
  [D] Delete the output → it's orphaned, remove it
  [?] Inspect the file first

  Your choice: _
```

## Backup System

### Automatic Backups

Each command that modifies state should:
1. Before writing state.json, copy current to state.json.prev
2. Keep last 3 .prev files (rotate: .prev → .prev.1 → .prev.2)

This gives us recovery points even if /repair-state hasn't been run.

### Manual Backup Trigger

User can run `/repair-state backup` to explicitly create a timestamped backup:
- state.json → state.json.backup.YYYYMMDD_HHMMSS

### Backup Location

```
[project]/
├── state.json              ← Current state
├── state.json.prev         ← Previous state (1 modification ago)
├── state.json.prev.1       ← 2 modifications ago
├── state.json.prev.2       ← 3 modifications ago
└── backups/
    ├── state.json.backup.20250203_143022
    └── state.json.backup.20250201_091544
```

## After You're Done

Tell the user:
1. What problem was found
2. What recovery action was taken
3. What the state looks like now
4. Whether any data was lost or at risk
5. How to prevent this in the future

## Integration with Other Commands

- `/status` should detect issues and suggest `/repair-state`
- All state-modifying commands should create backups before writing
- `/init-project` should check for existing corrupted state before creating new

## State Management

After completing repair:
1. No state.json update (we just fixed it!)
2. Append to `analysis/REPAIR_LOG.md`
3. Create/rotate backups as appropriate

## Common Scenarios

**"I pulled from git and now state is weird"**
- Likely a merge conflict in state.json, or .gitignore issues
- Solution: Compare state with outputs, reconcile

**"I accidentally deleted state.json"**
- Check backups/ directory first
- If no backups, reconstruct from outputs
- This is why we keep backups!

**"Commands keep failing with JSON errors"**
- Likely manual edit introduced syntax error
- Show the specific error location
- Offer automatic fix or restore from backup

**"State shows everything complete but outputs are missing"**
- Either outputs were deleted, or state was incorrectly updated
- Offer to reset affected stages to "pending"
- Warn that rerunning may produce different results

**"I'm in frame 3 but there's only frame-1 and frame-2 directories"**
- Frame state inconsistency
- Offer to fix current_frame to match actual frames
- Or create empty frame-3 directory
