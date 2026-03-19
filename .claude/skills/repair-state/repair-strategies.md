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
