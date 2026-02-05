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

## Gate B: Mechanism Evidence (after /mine-qual)

### Failure: No STRONG mechanism support

```
⛔ GATE B FAILED: Mechanism evidence insufficient

What happened:
  The qualitative evidence doesn't provide STRONG support for any mechanism.
  This means either:
  • The mechanism is plausible but not well-documented in your data
  • You have evidence but it's ambiguous or conflicting
  • The mechanism you're looking for isn't what's actually operating

What to do next:

  Option 1: Return to the data
    → Re-read transcripts looking specifically for HOW things happen
    → Mechanisms are about process, not just outcomes
    → Look for sequences: "First X, then Y, which caused Z"

  Option 2: Consider alternative mechanisms
    → Maybe the pattern is real but your explanation is wrong
    → What else could produce the pattern you see?
    → Run /mine-qual with different mechanism hypotheses

  Option 3: Document disconfirming evidence better
    → Sometimes mechanism support looks weak because you haven't
      accounted for cases where it doesn't operate
    → Bounded mechanisms ("X happens when Y is present") can be strong

  Option 4: Collect more qualitative data
    → If you have quant patterns but thin qual, more interviews may help
    → Targeted sampling toward mechanism illumination

What STRONG mechanism evidence looks like:
  • Multiple informants describing the same process independently
  • Observed sequences that match the theorized mechanism
  • Informants' own causal language ("I did X because Y")
  • Evidence of the mechanism NOT operating in negative cases

To retry: Run /mine-qual again after making changes
```

### Failure: Disconfirming evidence not documented

```
⛔ GATE B FAILED: No disconfirming evidence documented

What happened:
  You haven't documented any evidence that challenges your interpretation.
  This is a red flag—every mechanism has boundary conditions.

What to do next:

  You MUST find disconfirming evidence. This isn't optional.

  Look for:
  • Cases where the pattern didn't hold
  • Informants who described different processes
  • Times when the mechanism failed or backfired
  • Alternative explanations informants offered

  If you genuinely can't find any disconfirming evidence, ask:
  • Did you look hard enough? (Confirmation bias is real)
  • Is your sample too homogeneous?
  • Are you defining the mechanism too loosely?

Why this matters:
  Reviewers WILL ask about disconfirming evidence. If you don't address
  it proactively, they'll assume you're hiding something or didn't do
  rigorous analysis. Papers without disconfirming evidence discussion
  rarely survive review.

To retry: Run /mine-qual again and specifically hunt for challenges
```

---

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

## Gate D: Evaluations (after /eval-zuckerman, /eval-becker, /eval-genre)

### Failure: Zuckerman < 7/10

```
⛔ GATE D FAILED: Zuckerman evaluation below threshold

Score: [X]/10 (need 7+)

Failed criteria:
  [List specific criteria that failed]

What each means:

  1. THE PUZZLE - Is there a clear, interesting puzzle?
     Fix: Sharpen the "why is this surprising?" in your intro

  2. THE CANONICAL NULL - Is the conventional explanation clear?
     Fix: State what people currently believe and why it's wrong

  3. THE MECHANISM - Do you explain HOW, not just WHAT?
     Fix: Strengthen /mine-qual evidence, show the process

  4. THE CONTRIBUTION - Is it clear what we learn?
     Fix: Be explicit about the theoretical advance

  5. COLUMN CHOICE - Are you targeting the right literature?
     Fix: Reconsider /find-lens, maybe different positioning

  [Continue for all 10 criteria...]

To retry: Fix the specific issues, then run /eval-zuckerman again
```

### Failure: Becker FAIL

