# Living Paper: System Specification

**Status**: Concept spec for exploration
**Author**: Matt Beane
**Date**: December 2024

---

## What This Is

A "living paper" is a research artifact that maintains bidirectional links between claims and evidence throughout its lifecycle—from data collection through publication and beyond. Unlike static manuscripts, a living paper can:

1. Trace any claim back to its supporting evidence (quotes, observations, statistics)
2. Update when new data is added or existing data is reinterpreted
3. Surface when evidence no longer supports claims (or supports them more strongly)
4. Enable verification by others without exposing protected data

This spec explores what infrastructure would make living papers possible, with particular attention to the constraints of qualitative research under IRB protection.

---

## The Problem

### Current State

Academic papers are frozen artifacts. The journey from data to claim is:

```
Raw Data → Coding → Analysis → Claims → Manuscript → Publication
    ↓         ↓         ↓          ↓          ↓
 (lost)    (lost)   (partially   (implicit)  (static)
                     documented)
```

Once published, the paper is disconnected from its evidentiary basis. Reviewers and readers must trust the author's account of what the data showed. Replication requires starting from scratch—if the data is even available.

### What Gets Lost

1. **Provenance**: Which specific observations support which specific claims?
2. **Alternatives considered**: What framings were tried and abandoned? Why?
3. **Uncertainty**: How confident should we be in each claim? What would change our minds?
4. **Updateability**: When new data arrives, which claims should be revisited?

### The IRB Constraint

Qualitative data is often collected under IRB protocols that:
- Prohibit sharing raw data (PII, attribution risk)
- Require destruction after a period
- Limit who can access even anonymized transcripts

This creates a tension: we want verifiability, but we can't expose the evidence.

---

## Design Principles

### 1. Claims Are First-Class Objects

Every substantive claim in a paper is a discrete, addressable object with:
- Unique identifier
- Claim text
- Claim type (empirical observation, theoretical proposition, methodological assertion)
- Confidence level (author-assessed)
- Evidence links (see below)
- Revision history

### 2. Evidence Links Are Typed and Weighted

A claim can be supported by multiple pieces of evidence, each with:
- Evidence type (quote, field note, statistic, secondary source)
- Relationship type (supports, contradicts, qualifies, illustrates)
- Weight (central vs. peripheral)
- Verification status (verified by author, verified by external reviewer, unverified)

### 3. Data Stays Protected; Pointers Are Shareable

For IRB-protected data:
- Raw data never leaves the secure environment
- Evidence links point to *hashes* or *encrypted references*
- Verification can occur within the secure environment without exposing data
- Summaries and patterns can be exported; source material cannot

### 4. The Paper Is a View, Not the Truth

The published manuscript is one *rendering* of the underlying claim-evidence graph. Other views are possible:
- Evidence density map (which claims have the most support?)
- Contradiction report (where does evidence cut both ways?)
- Confidence distribution (how certain are we across the paper?)
- Update log (what changed since last version?)

---

## System Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────────┐
│                        LIVING PAPER                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │   CLAIMS     │◄──►│   EVIDENCE   │◄──►│    DATA      │       │
│  │   REGISTRY   │    │    LINKS     │    │   VAULT      │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│         │                   │                   │                │
│         ▼                   ▼                   ▼                │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │  MANUSCRIPT  │    │ VERIFICATION │    │    ACCESS    │       │
│  │  GENERATOR   │    │    ENGINE    │    │   CONTROL    │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Claims Registry

Stores all claims with:
```
claim_id: string (unique)
claim_text: string
claim_type: enum [empirical, theoretical, methodological, definitional, boundary_condition]
confidence: float [0-1]
status: enum [draft, verified, published, retracted, updated]
verification_status: enum [unverified, author_verified, external_verified]
parent_claim: claim_id | null (for claim hierarchies)
frame_id: string | null (for theoretical framing)

# Prevalence metadata (V0.5 - ethnographic authority context)
informant_coverage: string | null  # e.g., "12/47 informants", "widespread"
contradicting_count: int           # count of contradicting evidence (0 = none found)
saturation_note: string | null     # e.g., "Pattern consistent across all sites"
prevalence_basis: enum [representative, illustrative, singular, aggregate]

created_at: timestamp
modified_at: timestamp
modification_history: []{timestamp, old_text, new_text, reason}
```

