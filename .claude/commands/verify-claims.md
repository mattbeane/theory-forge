# Claims Verifier

You are the VERIFIER agent. Your job is to create a self-contained verification package that can be sent to a DIFFERENT AI system or skeptical colleague for adversarial review.

## State Management

Before starting:
1. Check for `state.json` in project root
2. Verify prerequisites:
   - `workflow.hunt_patterns.status === "completed"`
   - `workflow.smith_frames.status === "completed"`
   - `workflow.audit_claims.status === "completed"` ← **REQUIRED**
3. Check current frame number for context

**CRITICAL**: If `audit_claims` has not been run, STOP and tell the user:

```
STOP: You must run /audit-claims before /verify-claims.

The audit step searches your RAW DATA for evidence that supports AND challenges
each claim. Without this step, verification is meaningless—you're just checking
that the analysis is internally consistent, not that it's grounded in evidence.

Run: /audit-claims

This will:
1. Search all interview transcripts for relevant evidence
2. Identify supporting AND challenging evidence
3. Flag claims with weak or contested support
4. Generate the evidence files needed for living paper verification
```

If `audit_claims.high_concern_claims` is not empty, warn:
```
WARNING: The audit found HIGH CONCERN claims that may need revision:
[List the claims]

Proceeding with verification, but these claims should be addressed.
```

After completing:
1. Update `state.json`:
   - Set `workflow.verify_claims.status` to "completed"
   - Set `workflow.verify_claims.completed_at` to current ISO timestamp
   - Add output file paths to `workflow.verify_claims.outputs`
   - Update `updated_at` timestamp
2. Append entry to `DECISION_LOG.md`

## Why This Matters

The AI that helped you build the analysis shouldn't be the only one checking it. Verification by a different system (or human) catches:
- Coding errors
- Specification mistakes
- Logical gaps
- Alternative interpretations
- Overclaims

## Critical: This Produces a Package for External Review

Your output is a ZIP file the user will send ELSEWHERE. It must be:
- Self-contained (all code, data references, claims in one place)
- Clear to someone with no context
- Structured for systematic verification

## Inputs You Need

- `analysis/patterns/PATTERN_REPORT.md`
- `analysis/framing/FRAMING_OPTIONS.md` (the chosen framing)
- All analysis code used to generate findings
- Access to data files (or clear descriptions)

## Steps

1. **Extract all quantitative claims**

   Go through the pattern report and framing. List every claim that involves a number:
   - Effect sizes (β, OR, differences)
   - Sample sizes
   - Statistical significance (p-values)
   - Percentages, counts

2. **For each claim, document**:
   - The exact statement
   - The expected value
   - The data source
   - The analysis code that produces it

3. **Write verification code**

   For each claim, write standalone code that:
   - Loads the required data
   - Runs the exact analysis
   - Prints the result in a verifiable format
   - Can be run by someone with no context

4. **Document robustness checks**

   List all robustness checks that were run:
   - What was tested
   - What the result was
   - What wasn't tested (and why)

5. **Flag potential concerns**

   Be honest about:
   - Specification choices that could be questioned
   - Alternative interpretations
   - Limitations of the data
   - What you're assuming

6. **Create the verification brief**

   A markdown document that a reviewer can work through systematically.

7. **Package everything**

   Create a ZIP file containing:
   - VERIFICATION_BRIEF.md
   - All analysis code
   - Data descriptor (or data if shareable)
   - README with instructions

## Output Format

Create `analysis/verification/VERIFICATION_BRIEF.md`:

```markdown
# Verification Brief

**Paper**: [Working title]
**Date**: [Date]
**Prepared by**: [AI system used]
**For review by**: [External AI or colleague]

---

## Instructions for Reviewer

This package contains all claims, code, and data references needed to verify the quantitative findings. Please:

1. Check each claim against the provided code
2. Run the code if possible and confirm outputs match
3. Flag any concerns about specification, interpretation, or robustness
4. Note alternative interpretations you would consider

---

## Claims to Verify

### Claim 1: [Short description]

**Statement**: "[Exact claim as it will appear in paper]"

**Expected value**: [e.g., β = 0.21, p < 0.001]

**Data source**: [Filename, relevant variables]

**Verification code**:

```python
# Self-contained code to reproduce this claim
import pandas as pd
# ... [full code]
print(f"Result: {result}")  # Should print: [expected]
```

**Robustness**:
- [x] Survives control for [X]
- [x] Survives control for [Y]
- [ ] NOT tested: [Z] because [reason]

**Potential concerns**: [Any issues to flag]

---

### Claim 2: [Short description]

[Same structure]

---

[Repeat for all claims]

---

## Robustness Summary

| Claim | Base Result | With [Control A] | With [Control B] | Concern Level |
|-------|-------------|------------------|------------------|---------------|
| 1 | β=X | β=X | β=X | Low |
| 2 | ... | ... | ... | ... |

---

## Specification Choices

Decisions that could be questioned:

1. **[Choice]**: We chose [X] instead of [Y] because [reason]
2. **[Choice]**: We chose [X] instead of [Y] because [reason]

---

## Alternative Interpretations

Interpretations a skeptic might raise:

1. **[Alternative]**: [Description]
   - Our response: [How we address this]

2. **[Alternative]**: [Description]
   - Our response: [How we address this]

---

## Data Limitations

1. [Limitation]
2. [Limitation]

---

## Questions for Reviewer

1. [Specific question about analysis]
2. [Specific question about interpretation]

---

## Package Contents

- `VERIFICATION_BRIEF.md` (this file)
- `verification_code.py` (all analysis code)
- `DATA_DESCRIPTOR.md` (variable definitions)
- [Other files]
```

## Create the ZIP Package

After creating the brief, package everything:

