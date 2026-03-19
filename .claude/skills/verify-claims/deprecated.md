# DEPRECATED: Manual Evidence Generation

**DO NOT USE THIS APPROACH.** It produces circular verification — the same AI that built the analysis generates the evidence, which defeats the purpose.

Use `/audit-claims` instead, which searches raw data independently.

---

## Old Approach (for historical reference only)

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
