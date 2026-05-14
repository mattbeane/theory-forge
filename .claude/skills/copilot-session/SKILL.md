---
name: copilot-session
description: Run theory-forge as a co-pilot session — advisor and student share a single agent session as co-novices, neither in charge, joint artifact, no grading. Operationalizes the Seeking pathway from Inverted Apprenticeships. Use when the user explicitly says "co-pilot session", "joint session", "let's work on this together with advisor/student".
---

# /copilot-session

A theory-forge session with two human participants instead of one. Both type. Both see all output. Neither is the "owner." The session produces a single artifact, jointly attributed.

This skill operationalizes the Seeking pathway from Beane & Anthony, *Inverted Apprenticeships* — visible joint struggle, suspended hierarchy, durable shared artifact.

See `research-quals/docs/spec/COPILOT_SESSION_PROTOCOL.md` for the full protocol.

## What this skill does

1. **Initializes a shared session directory** at `~/.research-quals/shared/copilot/<session-uuid>/`. Both participants point their theory-forge instances at this directory.
2. **Tracks turn ownership.** The session manifest records whose turn it is. Both participants can take turns; the manifest enforces alternation softly (no hard locking; the protocol relies on the format's culture).
3. **Captures the joint transcript.** Every prompt is attributed to its actor. The transcript becomes the trace artifact when the session ends.
4. **Generates a joint reflection template.** When the session is winding down, both participants write into the same reflection file. The skill verifies that both UUIDs appear in the file's edit history before accepting `finish`.
5. **Reports the prompt-balance check.** On `finish`, computes prompt counts per participant. If either participant produced <20% of prompts, the session is flagged as **asymmetric** (likely Leveraging). This is the R1 check from the protocol.

## The hard rules (R1–R5)

Not enforced by code, enforced by the format. Read these out loud at the start of every session:

- **R1.** Both participants must touch the keyboard. The session warns if not.
- **R2.** No grading surface. The session produces a trace, not a score.
- **R3.** Joint attribution. Neither can publish solo.
- **R4.** The reflection is genuinely joint. Both must contribute to the file.
- **R5.** No advance preparation by one party for the other. The session is improvised. (No software check; cultural rule.)

## What this skill is NOT

- **Not a tutoring session.** No teacher/student asymmetry. If you find one party explaining things to the other, you're in a tutorial. Stop, restart with the format clear.
- **Not a defense.** No examiner. If you find one party probing the other's choices, you're in a viva. Stop.
- **Not a code review.** If you find one party critiquing the other's prior work, you're in v0 territory. Stop.

If the session keeps degenerating into one of these, the format isn't right for the participants in their current relationship. The most common reason: the advisor hasn't done Faculty Drill yet and is psychologically defending position. Solution: pause the co-pilot work, advisor takes Faculty Drill (`rq faculty-drill start`), then resume.

## The capstone use

The v1 BYOM capstone defense is replaced by a co-pilot session over the student's pipeline. See `research-quals/assessments/level-4-byom-coreflection.md`. Both parties run the student's pipeline together, then a reference pipeline together, then write a joint reflection. The trace is the deliverable.

## When to invoke

Invoke when the user explicitly says:
- "Let's run a co-pilot session"
- "Joint session with [name]"
- "I want to work on this with my advisor / student"
- "Co-reflection on my BYOM capstone"

Do NOT invoke automatically. Co-pilot sessions are deliberate; they require both participants to opt in.

## The default mode is solo

When the user is alone in theory-forge, they're in solo mode. Solo mode is the normal mode. Co-pilot is a special session type for the specific dynamic above. Most theory-forge work is and should be solo (or sandbox); co-pilot is specifically for the joint-struggle moments where the format adds value.
