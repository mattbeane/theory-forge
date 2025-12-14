# Replicability Approaches for AI-Assisted Qualitative Research

This document outlines approaches to making AI-assisted qualitative research replicable while respecting IRB constraints on sensitive data.

---

## Option 6: Tiered Transparency

Release different levels of detail based on sensitivity, giving readers maximum insight into your process while protecting participants.

### Tier Structure

```
replication_package/
├── PUBLIC/                          # Anyone can access
│   ├── code/
│   │   ├── analysis/                # All analysis scripts
│   │   ├── prompts/                 # Slash command templates used
│   │   └── requirements.txt         # Dependencies
│   ├── data_synthetic/
│   │   ├── quant_synthetic.csv      # Preserves distributions, correlations
│   │   ├── generation_script.py     # How synthetic data was created
│   │   └── validation_report.md     # How synthetic matches real properties
│   ├── data_aggregated/
│   │   ├── facility_month_agg.csv   # Real data, aggregated to safe level
│   │   └── aggregation_rules.md     # Min cell sizes, what was suppressed
│   ├── qual_metadata/
│   │   ├── interview_roster.csv     # ID, role type, tenure, site (no names)
│   │   ├── quote_provenance.csv     # For each quote: interview_id, line_range, informant_type
│   │   └── coding_scheme.md         # Mechanism hypotheses tested
│   ├── process/
│   │   ├── frame_genealogy.md       # All framings tried, what killed each
│   │   ├── decision_log.md          # Major analytical choices
│   │   ├── evidence_summary.md      # What evidence supported/challenged each hypothesis
│   │   └── disconfirming_evidence.md # What challenges the interpretation
│   └── verification/
│       ├── external_ai_review.pdf   # What the verification AI found
│       ├── author_responses.md      # How issues were addressed
│       └── verification_package_manifest.md  # What was sent for review
│
├── CONTROLLED/                      # Requires DUA
│   ├── data_deidentified/
│   │   ├── quant_individual.csv     # Individual-level, identifiers removed
│   │   ├── deidentification_log.md  # What was removed/transformed
│   │   └── reidentification_risk.md # Assessment of remaining risk
│   └── qual_transcripts/
│       ├── interviews/              # Full transcripts, names redacted
│       ├── redaction_protocol.md    # How redaction was done
│       └── quote_verification.csv   # Maps paper quotes to transcript locations
│
└── WITNESS_ONLY/                    # Verification witness access
    ├── data_original/               # Unredacted data
    ├── identifiers/                 # Linking files
    └── irb_protocol.pdf             # Original IRB approval
```

### Synthetic Data Generation Protocol

For quantitative data:

```python
# Example using SDV (Synthetic Data Vault)
from sdv.single_table import GaussianCopulaSynthesizer
from sdv.metadata import SingleTableMetadata

# Load real data
real_data = pd.read_csv('sensitive_data.csv')

# Define metadata
metadata = SingleTableMetadata()
metadata.detect_from_dataframe(real_data)

# Mark sensitive columns
metadata.update_column('worker_id', sdtype='id')
metadata.update_column('facility', sdtype='categorical')

# Generate synthetic data
synthesizer = GaussianCopulaSynthesizer(metadata)
synthesizer.fit(real_data)
synthetic_data = synthesizer.sample(num_rows=len(real_data))

# Validate: key statistics should match
validation_report = {
    'real_mean': real_data['outcome'].mean(),
    'synthetic_mean': synthetic_data['outcome'].mean(),
    'correlation_preserved': real_data[['x', 'y']].corr() - synthetic_data[['x', 'y']].corr(),
    # ... more checks
}
```

**Validation requirements**:
- Marginal distributions match (within tolerance)
- Key correlations preserved
- Regression coefficients similar direction/significance
- No individual from real data can be identified in synthetic

### Aggregation Rules

For releasing real data at aggregated level:

