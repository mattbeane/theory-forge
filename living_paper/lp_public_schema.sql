PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS paper (
  paper_id TEXT PRIMARY KEY,
  title TEXT,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS claim (
  claim_id TEXT PRIMARY KEY,
  paper_id TEXT NOT NULL,
  claim_type TEXT NOT NULL CHECK (claim_type IN ('empirical','theoretical','methodological','definitional','boundary_condition')),
  text TEXT NOT NULL,
  confidence REAL DEFAULT 0.5 CHECK (confidence >= 0 AND confidence <= 1),
  status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft','verified','published','retracted','updated')),
  verification_status TEXT DEFAULT 'unverified' CHECK (verification_status IN ('unverified','author_verified','external_verified')),
  verified_by TEXT,
  verified_at TEXT,
  verification_mode TEXT DEFAULT 'public_provenance',
  parent_claim_id TEXT,
  frame_id TEXT,
  -- Prevalence/representativeness metadata (ethnographic authority context)
  informant_coverage TEXT,              -- e.g., "12/47 informants", "widespread", "isolated"
  contradicting_count INTEGER DEFAULT 0, -- count of contradicting evidence items (0 = none found)
  saturation_note TEXT,                  -- e.g., "Pattern consistent across all sites", "Only observed at Site Alpha"
  prevalence_basis TEXT CHECK (prevalence_basis IN ('representative','illustrative','singular','aggregate')),
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (paper_id) REFERENCES paper(paper_id),
  FOREIGN KEY (parent_claim_id) REFERENCES claim(claim_id)
);

CREATE TABLE IF NOT EXISTS claim_revision (
  revision_id INTEGER PRIMARY KEY AUTOINCREMENT,
  claim_id TEXT NOT NULL,
  old_text TEXT NOT NULL,
  new_text TEXT NOT NULL,
  old_confidence REAL,
  new_confidence REAL,
  reason TEXT,
  revised_by TEXT,
  created_at TEXT NOT NULL,
  FOREIGN KEY (claim_id) REFERENCES claim(claim_id)
);

CREATE TABLE IF NOT EXISTS evidence (
  evidence_id TEXT PRIMARY KEY,
  paper_id TEXT NOT NULL,
  evidence_type TEXT NOT NULL,
  summary TEXT NOT NULL,
  sensitivity_tier TEXT NOT NULL CHECK (sensitivity_tier IN ('PUBLIC','CONTROLLED','WITNESS_ONLY')),
  reident_risk TEXT DEFAULT 'low' CHECK (reident_risk IN ('low','medium','high')),  -- deductive disclosure risk
  reident_notes TEXT,  -- why this risk level (small community, unique role, etc.)
  meta_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY (paper_id) REFERENCES paper(paper_id)
);

CREATE TABLE IF NOT EXISTS claim_evidence_link (
  claim_id TEXT NOT NULL,
  evidence_id TEXT NOT NULL,
  relation TEXT NOT NULL CHECK (relation IN ('supports','challenges','illustrates','qualifies','necessitates')),
  weight TEXT DEFAULT 'supporting' CHECK (weight IN ('central','supporting','peripheral')),
  note TEXT,
  analytic_note TEXT,  -- ATI-style: explains HOW evidence supports/challenges claim (interpretive reasoning)
  verification_status TEXT DEFAULT 'unverified' CHECK (verification_status IN ('unverified','author_verified','external_verified')),
  verified_by TEXT,
  verified_at TEXT,
  created_at TEXT NOT NULL,
  PRIMARY KEY (claim_id, evidence_id, relation),
  FOREIGN KEY (claim_id) REFERENCES claim(claim_id),
  FOREIGN KEY (evidence_id) REFERENCES evidence(evidence_id)
);

-- Aguinis & Solarino (2019) 12 transparency criteria for qualitative research
-- These are typically addressed in methods but can be tracked here for completeness
CREATE TABLE IF NOT EXISTS transparency_checklist (
  paper_id TEXT PRIMARY KEY,
  -- Research Design (criteria 1-4)
  c1_research_question TEXT,           -- Is the research question clearly stated?
  c2_theoretical_framework TEXT,       -- Is theoretical framework explained?
  c3_sampling_strategy TEXT,           -- Is sampling strategy described?
  c4_saturation TEXT,                  -- Was theoretical saturation reached? How defined?
  -- Measurement (criteria 5-8)
  c5_interview_protocol TEXT,          -- Is interview protocol available/described?
  c6_interview_context TEXT,           -- Are interview conditions described?
  c7_informant_selection TEXT,         -- How were informants identified/selected?
  c8_unexpected_events TEXT,           -- Were unexpected challenges documented?
  -- Data Analysis (criteria 9-12)
  c9_coding_process TEXT,              -- Is coding process described?
  c10_intercoder_reliability TEXT,     -- Was intercoder reliability assessed?
  c11_analysis_software TEXT,          -- What software was used?
  c12_data_availability TEXT,          -- Are data/excerpts available?
  -- Meta
  completed_by TEXT,
  completed_at TEXT,
  notes TEXT,
  FOREIGN KEY (paper_id) REFERENCES paper(paper_id)
);

-- Audit trail for verification actions
CREATE TABLE IF NOT EXISTS verification_audit (
  audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
  action_type TEXT NOT NULL CHECK (action_type IN ('claim_verify','link_verify','claim_update','evidence_update')),
  target_id TEXT NOT NULL,  -- claim_id or evidence_id or "claim_id:evidence_id" for links
  old_status TEXT,
  new_status TEXT,
  reviewer TEXT NOT NULL,
  notes TEXT,
  created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_claim_paper ON claim(paper_id);
CREATE INDEX IF NOT EXISTS idx_evidence_paper ON evidence(paper_id);
CREATE INDEX IF NOT EXISTS idx_link_claim ON claim_evidence_link(claim_id);
CREATE INDEX IF NOT EXISTS idx_link_evidence ON claim_evidence_link(evidence_id);
CREATE INDEX IF NOT EXISTS idx_audit_target ON verification_audit(target_id);
CREATE INDEX IF NOT EXISTS idx_audit_reviewer ON verification_audit(reviewer);