```
analysis/verification/
├── VERIFICATION_BRIEF.md
├── verification_code.py
├── DATA_DESCRIPTOR.md
└── VERIFICATION_PACKAGE.zip  ← Create this
```

## Living Paper Integration (Automated)

The `/audit-claims` step has already generated Living Paper-compatible files:
- `analysis/audit/claims.jsonl`
- `analysis/audit/evidence.jsonl`
- `analysis/audit/links.csv`

**You MUST run these commands automatically** (do not just tell the user to do it):

### Step 1: Copy audit files to verification directory

```bash
cp analysis/audit/claims.jsonl analysis/verification/
cp analysis/audit/evidence.jsonl analysis/verification/
cp analysis/audit/links.csv analysis/verification/
```

### Step 2: Initialize Living Paper (if not already done)

```bash
python3 living_paper/lp.py init
```

### Step 3: Ingest into Living Paper database

```bash
python3 living_paper/lp.py ingest \
  --claims analysis/verification/claims.jsonl \
  --evidence analysis/verification/evidence.jsonl \
  --links analysis/verification/links.csv
```

### Step 4: Run lint to verify traceability

```bash
python3 living_paper/lp.py lint
```

If lint fails, fix the issues before proceeding.

### Step 5: Generate reviewer package

Get the paper_id from the claims file (first line's paper_id field), then:

```bash
python3 living_paper/lp.py export-package --paper [PAPER_ID] --out analysis/verification/reviewer_package
```

This creates a folder reviewers can open directly—no CLI required on their end.

**DO NOT regenerate claims/evidence from the manuscript**. The audit files contain evidence found by searching raw data, including challenging evidence. Regenerating from the manuscript would lose this.

### If audit files don't exist

If for some reason audit files don't exist, STOP and run `/audit-claims` first. Do not proceed with verification without raw data grounding.

---

## DEPRECATED: Manual Generation (DO NOT USE)

The following section describes the OLD approach of generating evidence from manuscripts.
**This approach is deprecated because it produces circular verification.**

### ~~Generate `analysis/verification/claims.jsonl`~~

~~One JSON object per line. For each substantive claim in the paper:~~

```json
{"claim_id": "CLM-001", "paper_id": "PAPER_ID", "claim_type": "mechanism", "text": "The exact claim text", "status": "draft", "verification_mode": "public_provenance", "frame_id": "FRAME-N"}
```

**claim_type** values:
- `descriptive` — what happened (empirical pattern)
- `mechanism` — how/why it happens
- `boundary_condition` — when/for whom it holds
- `measurement` — how a construct is operationalized
- `process` — methodological choices

**verification_mode** values:
- `public_provenance` — metadata can be public
- `controlled_access` — requires DUA for verification
- `witness_only` — only witness can verify

### Generate `analysis/verification/evidence.jsonl`

One JSON object per line. For each piece of supporting/challenging evidence:

```json
{"evidence_id": "EVD-001", "paper_id": "PAPER_ID", "evidence_type": "quote", "summary": "Safe paraphrase of the evidence (no PII)", "sensitivity_tier": "PUBLIC", "meta": {"interview_id": "INT_XXX", "informant_role_bin": "manager", "informant_tenure_bin": "5y+", "site_bin": "SITE_A", "line_start": 234, "line_end": 238, "mechanism_hypothesis": "H1_name", "evidence_type": "supporting"}}
```

**evidence_type** values: `quote`, `fieldnote`, `observation`, `quant_output`, `other`

**sensitivity_tier** values: `PUBLIC`, `CONTROLLED`, `WITNESS_ONLY`

**meta fields** (for qual evidence):
- `interview_id` — hashed/pseudonymized interview identifier
- `informant_role_bin` — binned role category (not specific title)
- `informant_tenure_bin` — binned tenure (e.g., "<1y", "1-5y", "5y+")
- `site_bin` — site identifier if multiple sites
- `line_start`, `line_end` — location in source document
- `mechanism_hypothesis` — which mechanism this evidence relates to
- `evidence_type` — "supporting" or "challenging"

**Important**: Bin rare categories to prevent re-identification. If only one HR director was interviewed, use a broader role bin.

### Generate `analysis/verification/links.csv`

```csv
claim_id,evidence_id,relation,weight,note
CLM-001,EVD-001,supports,1.0,
CLM-001,EVD-002,challenges,1.0,
```

**relation** values: `supports`, `challenges`, `illustrates`

### After generating these files

Run the living paper linter to verify traceability:

```bash
python3 living_paper/lp.py init  # if not already initialized
python3 living_paper/lp.py ingest --claims analysis/verification/claims.jsonl --evidence analysis/verification/evidence.jsonl --links analysis/verification/links.csv
python3 living_paper/lp.py lint
```

If lint passes, the claim-evidence graph is complete. If it fails, it will tell you which claims lack evidence.

---

## After You're Done

Report to the user:

1. **Verification package ready**:
   - ZIP file location: `analysis/verification/VERIFICATION_PACKAGE.zip`
   - Living Paper reviewer package: `analysis/verification/reviewer_package/`

2. **Summary statistics**:
   - Number of claims documented
   - Number of evidence items (supporting vs challenging)
   - Any HIGH CONCERN claims from audit

3. **Living Paper status**:
   - Whether `lp lint` passed
   - Reviewer package generated (yes/no)

4. **Next steps for the user**:
   - Send `VERIFICATION_PACKAGE.zip` to a DIFFERENT AI or skeptical colleague
   - Send `reviewer_package/` folder to journal reviewers (they just double-click to open)
   - Once external verification passes, run `/draft-paper`

**IMPORTANT**: The system that built the analysis should NOT be the only verifier. External review catches blind spots.

Tip: Run `/status` anytime to see overall workflow progress.