| Data Element | Aggregation | Suppression Rule |
|-------------|-------------|------------------|
| Exit events | Facility-month | Suppress if < 5 events |
| Tenure | Binned (0-3mo, 3-12mo, 12mo+) | — |
| Performance | Facility-month mean | Suppress if < 10 workers |
| Automation timing | Exact dates OK | — |

### Quote Provenance Format

For qualitative evidence, release metadata without content:

```csv
quote_id,paper_location,interview_id,informant_role,informant_tenure,line_start,line_end,mechanism_hypothesis,evidence_type
Q1,p.12,INT_023,operations_manager,5_years,234,238,H2_uncertainty_response,supporting
Q2,p.12,INT_047,frontline_supervisor,2_years,89,94,H2_uncertainty_response,supporting
Q3,p.14,INT_011,temp_worker,3_months,156,162,H3_option_cultivation,supporting
Q4,p.18,INT_031,HR_director,8_years,445,451,H2_uncertainty_response,challenging
```

This lets readers see:
- Distribution of evidence across informant types
- Whether you're cherry-picking from few sources
- The balance of supporting vs. challenging evidence
- Exactly where each quote lives (for DUA-access verification)

---

## Option 4: Verification Witness Model

A trusted third party independently verifies your analysis with full data access.

### The IRB Challenge

**Problem**: Getting a non-UCSB researcher access to your IRB-protected data is genuinely hard. Options:

1. **Add them to your existing protocol**: IRB amendment to add external collaborator
   - Requires their institution's IRB to cede review or do parallel review
   - Can take 2-6 months
   - They may need CITI training, institutional agreement

2. **Have their institution get its own IRB approval**: They submit protocol to their IRB referencing yours
   - Even slower
   - Requires data sharing agreement between institutions

3. **Use a UCSB-affiliated verifier**: Someone already under UCSB IRB umbrella
   - Graduate student, postdoc, or colleague at UCSB
   - Much faster (just add to protocol)
   - But less "independent"—same institutional incentives

4. **Commercial/nonprofit verification service**: Some organizations specialize in this
   - Would need to be set up as a contractor with appropriate agreements
   - Novel but potentially faster than academic IRB

### Recommended Approach: Tiered Verification

**Tier 1: UCSB-internal witness (fast, less independent)**
- Add a UCSB colleague to IRB protocol (amendment, ~2-4 weeks)
- They do full verification
- Disclose in paper: "Verified by [Name], UCSB, who had no involvement in analysis"

**Tier 2: External witness via reliance agreement (slower, more independent)**
- Identify willing external verifier
- Their institution signs reliance agreement ceding IRB review to UCSB
- UCSB IRB approves them as external collaborator
- Timeline: 2-4 months

**Tier 3: Post-publication verification (slowest, most independent)**
- State in paper: "Full data access available to qualified researchers for verification"
- Set up DUA process
- First person to verify and publish attestation gets cited

### Verification Witness Protocol

What the witness actually does:

