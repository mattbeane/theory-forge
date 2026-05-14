---
name: export-trace
description: Export the current research session as an annotated, scrubbable trace bundle for the research-quals trace library. Use when the user says "export this session as a trace", "save this for the trace library", or has just finished a substantive theory-forge session and wants others to learn from it.
---

# /export-trace

Convert the current theory-forge session into a publishable trace bundle that conforms to the research-quals trace library schema (see `research-quals/docs/spec/TRACE_LIBRARY_SPEC.md`).

This is the bridge between theory-forge (where research happens) and research-quals (where the rehearsal layer lives). Without this skill, the rehearsal layer is empty and v1 fails.

## What this skill does

1. **Captures the session transcript.** Walks the message history, extracts user prompts, agent responses, and tool calls. Filters out chatter and ephemeral state changes.
2. **Walks the user through an annotation pass.** At each significant context shift (new tool call, framing change, decision point), asks the user: *"This looks like a decision point. Want to comment on what you were thinking here?"* Records their commentary as annotations.
3. **Extracts failure points.** Asks the user: *"Did the agent get anything wrong in this session? Was there a moment where you noticed it was producing the wrong thing?"* Records each instance with timestamp, what happened, and how the user caught it.
4. **Generates a draft MANIFEST.yaml.** Pulls metadata from session state: duration, tools used, dataset description (asks the user). User fills in tags, difficulty, license.
5. **Saves the bundle** to a directory the user specifies, conforming to the trace library schema.

## Sandbox awareness

If the current session is a sandbox session (`RQ_SANDBOX=1` env var set), this skill **refuses to export** unless the user passes the explicit flag `--i-am-electing-to-publish-this`. This is a deliberate friction surface — it forces the student to consciously elect to move content out of the protected zone. See `research-quals/docs/spec/SANDBOX_GUARANTEE.md`.

## Output

A directory containing:
- `MANIFEST.yaml`
- `transcript.jsonl` (the captured session)
- `annotations.md` (decision-point commentary)
- `failure-points.md` (moments the agent went wrong)
- `artifact/` (the produced output, if any)

The user can then `rq trace validate <dir>` to check schema conformance and submit it to the canonical library via PR.

## Anti-patterns this skill rejects

- **Cleaning up the session.** Don't cut the boring parts. Don't smooth over the dead ends. The boring parts are where students learn that real research is mostly waiting and re-prompting.
- **Composite traces.** Don't combine multiple sessions into one "best of." If you didn't run it as a single session, it's not a trace.
- **Tutorials masquerading as traces.** If you find yourself adding learning objectives, you're authoring a Foundation exercise. Put it in `research-quals/assessments/`.
- **Highlight reels.** Failure points are part of the value, not embarrassments to hide.

## Integration with the v1 protocol

This skill is the connective tissue. Without it:
- Sandbox mode produces sessions that nobody else can learn from
- The trace library stays empty
- The rehearsal layer claim in the v1 spec is theoretical

With it:
- Any session — published or, with explicit election, ex-sandbox — can become a teaching artifact
- The library grows organically as faculty and students do real work
- The Matthew effect alarm in `rq telemetry cohort` has data to flag against

## When to invoke

Invoke when the user has finished a substantive session and explicitly says any of:
- "Export this as a trace"
- "Save this for the trace library"
- "Make this teachable"
- "I want to share what I just did with my cohort"

Do NOT invoke automatically. The decision to publish a trace is the user's, always. Especially out of sandbox mode.
