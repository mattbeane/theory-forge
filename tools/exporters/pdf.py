"""
PDF exporter using pandoc.

Converts markdown drafts to PDF with optional bibliography.
Requires a LaTeX distribution (e.g., MacTeX, TeX Live).
"""

import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Tuple

from ..importers.bibtex import Reference, export_to_bibtex
from .docx import check_pandoc_available


def check_latex_available() -> bool:
    """Check if pdflatex is installed and available."""
    return shutil.which("pdflatex") is not None


def export_to_pdf(
    markdown_path: Path,
    output_path: Path,
    state_path: Optional[Path] = None,
    csl_style: Optional[Path] = None,
    template: Optional[Path] = None,
) -> Tuple[bool, str]:
    """
    Export markdown to PDF using pandoc and LaTeX.

    Args:
        markdown_path: Path to input .md file
        output_path: Path for output .pdf file
        state_path: Optional path to state.json for bibliography
        csl_style: Optional CSL file for citation formatting
        template: Optional LaTeX template

    Returns:
        Tuple of (success, message)
    """
    if not check_pandoc_available():
        return False, "Pandoc not found. Install with: brew install pandoc"

    if not check_latex_available():
        return False, "LaTeX not found. Install MacTeX or TeX Live for PDF export."

    if not markdown_path.exists():
        return False, f"Input file not found: {markdown_path}"

    cmd = [
        "pandoc",
        str(markdown_path),
        "-o", str(output_path),
        "--from", "markdown",
        "--to", "pdf",
        "--pdf-engine", "pdflatex",
    ]

    if template and template.exists():
        cmd.extend(["--template", str(template)])

    # Handle bibliography if state_path provided
    bib_path = None
    if state_path and state_path.exists():
        with open(state_path, "r") as f:
            state = json.load(f)

        refs_data = state.get("references", [])
        if refs_data:
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

            cmd.extend([
                "--bibliography", str(bib_path),
                "--citeproc",
            ])

    if csl_style and csl_style.exists():
        cmd.extend(["--csl", str(csl_style)])

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )

        msg = f"Exported to {output_path}"
        if bib_path:
            msg += f" with bibliography"

        return True, msg

    except subprocess.CalledProcessError as e:
        return False, f"Pandoc/LaTeX error: {e.stderr}"

    finally:
        # Clean up temp file
        if bib_path:
            bib_path.unlink(missing_ok=True)


def export_to_latex(
    markdown_path: Path,
    output_path: Path,
    state_path: Optional[Path] = None,
) -> Tuple[bool, str]:
    """
    Export markdown to LaTeX source (for Overleaf upload).

    Args:
        markdown_path: Path to input .md file
        output_path: Path for output .tex file
        state_path: Optional path to state.json for bibliography

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
        "--to", "latex",
        "--standalone",
    ]

    # Generate companion .bib file if references exist
    bib_output_path = output_path.with_suffix(".bib")

    if state_path and state_path.exists():
        with open(state_path, "r") as f:
            state = json.load(f)

        refs_data = state.get("references", [])
        if refs_data:
            references = [Reference.from_dict(r) for r in refs_data]
            bib_content = export_to_bibtex(references)

            with open(bib_output_path, "w", encoding="utf-8") as f:
                f.write(bib_content)

            cmd.extend([
                "--bibliography", str(bib_output_path),
                "--biblatex",
            ])

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )

        msg = f"Exported to {output_path}"
        if bib_output_path.exists():
            msg += f" and {bib_output_path}"
        msg += " (ready for Overleaf)"

        return True, msg

    except subprocess.CalledProcessError as e:
        return False, f"Pandoc error: {e.stderr}"