```markdown
# Verification Protocol for [Paper Title]

## Witness Responsibilities

1. **Quantitative Claims Verification**
   - Run all analysis code on original data
   - Confirm all statistics reported in paper match output
   - Verify robustness checks were actually run (not just claimed)
   - Check for coding errors, data processing mistakes

2. **Qualitative Claims Verification**
   - Locate each quote in source transcript
   - Verify quote is accurately transcribed
   - Verify context doesn't change meaning
   - Check that informant role/tenure matches paper's description

3. **Process Verification**
   - Review decision log for completeness
   - Confirm frame genealogy matches actual analysis history
   - Verify that disconfirming evidence was actually considered

4. **Independence Attestation**
   - Confirm no involvement in original analysis
   - Disclose any relationship with author
   - Disclose any conflicts of interest

## Witness Report Template

I, [Name], [Title] at [Institution], conducted independent verification of
[Paper Title] by [Author] on [Date].

**Data Access**: I had full access to:
- [ ] Original quantitative data (N = X observations)
- [ ] All interview transcripts (N = X interviews)
- [ ] Complete analysis code
- [ ] Decision logs and process documentation

**Quantitative Verification**:
- [ ] All reported statistics replicate exactly
- [ ] Robustness checks replicate
- [ ] No errors found in data processing

OR: [Describe discrepancies found]

**Qualitative Verification**:
- [ ] All quotes verified against source transcripts
- [ ] Context accurately represented
- [ ] Informant descriptions accurate

OR: [Describe discrepancies found]

**Process Verification**:
- [ ] Decision log complete and consistent
- [ ] Frame genealogy matches evidence
- [ ] Disconfirming evidence appropriately handled

**Independence Declaration**:
I had no involvement in the original analysis. My relationship with the
author is: [describe]. I have no financial or professional conflicts.

**Overall Assessment**:
[ ] Verified without reservations
[ ] Verified with minor notes: [describe]
[ ] Significant concerns: [describe]

Signed: _______________ Date: _______________
```

### Making Witness Verification Scalable

For future papers, build this into the workflow:

1. **At project start**: Identify potential witness, begin IRB paperwork early
2. **During analysis**: Keep verification-ready documentation
3. **Before submission**: Send verification package to witness
4. **With submission**: Include witness attestation in supplementary materials

---

## Option 7: Living Paper Architecture

The most radical approach: let readers query your data without seeing it.

### Concept

Instead of releasing data OR restricting access, create an *interface* that lets readers:
- Run pre-specified queries against your data
- Request specific robustness checks
- Explore patterns without extracting underlying data

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│  (Web app or Jupyter notebook with restricted execution)        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │ Pre-defined │  │ Custom      │  │ Natural Language        │ │
│  │ Queries     │  │ Robustness  │  │ Query Interface         │ │
│  │             │  │ Checks      │  │ (LLM-mediated)          │ │
│  └──────┬──────┘  └──────┬──────┘  └───────────┬─────────────┘ │
│         │                │                     │               │
└─────────┼────────────────┼─────────────────────┼───────────────┘
          │                │                     │
          ▼                ▼                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                      QUERY VALIDATOR                            │
│  - Checks query doesn't extract individual records              │
│  - Enforces minimum aggregation levels                          │
│  - Blocks queries that could enable reidentification            │
│  - Rate limits to prevent reconstruction attacks                │
└─────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SECURE EXECUTION ENV                         │
│  (Sandboxed container with no network egress)                   │
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────────────────────────┐│
│  │ QUANTITATIVE    │    │ QUALITATIVE                         ││
│  │ DATA            │    │ DATA                                ││
│  │                 │    │                                     ││
│  │ - Original data │    │ - Full transcripts                  ││
│  │ - Analysis code │    │ - Embeddings for semantic search    ││
│  │                 │    │ - Quote extraction (aggregated)     ││
│  └─────────────────┘    └─────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                     OUTPUT SANITIZER                            │
│  - Ensures no individual-level data in output                   │
│  - Adds noise if needed (differential privacy)                  │
│  - Formats for display                                          │
└─────────────────────────────────────────────────────────────────┘
          │
          ▼
     [Results displayed to user]
```

### Component Details

**1. Pre-defined Queries**

Let users run the exact analyses from the paper:

```python
# User selects from dropdown
available_queries = [
    "main_regression",           # Table 2 in paper
    "robustness_controls",       # Table 3
    "subgroup_analysis",         # Table 4
    "mechanism_evidence_count",  # How many quotes support each hypothesis
    "disconfirming_evidence",    # What challenges the interpretation
]

# User clicks "Run"
# System executes pre-written code, returns formatted output
```

**2. Custom Robustness Checks**

Let users specify alternative specifications:

```python
# User interface
robustness_request = {
    "base_model": "main_regression",
    "modifications": {
        "add_controls": ["facility_size", "region"],
        "change_sample": {"tenure_min": 6},  # Only workers with 6+ months
        "cluster_se": "facility",            # Different clustering
    }
}

