# Rubric-Based Claim Scoring

Score each claim systematically before packaging using rubric-eval.

## Step 1: Check for rubric-eval

```bash
which rubric-eval
```

**If not found**: Proceed to ZIP packaging without scores, and note to user:
> "Install rubric-eval for per-claim quality scoring: `pip install rubric-eval`"

## Step 2: Prepare claims for evaluation

For each claim in the VERIFICATION_BRIEF.md, create a temporary text file containing:
- The claim statement
- The supporting evidence (quoted from evidence.jsonl)
- The counter-evidence (if any)
- The reasoning/analysis

Save to `analysis/verification/claims_for_rubric/CLM-XXX.txt`

## Step 3: Run rubric-eval

```bash
rubric-eval eval \
  analysis/verification/claims_for_rubric/ \
  rubrics/claim_verification.json \
  --type research_claim \
  --loader text \
  --runs 3 \
  --model claude-3-5-haiku-20241022
```

## Step 4: Review flagged claims

```bash
rubric-eval flagged 1
```

Claims with scores below 28/40 (70%) should be flagged for review. Check:
- **Evidentiary Support < 7/10**: Insufficient or weak evidence
- **Logical Soundness < 7/10**: Reasoning gaps or fallacies
- **Hedging Appropriateness < 7/10**: Over- or under-claiming
- **Counter-Evidence < 7/10**: Fails to address challenges

## Step 5: Export scores

```bash
rubric-eval export 1 --output analysis/verification/claim_scores.csv
```

## Step 6: Add to VERIFICATION_BRIEF.md

In the "Claims to Verify" section, add a "Rubric Score" field for each claim.

## Step 7: Report needs_review claims

If any claims score below 28/40, include them in the state.json warning:

```json
{
  "workflow": {
    "verify_claims": {
      "rubric_flagged_claims": ["CLM-003", "CLM-007"],
      "low_scoring_criteria": {
        "CLM-003": "evidentiary_support",
        "CLM-007": "hedging_appropriateness"
      }
    }
  }
}
```