### Evidence Links

```
link_id: string
claim_id: string (foreign key)
evidence_id: string (foreign key to Data Vault)
relationship: enum [supports, contradicts, qualifies, illustrates, necessitates]
weight: enum [central, supporting, peripheral]
author_note: string (why this evidence matters)
verification_status: enum [unverified, author_verified, external_verified]
verified_by: string | null
verified_at: timestamp | null
```

### Data Vault

Two modes depending on data sensitivity:

**Mode A: Open Data**
```
evidence_id: string
evidence_type: enum [quote, fieldnote, statistic, document, secondary_source]
content: string (actual text/data)
source: string (interview ID, document name, etc.)
location: string (page number, timestamp, line number)
collected_at: timestamp
```

**Mode B: Protected Data (IRB/PII)**
```
evidence_id: string
evidence_type: enum [quote, fieldnote, statistic, document]
content_hash: string (SHA-256 of actual content)
content_summary: string (non-identifying summary)
source_hash: string (hashed interview/document ID)
location: string (page/timestamp—may need redaction)
collected_at: timestamp
access_tier: enum [author_only, approved_reviewers, verification_agents]
encryption_key_id: string (for approved access)
```

### Access Control Layer

For protected data:
- Author has full access
- Designated reviewers can access via secure environment (no export)
- Verification agents (AI or human) can query but not extract
- Public sees only: claim + evidence count + verification status + non-identifying summary

---

## Workflows

### Workflow A: New Project (Data Collection Ongoing)

```
1. SETUP
   - Create project with IRB protocol reference
   - Define data sensitivity level
   - Configure access tiers

2. DATA COLLECTION
   - Import interview transcripts, field notes, documents
   - Auto-hash PII fields (names, orgs, locations)
   - Generate evidence_ids for all importable units

3. EXPLORATION
   - Run /explore-data against Data Vault
   - Claims auto-generated are tagged [draft, unverified]
   - Evidence links created automatically with [unverified] status

4. ANALYSIS
   - Author reviews auto-generated claims
   - Promotes, modifies, or rejects
   - Adds manual claims with manual evidence links
   - Verification engine checks link validity

5. ITERATION
   - New data added → system flags claims that might be affected
   - Author reviews, updates claims, adds evidence
   - Revision history maintained

6. VERIFICATION
   - External reviewer granted secure access
   - Reviews evidence links for subset of claims
   - Marks as [external_verified] or flags issues

7. PUBLICATION
   - Manuscript generated from claims registry
   - Evidence links embedded as metadata (not visible in PDF, but queryable)
   - Public can see claim confidence + verification status
   - Protected data remains in vault
```

### Workflow B: Existing Data (Already Collected Under IRB)

```
1. IMPORT
   - Inventory existing data files
   - Map to original IRB protocol
   - Identify sensitivity level per data type

2. RETROACTIVE HASHING
   - Run PII detection on all text data
   - Generate hashes for identifiable information
   - Create mapping file (stored separately, author-only access)

3. EVIDENCE EXTRACTION
   - Run /explore-data and /mine-qual against hashed corpus
   - All quotes and references use hashed identifiers
   - Summaries generated are non-identifying

4. CLAIM CONSTRUCTION
   - Author builds claims with evidence links
   - Each link points to hashed evidence
   - Verification possible within secure environment

5. SELECTIVE DISCLOSURE
   - For verification: reviewer accesses secure environment
   - For publication: only summaries and patterns exported
   - For replication: another researcher could verify claims
     against their own access to the same site (if IRB allows)
```

### Workflow C: Mixed (Existing + New Collection)

```
1. BASELINE
   - Import existing data per Workflow B
   - Identify gaps in evidence for desired claims

2. TARGETED COLLECTION
   - Design new data collection to fill gaps
   - New IRB amendment if needed
   - Collect with living paper structure from start

3. INTEGRATION
   - New data enters same vault
   - Claims can draw on both old and new evidence
   - System tracks which claims depend on which data vintage

4. COMPARATIVE ANALYSIS
   - Does new data support or challenge claims from old data?
   - Temporal patterns become visible
   - Longitudinal claims become possible
```

---

## Verification Without Exposure

The core technical challenge: how can a reviewer verify that evidence supports claims without seeing protected data?

### Option 1: Secure Enclave Review

