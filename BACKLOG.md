# Theory-Forge Backlog

## Priority 1: Immediate / High Impact

### 1.1 ~~Skill-Forge Gate for New Users~~ (Removed)
**Status:** Removed
**Why removed:** Premature to couple tool access to a competency framework that's still a draft. The competency work (ResearchKit Quals) and the tooling work (TheoryForge) are independent projects evolving separately. The right relationship between them is an open question — previous implementation overclaimed the maturity of both projects.

**What was there:** Experience check in `/init-project`, competency gating via `check_quals.py` and hooks, redirect to research-quals.
**What remains:** Quality gates based on workflow state (e.g., don't run `/find-theory` before `/hunt-patterns`). These are about pipeline sequencing, not competency assessment.

---

### 1.2 Guided First Project Experience
**Status:** ✅ Complete
**Why:** Current onboarding assumes expertise. New users see wall of commands.

**Implementation:**
- ✅ Added `--guided` flag to `/init-project`
- ✅ 6-step walkthrough with explanations
- ✅ Progress indicators: "STEP X OF 6"
- ✅ "Why this matters" for each component
- ✅ Full pipeline overview at completion

---

### 1.3 Failure Recovery with Specific Fixes
**Status:** ✅ Complete
**Why:** Gate failures feel like dead ends.

**Implementation:**
- ✅ Created `gate-failure-templates.md` with standardized messages for all gates
- ✅ Each failure includes: what happened, why it matters, 3-4 options for next steps
- ✅ Specific guidance per gate (A through F)
- ✅ "Common mistake" warnings
- ✅ Retry instructions

---

### 1.4 Modular Use (Run Single Evals)
**Status:** ✅ Complete
**Why:** Researchers with existing papers should be able to run just `/eval-genre` without full pipeline.

**Implementation:**
- ✅ Created `/eval` command for running any evaluation independently
- ✅ Usage: `/eval genre`, `/eval zuckerman --file paper.md`, `/eval becker --quick`
- ✅ `--quick` flag for verdict-only output
- ✅ `--fix` flag to generate suggested fixes
- ✅ Documents all available evaluations and when to use each

---

## Priority 2: Important / Medium Term

### 2.1 Example Worked Project
**Status:** Not started
**Why:** Users need to see what "done" looks like at each stage.

**Implementation:**
- Use surgery data → shadow learning paper as canonical example
- Create `/examples/shadow-learning/` with all artifacts
- Each pipeline stage has "here's what this looked like for shadow learning"
- Link from documentation

---

### 2.2 Messaging: AI-Assisted, Human-Directed
**Status:** ✅ Complete (partial - README updated)
**Why:** Reduce anxiety, clarify value prop.

**Implementation:**
- ✅ README: "This Tool Is For Experienced Researchers" section
- ✅ Clear "What it does" vs "What it doesn't do" lists
- ✅ "Researchers who can supervise AI are more valuable than ever"
- ✅ "Your job is to catch when the AI is wrong. That skill is why you're irreplaceable."
- ⏳ Pipeline output highlighting (future)
- ⏳ Credit lines on outputs (future)

---

### 2.3 Confidence Indicators
**Status:** ✅ Complete
**Why:** Users trust AI output too much or too little.

**Implementation:**
- ✅ Created `lib/consensus/formatters.py` with markdown formatting functions
- ✅ Stability badges: 🟢 HIGH, 🟡 MEDIUM, 🔴 LOW, ⚪ UNKNOWN
- ✅ Full confidence section formatter for command output
- ✅ Quote stability display for qualitative mining
- ✅ Flagged items callout for items needing review
- ✅ Updated `/hunt-patterns` to use formatters
- ✅ Updated `/mine-qual` to use formatters
- ✅ Created `docs/CONFIDENCE_INDICATORS.md` documentation

---

### 2.4 Import/Export Integration
**Status:** ✅ Complete (core)
**Why:** Researchers have existing tools.

**Implementation:**
- ✅ Created `tools/importers/bibtex.py` - Parse BibTeX from Zotero/Mendeley
- ✅ Reference dataclass with deduplication logic
- ✅ import_bibtex_file() stores refs in state.json
- ✅ Created `tools/exporters/docx.py` - Word export via pandoc
- ✅ export_with_bibliography() includes refs from state.json
- ✅ Created `tools/exporters/pdf.py` - PDF export via pandoc/LaTeX
- ✅ export_to_latex() for Overleaf with companion .bib file
- ✅ Updated `/import-refs` and `/export` commands
- ⏳ NVivo import (future)
- ⏳ Direct Overleaf push (future)

---

### 2.5 Audit Trail / Transparency
**Status:** ✅ Complete
**Why:** No black boxes.

**Implementation:**
- ✅ Created `lib/audit/` module with tracker, reporter, history
- ✅ Decision dataclass with full metadata (reasoning, alternatives, evidence)
- ✅ DecisionType enum covering all pipeline decision types
- ✅ log_decision() for structured decision logging to state.json
- ✅ format_audit_trail() for markdown output
- ✅ format_methods_appendix() for paper supplementary materials
- ✅ Claude Code history linkage via ~/.claude/history.jsonl
- ✅ Created `/audit-trail` command with filtering and export options

---

## Priority 3: Nice to Have / Long Term

### 3.1 Video Walkthroughs
**Status:** Not started
**Why:** Some users learn better watching.

**Implementation:**
- Record guided project walkthrough
- Stage-by-stage explanations
- "What to do when Gate D fails" video
- Host on YouTube, link from docs

---

### 3.2 Common Mistakes Documentation
**Status:** Not started
**Why:** Proactive failure prevention.

**Implementation:**
- For each gate: top 3 failure reasons
- Before/after examples
- "Red flag" patterns to avoid
- Add to `/docs/common-mistakes/`

---

### 3.3 Web Interface
**Status:** Not started
**Why:** Not everyone is comfortable with CLI.

**Implementation:**
- Web app wrapping core functionality
- Visual pipeline progress
- Point-and-click eval running
- Consider: hosted vs. self-hosted

---

### 3.4 Collaborative Mode
**Status:** Not started
**Why:** Research is often collaborative.

**Implementation:**
- Multi-user projects
- Track who made which decisions
- Comment threads on artifacts
- Version control integration

---

## Technical Debt

### T1: Consistent Output Formats
All commands should produce consistent markdown/JSON.

### T2: Error Handling
Graceful failures with helpful messages.

### T3: Testing
Automated tests for pipeline stages.

### T4: Documentation Audit
Ensure all commands are documented with examples.

---

## Completed

- [x] ~~P1.1: Research-quals gate for new users (2025-02-04)~~ — Removed: premature coupling
- [x] P1.2: Guided first project experience (2025-02-04)
- [x] P1.3: Failure recovery with specific fixes (2025-02-04)
- [x] P1.4: Modular eval use (2025-02-04)
- [x] P2.2: AI-assisted messaging (README portion) (2025-02-04)
- [x] Post-revision genre re-check warning (2025-02-04)
- [x] ~~Level 4 Capstone in research-quals (linked tool) (2025-02-04)~~ — Removed: premature coupling
- [x] ~~Ecosystem framing with research-quals (2025-02-04)~~ — Removed: premature coupling
- [x] P2.3: Confidence indicators in output (2025-02-04)
- [x] P2.5: Audit trail / transparency (2025-02-04)
- [x] P2.4: Import/Export integration (2025-02-04)

---

*Last updated: 2025-02-12*
