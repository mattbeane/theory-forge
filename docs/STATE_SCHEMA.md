# State Schema Reference

This document describes the `state.json` file that tracks workflow progress.

## Overview

`state.json` is auto-managed by the pipeline. You shouldn't need to edit it manually, but understanding its structure helps debug issues and understand what's deterministic vs model-dependent.

## Schema

```json
{
  "version": "1.0.0",
  "project_name": "string",
  "created_at": "ISO 8601 timestamp",
  "updated_at": "ISO 8601 timestamp",
  "current_frame": 1,
  "workflow": { /* see below */ },
  "frames": { /* see below */ },
  "decisions": [],
  "metadata": { /* see below */ }
}
```

## Workflow Object

Tracks completion status for each pipeline stage:

```json
{
  "workflow": {
    "explore_data": {
      "status": "pending | in_progress | completed",
      "completed_at": "ISO timestamp | null",
      "outputs": ["analysis/exploration/summary.md"]
    },
    "hunt_patterns": { /* same structure */ },
    "find_theory": { /* same structure */ },
    "find_lens": { /* same structure */ },
    "mine_qual": { /* same structure */ },
    "smith_frames": { /* same structure */ },
    "audit_claims": {
      "status": "pending | in_progress | completed",
      "completed_at": "ISO timestamp | null",
      "outputs": [],
      "supporting_count": 0,
      "challenging_count": 0,
      "high_concern_claims": []
    },
    "verify_claims": { /* same structure */ },
    "draft_paper": { /* same structure */ }
  }
}
```

### Status Values

| Status | Meaning |
|--------|---------|
| `pending` | Not started |
| `in_progress` | Currently running (rare—usually completes immediately) |
| `completed` | Finished successfully |

## Frames Object

Tracks theoretical iterations:

```json
{
  "frames": {
    "1": {
      "created_at": "ISO timestamp",
      "theory": "string | null",
      "lens": "string | null",
      "framing": "string | null",
      "status": "active | archived"
    }
  }
}
```

Running `/new-frame` archives the current frame and creates a new one. Empirical work (exploration, patterns) carries forward; theory/lens/framing reset.

## Metadata Object

```json
{
  "metadata": {
    "target_journal": "ASQ | OrgSci | ManSci | null",
    "domain": "string | null",
    "anonymization_rules": {}
  }
}
```

## What's Deterministic vs Model-Dependent

| Deterministic | Model-Dependent |
|---------------|-----------------|
| `status` transitions | Content of `outputs` files |
| `completed_at` timestamps | Theory/lens/framing text |
| `current_frame` number | Pattern identification |
| File paths in `outputs` | Claim verification results |

The state file tracks *that* you completed a stage, not *what* the model produced. Running the same stage twice may yield different content, but the state transitions are deterministic.

## Quality Gates

The hooks in `.claude/hooks.json` read `state.json` to enforce workflow order. For example, `/find-theory` checks that `hunt_patterns.status === 'completed'` before proceeding.

These are warnings, not blocks—you can override if needed.

## Multi-Project Mode

In multi-project mode, each project has its own `state.json` at `projects/[name]/state.json`. A `workspace.json` at the root tracks which project is active.
