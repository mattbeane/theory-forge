## Data Inventory

### Interviews (N=XX)
- Site A: XX interviews (roles: manager, supervisor, worker...)
- Site B: XX interviews (roles: ...)
- [List all, not just the ones cited in the paper]

### Field Notes (N=XX)
- Site A: XX pages
- Site B: XX pages

### Quantitative Data
- [Dataset 1]: XX observations, key variables: ...
- [Dataset 2]: ...

### UNUSED DATA
- [List any data that exists but wasn't drawn on in the current analysis]
```

### Step 2: Extract Claims

From the current framing/manuscript, extract each substantive claim:

For each claim, note:
- Claim ID (CLM-001, etc.)
- Claim type (descriptive, mechanism, boundary_condition, measurement, process)
- The exact claim text
- What evidence WOULD challenge this claim (pre-register your disconfirmation criteria)

### Step 3: Search Raw Data for EACH Claim

For each claim, systematically search:

**A. Search for SUPPORTING evidence**
- Search all interviews for relevant keywords/concepts
- Search field notes
- Check quantitative patterns
- Note: Find NEW supporting evidence, not just what's already cited

**B. Search for CHALLENGING evidence**
- What would contradict this claim?
- Search for informants who experienced the opposite
- Look for cases where the mechanism didn't operate
- Check for alternative explanations
- Look for disconfirming quantitative patterns

**C. Assess evidence distribution**
- How many informants support vs. challenge?
- Are challengers from specific roles/sites?
- Is the supporting evidence concentrated in few sources?

### Step 4: Document Evidence

**CRITICAL: ANONYMIZATION REQUIRED**

You MUST anonymize all evidence before writing to files:
- NO real names (use informant codes: "Informant A1", "Manager M3", etc.)
- NO company names (use pseudonyms from project_config.yaml site_mappings)
- NO locations that could identify (use "Site A", "Site B", etc.)
- Paraphrase quotes to remove identifying details while preserving meaning

Check `project_config.yaml` for:
- `anonymization.redact_patterns` - strings to replace
- `anonymization.site_mappings` - site pseudonyms to use

For each piece of evidence found, create an evidence item:

```json
{
  "evidence_id": "EVD-XXX",
  "paper_id": "PAPER_ID",
  "evidence_type": "quote|fieldnote|observation|quant_output",
  "summary": "Safe paraphrase (no PII, no real names, no company names)",
  "sensitivity_tier": "PUBLIC|CONTROLLED|WITNESS_ONLY",
  "audit_source": "raw_data",  // NOT "manuscript"
  "meta": {
    "interview_id": "INT_XXX",  // Use codes, NOT real names
    "informant_role_bin": "...",  // Generic role: "manager", "worker", "engineer"
    "informant_tenure_bin": "...",
    "site_bin": "SITE_A",  // Use pseudonyms, NOT real locations
    "line_start": N,
    "line_end": N,
    "mechanism_hypothesis": "...",
    "evidence_type": "supporting|challenging|ambiguous"
  }
}
```

**Example of WRONG vs RIGHT:**

WRONG (contains PII):
```json
{"summary": "Jane from the Chicago facility said workers leave when changes are announced"}
```

RIGHT (anonymized):
```json
{"summary": "Planning manager at Site A reported workers leaving when changes announced", "meta": {"interview_id": "INT_MGR_07", "site_bin": "SITE_A"}}
```

**IMPORTANT**: Mark evidence as:
- `supporting` — directly supports the claim
- `challenging` — contradicts or qualifies the claim
- `ambiguous` — could be read either way

### Step 5: Create Links with Honest Weights

```csv
claim_id,evidence_id,relation,weight,note
CLM-001,EVD-001,supports,1.0,Strong direct support
CLM-001,EVD-002,challenges,0.8,Contradicts mechanism in Site B context
CLM-001,EVD-003,supports,0.3,Weak/indirect support
```

**Weight guidelines**:
- 1.0 = Direct, clear, strong evidence
- 0.7-0.9 = Good evidence with minor ambiguity
- 0.4-0.6 = Indirect or partially relevant
- 0.1-0.3 = Weak, tangential, or heavily qualified

### Step 6: Generate Audit Report

Create `analysis/verification/AUDIT_REPORT.md`:

```markdown
# Claims Audit Report

**Paper**: [Title]
**Audit Date**: [Date]
**Data Sources Searched**: [List all]

---
