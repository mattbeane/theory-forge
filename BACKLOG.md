# Theory-Forge Backlog

## Priority 1: Immediate / High Impact

### 1.1 Skill-Forge Gate for New Users
**Status:** ✅ Complete
**Why:** PhD students may use theory-forge as a crutch before developing judgment. The tool should detect this and redirect.

**Implementation:**
- ✅ Added to `/init-project` - Step 0: Experience Check
- ✅ Prompt: "Have you independently written and submitted (or published) a mixed-methods paper?"
- ✅ If no: Warning message with skill-forge redirect
- ✅ Three options: proceed anyway (logged), go to skill-forge, cancel
- ✅ Decisions logged to DECISION_LOG.md

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
**Status:** Not started
**Why:** Users trust AI output too much or too little.

**Implementation:**
- Pattern recognition: Show confidence level
- Mechanism identification: Flag uncertainty
- Claim verification: Mark strength of evidence links
- Color coding: Green (high confidence) → Yellow (verify) → Red (uncertain)

---

### 2.4 Import/Export Integration
**Status:** Atlas.ti parser exists; others don't
**Why:** Researchers have existing tools.

**Implementation:**
- NVivo import
- Overleaf export (direct push)
- Word export
- Zotero integration for references

---

### 2.5 Audit Trail / Transparency
**Status:** state.json exists but incomplete
**Why:** No black boxes.

**Implementation:**
- Log every AI decision with reasoning
- Reviewable trail: "At 2:30pm, AI identified pattern X because..."
- Export audit trail for methods appendix

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

- [x] P1.1: Skill-forge gate for new users (2025-02-04)
- [x] P1.2: Guided first project experience (2025-02-04)
- [x] P1.3: Failure recovery with specific fixes (2025-02-04)
- [x] P1.4: Modular eval use (2025-02-04)
- [x] P2.2: AI-assisted messaging (README portion) (2025-02-04)
- [x] Post-revision genre re-check warning (2025-02-04)
- [x] Level 4 Capstone in skill-forge (linked tool) (2025-02-04)
- [x] Ecosystem framing with skill-forge (2025-02-04)

---

*Last updated: 2025-02-04*
