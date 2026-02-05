"""
BibTeX importer for Zotero and other reference managers.

Parses .bib files and stores references in state.json for use in
citation management and bibliography generation.
"""

import json
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class Reference:
    """A bibliographic reference."""

    # Core identifiers
    citekey: str  # e.g., "eisenhardt1989building"
    entry_type: str  # article, book, inproceedings, etc.

    # Standard fields
    title: str = ""
    author: str = ""
    year: str = ""
    journal: str = ""
    volume: str = ""
    number: str = ""
    pages: str = ""
    publisher: str = ""
    booktitle: str = ""  # For conference papers

    # Identifiers
    doi: str = ""
    isbn: str = ""
    issn: str = ""
    url: str = ""

    # Abstract and notes
    abstract: str = ""
    keywords: str = ""
    notes: str = ""

    # Metadata
    imported_at: str = field(default_factory=lambda: datetime.now().isoformat())
    source_file: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for JSON storage."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Reference":
        """Deserialize from JSON."""
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

    def matches(self, other: "Reference") -> bool:
        """Check if this reference matches another (for deduplication)."""
        # Match by DOI (strongest)
        if self.doi and other.doi:
            return self.doi.lower() == other.doi.lower()

        # Match by citekey
        if self.citekey and other.citekey:
            return self.citekey.lower() == other.citekey.lower()

        # Match by title similarity (fuzzy)
        if self.title and other.title:
            t1 = re.sub(r"[^\w\s]", "", self.title.lower())
            t2 = re.sub(r"[^\w\s]", "", other.title.lower())
            return t1 == t2

        return False


def parse_bibtex(content: str) -> List[Reference]:
    """
    Parse BibTeX content into Reference objects.

    This is a lightweight parser that handles most common BibTeX formats.
    For complex cases, consider using the bibtexparser library.

    Args:
        content: Raw BibTeX string

    Returns:
        List of Reference objects
    """
    references = []

    # Pattern for BibTeX entries
    # @type{citekey,
    #   field = {value},
    #   ...
    # }
    entry_pattern = r"@(\w+)\s*\{\s*([^,]+)\s*,([^@]*?)\n\s*\}"

    for match in re.finditer(entry_pattern, content, re.DOTALL):
        entry_type = match.group(1).lower()
        citekey = match.group(2).strip()
        fields_str = match.group(3)

        # Parse fields
        fields = _parse_fields(fields_str)

        ref = Reference(
            citekey=citekey,
            entry_type=entry_type,
            title=fields.get("title", ""),
            author=fields.get("author", ""),
            year=fields.get("year", ""),
            journal=fields.get("journal", ""),
            volume=fields.get("volume", ""),
            number=fields.get("number", ""),
            pages=fields.get("pages", ""),
            publisher=fields.get("publisher", ""),
            booktitle=fields.get("booktitle", ""),
            doi=fields.get("doi", ""),
            isbn=fields.get("isbn", ""),
            issn=fields.get("issn", ""),
            url=fields.get("url", ""),
            abstract=fields.get("abstract", ""),
            keywords=fields.get("keywords", ""),
            notes=fields.get("note", ""),
        )

        references.append(ref)

    return references


def _parse_fields(fields_str: str) -> Dict[str, str]:
    """Parse BibTeX field assignments."""
    fields = {}

    # Pattern for field = {value} or field = "value" or field = value
    field_pattern = r"(\w+)\s*=\s*(?:\{([^}]*)\}|\"([^\"]*)\"|(\d+))"

    for match in re.finditer(field_pattern, fields_str, re.DOTALL):
        field_name = match.group(1).lower()
        # Value is in one of three groups
        value = match.group(2) or match.group(3) or match.group(4) or ""
        # Clean up whitespace
        value = " ".join(value.split())
        fields[field_name] = value

    return fields


def import_bibtex_file(
    bib_path: Path,
    state_path: Path,
) -> Tuple[int, int, int]:
    """
    Import references from a BibTeX file into state.json.

    Args:
        bib_path: Path to .bib file
        state_path: Path to state.json

    Returns:
        Tuple of (total_parsed, new_added, duplicates_skipped)
    """
    # Read and parse BibTeX
    with open(bib_path, "r", encoding="utf-8") as f:
        content = f.read()

    parsed_refs = parse_bibtex(content)

    # Mark source file
    for ref in parsed_refs:
        ref.source_file = str(bib_path)

    # Load existing state
    if state_path.exists():
        with open(state_path, "r") as f:
            state = json.load(f)
    else:
        state = {}

    # Get existing references
    existing_refs = [
        Reference.from_dict(r) for r in state.get("references", [])
    ]

    # Deduplicate
    new_refs = []
    duplicates = 0

    for ref in parsed_refs:
        is_duplicate = any(ref.matches(existing) for existing in existing_refs)
        if is_duplicate:
            duplicates += 1
        else:
            new_refs.append(ref)
            existing_refs.append(ref)  # Add to existing for subsequent dedup

    # Update state
    state["references"] = [r.to_dict() for r in existing_refs]
    state["updated_at"] = datetime.now().isoformat()

    # Write back
    with open(state_path, "w") as f:
        json.dump(state, f, indent=2)

    return len(parsed_refs), len(new_refs), duplicates


def deduplicate_references(references: List[Reference]) -> List[Reference]:
    """
    Remove duplicate references from a list.

    Args:
        references: List of Reference objects

    Returns:
        Deduplicated list (preserves first occurrence)
    """
    unique = []
    for ref in references:
        if not any(ref.matches(u) for u in unique):
            unique.append(ref)
    return unique


def export_to_bibtex(references: List[Reference]) -> str:
    """
    Export references back to BibTeX format.

    Args:
        references: List of Reference objects

    Returns:
        BibTeX string
    """
    lines = []

    for ref in references:
        lines.append(f"@{ref.entry_type}{{{ref.citekey},")

        # Add non-empty fields
        field_order = [
            ("author", ref.author),
            ("title", ref.title),
            ("journal", ref.journal),
            ("booktitle", ref.booktitle),
            ("year", ref.year),
            ("volume", ref.volume),
            ("number", ref.number),
            ("pages", ref.pages),
            ("publisher", ref.publisher),
            ("doi", ref.doi),
            ("url", ref.url),
            ("abstract", ref.abstract),
            ("keywords", ref.keywords),
        ]

        for field_name, value in field_order:
            if value:
                # Escape special characters
                value = value.replace("{", "\\{").replace("}", "\\}")
                lines.append(f"  {field_name} = {{{value}}},")

        lines.append("}")
        lines.append("")

    return "\n".join(lines)
