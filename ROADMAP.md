# Roadmap

Product roadmap for paper-mining-agent-suite and the living-paper ecosystem.

**Status key:** ✅ Shipped | 🚧 In Progress | 📋 Planned | 💭 Exploring

---

## Now (Shipped)

### Core Pipeline
- ✅ Full agent workflow: explore → patterns → puzzle check → theory → lens → qual mining → framing → audit → verify → draft
- ✅ Zuckerman criteria integration (two-stage: lite + full)
- ✅ Frame management (`/new-frame`, compare, archive)
- ✅ State tracking (`state.json`) with quality gate warnings
- ✅ Style enforcer module for ASQ/OrgSci/ManSci register

### Living Paper Integration
- ✅ Bundled `living_paper/` — no separate install needed
- ✅ `/audit-claims` generates LP-compatible files (claims.jsonl, evidence.jsonl, links.csv)
- ✅ `/verify-claims` auto-runs LP commands (init, ingest, lint, export-package)
- ✅ Reviewer packages: standalone HTML, double-click launchers, no CLI for reviewers
- ✅ Entity redaction tools for IRB compliance
- ✅ Contradiction badges in reviewer interface

### Documentation
- ✅ State schema documentation (`docs/STATE_SCHEMA.md`)
- ✅ Workflow diagram
- ✅ Zuckerman criteria reference (bundled PDF)
- ✅ Nguyen-Welch comparison (positioning vs. AI-qual critiques)

---

## Next (Near-term)

### Adoption & Onboarding
- 📋 **Golden path demo**: `examples/` folder with sample dataset + expected outputs
- 📋 **`make demo`** or **`/demo`** command to generate sample project end-to-end
- 📋 **Quickstart video** (3-5 min) showing clone → first pattern report

### Data Governance
- 📋 **Sanitize script**: Nuke all input data, caches, logs — leave only code + final outputs
- 📋 **Pre-commit hook**: Block commits containing common PII patterns
- 📋 **Governance section in README**: IRB-friendly language for ethics boards

### Quality of Life
- 📋 **Better error messages**: When agents fail, explain why and suggest fixes
- 📋 **`/doctor` command**: Diagnose common setup issues (missing files, bad state, etc.)

---

## Later (Planned)

### Accessibility
- 💭 **Docker/DevContainer**: One-click setup, no local Python/CLI knowledge needed
- 💭 **Web UI wrapper**: Streamlit or similar — run agents from browser
- 💭 **VS Code extension**: Sidebar for workflow status, run agents from command palette

### Model Flexibility
- 💭 **Model-agnostic backend**: LiteLLM or similar — swap Claude for GPT-4, Llama, etc.
- 💭 **Local model support**: Run fully offline with Ollama + capable open model
- 💭 **Cost tracking**: Estimate/report token usage per agent run

### Living Paper Enhancements
- 💭 **Markdown input**: Write claims inline in your draft, compile to structured format
- 💭 **Quote anchoring**: Verify quoted text exists verbatim in source transcripts
- 💭 **Lazy-load HTML**: Chunk large reviewer packages to avoid file bloat
- 💭 **Diff view**: Show what changed between verification package versions

### Research Workflow
- 💭 **Multi-paper workspace**: Shared literature library across projects
- 💭 **Citation integration**: Direct Zotero/BibTeX sync
- 💭 **Reviewer response mode**: Track R&R changes, regenerate verification for revised claims

---

## Ideas (Exploring)

Not committed. Might be good, might not. Open for discussion.

- **Journal-specific templates**: Pre-configured style rules for target journals
- **Collaborative mode**: Multiple researchers on same project with merge/conflict handling
- **Pre-registration export**: Commit evidence structure before writing narrative (novel for qual)
- **Replication packages**: Auto-generate materials for data repositories (ICPSR, OSF)
- **Teaching mode**: Verbose explanations at each step for methods courses
- **Audit log**: Immutable record of all agent decisions for transparency

---

## Contributing

See something you want to build? Open an issue to discuss before PRing.

Priorities:
1. Things that reduce friction for new users
2. Things that increase rigor/verifiability
3. Things that make the workflow faster for power users

---

## Changelog

- **2024-12-14**: Seamless Living Paper integration (auto-ingest, auto-export-package)
- **2024-12-14**: Fixed clone URL, added state schema docs, CITATION.cff for living-paper
