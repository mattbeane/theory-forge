#!/usr/bin/env python3
"""Check if user has required quals for a TheoryForge command.

Usage: python3 check_quals.py <command_name>
Exit 0 = allowed (or no student record = faculty mode)
Exit 1 = quals not met
Prints missing requirements to stderr on failure.
"""
import json
import sys
from pathlib import Path

UNLOCK_MAP = {
    "hunt-patterns": {"domain-1": 3},
    "find-theory": {"domain-1": 3, "domain-2": 3},
    "find-lens": {"domain-1": 3, "domain-2": 3},
    "mine-qual": {"domain-2": 3, "domain-3": 3},
    "smith-frames": {"domain-3": 3, "domain-4": 3},
    "eval-zuckerman": {"domain-3": 3, "domain-4": 3},
    "eval-genre": {"domain-4": 3, "domain-5": 3},
    "draft-paper": {"domain-4": 3, "domain-5": 3},
    "eval-limitations": {"domain-5": 3},
    "eval-citations": {"domain-5": 3},
    "audit-claims": {"domain-5": 3, "domain-6": 3},
    "verify-claims": {"domain-5": 3, "domain-6": 3},
    "package-verification": {"domain-6": 3, "domain-7": 3},
}

# Foundational skills (affect quality enforcement, not access)
# These do NOT gate command access. They affect the strictness of
# writing quality enforcement in commands that produce written output.
# See docs/ARGUMENT_CONSTRUCTION_RULES.md for the full rule reference.
FOUNDATION_MAP = {
    "argument-construction": {
        "affects": ["draft-paper", "build-lit-review"],
        "behavior": "quality_guidance",  # Not "gate"
    }
}

def check_foundation(command, record):
    """Check if a foundation skill is relevant to this command.
    Returns guidance message if foundation not yet demonstrated, None otherwise.
    """
    for foundation, config in FOUNDATION_MAP.items():
        if command in config["affects"]:
            foundation_level = (
                record.get("foundations", {})
                .get(foundation, {})
                .get("level", 0)
            )
            if foundation_level < 1:
                return (
                    f"Note: Argument Construction foundational skill not yet assessed.\n"
                    f"The draft will include argument construction rules as guidance.\n"
                    f"See docs/ARGUMENT_CONSTRUCTION_RULES.md for reference."
                )
    return None


def main():
    if len(sys.argv) < 2:
        sys.exit(0)

    command = sys.argv[1]
    if command not in UNLOCK_MAP:
        sys.exit(0)  # Ungated command

    record_path = Path.home() / ".skillforge" / "record.json"
    if not record_path.exists():
        sys.exit(0)  # No student record = faculty/expert mode

    record = json.loads(record_path.read_text())
    requirements = UNLOCK_MAP[command]

    missing = []
    for domain, level in requirements.items():
        student_level = record.get("domains", {}).get(domain, {}).get("level", 0)
        if student_level < level:
            missing.append(f"{domain} Level {level}")

    if missing:
        print(", ".join(missing), file=sys.stderr)
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()
