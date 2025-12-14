# Repository Architecture: living-paper vs paper-mining-agents

## Two Repos, Two Purposes

### `living-paper` (github.com/mattbeane/living-paper)

**Purpose**: Shareable library for the research community

**Audience**: Other researchers adopting living paper methodology

**Philosophy**: Minimal, documented, reusable

**Contents**:
- `lp.py` (~600 lines) - Core CLI
- `anonymize.py`, `hasher.py`, `vault.py`, `visualize.py` - Supporting tools
- `docs/` - Newcomer documentation (GETTING_STARTED.md, FOR_REVIEWERS.md, CONCEPTS.md)
- `examples/` - Sample data for learning

**Commands**: init, ingest, lint, export, verify-export, prereview

---

### `paper-mining-agent-suite/living_paper/`

**Purpose**: Working application for actual paper verification

**Audience**: Matt (and collaborators on specific papers)

**Philosophy**: Feature-rich, handles real PII concerns, generates reviewer packages

**Contents**:
- `lp.py` (~1300 lines) - Extended CLI with additional commands
- `reviewer_app.py` - Flask web interface for verification
- `redact.py` - Entity-based PII redaction system
- `entities_example.yaml` - Template for PII mappings
- Actual paper data in `analysis/`

**Additional Commands**: migrate-redact, export-html, export-package

---

## The Relationship

```
living-paper (LIBRARY)              paper-mining-agent-suite/living_paper/ (APPLICATION)
├── Core schema                     ├── Same core schema
├── init/ingest/lint/export         ├── Same + migrate-redact, export-html, export-package
├── Generic anonymize.py            ├── + redact.py (entity-based PII)
├── Basic docs for adopters         ├── + reviewer_app.py (Flask web UI)
└── Examples for learning           └── + entities.yaml (actual PII mappings)
```

**Flow is one-directional**: Develop in paper-mining-agent-suite → backport generic parts to living-paper

---

## Why Separate?

1. **Different audiences**: living-paper teaches the methodology; paper-mining-agent-suite uses it
2. **Sensitivity boundary**: paper-mining-agent-suite contains actual research data, entities.yaml with real PII mappings
3. **Feature stability**: living-paper stays lean while paper-mining-agent-suite can experiment
4. **Publication alignment**: Methodology papers cite the clean living-paper repo

---

## Sync Workflow

When a feature in paper-mining-agent-suite is generic enough for others:

1. **Identify generic portion** - Strip project-specific details
2. **Port to living-paper** - Add to lp.py or as new module
3. **Document for newcomers** - Add to appropriate doc in living-paper/docs/
4. **Bump version** - living-paper follows semver (v0.1 → v0.2, etc.)

Features that stay in paper-mining-agent-suite only:
- `entities.yaml` (real PII mappings)
- `reviewer_app.py` (overkill for most users - static HTML is enough)
- Project-specific analysis scripts

---

## Current State (Dec 2025)

| Feature | living-paper | paper-mining-agent-suite |
|---------|--------------|---------------------|
| Core schema | ✓ v0.1 | ✓ v0.5 (extended) |
| init/ingest/lint/export | ✓ | ✓ |
| prereview | ✓ | ✓ |
| PII redaction | ✗ | ✓ redact.py |
| Static HTML export | ✗ | ✓ export-html |
| Reviewer packages | ✗ | ✓ export-package |
| Flask web UI | ✗ | ✓ reviewer_app.py |
| Prevalence metadata | ✗ | ✓ (schema extended) |
| Contradiction badges | ✗ | ✓ |

**Next sync candidates**:
- Prevalence metadata fields (informant_coverage, etc.)
- Static HTML export (export-html) - valuable for any user
- Contradiction badge display

---

## Future Options

If the sync overhead becomes painful:

**Option A: pip-installable living-paper**
```
pip install living-paper
```
Then paper-mining-agent-suite imports it and extends. Requires stabilizing API.

**Option B: Plugin architecture**
```python
# paper-mining-agent-suite/living_paper_ext/
from living_paper import lp
lp.register_command('export-html', export_html_cmd)
```

For now, manual sync is fine - a few features per quarter.
