---
name: verify-claims
description: Create a self-contained verification package that can be sent to a DIFFERENT AI system or skeptical colleague for adversarial review
---

# Claims Verifier

You are the VERIFIER agent. Your job is to create a self-contained verification package that can be sent to a DIFFERENT AI system or skeptical colleague for adversarial review.

## Prerequisites

- `workflow.hunt_patterns.status === "completed"`
- `workflow.smith_frames.status === "completed"`
- `workflow.audit_claims.status === "completed"` — **REQUIRED, non-negotiable**

**CRITICAL**: If `audit_claims` has not been run, STOP immediately:

```
STOP: You must run /audit-claims before /verify-claims.

The audit step searches your RAW DATA for evidence that supports AND challenges
each claim. Without this step, verification is meaningless — you're just checking
that the analysis is internally consistent, not that it's grounded in evidence.
```

If `audit_claims.high_concern_claims` is not empty, warn the user but proceed.

For full state management protocol, see [../../_shared/state-management.md](../../_shared/state-management.md)

## Why This Matters

The AI that helped you build the analysis shouldn't be the only one checking it. Verification by a different system (or human) catches coding errors, specification mistakes, logical gaps, alternative interpretations, and overclaims.

## Inputs You Need

- `analysis/patterns/PATTERN_REPORT.md`
- `analysis/framing/FRAMING_OPTIONS.md` (the chosen framing)
- All analysis code used to generate findings
- Access to data files (or clear descriptions)

## Steps

1. **Extract all quantitative claims** — Go through the pattern report and framing. List every claim involving a number: effect sizes, sample sizes, p-values, percentages, counts.

2. **For each claim, document**: the exact statement, expected value, data source, and analysis code that produces it.

3. **Write verification code** — Standalone code for each claim that loads data, runs the analysis, prints verifiable results. Must be runnable by someone with no context.

4. **Document robustness checks** — What was tested, results, and what wasn't tested (and why).

5. **Flag potential concerns** — Be honest about specification choices, alternative interpretations, data limitations, assumptions.

6. **Create the verification brief** — See [output-template.md](output-template.md) for the full template.

7. **Score claims with rubric-eval** (if available) — See [rubric-scoring.md](rubric-scoring.md) for the rubric-based scoring workflow.

8. **Run Living Paper integration** — See [living-paper.md](living-paper.md) for automated claim-evidence traceability.

9. **Package everything** into a self-contained ZIP.

## Create the ZIP Package

**CRITICAL: The package MUST be self-contained.** An external reviewer (AI or human) must be able to verify claims WITHOUT access to anything outside the ZIP file. DO NOT ask the user whether to include data — just include it.

### Required Package Contents

```
analysis/verification/
├── README_REVIEWER.md         — Instructions for external reviewer
├── VERIFICATION_BRIEF.md      — All claims with verification logic
├── DATA_DESCRIPTOR.md         — Variable definitions
├── data/                      — ACTUAL DATA FILES (not symlinks)
│   ├── case_timing.xlsx       — Quantitative data (copy, not link)
│   └── [other data files]
├── code/                      — Analysis code (if exists)
│   └── analysis.py            — Reproducible analysis script
├── evidence/                  — Qualitative evidence
│   └── key_quotes.md          — Anonymized quotes with source refs
└── REVIEW_PACKAGE.zip         — Final package
```

### Mandatory Steps (DO NOT SKIP)

1. **Copy actual data files** into `analysis/verification/data/` — no symlinks
2. **Include or create analysis code** — must be runnable with only the included data
3. **Extract key qualitative evidence** — anonymized quotes to `evidence/key_quotes.md`
4. **Create README_REVIEWER.md** with contents, how to verify, questions for reviewer
5. **Create the ZIP**:
   ```bash
   cd analysis/verification
   zip -r REVIEW_PACKAGE.zip README_REVIEWER.md VERIFICATION_BRIEF.md DATA_DESCRIPTOR.md data/ code/ evidence/
   ```

**If you find yourself about to ask "should I include X?" — the answer is YES.**

## After You're Done

Report to the user:

1. **Verification package ready**: ZIP location and Living Paper reviewer package location
2. **Summary statistics**: claim count, evidence counts (supporting vs challenging), HIGH CONCERN claims, defensibility ratings (if consensus)
3. **Living Paper status**: whether `lp lint` passed, reviewer package generated
4. **Next steps**: Send package to a DIFFERENT AI or skeptical colleague, then run `/draft-paper`

**IMPORTANT**: The system that built the analysis should NOT be the only verifier.

For consensus mode behavior, see [../../_shared/consensus-mode.md](../../_shared/consensus-mode.md)
For staleness detection, see [../../_shared/staleness-check.md](../../_shared/staleness-check.md)
For eval result persistence, see [../../_shared/eval-persistence.md](../../_shared/eval-persistence.md)

### Skill-Specific Persistence

- **eval_results key**: `claim_verification`
- **Upstream files**: `analysis/audit/claims.jsonl`, `evidence.jsonl`, `links.csv`
- **Scores**: `claims_defensible`, `claims_mostly_defensible`, `claims_not_defensible`
- **Verdict**: PASS if all claims defensible/mostly; FAIL if any not defensible
- **Default consensus N**: 10 (higher than other evals — this is the final verification gate)

### Deprecated Approach

The old manual evidence generation approach is preserved in [deprecated.md](deprecated.md) for historical reference. Do not use it.