# Validator checks:
# - Are requested variables in the data?
# - Does sample restriction leave enough observations?
# - Is this a reasonable specification?

# If valid, executes and returns results
```

**3. Natural Language Query Interface (Qualitative)**

This is the novel part—let users query qualitative data via LLM:

```python
# User asks: "How many informants described feeling uncertain about automation?"

# System:
# 1. LLM interprets query as a coding task
# 2. Searches interview embeddings for relevant passages
# 3. LLM codes each passage (uncertain: yes/no/ambiguous)
# 4. Returns AGGREGATE results only

response = {
    "query": "uncertainty about automation",
    "total_informants": 47,
    "mentioned_uncertainty": 23,
    "examples": [  # Paraphrased, not direct quotes
        "Several managers expressed concern about timeline unpredictability",
        "Some frontline workers reported not knowing if their jobs were safe"
    ],
    "note": "Direct quotes not available; summaries generated from source material"
}
```

**4. Privacy Protections**

| Protection | Implementation |
|-----------|----------------|
| Minimum aggregation | No query returns < 5 individuals |
| Rate limiting | Max 100 queries per user per day |
| Query logging | All queries recorded for audit |
| Differential privacy | Add noise to continuous outputs |
| No raw text | Qualitative queries return summaries, not quotes |
| Reconstruction detection | Flag if query pattern suggests attempt to extract data |

### Technical Implementation Options

**Option A: Hosted Jupyter with Restrictions**

- Use JupyterHub with custom kernel
- Kernel intercepts all code execution
- Blocks file writes, network access, display of raw data
- Users can run analysis code but can't extract data

**Option B: Secure Enclave Service**

- Partner with existing secure computation provider
- Data never leaves secure environment
- Users submit queries via API
- Results returned after sanitization

**Option C: Custom Web Application**

- Build bespoke interface for your specific paper
- More work but most control
- Could become a template for others

**Option D: Federated/Encrypted Computation**

- Data stays encrypted even during computation
- Technically possible but cutting-edge
- Homomorphic encryption, secure multi-party computation
- Probably overkill for now

### Realistic Path to Option 7

**Phase 1 (Now)**: For current papers, use Options 4+6. Document the architecture vision.

**Phase 2 (Next paper)**: Build a simple prototype
- Pre-defined queries only
- Hosted notebook with restricted execution
- Test with a few beta users

**Phase 3 (Scale)**: If prototype works, generalize
- Open source the infrastructure
- Let others use for their papers
- Build community around standard

**Phase 4 (Dream)**: Living Paper as norm
- Journals expect/require interactive verification
- Standard infrastructure exists
- Qualitative replicability becomes tractable

---

## Summary: What to Do Now

For papers currently in development:

1. **Build Tier Structure (Option 6)**
   - Create `replication_package/` with PUBLIC, CONTROLLED, WITNESS_ONLY tiers
   - Generate synthetic quantitative data
   - Create quote provenance metadata
   - Document full analytical process

2. **Initiate Verification Witness (Option 4)**
   - Identify UCSB colleague willing to verify (Tier 1, fast)
   - Begin IRB amendment to add them
   - Simultaneously explore external witness for Tier 2

3. **Document Option 7 Vision**
   - Include in paper's discussion: "Future work could enable interactive verification..."
   - Or write a methods paper proposing the architecture
   - Position yourself as leader in this space

4. **In the Paper**
   - Transparent methods section describing AI collaboration
   - Reference to replication package
   - Witness attestation in supplementary materials
   - Explicit statement about what's available and what's protected

This positions you to say: "We've done everything possible to make this replicable while respecting participant confidentiality. Here's what you can access now, here's how to request more, and here's who has already verified the full analysis."
