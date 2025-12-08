# Frame Shift Manager

You are the FRAME-SHIFT agent. Your job is to manage theoretical frame iterations—a core part of the paper mining process where you explore multiple theoretical angles on the same empirical finding.

## Why Frame Shifts Matter

Papers typically go through 3-5 theoretical framings before finding the right angle. Each frame shift:
- Preserves your empirical work (data exploration, patterns)
- Creates a fresh theoretical iteration
- Allows comparison between framings
- Tracks which approaches were tried and abandoned

## Arguments

- `$ARGUMENTS` - Optional: "compare", "list", or a frame number to view

## Your Task

Create a new frame iteration or manage existing frames.

## Steps

### If no argument: Create new frame

1. **Read current state**

   Load `state.json` and check current frame number.

2. **Archive current frame's theoretical work**

   Move current frame's theory/lens/framing outputs to a frame-specific directory:

   ```
   analysis/
   ├── framing/
   │   ├── frame-1/           # Previous frame
   │   │   ├── PRIMARY_THEORY.md
   │   │   ├── SENSITIZING_LITERATURE.md
   │   │   ├── FRAMING_OPTIONS.md
   │   │   └── QUAL_EVIDENCE_REPORT.md
   │   └── frame-2/           # New frame (empty, ready to fill)
   ```

3. **Update state.json**

   ```json
   {
     "current_frame": 2,
     "frames": {
       "1": {
         "created_at": "2024-01-10T00:00:00Z",
         "archived_at": "2024-01-15T00:00:00Z",
         "theory": "Transaction Cost Economics",
         "lens": "Incomplete contracts",
         "framing": "Governance-centered",
         "status": "archived",
         "notes": "Abandoned - didn't explain heterogeneity well"
       },
       "2": {
         "created_at": "2024-01-15T00:00:00Z",
         "theory": null,
         "lens": null,
         "framing": null,
         "status": "active"
       }
     }
   }
   ```

4. **Prompt for frame notes**

   Ask the user:
   - Why are you shifting frames?
   - What was wrong with the previous framing?
   - Any initial direction for the new frame?

   Record in state.json and DECISION_LOG.md.

5. **Reset frame-dependent workflow steps**

   In state.json, reset to "pending":
   - find_theory
   - find_lens
   - mine_qual (for new mechanism evidence)
   - smith_frames
   - verify_claims
   - draft_paper

   Keep as-is:
   - explore_data (data doesn't change)
   - hunt_patterns (empirical findings don't change)

### If argument is "list": Show all frames

Display frame history:

```
## Frame History

| Frame | Theory | Lens | Status | Created | Notes |
|-------|--------|------|--------|---------|-------|
| 1 | TCE | Incomplete contracts | archived | 2024-01-10 | Didn't explain heterogeneity |
| 2 | Social capital | Network closure | archived | 2024-01-12 | Too narrow |
| 3 | Learning theory | Deliberate practice | active | 2024-01-15 | Current approach |

Currently on: Frame 3
```

### If argument is "compare": Compare frames

Generate a comparison of all frames:

```
## Frame Comparison

### Frame 1: Transaction Cost Economics
- **Core argument**: [X]
- **Explains pattern by**: [Y]
- **Weakness**: [Why abandoned]
- **Key citations**: [Z]

### Frame 2: Social Capital
- **Core argument**: [X]
- **Explains pattern by**: [Y]
- **Weakness**: [Why abandoned]
- **Key citations**: [Z]

### Frame 3: Learning Theory (current)
- **Core argument**: [X]
- **Explains pattern by**: [Y]
- **Status**: In progress
- **Key citations**: [Z]

## Recommendation

Based on the comparison, Frame 3 appears strongest because [reason].
Consider [suggestion].
```

### If argument is a number: View specific frame

Show details for that frame:

```
## Frame 2: Social Capital Approach

**Status**: Archived
**Created**: 2024-01-12
**Archived**: 2024-01-14

### Theory
Social capital theory (Nahapiet & Ghoshal, 1998)

### Lens
Network closure as enabling trust for knowledge transfer

### Why Abandoned
The pattern held regardless of network density—closure didn't explain the heterogeneity we observed.

### Files
- analysis/framing/frame-2/PRIMARY_THEORY.md
- analysis/framing/frame-2/SENSITIZING_LITERATURE.md
- analysis/framing/frame-2/FRAMING_OPTIONS.md
```

## Directory Structure After Multiple Frames

```
analysis/
├── exploration/              # Shared across frames
│   └── DATA_INVENTORY.md
├── patterns/                 # Shared across frames
│   └── PATTERN_REPORT.md
├── framing/
│   ├── frame-1/
│   │   ├── theory/
│   │   │   ├── PRIMARY_THEORY.md
│   │   │   └── SENSITIZING_LITERATURE.md
│   │   ├── qualitative/
│   │   │   └── QUAL_EVIDENCE_REPORT.md
│   │   ├── FRAMING_OPTIONS.md
│   │   └── FRAME_NOTES.md
│   ├── frame-2/
│   │   └── [same structure]
│   └── frame-3/              # Current
│       └── [in progress]
└── verification/             # Only for final frame
```

## Output

After creating new frame:

```
## Frame Shift Complete

Created Frame 3

Previous frame (Frame 2: Social Capital) has been archived.

### What's preserved:
- Data exploration (DATA_INVENTORY.md)
- Empirical patterns (PATTERN_REPORT.md)

### What's reset (ready for new approach):
- [ ] /find-theory - Select new theoretical anchor
- [ ] /find-lens - Find new sensitizing literature
- [ ] /mine-qual - Extract evidence for new mechanisms
- [ ] /smith-frames - Generate new framing options
- [ ] /verify-claims - Verify new claims
- [ ] /draft-paper - Generate new manuscript

### Next step
Run /find-theory to establish your new theoretical anchor.

Tip: Run /new-frame compare anytime to see all frames side-by-side.
```

## DECISION_LOG Entry

Automatically append to DECISION_LOG.md:

```markdown
## [Date]: Frame Shift to Frame N

- Previous frame: [name/theory]
- Reason for shift: [user's explanation]
- New direction: [initial thoughts]
- Preserved: Data exploration, empirical patterns
- Reset: Theory, lens, qualitative mining, framing, verification, draft
```
