# State Management Protocol

Every skill follows this protocol for reading and updating `state.json`.

## Before Starting

1. Check for `state.json` in project root (or `projects/[active]/state.json` for multi-project)
2. Verify prerequisites — each skill has specific `workflow.{key}.status === "completed"` checks
3. If prerequisites not met, inform user and suggest the missing skill
4. Check current frame number: `state.json` → `current_frame`
5. Check if **student mode** is enabled: `state.json` → `student_mode.enabled`
6. Check if **consensus mode** is enabled: `state.json` → `consensus.stages.{skill_name}.enabled`

## After Completing

1. Update `state.json`:
   - Set `workflow.{skill_name}.status` to `"completed"`
   - Set `workflow.{skill_name}.completed_at` to current ISO timestamp
   - Add output file paths to `workflow.{skill_name}.outputs`
   - If consensus mode was active: add `workflow.{skill_name}.consensus_result` with stability summary
   - Update root `updated_at` timestamp
2. Append entry to `DECISION_LOG.md` with skill name, key findings, and timestamp
3. If student mode: append session record to `STUDENT_WORK.md`

## Multi-Project Support

If no `state.json` in project root, check `projects/*/state.json`. The active project is determined by `switch-project` or the most recently modified state file.

## State Recovery

If `state.json` is corrupted or missing, direct user to `/repair-state`.