- Reviewer accesses data through secure environment (VDI, secure room)
- Can read but not export
- Marks verification status in system
- Audit log tracks what was accessed

**Pros**: Full verification possible
**Cons**: Friction; requires trust in reviewer; doesn't scale

### Option 2: AI Verification Agent

- Trained verification model runs inside secure environment
- Takes claim + evidence links as input
- Outputs: consistency score, red flags, suggested additional evidence
- Never exports raw data

**Pros**: Scalable; consistent; no human exposure to PII
**Cons**: AI limitations; may miss subtle issues; requires trust in model

### Option 3: Zero-Knowledge Proofs (Experimental)

- Cryptographic proof that evidence exists and matches claimed properties
- Verifier can confirm "a quote exists in the corpus that contains these concepts" without seeing the quote
- Author generates proof; anyone can verify

**Pros**: Mathematically guaranteed privacy; public verification
**Cons**: Complex to implement; limited expressiveness; cutting-edge

### Option 4: Differential Privacy Summaries

- Generate statistical summaries of evidence that protect individual data points
- "73% of informants expressed sentiment X" verifiable without identifying any informant
- Noise added to prevent re-identification

**Pros**: Established techniques; good for quantitative claims
**Cons**: Doesn't work well for qualitative claims; loses richness

### Recommended Approach

Hybrid:
- AI Verification Agent for first-pass review (scalable, catches obvious issues)
- Secure Enclave Review for contested or high-stakes claims (human judgment)
- Zero-Knowledge Proofs as aspirational goal for public verification

---

## Manuscript Generation

The living paper generates traditional manuscripts on demand:

### Render Modes

**Standard Academic**
- Claims assembled into narrative prose
- Evidence links become in-text citations and quotes
- Confidence levels omitted (traditional presentation)
- Outputs: Word, LaTeX, PDF

**Transparent Academic**
- Same as Standard, plus:
- Confidence indicators (visual or textual)
- Evidence density annotations
- Link to online supplement with full claim graph
- Outputs: Word, LaTeX, PDF + HTML supplement

**Full Living Paper**
- Interactive web document
- Click any claim to see evidence links
- Verification status visible
- Update history accessible
- Filter by confidence, verification status, evidence type
- Outputs: HTML, hosted web app

### Journal Compatibility

Most journals accept Standard Academic output. Transparent Academic works for journals with online supplements. Full Living Paper requires either:
- Journal infrastructure to host (unlikely near-term)
- Author-hosted supplement with DOI
- Integration with OSF, Dataverse, or similar

---

## Data Model: Worked Example

### Claim

```json
{
  "claim_id": "c_001",
  "claim_text": "Surgical trainees who engaged in shadow learning achieved skill gains 2-3x faster than peers who relied solely on formal training",
  "claim_type": "empirical",
  "confidence": 0.85,
  "status": "verified",
  "evidence_links": ["el_001", "el_002", "el_003", "el_004"],
  "created_at": "2024-03-15T10:00:00Z",
  "modified_at": "2024-06-20T14:30:00Z",
  "modification_history": [
    {
      "timestamp": "2024-06-20T14:30:00Z",
      "old_text": "...achieved skill gains 3-4x faster...",
      "new_text": "...achieved skill gains 2-3x faster...",
      "reason": "Revised after additional data collection narrowed estimate"
    }
  ]
}
```

### Evidence Link

```json
{
  "link_id": "el_001",
  "claim_id": "c_001",
  "evidence_id": "ev_047",
  "relationship": "supports",
  "weight": "central",
  "author_note": "Direct observation of trainee performing procedure independently after 8 cases vs. typical 25+",
  "verification_status": "external_verified",
  "verified_by": "reviewer_002",
  "verified_at": "2024-07-01T09:00:00Z"
}
```

### Evidence (Protected Mode)

```json
{
  "evidence_id": "ev_047",
  "evidence_type": "fieldnote",
  "content_hash": "a3f2b8c9d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9",
  "content_summary": "Observation of junior trainee performing complex procedure with minimal supervision; attending noted unusual proficiency for case volume",
  "source_hash": "h_site_03_obs_127",
  "location": "Field note 127, lines 45-62",
  "collected_at": "2023-11-14T14:30:00Z",
  "access_tier": "approved_reviewers"
}
```

---

## Open Questions

### Governance

