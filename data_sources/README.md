# Data Sources

This directory contains documentation for each data source supported by theory-forge.

## Built-in Sources

- **CSV / Excel**: Native support, no importer needed
- **Plain text transcripts**: Native support — place in `data/qual/interviews/` or `data/qual/fieldnotes/`
- **BibTeX**: Import via `/import-refs` (importer at `tools/importers/bibtex.py`)

## Adding a New Data Source

Run `/author-data-source [tool-name]` to generate:
1. A Python importer at `tools/importers/[name].py`
2. A documentation file in this directory
3. A registry entry in `registry.json`

See the [Contributing section](../README.md#contributing-add-your-own-data-sources--methodologies) in the README.
