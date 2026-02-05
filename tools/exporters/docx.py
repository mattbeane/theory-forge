"""
Word document exporter using pandoc.

Converts markdown drafts to .docx with optional bibliography.
"""

import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import List, Optional, Tuple

from ..importers.bibtex import Reference, export_to_bibtex


def check_pandoc_available() -> bool:
    """Check if pandoc is installed and available."""
    return shutil.which("pandoc") is not None


def export_to_docx(
    markdown_path: Path,
    output_path: Path,
    reference_doc: Optional[Path] = None,
) -> Tuple[bool, str]:
    """
    Export markdown to Word document using pandoc.

    Args:
        markdown_path: Path to input .md file
        output_path: Path for output .docx file
        reference_doc: Optional Word template for styling

    Returns:
        Tuple of (success, message)
    """
    if not check_pandoc_available():
        return False, "Pandoc not found. Install with: brew install pandoc"

    if not markdown_path.exists():
        return False, f"Input file not found: {markdown_path}"

    cmd = [
        "pandoc",
        str(markdown_path),
        "-o", str(output_path),
        "--from", "markdown",
        "--to", "docx",
    ]

    if reference_doc and reference_doc.exists():
        cmd.extend(["--reference-doc", str(reference_doc)])

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )
        return True, f"Exported to {output_path}"
    except subprocess.CalledProcessError as e:
        return False, f"Pandoc error: {e.stderr}"


def export_with_bibliography(
    markdown_path: Path,
    output_path: Path,
    state_path: Path,
    csl_style: Optional[Path] = None,
    reference_doc: Optional[Path] = None,
) -> Tuple[bool, str]:
    """
    Export markdown to Word with bibliography from state.json references.

    Args:
        markdown_path: Path to input .md file
        output_path: Path for output .docx file
        state_path: Path to state.json (contains references)
        csl_style: Optional CSL file for citation formatting
        reference_doc: Optional Word template

    Returns:
        Tuple of (success, message)
    """
    if not check_pandoc_available():
        return False, "Pandoc not found. Install with: brew install pandoc"

    if not markdown_path.exists():
        return False, f"Input file not found: {markdown_path}"

    # Load references from state
    if not state_path.exists():
        return False, f"State file not found: {state_path}"

    with open(state_path, "r") as f:
        state = json.load(f)

    refs_data = state.get("references", [])
    if not refs_data:
        # No references, just do basic export
        return export_to_docx(markdown_path, output_path, reference_doc)

    # Convert to Reference objects and export to temp .bib
    references = [Reference.from_dict(r) for r in refs_data]
    bib_content = export_to_bibtex(references)

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".bib",
        delete=False,
        encoding="utf-8",
    ) as f:
        f.write(bib_content)
        bib_path = Path(f.name)

    try:
        cmd = [
            "pandoc",
            str(markdown_path),
            "-o", str(output_path),
            "--from", "markdown",
            "--to", "docx",
            "--bibliography", str(bib_path),
            "--citeproc",
        ]

        if csl_style and csl_style.exists():
            cmd.extend(["--csl", str(csl_style)])

        if reference_doc and reference_doc.exists():
            cmd.extend(["--reference-doc", str(reference_doc)])

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )

        return True, f"Exported to {output_path} with {len(references)} references"

    except subprocess.CalledProcessError as e:
        return False, f"Pandoc error: {e.stderr}"

    finally:
        # Clean up temp file
        bib_path.unlink(missing_ok=True)


def get_available_csl_styles() -> List[str]:
    """
    List commonly used CSL styles for academic writing.

    These can be downloaded from https://www.zotero.org/styles
    """
    return [
        "apa",  # American Psychological Association
        "asa",  # American Sociological Association
        "chicago-author-date",
        "chicago-note-bibliography",
        "harvard-cite-them-right",
        "ieee",
        "mla",
        "nature",
        "vancouver",
        "academy-of-management-review",  # AMR style
    ]
