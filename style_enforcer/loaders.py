"""
Document loaders for different file formats.

All loaders return dict[str, str] mapping section names to content.
The validation architecture is format-agnostic once text is extracted.
"""

from pathlib import Path
import re


def detect_format(path: Path) -> str:
    """Detect document format from extension."""
    suffix = path.suffix.lower()
    if suffix == '.tex':
        return 'latex'
    elif suffix == '.docx':
        return 'word'
    elif suffix == '.md':
        return 'markdown'
    else:
        raise ValueError(f"Unsupported format: {suffix}")


def load_latex(path: Path) -> dict[str, str]:
    """Load LaTeX document into sections."""
    content = path.read_text(encoding='utf-8')
    section_pattern = re.compile(r'\\section\*?\{([^}]+)\}', re.IGNORECASE)

    sections = {}
    matches = list(section_pattern.finditer(content))

    for i, match in enumerate(matches):
        name = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        sections[name] = content[start:end].strip()

    return sections


def load_markdown(path: Path) -> dict[str, str]:
    """Load Markdown document into sections."""
    content = path.read_text(encoding='utf-8')
    section_pattern = re.compile(r'^##\s+(.+)$', re.MULTILINE)

    sections = {}
    matches = list(section_pattern.finditer(content))

    for i, match in enumerate(matches):
        name = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        sections[name] = content[start:end].strip()

    return sections


def _is_section_keyword(text: str) -> bool:
    """Check if text matches common section header patterns."""
    text_lower = text.lower().strip()

    # Remove numbering (1. Introduction, I. Introduction, etc.)
    text_lower = re.sub(r'^[\divxIVX]+[\.\)]\s*', '', text_lower)

    keywords = [
        'introduction', 'abstract', 'background', 'literature review',
        'theory', 'theoretical', 'methods', 'methodology', 'research setting',
        'data', 'findings', 'results', 'analysis', 'discussion',
        'contributions', 'implications', 'conclusion', 'conclusions',
        'references', 'appendix', 'acknowledgments',
    ]

    return any(text_lower.startswith(kw) for kw in keywords)


def load_word(path: Path) -> dict[str, str]:
    """
    Load Word document into sections.

    Section detection strategy:
    1. Look for paragraphs with Heading 1 or Heading 2 styles
    2. Fall back to detecting ALL CAPS short paragraphs as headers
    3. Fall back to "Introduction", "Methods", etc. keywords
    """
    try:
        from docx import Document
    except ImportError:
        raise ImportError(
            "python-docx is required for Word document support. "
            "Install with: pip install python-docx"
        )

    doc = Document(path)
    sections = {}
    current_section = None
    current_content = []

    # Heading styles that indicate section boundaries
    heading_styles = {'Heading 1', 'Heading 2', 'Title', 'Heading'}

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        # Check if this paragraph is a section header
        is_header = False

        # Method 1: Check paragraph style
        if para.style and para.style.name in heading_styles:
            is_header = True

        # Method 2: Short ALL CAPS text (common in manuscripts)
        elif len(text) < 60 and text.isupper() and len(text) > 3:
            is_header = True

        # Method 3: Common section name patterns
        elif _is_section_keyword(text) and len(text) < 80:
            is_header = True

        if is_header:
            # Save previous section
            if current_section and current_content:
                sections[current_section] = '\n\n'.join(current_content)

            current_section = text
            current_content = []
        else:
            # Add to current section content
            current_content.append(text)

    # Save final section
    if current_section and current_content:
        sections[current_section] = '\n\n'.join(current_content)

    return sections


def load_document(path: Path) -> dict[str, str]:
    """
    Load document from any supported format.
    Auto-detects format from file extension.

    Args:
        path: Path to document file (.tex, .docx, or .md)

    Returns:
        Dictionary mapping section names to section content

    Raises:
        ValueError: If file format is not supported
        ImportError: If python-docx not installed (for .docx files)
    """
    fmt = detect_format(path)

    if fmt == 'latex':
        return load_latex(path)
    elif fmt == 'word':
        return load_word(path)
    elif fmt == 'markdown':
        return load_markdown(path)
    else:
        raise ValueError(f"Unsupported format: {fmt}")
