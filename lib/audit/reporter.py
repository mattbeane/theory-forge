"""
Audit report formatting.

Generates markdown reports and methods appendix sections from decision logs.
"""

from datetime import datetime
from pathlib import Path
from typing import List, Optional

from .tracker import Decision, DecisionType, get_decisions, get_decisions_by_stage


def format_audit_trail(
    state_path: Path,
    stage: Optional[str] = None,
    include_reasoning: bool = True,
    include_alternatives: bool = True,
) -> str:
    """
    Format the audit trail as markdown.

    Args:
        state_path: Path to state.json
        stage: Optional stage filter
        include_reasoning: Include detailed reasoning
        include_alternatives: Include alternatives considered

    Returns:
        Markdown string
    """
    if stage:
        decisions = get_decisions_by_stage(state_path, stage)
        title = f"# Audit Trail: {stage.replace('_', ' ').title()}"
    else:
        decisions = get_decisions(state_path)
        title = "# Complete Audit Trail"

    if not decisions:
        return f"{title}\n\n*No decisions logged yet.*\n"

    lines = [title, ""]

    # Group by stage
    stages_seen = []
    for d in decisions:
        if d.stage not in stages_seen:
            stages_seen.append(d.stage)

    for stage_name in stages_seen:
        stage_decisions = [d for d in decisions if d.stage == stage_name]
        lines.append(f"## {stage_name.replace('_', ' ').title()}")
        lines.append("")

        for d in stage_decisions:
            lines.extend(_format_decision(d, include_reasoning, include_alternatives))
            lines.append("")

    return "\n".join(lines)


def _format_decision(
    decision: Decision,
    include_reasoning: bool = True,
    include_alternatives: bool = True,
) -> List[str]:
    """Format a single decision."""
    lines = []

    # Header
    timestamp = datetime.fromisoformat(decision.timestamp).strftime("%Y-%m-%d %H:%M")
    action_icon = _get_action_icon(decision.action)
    lines.append(f"### {action_icon} {decision.entity_label}")
    lines.append(f"*{decision.id} | {timestamp}*")
    lines.append("")

    # Description
    lines.append(f"**Decision:** {decision.description}")
    lines.append("")

    # Reasoning
    if include_reasoning and decision.reasoning:
        lines.append(f"**Reasoning:** {decision.reasoning}")
        lines.append("")

    # Evidence
    if decision.supporting_evidence:
        lines.append("**Supporting evidence:**")
        for e in decision.supporting_evidence:
            lines.append(f"- {e}")
        lines.append("")

    if decision.challenging_evidence:
        lines.append("**Challenging evidence:**")
        for e in decision.challenging_evidence:
            lines.append(f"- {e}")
        lines.append("")

    # Alternatives
    if include_alternatives and decision.alternatives_considered:
        lines.append("**Alternatives considered:**")
        for a in decision.alternatives_considered:
            lines.append(f"- {a}")
        lines.append("")

    # Confidence
    confidence_icon = {"high": "🟢", "medium": "🟡", "low": "🔴"}.get(
        decision.confidence, "⚪"
    )
    lines.append(f"**Confidence:** {confidence_icon} {decision.confidence.upper()}")

    # CC linkage
    if decision.claude_turn_id:
        lines.append(f"**CC Turn:** `{decision.claude_turn_id}`")

    lines.append("")
    lines.append("---")

    return lines


def _get_action_icon(action: str) -> str:
    """Get icon for action type."""
    icons = {
        "accepted": "✅",
        "selected": "✅",
        "rejected": "❌",
        "flagged": "⚠️",
        "passed": "✅",
        "failed": "❌",
        "identified": "🔍",
        "generated": "📝",
        "verified": "✓",
    }
    return icons.get(action.lower(), "•")


def format_methods_appendix(
    state_path: Path,
    paper_title: str = "Untitled Paper",
) -> str:
    """
    Generate a methods appendix section from the audit trail.

    This creates a narrative suitable for inclusion in a paper's
    online appendix or supplementary materials.

    Args:
        state_path: Path to state.json
        paper_title: Title for the appendix

    Returns:
        Markdown string suitable for a methods appendix
    """
    decisions = get_decisions(state_path)

    if not decisions:
        return "# Analytical Decisions\n\n*No decisions logged.*\n"

    lines = [
        "# Analytical Decisions",
        "",
        f"*Methods appendix for: {paper_title}*",
        "",
        "This appendix documents key analytical decisions made during the research process, ",
        "including the reasoning behind pattern selection, theoretical framing choices, ",
        "and evidence evaluation.",
        "",
    ]

    # Pattern Selection section
    pattern_decisions = [
        d
        for d in decisions
        if d.decision_type
        in (DecisionType.PATTERN_SELECTED, DecisionType.PATTERN_REJECTED)
    ]
    if pattern_decisions:
        lines.extend(_format_pattern_section(pattern_decisions))

    # Theory Selection section
    theory_decisions = [
        d
        for d in decisions
        if d.decision_type
        in (DecisionType.THEORY_SELECTED, DecisionType.LENS_SELECTED)
    ]
    if theory_decisions:
        lines.extend(_format_theory_section(theory_decisions))

    # Qualitative Decisions section
    qual_decisions = [
        d
        for d in decisions
        if d.decision_type
        in (
            DecisionType.MECHANISM_IDENTIFIED,
            DecisionType.QUOTE_SELECTED,
            DecisionType.DISCONFIRMING_NOTED,
        )
    ]
    if qual_decisions:
        lines.extend(_format_qual_section(qual_decisions))

    # Framing Decisions section
    frame_decisions = [
        d
        for d in decisions
        if d.decision_type
        in (
            DecisionType.FRAME_GENERATED,
            DecisionType.FRAME_SELECTED,
            DecisionType.FRAME_REJECTED,
        )
    ]
    if frame_decisions:
        lines.extend(_format_framing_section(frame_decisions))

    return "\n".join(lines)


