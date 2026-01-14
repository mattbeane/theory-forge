#!/usr/bin/env python3
"""
Validate all exemplar papers to check for false positives in the validator suite.

These are all published papers in top journals, so any violations detected
are likely false positives that need fixing in the validators.
"""

import re
import sys
from pathlib import Path
from collections import defaultdict

from .config import PaperType
from .validator import StyleValidator, ValidationResult, ViolationType


EXEMPLAR_DIR = Path("/Users/mattbeane/Desktop/Exemplar MDs")


def parse_markdown_sections(content: str) -> dict[str, str]:
    """
    Parse markdown content into sections based on ## headers.
    """
    # Pattern to match ## Section Name
    section_pattern = re.compile(r'^##\s+(.+)$', re.MULTILINE)

    sections = {}
    matches = list(section_pattern.finditer(content))

    for i, match in enumerate(matches):
        section_name = match.group(1).strip()

        # Get content from this section to the next (or end)
        start = match.end()
        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(content)

        section_content = content[start:end].strip()
        sections[section_name] = section_content

    return sections


def get_section_type(section_name: str) -> str | None:
    """Map section name to a standard type for validation context."""
    name_lower = section_name.lower()

    if any(k in name_lower for k in ["intro", "introduction"]):
        return "introduction"
    elif any(k in name_lower for k in ["theory", "theoretical", "background", "literature", "lens", "sensitizing"]):
        return "theory"
    elif any(k in name_lower for k in ["method", "setting", "data", "research site"]):
        return "methods"
    elif any(k in name_lower for k in ["finding", "result", "empirical", "analysis"]):
        return "findings"
    elif any(k in name_lower for k in ["discussion", "contribution", "implication"]):
        return "discussion"
    elif any(k in name_lower for k in ["conclusion"]):
        return "conclusion"
    return None


def validate_paper(paper_path: Path, validator: StyleValidator) -> dict:
    """Validate a single paper and return results."""
    content = paper_path.read_text(encoding="utf-8")
    sections = parse_markdown_sections(content)

    results = {
        "paper": paper_path.stem,
        "section_count": len(sections),
        "violations_by_section": {},
        "violations_by_type": defaultdict(list),
        "total_hard": 0,
        "total_soft": 0,
    }

    for section_name, section_content in sections.items():
        section_type = get_section_type(section_name)

        result = validator.validate(
            section_content,
            section_name=section_type,
        )

        if result.violations:
            results["violations_by_section"][section_name] = result.violations
            for v in result.violations:
                results["violations_by_type"][v.type.value].append({
                    "section": section_name,
                    "location": v.location,
                    "message": v.message,
                })

        results["total_hard"] += result.hard_violation_count
        results["total_soft"] += result.soft_violation_count

    return results


def print_summary(all_results: list[dict]):
    """Print summary of all validation results."""
    print("=" * 80)
    print("EXEMPLAR PAPER VALIDATION SUMMARY")
    print("=" * 80)
    print()

    # Per-paper summary
    print("PER-PAPER RESULTS:")
    print("-" * 80)
    for r in all_results:
        status = "✅ CLEAN" if r["total_hard"] == 0 and r["total_soft"] == 0 else "⚠️  ISSUES"
        print(f"{status} {r['paper'][:50]:<50} Hard: {r['total_hard']:>2}  Soft: {r['total_soft']:>2}")

    # Aggregate by violation type
    print()
    print("VIOLATIONS BY TYPE (across all papers):")
    print("-" * 80)

    type_counts = defaultdict(int)
    type_examples = defaultdict(list)

    for r in all_results:
        for vtype, violations in r["violations_by_type"].items():
            type_counts[vtype] += len(violations)
            for v in violations[:2]:  # Keep first 2 examples per paper
                type_examples[vtype].append({
                    "paper": r["paper"][:30],
                    "section": v["section"][:20],
                    "location": v["location"][:60] if v["location"] else "N/A",
                })

    for vtype, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"\n{vtype}: {count} occurrences")
        for ex in type_examples[vtype][:3]:  # Show first 3 examples
            print(f"  - {ex['paper']} / {ex['section']}")
            print(f"    Location: {ex['location']}")

    # Totals
    total_hard = sum(r["total_hard"] for r in all_results)
    total_soft = sum(r["total_soft"] for r in all_results)

    print()
    print("=" * 80)
    print(f"TOTALS: {total_hard} hard violations, {total_soft} soft violations")
    print(f"Papers with issues: {sum(1 for r in all_results if r['total_hard'] > 0 or r['total_soft'] > 0)}/{len(all_results)}")
    print("=" * 80)

    if total_hard > 0 or total_soft > 0:
        print()
        print("⚠️  These are published exemplar papers - violations are likely FALSE POSITIVES")
        print("   Review patterns above to identify overly aggressive rules.")


def main():
    if not EXEMPLAR_DIR.exists():
        print(f"Error: Exemplar directory not found: {EXEMPLAR_DIR}")
        sys.exit(1)

    # Get all markdown files
    md_files = sorted(EXEMPLAR_DIR.glob("*.md"))

    if not md_files:
        print(f"Error: No markdown files found in {EXEMPLAR_DIR}")
        sys.exit(1)

    print(f"Found {len(md_files)} exemplar papers to validate")
    print()

    # Create validator (qual-forward since these are all qual papers)
    validator = StyleValidator(paper_type=PaperType.QUAL_FORWARD)

    # Validate each paper
    all_results = []
    for paper_path in md_files:
        if paper_path.name.startswith("."):
            continue
        print(f"Validating: {paper_path.name}...")
        results = validate_paper(paper_path, validator)
        all_results.append(results)

    print()
    print_summary(all_results)


if __name__ == "__main__":
    main()
