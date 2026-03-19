# Changelog

All notable changes to the Paper Mining Agent Suite will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

#### Statistical Consensus Mode
- **`/consensus-config`** - Configure statistical consensus settings for defensible analysis
- **`lib/consensus/`** - Python library for N-run execution with statistical aggregation
  - `engine.py` - Async execution engine supporting Anthropic and OpenAI
  - `extractors.py` - Metric and quote extraction from LLM responses
  - `stability.py` - CV calculation, confidence intervals, stability ratings
  - `config.py` - Default thresholds and per-stage configuration
- **Consensus-enabled stages**:
  - `/hunt-patterns` - Effect sizes with confidence intervals (n=25 default)
  - `/mine-qual` - Quote stability tracking (n=15 default)
  - `/verify-claims` - Claim defensibility ratings (n=10 default)
- **Stability ratings**: HIGH (CV<10%), MEDIUM (CV 10-25%), LOW (CV>25%)
- **Quote stability**: Tracks appearance rate across N runs to catch cherry-picking
- State schema updated to v1.1.0 with `consensus` configuration block
- Output formats enhanced with stability tables and flagged items

#### State Persistence & Project Management
- **`/init-project`** - Initialize new paper projects with full directory structure and `state.json` tracking
- **`/switch-project`** - Switch between papers in multi-project workspaces
- **`/status`** - View comprehensive workflow progress with visual indicators
- **`state.json`** - Centralized state tracking for workflow progress, frame iterations, and metadata

#### Frame Shift Support
- **`/new-frame`** - Create new theoretical frame iterations, archiving previous attempts
- **`/new-frame list`** - View all frame attempts with status
- **`/new-frame compare`** - Compare framings side-by-side
- Frame-aware output paths: `analysis/framing/frame-1/`, `frame-2/`, etc.
- Automatic preservation of empirical work (data exploration, patterns) across frames

#### Quality Gates (Hooks)
- Pre-skill validation via `.claude/hooks.json`
- Warns when running skills out of sequence
- Checks for required prerequisite outputs before proceeding
- Non-blocking warnings (can still proceed if needed)

#### Verification & Export
- **`/package-verification`** - Automatically create ZIP packages for external review
- **`templates/PRESUBMISSION_REVIEW_INSTRUCTIONS.md`** - Detailed instructions for external reviewers to provide thorough, constructive feedback (Major Issues, Claim-by-Claim Assessment, Clarity Checks, Evidence Audit, Theory Stress Test, etc.)
- Checksums for reproducibility verification
- README generation for reviewers
- **`/export [format]`** - Convert manuscripts to LaTeX, Word, PDF, HTML via pandoc
- Journal-specific template support
- Submission package creation

#### Reference Management
- **`/import-refs bibtex [file]`** - Import from BibTeX files
- **`/import-refs zotero [collection]`** - Zotero integration guide
- **`/import-refs doi [doi]`** - Fetch references by DOI from CrossRef
- **`/import-refs search [query]`** - Search Semantic Scholar and import
- Duplicate detection and bibliography status reporting

### Changed

#### Existing Commands Updated
- All 8 original skills now include State Management sections
- Commands read/write to `state.json` on completion
- Commands append to `DECISION_LOG.md` automatically
- Frame-aware output paths for theory/lens/qual/framing stages
- `/status` tip added to all skill completion messages

#### Directory Structure Enhanced
```
project/
├── data/
│   ├── quant/
│   └── qual/
│       ├── interviews/
│       └── fieldnotes/
├── analysis/
│   ├── exploration/
│   ├── patterns/
│   ├── framing/
│   │   ├── frame-1/
│   │   │   ├── theory/
│   │   │   ├── qualitative/
│   │   │   └── FRAMING_OPTIONS.md
│   │   └── frame-2/
│   └── verification/
├── literature/
│   ├── primary/
│   ├── sensitizing/
│   └── refs.bib
├── output/
│   ├── drafts/
│   ├── exports/
│   ├── tables/
│   └── figures/
├── PROJECT_CONTEXT.md
├── DECISION_LOG.md
└── state.json
```

### Multi-Project Support
- Workspace mode with `workspace.json` tracking multiple papers
- Shared literature directory across projects
- Project switching with status summary
- Independent state tracking per project

---

## [0.1.0] - 2024-XX-XX

### Added
- Initial release with 8 core agents:
  - `/explore-data` - Data reconnaissance
  - `/hunt-patterns` - Pattern identification
  - `/find-theory` - Theory violation identification
  - `/find-lens` - Sensitizing literature search
  - `/mine-qual` - Qualitative evidence extraction
  - `/smith-frames` - Framing generation
  - `/verify-claims` - Verification package creation
  - `/draft-paper` - Manuscript generation
- `templates/PROJECT_SETUP.md` - Manual setup guide
- `WORKFLOW_DIAGRAM.md` - Visual workflow documentation
- Basic `.gitignore` for data protection
