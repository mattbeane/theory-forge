# Theory-Forge Backlog

## Priority 1: Immediate / High Impact

### 1.1 Skill-Forge Gate for New Users
**Status:** Not started
**Why:** PhD students may use theory-forge as a crutch before developing judgment. The tool should detect this and redirect.

**Implementation:**
- Add `/init-project --first-time` flow
- Prompt: "Have you independently written and published (or submitted) a mixed-methods paper?"
- If no: "Theory-forge is powerful, but it works best when you already know how to write good papers. We recommend completing skill-forge training first: [link]. This ensures you can catch what AI gets wrong."
- If yes: Proceed normally
- Store user status in config so prompt doesn't repeat

---

### 1.2 Guided First Project Experience
**Status:** Not started
**Why:** Current onboarding assumes expertise. New users see wall of commands.

**Implementation:**
- Create `/init-project --guided`
- Step-by-step walkthrough with explanations at each stage
- "Why this gate?" explanations inline
- Progress indicators: "You're at stage 3 of 10"
- Estimated time remaining

---

### 1.3 Failure Recovery with Specific Fixes
**Status:** Partial (genre eval does this)
**Why:** Gate failures feel like dead ends.

**Implementation:**
- Every gate failure should output:
  - What specifically failed
  - Why it matters
  - Concrete next steps
  - Example of what "passing" looks like
- Template for all gate outputs

---

### 1.4 Modular Use (Run Single Evals)
**Status:** Works but not documented
**Why:** Researchers with existing papers should be able to run just `/eval-genre` without full pipeline.

**Implementation:**
- Document standalone eval usage
- Remove pipeline-only assumptions from eval commands
- Add `/check-paper` command that runs all Gate D evals on any .tex or .md file

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
**Status:** Not started
**Why:** Reduce anxiety, clarify value prop.

**Implementation:**
- Update README with clear framing
- Add "Philosophy" section explaining human-AI collaboration model
- Pipeline output should highlight human decision points: "You selected... You confirmed... You approved..."
- Credit line on outputs: "Generated with theory-forge, directed by [user]"

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

- [x] Post-revision genre re-check warning (2025-02-04)
- [x] Level 4 Capstone in skill-forge (linked tool) (2025-02-04)

---

*Last updated: 2025-02-04*