- Who controls the canonical version of a living paper?
- What happens when co-authors disagree about claim confidence?
- How do we handle claims that become unsupported after publication?
- Retraction vs. revision vs. annotation?

### Incentives

- Do journals have any reason to support this?
- Does this create more work for authors with no reward?
- Could verification status become a quality signal that matters?

### Technical

- How do we handle evidence that supports multiple claims?
- What's the right granularity for claims? (Sentence? Paragraph? Section?)
- How do we version the claim graph when the paper structure changes?
- Can we meaningfully verify qualitative claims with AI?

### Practical

- What's the minimum viable version that provides value?
- Who would use this first? (Probably not senior faculty with working systems)
- How does this interact with preregistration movements?

---

## Minimum Viable Implementation

If building this incrementally, start with:

### V0.1: Claim Tracker
- Simple database of claims with manual evidence links
- No data vault integration
- Author-only
- Value: Forces explicit claim-evidence mapping during writing

### V0.2: Evidence Integration
- Connect to data files (interviews, field notes)
- Auto-generate evidence IDs
- Link claims to specific locations in source files
- Value: Provenance tracking; easier verification prep

### V0.3: Verification Workflow
- Add verification status to evidence links
- Export verification package for reviewer
- Import reviewer annotations
- Value: Structured external review

### V0.4: Protected Data Mode
- Add hashing layer for PII
- Implement access control
- Secure environment for review
- Value: IRB-compliant verification

### V0.4.5: Pre-Review Workflow
- Surface contested claims (challenges, low confidence, weak support)
- Generate pre-review report with adjudication prompts
- Apply quant/qual hierarchy for mechanism adjudication
- Track claim revisions with reasoning
- Value: Adversarial self-audit before submission; stronger claims; preempted reviewer objections

**Key insight**: When the system surfaces challenges, engaging with them productively *is* the review process—just earlier. This isn't p-hacking (quant data is fixed); it's principled mechanism refinement with an audit trail.

See `living_paper/PREREVIEW.md` for the full methodology.

### V0.5: Reviewer Interface & Export Package
- Interactive web reviewer interface (`reviewer_app.py`)
- Static HTML export for non-technical reviewers (`export-html`, `export-package`)
- PII redaction system for entity protection (`redact.py`, `entities.yaml`)
- Prevalence metadata for ethnographic claims (informant coverage, contradicting counts, saturation notes)
- Reviewer packages with double-click launchers for Mac/Windows
- localStorage-based progress saving, downloadable verification reports
- Value: External verification without exposing protected data; accessible to non-technical reviewers

**New Commands**:
- `lp.py export-html --paper PAPER_ID --out FILE` - Static HTML reviewer
- `lp.py export-package --paper PAPER_ID --out FOLDER` - Complete reviewer package with launchers
- `lp.py migrate-redact --entities entities.yaml` - Apply redaction to existing records

### V0.6: Manuscript Generation
- Generate standard academic output from claim graph
- Evidence links become citations/quotes
- Value: Living paper becomes practical writing tool

### V1.0: Full Living Paper
- Interactive web rendering
- Public claim graph (with protected data hidden)
- Update/revision workflow
- Value: New form of scholarly communication

---

## Why This Matters

The replication crisis in social science stems partly from the disconnect between claims and evidence. We ask readers to trust that the data said what we say it said. Living papers make that relationship explicit, auditable, and—where possible—verifiable.

For qualitative research specifically, this addresses the persistent critique that findings are unfalsifiable because evidence is inaccessible. Living papers don't solve that entirely (protected data is still protected), but they create infrastructure for verification that doesn't currently exist.

The PhD students learning paper-mining-agents today will be faculty in 10 years. If they build habits around claim-evidence traceability now, they'll be positioned to adopt (or demand) living paper infrastructure when it exists.

This spec is an invitation to explore what that infrastructure could look like.

---

## Next Steps

1. Review with collaborators for feasibility and priority
2. Identify minimum viable version worth building
3. Find a pilot project (ideally with non-sensitive data for V0.1-V0.3)
4. Build incrementally, learning what actually helps vs. what's theoretically nice

---

## References

This spec draws on several streams of work on transparency, reproducibility, and replicability in qualitative research:

### Foundational Frameworks

