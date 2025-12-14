# living_paper v0.1 (local-first)

This is a minimal "living paper" layer you can run locally to maintain bidirectional links between claims and evidence,
while keeping protected pointers out of the shareable store.

## What it does (v0.1)
- Maintains two SQLite DBs:
  - `analysis/living_paper/lp_public.sqlite` (safe-to-commit metadata)
  - `analysis/living_paper/lp_private.sqlite` (protected pointers; should be gitignored)
- CLI:
  - `lp init`    : create DBs + default policy stub
  - `lp ingest`  : load claims/evidence/links from JSONL/CSV emitted by /verify-claims
  - `lp lint`    : fail if traceability rules are broken
  - `lp export`  : generate PUBLIC-facing provenance + evidence summaries

## Install
No external deps. Requires Python 3.10+.

## Usage
From your project root:

```bash
python3 living_paper/lp.py init
python3 living_paper/lp.py ingest --claims analysis/verification/claims.jsonl --evidence analysis/verification/evidence.jsonl --links analysis/verification/links.csv
python3 living_paper/lp.py lint
python3 living_paper/lp.py export --out analysis/living_paper/exports/replication_package/PUBLIC
```

## Expected input formats
### claims.jsonl (one JSON object per line)
Required keys:
- claim_id (string)
- paper_id (string)
- claim_type (e.g., descriptive/mechanism/boundary_condition/measurement/process)
- text (string)
Optional:
- status (draft/verified/superseded/retracted)
- frame_id (string)
- verification_mode (public_provenance/controlled_access/witness_only)

### evidence.jsonl
Required keys:
- evidence_id (string)
- paper_id (string)
- evidence_type (quote/fieldnote/observation/quant_output/other)
- summary (string)  # safe paraphrase / description
- sensitivity_tier (PUBLIC/CONTROLLED/WITNESS_ONLY)
- meta (object)     # safe metadata; e.g. interview_id, informant_role_bin, informant_tenure_bin, line_start, line_end

### links.csv
Columns:
- claim_id,evidence_id,relation,weight,note
Where relation in {supports,challenges,illustrates}.

## Git hygiene
Add this to your `.gitignore`:
```
analysis/living_paper/lp_private.sqlite
analysis/living_paper/exports/replication_package/WITNESS_ONLY/
analysis/living_paper/exports/replication_package/CONTROLLED/
```

## Notes
This is intentionally minimal. Once you're using it daily, you'll know what to add next (witness bundles, claim-graph diffs, etc.).
