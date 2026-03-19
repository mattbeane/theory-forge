---
name: gate-failure-templates
description: Gate Failure Templates
---

# Gate Failure Templates

This document provides standardized failure messages for each gate. When a gate fails, use these templates to give users actionable guidance.

---

## Gate A: Pattern Robustness (after /hunt-patterns)

### Failure: No HIGH confidence patterns

```
⛔ GATE A FAILED: No robust patterns found

What happened:
  The pattern analysis didn't find any patterns with HIGH confidence.
  This means either:
  • The patterns in your data are too weak or noisy
  • The data needs more exploration before patterns emerge
  • There may not be a paper here (yet)

What to do next:

  Option 1: Dig deeper
    → Run /explore-data again with different slices
    → Look at subgroups, time periods, or contexts separately
    → Sometimes patterns are strong in subsets but wash out overall

  Option 2: Get more data
    → If patterns are borderline, more observations may clarify
    → Consider whether you have enough variation to see anything

  Option 3: Reframe what you're looking for
    → Maybe the interesting finding is the ABSENCE of a pattern
    → "Why doesn't X predict Y when theory says it should?"

  Option 4: Accept this isn't ready
    → Not every dataset yields a paper
    → Better to know now than after drafting

To retry: Run /hunt-patterns again after making changes

Common mistake: Forcing a pattern that isn't really there. If you find
yourself arguing with the analysis, step back and ask: "Would a skeptical
reviewer find this convincing?"
```

---

For gate b: mechanism evidence failure templates, see [gate-b.md](gate-b.md)


## Gate C: Framing Selection (after /smith-frames)

### Failure: No HIGH robustness framing

```
⛔ GATE C FAILED: No robust framing available

What happened:
  None of the generated framings have HIGH robustness ratings.
  This means the evidence doesn't strongly support any particular
  theoretical positioning.

What to do next:

  Option 1: Generate more framings
    → Run /smith-frames again with different theoretical hooks
    → Consider adjacent literatures you haven't explored

  Option 2: Strengthen your evidence base
    → Return to /mine-qual and look for more mechanism support
    → The framing can only be as strong as the evidence behind it

  Option 3: Lower your sights (temporarily)
    → Maybe this is a MEDIUM-robustness paper right now
    → You can still write it, but hedge claims appropriately
    → Come back with more data later

  Option 4: Reconsider the pattern
    → If no framing works, maybe the pattern isn't what you think
    → Return to /hunt-patterns with fresh eyes

What makes a framing robust:
  • Clear mechanism with strong evidence
  • Well-defined contribution to specific literature
  • Defensible positioning (not overclaiming)
  • Evidence addresses obvious objections

To retry: Run /smith-frames again or strengthen evidence first
```

---

For gate d: evaluations failure templates, see [gate-d.md](gate-d.md)


## Gate E: Verification (after /audit-claims, /verify-claims)

### Failure: HIGH concern claims

```
⛔ GATE E FAILED: Claims with insufficient evidence

Claims flagged as HIGH concern:
  [List claims with their issues]

For each claim, the problem is one of:

  UNSUPPORTED - No evidence links to this claim
    → Either find evidence or remove the claim

  CONTRADICTED - Evidence actively challenges this claim
    → Address the contradiction explicitly or revise claim

  OVERSTATED - Claim is stronger than evidence supports
    → Add hedging language or strengthen evidence

What to do:

  1. For each HIGH concern claim:
     → Can you find evidence you missed? Re-run /audit-claims
     → Can you weaken the claim to match evidence?
     → Should you remove the claim entirely?

  2. Create verification package
     → Ensure each claim has at least 3 supporting pieces of evidence
     → Document how you addressed disconfirming evidence

Why this matters:
  Theory-building papers live or die on claim-evidence fit.
  Reviewers will check your claims against your data.
  Better to find the gaps now than in a rejection letter.

To retry: Fix claims or find more evidence, then run /verify-claims again
```

---

For gate f: quality failure templates, see [gate-f.md](gate-f.md)


## Usage Notes

When a gate fails:

1. Show the appropriate template above
2. Fill in specific details from the actual evaluation
3. Be direct about what failed and why
4. Provide concrete next steps
5. Link to the retry command

Never let users proceed past a failed gate without explicit override.
Overrides must be logged in DECISION_LOG.md with justification.
