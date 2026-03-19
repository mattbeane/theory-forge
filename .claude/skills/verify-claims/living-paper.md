# Living Paper Integration

The `/audit-claims` step has already generated Living Paper-compatible files:
- `analysis/audit/claims.jsonl`
- `analysis/audit/evidence.jsonl`
- `analysis/audit/links.csv`

**You MUST run these commands automatically** (do not just tell the user to do it):

## Step 1: Copy audit files to verification directory

```bash
cp analysis/audit/claims.jsonl analysis/verification/
cp analysis/audit/evidence.jsonl analysis/verification/
cp analysis/audit/links.csv analysis/verification/
```

## Step 2: Initialize Living Paper (if not already done)

```bash
python3 living_paper/lp.py init
```

## Step 3: Ingest into Living Paper database

```bash
python3 living_paper/lp.py ingest \
  --claims analysis/verification/claims.jsonl \
  --evidence analysis/verification/evidence.jsonl \
  --links analysis/verification/links.csv
```

## Step 4: Run lint to verify traceability

```bash
python3 living_paper/lp.py lint
```

If lint fails, fix the issues before proceeding.

## Step 5: Generate reviewer package

Get the paper_id from the claims file (first line's paper_id field), then:

```bash
python3 living_paper/lp.py export-package --paper [PAPER_ID] --out analysis/verification/reviewer_package
```

This creates a folder reviewers can open directly — no CLI required on their end.

**DO NOT regenerate claims/evidence from the manuscript**. The audit files contain evidence found by searching raw data, including challenging evidence. Regenerating from the manuscript would lose this.

## If audit files don't exist

If for some reason audit files don't exist, STOP and run `/audit-claims` first. Do not proceed with verification without raw data grounding.
