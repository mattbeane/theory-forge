# Manuscript Exporter

You are the EXPORT agent. Your job is to convert the manuscript to different formats using pandoc.

## Arguments

- `$ARGUMENTS` - Target format(s): `latex`, `word`, `pdf`, `html`, or `all`

## Prerequisites

- `output/manuscript.md` or `output/manuscript.tex` must exist
- `output/references.bib` should exist for citations
- Pandoc must be installed (check with `which pandoc`)

## Supported Formats

| Format | Output File | Notes |
|--------|-------------|-------|
| `latex` | `output/exports/manuscript.tex` | For Overleaf/journal submission |
| `word` | `output/exports/manuscript.docx` | For Word-based journals/coauthors |
| `pdf` | `output/exports/manuscript.pdf` | For quick review (requires LaTeX) |
| `html` | `output/exports/manuscript.html` | For web sharing/preview |
| `all` | All of the above | Full export |

## Steps

1. **Check prerequisites**

   ```bash
   # Verify pandoc is installed
   which pandoc || echo "Pandoc not found. Install with: brew install pandoc"

   # Check for manuscript
   test -f output/manuscript.md || test -f output/manuscript.tex
   ```

2. **Create export directory**

   ```bash
   mkdir -p output/exports
   ```

3. **Export to requested format(s)**

   ### LaTeX Export
   ```bash
   pandoc output/manuscript.md \
     --from markdown \
     --to latex \
     --bibliography output/references.bib \
     --citeproc \
     --standalone \
     -o output/exports/manuscript.tex
   ```

   ### Word Export
   ```bash
   pandoc output/manuscript.md \
     --from markdown \
     --to docx \
     --bibliography output/references.bib \
     --citeproc \
     --reference-doc=templates/reference.docx \
     -o output/exports/manuscript.docx
   ```

   ### PDF Export
   ```bash
   pandoc output/manuscript.md \
     --from markdown \
     --to pdf \
     --bibliography output/references.bib \
     --citeproc \
     --pdf-engine=xelatex \
     -o output/exports/manuscript.pdf
   ```

   ### HTML Export
   ```bash
   pandoc output/manuscript.md \
     --from markdown \
     --to html \
     --bibliography output/references.bib \
     --citeproc \
     --standalone \
     --toc \
     -o output/exports/manuscript.html
   ```

4. **Apply journal-specific templates (if specified)**

   Check `state.json` for `metadata.target_journal` and apply appropriate template:

   | Journal | Template | Notes |
   |---------|----------|-------|
   | Management Science | `templates/mgmt-sci.tex` | Formal structure |
   | ASQ | `templates/asq.tex` | Theory emphasis |
   | AMJ | `templates/amj.tex` | Clear H1/H2/H3 |
   | Organization Science | `templates/orgsci.tex` | Exploratory ok |

5. **Copy supporting files**

   ```bash
   # Copy tables
   cp -r output/tables output/exports/

   # Copy figures
   cp -r output/figures output/exports/

   # Copy bibliography
   cp output/references.bib output/exports/
   ```

6. **Create submission package**

   If exporting for journal submission:

   ```bash
   cd output/exports
   zip -r submission_package.zip \
     manuscript.tex \
     references.bib \
     tables/ \
     figures/
   ```

## Output

```
╔══════════════════════════════════════════════════════════════════╗
║  EXPORT COMPLETE                                                 ║
╚══════════════════════════════════════════════════════════════════╝

Exported to: output/exports/

  ✓ manuscript.tex      (LaTeX)     142 KB
  ✓ manuscript.docx     (Word)      89 KB
  ✓ manuscript.pdf      (PDF)       234 KB
  ✓ manuscript.html     (HTML)      67 KB

Supporting files:
  ✓ references.bib      (45 references)
  ✓ tables/             (3 files)
  ✓ figures/            (2 files)

─────────────────────────────────────────────────────────────────────
SUBMISSION PACKAGES
─────────────────────────────────────────────────────────────────────

For Overleaf:
  → Upload output/exports/submission_package.zip

For journal portal:
  → manuscript.docx or manuscript.pdf
  → Figures as separate files if required

─────────────────────────────────────────────────────────────────────
FORMATTING NOTES
─────────────────────────────────────────────────────────────────────

Target journal: [from state.json]

- [ ] Check citation format matches journal style
- [ ] Verify table/figure numbering
- [ ] Review anonymization in all formats
- [ ] Check word count meets requirements

─────────────────────────────────────────────────────────────────────
```

## If Pandoc Not Installed

```
╔══════════════════════════════════════════════════════════════════╗
║  PANDOC NOT FOUND                                                ║
╚══════════════════════════════════════════════════════════════════╝

Pandoc is required for format conversion but was not found.

Install options:

macOS:
  brew install pandoc

Ubuntu/Debian:
  sudo apt-get install pandoc

Windows:
  choco install pandoc

Or download from: https://pandoc.org/installing.html

For PDF export, you also need LaTeX:
  brew install --cask mactex-no-gui

After installing, run /export again.
```

## Journal Template Stubs

If a journal template is specified but doesn't exist, create a stub:

```latex
% templates/[journal].tex
% Template for [Journal Name]
%
% To customize:
% 1. Download official template from journal website
% 2. Replace this file
% 3. Re-run /export latex

\documentclass[12pt]{article}
\usepackage{natbib}
\usepackage{graphicx}

% Journal-specific formatting goes here

\begin{document}
$body$
\end{document}
```

## Update State

After export:
1. Update `state.json`:
   - Add export paths to `workflow.draft_paper.outputs`
   - Update `updated_at` timestamp
2. Append entry to `DECISION_LOG.md` noting export
