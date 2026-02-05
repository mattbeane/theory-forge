# Audit Trail

View and export the decision audit trail for transparent methodology.

## Usage

```
/audit-trail                           # Show all decisions
/audit-trail --stage hunt_patterns     # Filter by pipeline stage
/audit-trail --export appendix         # Generate methods appendix
/audit-trail --link                    # Auto-link decisions to CC conversations
/audit-trail --summary                 # Brief summary only
```

## State Management

Before starting:
1. Check for `state.json` in project root
2. Read `state.json.decisions` array
3. If empty, inform user no decisions have been logged yet

## What This Shows

The audit trail documents every significant analytical decision:

- **Pattern Selection**: Which patterns were pursued/rejected and why
- **Theory Choices**: Which theories were selected as primary/sensitizing
- **Qualitative Coding**: Mechanisms identified, quotes selected, disconfirming evidence
- **Framing Decisions**: Which frames were generated/selected/rejected
- **Claim Verification**: Which claims were verified/flagged

Each decision includes:
- Timestamp and unique ID
- What was decided and why
- Alternatives considered
- Supporting and challenging evidence
- Confidence level
- Link to Claude Code conversation (if available)

## Output Modes

### Default: Full Trail

Shows all decisions with reasoning:

```markdown
# Complete Audit Trail

## Hunt Patterns

### ✅ Shadow Learning Pattern
*DEC-A1B2C3D4 | 2025-02-04 14:30*

**Decision:** Selected shadow learning as core pattern

**Reasoning:** High effect size (β=0.38), robust to controls, heterogeneity suggests mechanism

**Supporting evidence:**
- Effect survives 12 control specifications
- Varies by OR type (hypothesis-generating)

**Alternatives considered:**
- Pure OR17 effect (rejected: less novelty)
- Resident count alone (rejected: expected finding)

**Confidence:** 🟢 HIGH

---
```

### With `--stage <stage_name>`

Filter to specific pipeline stage:

```
/audit-trail --stage mine_qual
```

Shows only qualitative mining decisions.

### With `--export appendix`

Generate a methods appendix suitable for paper supplementary materials:

```markdown
# Analytical Decisions

*Methods appendix for: Shadow Learning in Surgical Training*

This appendix documents key analytical decisions...

## Pattern Selection

### Shadow Learning
We identified **shadow learning** as a core empirical pattern based on:
- Effect size: β=0.38 (95% CI: 0.34-0.42)
- Robustness: Survived 12 control specifications
- Heterogeneity: Effect varies by OR type, suggesting mechanism

**Alternatives considered:**
- Pure OR17 effect: Rejected due to limited novelty
- Resident count alone: Rejected as expected finding

## Theoretical Positioning
...
```

### With `--link`

Auto-link decisions to Claude Code conversation history:

```
/audit-trail --link
```

Searches `~/.claude/history.jsonl` for conversations within ±5 minutes of each decision timestamp and links them for full traceability.

Reports: "Linked 8 of 12 decisions to CC conversations"

### With `--summary`

Brief summary for status displays:

```
12 decisions: 3 pattern selected, 2 pattern rejected, 5 quote selected, 2 frame selected
```

## How Decisions Get Logged

Decisions are logged automatically by pipeline commands when they:
- Accept or reject a pattern
- Select a theory or sensitizing lens
- Identify a mechanism
- Select a quote for the paper
- Note disconfirming evidence
- Generate, select, or reject a framing
- Pass or fail a gate

You can also manually log decisions using the tracker:

```python
from lib.audit import log_decision, DecisionType

log_decision(
    state_path=Path("state.json"),
    stage="hunt_patterns",
    decision_type=DecisionType.PATTERN_SELECTED,
    action="selected",
    entity_type="pattern",
    entity_id="shadow-learning",
    entity_label="Shadow Learning Pattern",
    description="Selected shadow learning as core pattern",
    reasoning="High effect size, robust to controls, heterogeneity suggests mechanism",
    alternatives=["Pure OR17 effect", "Resident count alone"],
    supporting=["β=0.38", "Survives 12 controls"],
    confidence="high",
)
```

## Why This Matters

### For Peer Review

Reviewers increasingly ask: "How did you arrive at this interpretation?" The audit trail provides:
- Complete decision history
- Reasoning at each step
- Alternatives considered
- Evidence for and against

### For Methods Sections

The `--export appendix` output can go directly into supplementary materials, demonstrating transparent methodology.

### For Reproducibility

With Claude Code conversation linkage, future researchers can see exactly what analysis was run and why decisions were made.

### For Learning

For students using theory-forge, the audit trail shows how expert-like analytical decisions are structured.

## Tips

- Run `/audit-trail --summary` during pipeline to see decision count
- Run `/audit-trail --export appendix` before submission to generate methods documentation
- Run `/audit-trail --link` after major work sessions to connect decisions to CC history
- The trail is stored in `state.json.decisions` and persists across sessions

## Related Commands

- `/status` - See overall pipeline progress
- `/verify-claims` - Create verification package (uses audit trail)
- `/package-verification` - Full verification package for reviewers