def _format_pattern_section(decisions: List[Decision]) -> List[str]:
    """Format pattern selection section for methods appendix."""
    lines = [
        "## Pattern Selection",
        "",
    ]

    selected = [d for d in decisions if d.action in ("accepted", "selected")]
    rejected = [d for d in decisions if d.action == "rejected"]

    if selected:
        for d in selected:
            lines.append(f"### {d.entity_label}")
            lines.append("")
            lines.append(f"We identified **{d.entity_label}** as a core empirical pattern based on:")
            lines.append("")
            for e in d.supporting_evidence:
                lines.append(f"- {e}")
            lines.append("")
            if d.reasoning:
                lines.append(f"{d.reasoning}")
                lines.append("")

    if rejected:
        lines.append("### Patterns Considered but Not Pursued")
        lines.append("")
        for d in rejected:
            lines.append(f"- **{d.entity_label}**: {d.reasoning}")
        lines.append("")

    return lines


def _format_theory_section(decisions: List[Decision]) -> List[str]:
    """Format theory selection section for methods appendix."""
    lines = [
        "## Theoretical Positioning",
        "",
    ]

    for d in decisions:
        if d.decision_type == DecisionType.THEORY_SELECTED:
            lines.append(f"### Primary Theory: {d.entity_label}")
        else:
            lines.append(f"### Sensitizing Literature: {d.entity_label}")
        lines.append("")
        lines.append(d.reasoning)
        lines.append("")

    return lines


def _format_qual_section(decisions: List[Decision]) -> List[str]:
    """Format qualitative analysis section for methods appendix."""
    lines = [
        "## Qualitative Analysis",
        "",
    ]

    mechanisms = [
        d for d in decisions if d.decision_type == DecisionType.MECHANISM_IDENTIFIED
    ]
    if mechanisms:
        lines.append("### Mechanisms Identified")
        lines.append("")
        for d in mechanisms:
            lines.append(f"**{d.entity_label}**: {d.description}")
            lines.append("")

    disconfirming = [
        d for d in decisions if d.decision_type == DecisionType.DISCONFIRMING_NOTED
    ]
    if disconfirming:
        lines.append("### Disconfirming Evidence")
        lines.append("")
        lines.append(
            "We actively searched for evidence that challenged our interpretation:"
        )
        lines.append("")
        for d in disconfirming:
            lines.append(f"- {d.description}")
        lines.append("")

    return lines


def _format_framing_section(decisions: List[Decision]) -> List[str]:
    """Format framing decisions section for methods appendix."""
    lines = [
        "## Theoretical Framing",
        "",
    ]

    selected = [d for d in decisions if d.action == "selected"]
    rejected = [d for d in decisions if d.action == "rejected"]

    if selected:
        d = selected[0]  # Usually one selected frame
        lines.append(f"### Selected Framing: {d.entity_label}")
        lines.append("")
        lines.append(d.reasoning)
        lines.append("")

    if rejected:
        lines.append("### Alternative Framings Considered")
        lines.append("")
        for d in rejected:
            lines.append(f"**{d.entity_label}**: {d.reasoning}")
            lines.append("")

    return lines


def format_decision_summary(state_path: Path) -> str:
    """
    Format a brief summary of decisions for status displays.

    Returns something like:
    "12 decisions: 3 patterns selected, 2 rejected, 5 quotes, 2 frames"
    """
    decisions = get_decisions(state_path)

    if not decisions:
        return "No decisions logged"

    # Count by type
    type_counts = {}
    for d in decisions:
        key = d.decision_type.value.replace("_", " ")
        type_counts[key] = type_counts.get(key, 0) + 1

    total = len(decisions)
    summary_parts = [f"{count} {type_name}" for type_name, count in type_counts.items()]

    return f"{total} decisions: {', '.join(summary_parts[:4])}" + (
        "..." if len(summary_parts) > 4 else ""
    )
