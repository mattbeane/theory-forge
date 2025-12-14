# living_paper v0.5 (local-first)

This is a minimal "living paper" layer you can run locally to maintain bidirectional links between claims and evidence,
while keeping protected pointers out of the shareable store.

## What it does (v0.5)
- Maintains two SQLite DBs:
  - `analysis/living_paper/lp_public.sqlite` (safe-to-commit metadata)
  - `analysis/living_paper/lp_private.sqlite` (protected pointers; should be gitignored)
- CLI:
  - `lp init`           : create DBs + default policy stub
  - `lp ingest`         : load claims/evidence/links from JSONL/CSV
  - `lp lint`           : fail if traceability rules are broken
  - `lp export`         : generate PUBLIC-facing provenance + evidence summaries
  - `lp verify-export`  : export verification package for external reviewers
  - `lp prereview`      : generate pre-review report of contested claims
  - `lp export-html`    : export self-contained HTML reviewer (no server)
  - `lp export-package` : export complete reviewer package (HTML + launchers + README)
  - `lp migrate-redact` : apply entity redaction to existing DB records

- **PII Redaction**: `redact.py` + `entities.yaml` for protecting identifying information
- **Reviewer Interface**: `reviewer_app.py` for interactive web-based verification
- **Prevalence Metadata**: Track informant coverage, contradicting evidence, saturation notes

## Install
No external deps for core. Optional: `pip install pyyaml flask` for YAML entities and web interface.

## Usage
From your project root:

```bash
# Initialize
python3 living_paper/lp.py init

# Ingest data (with optional PII redaction)
python3 living_paper/lp.py ingest \
  --claims analysis/verification/claims.jsonl \
  --evidence analysis/verification/evidence.jsonl \
  --links analysis/verification/links.csv \
  --entities living_paper/entities.yaml  # optional

# Check traceability
python3 living_paper/lp.py lint

# Export public provenance
python3 living_paper/lp.py export --out analysis/living_paper/exports/replication_package/PUBLIC

# Generate reviewer package (for external reviewers)
python3 living_paper/lp.py export-package --paper PAPER_ID --out /path/to/reviewer_folder

# Run interactive reviewer interface (requires Flask)
python3 living_paper/reviewer_app.py --port 5050
```

## For External Reviewers
The `export-package` command creates a folder containing:
- `review.html` - Self-contained reviewer interface (works offline)
- `README.txt` - Instructions for reviewers
- `Open Review.command` - Mac double-click launcher
- `Open Review.bat` - Windows double-click launcher

Reviewers open the HTML file in any browser, do their review, then click "Generate Report" to download a markdown file to send back.

## Expected input formats
### claims.jsonl (one JSON object per line)
Required keys:
- claim_id (string)
- paper_id (string)
- claim_type (empirical/theoretical/methodological/definitional/boundary_condition)
- text (string)
Optional:
- confidence (float 0-1, default 0.5)
- status (draft/verified/published/retracted/updated)
- verification_status (unverified/author_verified/external_verified)
- frame_id (string)
- verification_mode (public_provenance/controlled_access/witness_only)
- informant_coverage (string, e.g., "12/47 informants")
- contradicting_count (int, default 0)
- saturation_note (string)
- prevalence_basis (representative/illustrative/singular/aggregate)

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
Where:
- relation in {supports, challenges, illustrates, qualifies, necessitates}
- weight in {central, supporting, peripheral}

## Entity Redaction (PII Protection)
Create `entities.yaml` with entity→replacement mappings:
```yaml
vendors:
  Kindred: "Vendor A"
  Vicarious: "Vendor B"
sites:
  Bloomington: "Site Alpha"
patterns:
  - pattern: "\\$\\d+K"
    replacement: "[AMOUNT]"
```

See `entities_example.yaml` for a template. The entities file should be gitignored (it reveals PII mappings).

## Git hygiene
Add this to your `.gitignore`:
```
analysis/living_paper/lp_private.sqlite
analysis/living_paper/exports/replication_package/WITNESS_ONLY/
analysis/living_paper/exports/replication_package/CONTROLLED/
entities.yaml
**/entities.yaml
```

## Notes
This is v0.5 implementing the reviewer interface milestone from `docs/LIVING_PAPER_SPEC.md`. See that document for the full roadmap.
