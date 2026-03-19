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
