# /eval-becker - Becker Generalization Test

Run the Becker test (from "Tricks of the Trade" 1998) to evaluate whether a framing describes a generalizable social process or is locked to domain-specific description.

**Core Test:** Can you state your finding without domain-specific nouns?

## When to Run

- After `/smith-frames` generates framings
- Before `/audit-claims` or `/draft-paper`
- When uncertain if framing is "middle-range theory" vs. context-specific description

## State Management

**Requires:** `smith_frames.complete = true` in state.json
**Sets:** `eval_becker.complete = true` and `eval_becker.verdict` (PASS/CONDITIONAL/FAIL)

## Evaluation Steps

### Step 1: Domain-Noun Extraction

Identify all domain-specific nouns in the current framing:
- Setting nouns (hospital, operating room, clinic)
- Role nouns (surgeon, trainee, attending, nurse)
- Technology nouns (robot, console, da Vinci, laparoscope)
- Activity nouns (surgery, procedure, operation)

List them explicitly.

### Step 2: Abstract Reformulation

Restate the core finding replacing domain nouns with abstract equivalents:
- "surgeon" → "expert" or "skilled practitioner"
- "trainee" → "peripheral participant" or "learner"
- "operating room" → "work setting" or "task environment"
- "dual console" → "technology configuration" or "resource arrangement"
- "surgery" → "complex collaborative task"

Write the abstracted claim.

### Step 3: Generalization Check

Evaluate if the abstracted claim describes a **social process** (generalizable) or a **domain fact** (specific):

**Social process indicators:**
- Describes relationships between categories of actors
- Identifies mechanisms that could operate elsewhere
- References resource arrangements, role structures, or coordination patterns

**Domain fact indicators:**
- Only makes sense with original nouns restored
- Describes a unique property of this setting
- No clear mechanism that transfers

### Step 4: Domain Transfer Test

Attempt to apply the abstracted finding to 3+ unrelated domains:
- Manufacturing/factory work
- Software development
- Restaurant/food service
- Air traffic control
- Architecture/design firms
- Legal practice
- Teaching/education

For each domain: Does the finding produce a testable, non-trivial prediction?

### Step 5: Theory Connection

Link the abstracted claim to existing middle-range theory:
- Coordination theory (Thompson, Galbraith)
- Communities of practice (Lave & Wenger)
- Process loss/gain (Steiner)
- Technology affordances (Leonardi, Gibson)
- Role theory (Biddle, Katz & Kahn)

Does it extend, qualify, or challenge existing theory?

## Verdict Logic

| Verdict | Criteria |
|---------|----------|
| ✓ **PASS** | Abstraction successful + 3+ transfer domains work + connects to theory |
| ⚠️ **CONDITIONAL** | Abstraction works but domain transfer limited OR theory connection unclear |
| ✗ **FAIL** | Cannot abstract without domain nouns OR only applies to original context |

## Output Format

Create `analysis/framing/BECKER_EVAL.md`:

```markdown
# Becker Generalization Test Results

## Verdict: [PASS/CONDITIONAL/FAIL]

## Step 1: Domain Nouns Identified
- [list]

## Step 2: Abstract Reformulation
**Original:** [domain-specific claim]
**Abstracted:** [generalized claim]

## Step 3: Generalization Assessment
[Social process or domain fact? Why?]

## Step 4: Domain Transfer Results
| Domain | Prediction | Viable? |
|--------|------------|---------|
| ... | ... | ✓/✗ |

## Step 5: Theory Connections
[Which theories does this extend/qualify?]

## Recommendations
[If CONDITIONAL/FAIL: specific suggestions for re-framing]
```

## Common Failure Modes

1. **Noun-swapping without mechanism**: Replacing "surgeon" with "expert" but the claim only works for surgeons
2. **False generality**: Abstraction so vague it's unfalsifiable ("technology affects work")
3. **Single-domain lock**: Finding genuinely unique to medical/surgical context
4. **Missing the mechanism**: Abstract nouns present but no causal process articulated

## Example Application

**Original framing:** "Dual-console robotic systems reduce trainee-associated time costs by enabling productive observer roles"

**Domain nouns:** dual-console, robotic, trainee, surgery (implied)

**Abstracted:** "Technology configurations that create productive peripheral participant roles reduce the coordination costs of adding learners to complex collaborative tasks"

**Transfer test:**
- Software dev: Pair programming stations → junior dev can observe/assist without blocking senior
- ATC: Dual-screen setups → trainee monitors while expert handles traffic
- Restaurants: Expo stations → trainee can expedite without slowing line cook

**Verdict:** PASS - describes how technology-enabled role structures mediate learning costs across settings

## Reference

Becker, Howard S. 1998. *Tricks of the Trade: How to Think About Your Research While You're Doing It.* Chicago: University of Chicago Press. Chapter 3: "Concepts."

---

## Consensus Mode

Check `state.json` → `consensus.enabled` (default: true).

If enabled and `--quick` not specified:
1. Run this evaluation 5 times (default: 5, configurable via `/consensus-config`)
2. For each scored criterion: compute mean, SD, 95% CI, CV across runs
3. For overall verdict: compute agreement rate across runs
4. Include stability assessment using `lib/consensus/` formatters:
   - 🟢 HIGH: CV < 10% or agreement ≥ 90%
   - 🟡 MEDIUM: CV 10-25% or agreement 70-89%
   - 🔴 LOW: CV > 25% or agreement < 70%
5. Persist consensus stats in eval_results (see State Persistence below)

If `--quick` flag is set: Run once, skip consensus, still persist results.

---

## Staleness Check

Before running this evaluation:
1. Read `state.json` → `eval_results.becker.frame_[current_frame].latest`
2. If a previous result exists:
   a. Compute current SHA-256 of upstream files:
      ```bash
      shasum -a 256 analysis/framing/frame-[N]/FRAMING_OPTIONS.md | cut -d' ' -f1
      ```
   b. Compare against stored `upstream_checksums`
   c. If ALL match: "Previous results are current (ran [timestamp]). Re-run anyway? [Y/n]"
   d. If ANY differ: "Upstream files changed since last eval. Running fresh evaluation."
3. If no previous result exists: proceed with evaluation.

---

## State Persistence

In addition to the workflow state updates above (`eval_becker.complete` and `eval_becker.verdict`), also persist to eval_results for the test suite:

After evaluation completes:
1. Read `state.json`
2. Compute SHA-256 checksums of upstream files:
   - `analysis/framing/frame-[N]/FRAMING_OPTIONS.md`
3. Write to `eval_results.becker.frame_[current_frame].latest`:
   ```json
   {
     "timestamp": "[current ISO timestamp]",
     "scores": {
       "concepts_clarity": N,
       "abstraction_level": N,
       "theoretical_utility": N
     },
     "total": null,
     "max_total": null,
     "verdict": "[PASS|CONDITIONAL|FAIL]",
     "consensus": {
       "n_runs": 5,
       "stability": "[HIGH|MEDIUM|LOW]",
       "cv": [computed CV],
       "ci_lower": [lower bound],
       "ci_upper": [upper bound]
     },
     "stale": false,
     "stale_reason": null,
     "upstream_checksums": {
       "analysis/framing/frame-[N]/FRAMING_OPTIONS.md": "sha256:[hash]"
     },
     "output_file": "analysis/framing/BECKER_EVAL.md"
   }
   ```
4. Update `updated_at` timestamp
5. Log to `DECISION_LOG.md`: "becker — [verdict]"