```
⛔ GATE D FAILED: Becker generalization test failed

What happened:
  Your finding cannot be stated without domain-specific nouns.
  This suggests the contribution is too narrow—it's about your
  specific context rather than a generalizable mechanism.

The Becker test:
  "Can you state your finding using only abstract, domain-neutral terms?"

Your finding (current):
  [Show current domain-specific statement]

What to do:

  1. Identify what's really generalizable
     → Strip away the context: What's the MECHANISM?
     → "Hospitals do X" → "Organizations facing Y do X"

  2. Reframe around the mechanism, not the setting
     → The setting is evidence, not the contribution
     → You studied hospitals, but what does it say about ORGANIZATIONS?

  3. Consider if you're overclaiming
     → Maybe it IS just about hospitals
     → That's OK—just target different journals

Examples of abstraction:
  Specific: "Surgical trainees learn through shadow practices"
  Abstract: "When technology excludes novices from legitimate participation,
            they develop norm-challenging alternatives"

To retry: Revise your core claim, then run /eval-becker again
```

### Failure: Genre FAIL

```
⛔ GATE D FAILED: Genre mismatch detected

What happened:
  Your paper uses hypothesis-testing language for discovery research
  (or vice versa). This mismatch will confuse reviewers.

Problems found:
  [List specific language violations]

Discovery papers (ASQ, Org Science for inductive work):
  ✓ "I observed that..."
  ✓ "The data revealed..."
  ✓ "This led me to see..."
  ✗ "I hypothesize that..."
  ✗ "H1: X leads to Y"
  ✗ "Results support our prediction"

Testing papers (AMJ, Management Science):
  ✓ "Theory predicts that..."
  ✓ "H1 was supported"
  ✓ "We find evidence consistent with..."
  ✗ "I came to understand..."
  ✗ "The mechanism emerged from..."

What to do:

  If your research was INDUCTIVE (you discovered things):
    → Remove all hypothesis language
    → Rename "Hypothesis Development" → "Analytical Framework"
    → Use past tense discovery verbs
    → Frame theory as lens, not source of predictions

  If your research was DEDUCTIVE (you tested predictions):
    → Make hypotheses explicit
    → Show clear prediction → test → result logic
    → Target journals that expect this

Specific fixes needed:
  [List each problematic passage with suggested revision]

To retry: Fix the language issues, then run /eval-genre again
```

---

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

## Gate F: Quality (after /eval-limitations, /eval-citations)

### Failure: Limitations section

```
⛔ GATE F FAILED: Limitations section needs revision

Issues found:
  [Specific problems]

Common problems:

  TOO LONG (>400 words):
    → You're over-disclosing
    → Reviewers read long limitations as lack of confidence
    → Consolidate to 2 paragraphs max

  ENUMERATED CONFESSIONS:
    → Don't list limitations as numbered bullets
    → This emphasizes weaknesses
    → Write in flowing prose that addresses and moves on

  MISSING GENERALIZABILITY:
    → Second paragraph should discuss where findings apply
    → "These dynamics may operate wherever..."

Suggested structure:
  Paragraph 1 (~150 words): Core limitations and how addressed
  Paragraph 2 (~150 words): Generalizability scope and future research

To retry: Revise limitations section, then run /eval-limitations again
```

### Failure: Citation coverage

```
⛔ GATE F FAILED: Citation coverage below minimum

Current count: [X] citations
Target minimum: [Y] citations (for [Journal])

Issues found:
  [List missing canonical works]
  [List underrepresented areas]

What to do:

  1. Add canonical works you're missing
     [List specific suggestions]

  2. Strengthen literature coverage in:
     [List weak areas]

  3. Don't pad—add relevant citations only
     → Each citation should earn its place
     → But major literatures need representation

Journal benchmarks:
  Organization Science: 50-100 citations
  ASQ: 60-120 citations
  AMJ: 80-150 citations
  Management Science: 40-80 citations

To retry: Add citations, then run /eval-citations again
```

---

## Usage Notes

When a gate fails:

1. Show the appropriate template above
2. Fill in specific details from the actual evaluation
3. Be direct about what failed and why
4. Provide concrete next steps
5. Link to the retry command

Never let users proceed past a failed gate without explicit override.
Overrides must be logged in DECISION_LOG.md with justification.
