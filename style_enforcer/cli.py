#!/usr/bin/env python3
"""
Command-line interface for style enforcer validation.

Usage:
    # Pattern-based validation only (fast, no LLM)
    python -m style_enforcer.cli paper.tex --paper-type qual_forward
    python -m style_enforcer.cli paper.docx --paper-type qual_forward

    # Full validation including cross-section coherence (requires LLM)
    python -m style_enforcer.cli paper.tex --paper-type qual_forward --coherence

    # Coherence validation only
    python -m style_enforcer.cli paper.tex --coherence-only

Supported formats: .tex (LaTeX), .docx (Word), .md (Markdown)
"""

import argparse
import re
import sys
from pathlib import Path

from .config import PaperType
from .loaders import load_document, detect_format
from .validator import StyleValidator, ValidationResult


def strip_latex_commands(text: str) -> str:
    """Remove common LaTeX commands for cleaner validation."""
    # Remove comments
    text = re.sub(r'%.*$', '', text, flags=re.MULTILINE)

    # Remove common commands but preserve text content
    # \textit{text} -> text
    text = re.sub(r'\\textit\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\textbf\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\emph\{([^}]*)\}', r'\1', text)

    # Remove \cite{...}
    text = re.sub(r'\\cite[pt]?\{[^}]*\}', '', text)

    # Remove \label{...} and \ref{...}
    text = re.sub(r'\\(label|ref|eqref)\{[^}]*\}', '', text)

    # Remove figure/table environments (content handled separately)
    text = re.sub(r'\\begin\{(figure|table)\}.*?\\end\{\1\}', '', text, flags=re.DOTALL)

    return text


def run_pattern_validation(
    sections: dict[str, str],
    paper_type: PaperType,
    doc_format: str = 'latex',
) -> dict[str, ValidationResult]:
    """Run pattern-based validation on all sections."""
    validator = StyleValidator(paper_type=paper_type)
    results = {}

    for section_name, content in sections.items():
        # Only strip LaTeX commands for LaTeX documents
        if doc_format == 'latex':
            clean_content = strip_latex_commands(content)
        else:
            clean_content = content
        result = validator.validate(
            clean_content,
            section_name=section_name,
        )
        results[section_name] = result

    return results


def run_coherence_validation(
    sections: dict[str, str],
    llm_client,
    doc_format: str = 'latex',
) -> "CoherenceReport":
    """Run cross-section coherence validation."""
    from .coherence_validator import CoherenceValidator

    # Clean sections for coherence analysis (only for LaTeX)
    if doc_format == 'latex':
        clean_sections = {
            name: strip_latex_commands(content)
            for name, content in sections.items()
        }
    else:
        clean_sections = sections

    validator = CoherenceValidator(llm_client)
    return validator.validate(clean_sections)


def print_pattern_results(results: dict[str, ValidationResult]) -> int:
    """Print pattern validation results. Returns total violation count."""
    total_hard = 0
    total_soft = 0

    print("=" * 60)
    print("PATTERN-BASED VALIDATION RESULTS")
    print("=" * 60)

    for section_name, result in results.items():
        if not result.violations:
            continue

        print(f"\n{section_name}:")
        print("-" * 40)

        for v in result.violations:
            icon = "\u274c" if v.severity.value == "hard" else "\u26a0\ufe0f"
            print(f"  {icon} [{v.severity.value.upper()}] {v.type.value}")
            print(f"     {v.message}")
            if v.location:
                loc = v.location[:60] + "..." if len(v.location) > 60 else v.location
                print(f"     Location: {loc}")
            if v.suggestion:
                print(f"     Suggestion: {v.suggestion}")
            print()

        total_hard += result.hard_violation_count
        total_soft += result.soft_violation_count

    print("-" * 60)
    print(f"Total: {total_hard} hard violations, {total_soft} soft violations")

    if total_hard == 0 and total_soft == 0:
        print("\u2705 No pattern violations found!")

    return total_hard + total_soft


def get_llm_client():
    """
    Get an LLM client for coherence validation.

    Tries to import and configure an Anthropic client.
    Override this function for different LLM providers.
    """
    try:
        import anthropic
        client = anthropic.Anthropic()

        # Wrap the client to match expected interface
        class LLMWrapper:
            def __init__(self, client):
                self.client = client

            def chat(self, prompt: str) -> str:
                response = self.client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=4096,
                    messages=[{"role": "user", "content": prompt}],
                )
                return response.content[0].text

        return LLMWrapper(client)

    except ImportError:
        print("Error: anthropic package not installed.")
        print("Install with: pip install anthropic")
        sys.exit(1)
    except Exception as e:
        print(f"Error initializing LLM client: {e}")
        print("Ensure ANTHROPIC_API_KEY is set.")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Validate academic paper style for management journals"
    )
    parser.add_argument(
        "paper_path",
        type=str,
        help="Path to paper file (.tex, .docx, or .md)",
    )
    parser.add_argument(
        "--paper-type",
        type=str,
        choices=["qual_forward", "quant_forward"],
        default="qual_forward",
        help="Paper type (default: qual_forward)",
    )
    parser.add_argument(
        "--coherence",
        action="store_true",
        help="Include cross-section coherence validation (requires LLM)",
    )
    parser.add_argument(
        "--coherence-only",
        action="store_true",
        help="Only run coherence validation, skip pattern checks",
    )
    parser.add_argument(
        "--section",
        type=str,
        help="Only validate a specific section (by name)",
    )

    args = parser.parse_args()

    # Load paper
    paper_path = Path(args.paper_path)
    if not paper_path.exists():
        print(f"Error: File not found: {paper_path}")
        sys.exit(1)

    # Detect format and load document
    try:
        doc_format = detect_format(paper_path)
        sections = load_document(paper_path)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except ImportError as e:
        print(f"Error: {e}")
        sys.exit(1)

    if not sections:
        print("Warning: No sections found in document")
        sys.exit(1)

    print(f"Format: {doc_format}")
    print(f"Found {len(sections)} sections: {', '.join(sections.keys())}")

    # Filter to specific section if requested
    if args.section:
        matching = {k: v for k, v in sections.items() if args.section.lower() in k.lower()}
        if not matching:
            print(f"Error: No section matching '{args.section}'")
            sys.exit(1)
        sections = matching

    # Determine paper type
    paper_type = PaperType.QUAL_FORWARD if args.paper_type == "qual_forward" else PaperType.QUANT_FORWARD

    violation_count = 0

    # Run pattern validation (unless coherence-only)
    if not args.coherence_only:
        results = run_pattern_validation(sections, paper_type, doc_format)
        violation_count += print_pattern_results(results)

    # Run coherence validation if requested
    if args.coherence or args.coherence_only:
        print("\n" + "=" * 60)
        print("Running cross-section coherence analysis...")
        print("(This requires LLM calls and may take a moment)")
        print("=" * 60 + "\n")

        llm_client = get_llm_client()
        report = run_coherence_validation(sections, llm_client, doc_format)
        print(report.format_report())
        violation_count += len(report.violations)

    # Exit code based on violations
    sys.exit(1 if violation_count > 0 else 0)


if __name__ == "__main__":
    main()
