---
name: sandbox-mode
description: Honor research-quals v1 sandbox mode. When RQ_SANDBOX=1 is set, theory-forge must not write to any public surface (audit trail, telemetry, portfolio) and must respect the architectural guarantee that sandbox sessions are invisible to advisors. Use when the user mentions "sandbox", "advisor-blind", or "private session", or whenever a session starts inside an existing sandbox.
---

# Sandbox Mode (theory-forge integration)

theory-forge runs inside research-quals v1's sandbox mode whenever the `RQ_SANDBOX=1` environment variable is set. This skill documents the contract.

See `research-quals/docs/spec/SANDBOX_GUARANTEE.md` for the full threat model.

## The contract

When `RQ_SANDBOX=1`:

1. **No writes to the public portfolio.** Any command that would normally write to `~/.research-quals/public/<student-uuid>/` must instead write to `$RQ_SANDBOX_DIR`.
2. **No telemetry.** Any logging surface that would propagate beyond the sandbox dir is disabled. This includes `audit-trail`, `eval-persistence`, and any opt-in remote logging.
3. **No publication-by-default.** `/draft-paper`, `/export`, `/check-submission` and other surfacing commands print a warning: *"You are in sandbox mode. Output will be written to your local sandbox dir only. To publish, exit the sandbox and re-run."*
4. **export-trace requires explicit election.** Even with all the above, `export-trace` from a sandbox session is refused unless the user passes `--i-am-electing-to-publish-this`. This is deliberate friction — the student must consciously decide to move content out.

## Why this is theory-forge's responsibility

The sandbox guarantee is enforced at two layers:

- **Filesystem layer** (research-quals): the `is_sandbox_path()` guard in `rq.paths` prevents advisor-side reads.
- **Tool layer** (theory-forge): every theory-forge skill that writes anywhere must check `RQ_SANDBOX` and choose the sandbox dir over any public path.

If theory-forge skills don't honor the contract, the filesystem layer can't save them. A skill that writes to `~/.research-quals/public/.../` from a sandbox session has leaked sandbox content into the public space, defeating the guarantee.

This skill documents the contract so that future theory-forge skill authors know what to check.

## What every theory-forge skill must do at startup

```python
import os
in_sandbox = os.environ.get("RQ_SANDBOX") == "1"
sandbox_dir = os.environ.get("RQ_SANDBOX_DIR")

if in_sandbox:
    output_root = sandbox_dir
    # disable any telemetry
    # disable any audit-trail propagation
    # warn user that this session is invisible
else:
    output_root = the_normal_path
```

## What this skill does NOT do

It does not enforce the contract — it documents it. Enforcement is up to each individual theory-forge skill that writes anywhere. We are working on a centralized check (a `theory_forge.io.write_safe()` wrapper that all skills route through), but for v1.0 the contract is documentation + per-skill discipline.

## Audit

`rq doctor sandbox` checks that:
- The filesystem isolation holds
- The `is_sandbox_path()` guard returns the right answers
- The env var doesn't leak out of subshells

It does NOT yet check that every theory-forge skill honors the contract. That's a v1.1 audit pass — a static check across all `.claude/skills/*/SKILL.md` files.

## When the user invokes a sandbox session

The flow:

```bash
$ rq sandbox start
[entering sandbox: <uuid>]
This session is invisible to your advisor and to cohort telemetry.

[rq sandbox] $ theory-forge /explore-data ./mydata/
# theory-forge sees RQ_SANDBOX=1, writes only to $RQ_SANDBOX_DIR
# no audit trail, no telemetry, no portfolio writes
# the student fails freely

[rq sandbox] $ exit
```

The session ends when the subshell exits. Anything in the sandbox dir is the student's. Nothing is propagated.
