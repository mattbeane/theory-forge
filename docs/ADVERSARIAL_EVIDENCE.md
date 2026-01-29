# Adversarial Evidence: A Standard Feature

**This is not a student mode feature. This is how theory-forge works by default.**

---

## Why Adversarial Evidence Is Standard

Reviewers are adversarial. They look for:
- Evidence you ignored
- Alternative interpretations you didn't consider
- Boundary conditions you didn't test
- Claims that outrun your data

If you don't find these problems first, they will. Better to address them proactively than to get desk-rejected.

Theory-forge is designed to make cherry-picking harder, not easier.

---

## Where Adversarial Evidence Appears

### `/hunt-patterns`
- Tests patterns against controls (things that could explain away the effect)
- Documents "killed findings" (patterns that didn't survive)
- Flags heterogeneity (effect varies by subgroup—could be a boundary condition)

### `/mine-qual`
- Requires disconfirming evidence section
- Asks: "What would challenge this claim?"
- Searches for informants who experienced the opposite
- Documents "Challenging evidence" alongside "Supporting evidence"

### `/audit-claims`
- **Explicitly adversarial agent**
- Searches ALL raw data for evidence supporting AND challenging each claim
- Flags claims where challenging evidence outweighs support
- Identifies alternative interpretations the data supports
- Documents evidence distribution by role/site (are you only hearing from managers?)

### `/smith-frames`
- For each framing option:
  - Counter-evidence that challenges the frame
  - Alternative interpretations that could explain the same pattern
  - Boundary conditions where the frame wouldn't apply
  - "Weakest claim" — which part is most vulnerable?
  - "Survivability" rating — can this frame survive a hostile R2?

### `/verify-claims`
- Creates package for EXTERNAL (different AI or human) adversarial review
- Documents "Alternative Interpretations" section
- Documents "Specification Choices" that could be questioned
- Documents "Data Limitations"

---

## The Philosophy

**Your analysis is a hypothesis, not a conclusion.**

Every claim you make could be wrong. Every interpretation could have alternatives. Every finding could be a boundary condition away from irrelevance.

Good scholarship means:
1. Finding the problems before reviewers do
2. Addressing them in the paper (not hiding them)
3. Being honest about what the data can and can't support

Theory-forge encodes this into the workflow. You can't skip to `/draft-paper` without `/audit-claims`. You can't run `/verify-claims` without documenting alternative interpretations.

---

## What "Adversarial" Doesn't Mean

It doesn't mean:
- Destroying your own argument
- Finding so many problems you can't publish
- Paralyzing yourself with doubt

It means:
- Being honest about the strength of your evidence
- Addressing obvious objections before they're raised
- Hedging claims appropriately (not overclaiming)
- Building a defensible argument, not a brittle one

---

## Example: Good vs. Bad Practice

**Bad (cherry-picking)**:
1. Find quantitative pattern
2. Ask AI to find supporting qual quotes
3. Put quotes in paper
4. Claim qual "confirms" quant finding

**Good (adversarial)**:
1. Find quantitative pattern
2. Search ALL qual data for evidence about this pattern
3. Document supporting AND challenging evidence
4. Note that challenging evidence comes from [specific context]
5. Add boundary condition: "This pattern holds for X but not Y"
6. Claim qual "illuminates" quant finding while noting where it diverges

---

## Integration with Consensus Mode

When consensus mode is enabled, adversarial evidence gets statistical teeth:

- **Quote stability**: If a supporting quote only appears in 30% of extraction runs, it might be cherry-picked
- **Claim defensibility**: If claim direction varies across runs, it's not robust
- **Effect variance**: If effect size varies >25% across runs, something is ambiguous

Single-run analysis can confirm your biases. Multi-run analysis with stability metrics makes cherry-picking visible.

---

## Related Commands

- `/audit-claims` — Primary adversarial evidence generation
- `/mine-qual` — Mechanism evidence with disconfirming search
- `/smith-frames` — Framing evaluation with adversarial checks
- `/verify-claims` — External verification package with alternatives documented
- `/consensus-config` — Enable statistical adversarial checks