**Aguinis, H., & Solarino, A. M. (2019).** Transparency and replicability in qualitative research: The case of interviews with elite informants. *Strategic Management Journal*, 40(8), 1291-1315.
https://sms.onlinelibrary.wiley.com/doi/10.1002/smj.3015

- Analyzed 52 SMJ articles; none met 12 transparency criteria
- Offers behaviorally-anchored rating scales for transparency evaluation
- Criteria cover research design, measurement, data analysis, data disclosure

**Aguinis, H., et al. (2025).** Transparency, reproducibility, and replicability in human resource management research. *Personnel Review*.
https://www.emerald.com/insight/content/doi/10.1108/pr-10-2024-0946/full/html

- Introduces TRRUST framework (Transparency, Replicability, Reproducibility, Unified ontology, Shared culture of science, Trust and values)
- 25 actionable recommendations including data sharing, pre-registration, sensitivity analyses

### Annotation and Verification Systems

**Qualitative Data Repository (QDR).** Annotation for Transparent Inquiry (ATI).
https://qdr.syr.edu/ati

- Digital annotations linking claims to evidence excerpts
- Data Overview (~1,000 words) + passage-level annotations
- Elements: citation, source excerpt (100-150 words), translation, analytic note, data source link

**QDR Guide to ATI.**
https://qdr.syr.edu/ati/guide-ati

- Specifies Data Overview requirements: data generation context, procedures, selection rationale, gaps, analysis methodology
- Analytic notes explain HOW evidence supports claims (interpretive reasoning)

**Moravcsik, A.** Active Citation framework.
https://qdr.syr.edu/content/guide-active-citation

- Pioneered three dimensions: data transparency, analytic transparency, production transparency
- System of digitally-enabled citations linked to annotated source excerpts

### Journal Verification Policies

**American Journal of Political Science.** Our Experience with the AJPS Transparency and Verification Process for Qualitative Research (2019).
https://ajps.org/2019/05/09/our-experience-with-the-ajps-transparency-and-verification-process-for-qualitative-research/

- QDR reviews materials, generates report: "supported," "partially supported," "not documented/referenced"
- Authors revise based on report; improves quality and aligns claims with evidence

### Data Sharing Barriers and Solutions

**Childs, S., et al. (2022).** Barriers and facilitators to qualitative data sharing in the United States: A survey of qualitative researchers. *PLOS ONE*.
https://pmc.ncbi.nlm.nih.gov/articles/PMC8719660/

- Four barrier categories: scientific quality, permission, confidentiality, researcher burden
- Deductive disclosure risk: participants may recognize themselves even with pseudonyms
- Ethnographic field notes present special challenges

**Turcotte-Tremblay, A. M., & Mc Sween-Cadieux, E. (2018).** A reflection on the challenge of protecting confidentiality while preserving analytical rigor in qualitative data sharing. *Qualitative Health Research*.
https://pmc.ncbi.nlm.nih.gov/articles/PMC2805454/

- "Internal confidentiality" violations: study participants recognize each other
- Graded access systems recommended

### Qualitative Open Science

**Haven, T., & Van Grootel, D. (2019).** What does reproducibility mean for qualitative research?
https://openworking.wordpress.com/2019/02/11/what-does-reproducibility-mean-for-qualitative-research/

- Argues quality should be judged by transparency of process, not reproducibility of findings
- Distinguishes production transparency from analytic transparency

**Kapiszewski, D., & Karcher, S. (2021).** Rethinking Transparency and Rigor from a Qualitative Open Science Perspective. *Journal of Trial & Error*.
https://journal.trialanderror.org/pub/rethinking-transparency/release/1

- Recommends positionality statements, reflexivity practices, thick description, audit trails
- Data papers as supplementary methodology publications
- Preregistration should document "why" (theoretical framework) not just "what"

### Review Articles

**Open science interventions to improve reproducibility and replicability of research: a scoping review (2025).** *PMC*.
https://pmc.ncbi.nlm.nih.gov/articles/PMC11979971/

- Studies on reproducibility peaked 2022-2023
- Growing intervention studies across disciplines

**Is replication possible in qualitative research? A response to Makel et al. (2024).** *Educational Research and Evaluation*.
https://www.tandfonline.com/doi/full/10.1080/13803611.2024.2314526

- Calls for nuanced appraisal of replication compatibility with qualitative epistemology/ontology
