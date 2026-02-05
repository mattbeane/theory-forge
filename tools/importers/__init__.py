"""
Theory-Forge Importers

Import data from external research tools:
- BibTeX (.bib) from Zotero, Mendeley, etc.
- Atlas.ti exports
- (Future) NVivo exports
"""

from .bibtex import (
    parse_bibtex,
    import_bibtex_file,
    Reference,
    deduplicate_references,
)

__all__ = [
    "parse_bibtex",
    "import_bibtex_file",
    "Reference",
    "deduplicate_references",
]
