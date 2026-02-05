"""
Markdown formatters for consensus results.

Surfaces statistical confidence and stability information in command output,
making consensus results visible to researchers rather than just storing them
in state.json.
"""

from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .engine import ConsensusResult, MetricConsensus, QuoteConsensus

from .stability import StabilityRating


def stability_emoji(stability: StabilityRating) -> str:
    """Return colored emoji for stability rating."""
    return {
        StabilityRating.HIGH: "🟢",
        StabilityRating.MEDIUM: "🟡",
        StabilityRating.LOW: "🔴",
        StabilityRating.UNKNOWN: "⚪",
    }.get(stability, "⚪")


def stability_label(stability: StabilityRating) -> str:
    """Return label with emoji for stability rating."""
    emoji = stability_emoji(stability)
    return f"{emoji} {stability.value.upper()}"


def format_confidence_section(
    result: "ConsensusResult",
    include_metrics: bool = True,
    include_quotes: bool = True,
    include_flags: bool = True,
) -> str:
    """
    Format a full confidence assessment section for markdown output.

    Returns a markdown string like:

    ## Confidence Assessment

    ### Metrics
    | Finding | Value | 95% CI | CV | Stability |
    |---------|-------|--------|-----|-----------|
    | Effect size (β) | 0.38 | [0.34, 0.42] | 8% | 🟢 HIGH |

    ### Quote Stability
    ...

    ### Flags for Review
    ...
    """
    sections = []

    sections.append("## Confidence Assessment")
    sections.append("")
    sections.append(f"*Based on {result.n_runs} consensus runs ({result.model})*")
    sections.append("")

    # Overall assessment
    overall = stability_label(result.overall_stability)
    sections.append(f"**Overall Stability:** {overall}")
    sections.append("")

    # Metrics table
    if include_metrics and result.metrics:
        sections.append("### Metrics")
        sections.append("")
        sections.append("| Finding | Value | 95% CI | CV | Stability |")
        sections.append("|---------|-------|--------|-----|-----------|")

        for name, metric in result.metrics.items():
            row = format_metric_row(metric)
            sections.append(row)

        sections.append("")

    # Quote stability table
    if include_quotes and result.quotes:
        sections.append("### Quote Stability")
        sections.append("")
        sections.append("| Quote (truncated) | Appearances | Rate | Stability |")
        sections.append("|-------------------|-------------|------|-----------|")

        for quote in result.quotes:
            row = format_quote_row(quote)
            sections.append(row)

        sections.append("")

    # Flags for review
    if include_flags and result.flagged_items:
        sections.append("### ⚠️ Flags for Review")
        sections.append("")
        for flag in result.flagged_items:
            sections.append(f"- {flag}")
        sections.append("")

    # Execution metadata
    sections.append("### Execution Details")
    sections.append("")
    sections.append(f"- **Runs:** {result.n_runs}")
    sections.append(f"- **Time:** {result.execution_time_seconds:.1f}s")
    sections.append(f"- **Tokens:** {result.total_tokens:,}")
    sections.append(f"- **Est. Cost:** ${result.estimated_cost_usd:.2f}")
    sections.append("")

    return "\n".join(sections)


def format_metric_row(metric: "MetricConsensus", precision: int = 2) -> str:
    """Format a single metric as a table row."""
    name = metric.name

    if not metric.values:
        return f"| {name} | — | — | — | ⚪ UNKNOWN |"

    value = round(metric.mean, precision)
    ci_low = round(metric.ci_lower, precision)
    ci_high = round(metric.ci_upper, precision)
    cv_pct = round(metric.cv * 100, 1)

    stability = stability_label(metric.stability)

    return f"| {name} | {value} | [{ci_low}, {ci_high}] | {cv_pct}% | {stability} |"


def format_quote_row(quote: "QuoteConsensus", max_length: int = 50) -> str:
    """Format a single quote as a table row."""
    # Truncate quote text for table display
    text = quote.text
    if len(text) > max_length:
        text = text[:max_length-3] + "..."

    # Escape pipe characters for markdown table
    text = text.replace("|", "\\|")

    rate_pct = round(quote.appearance_rate * 100, 0)
    stability = stability_label(quote.stability)

    return f"| {text} | {quote.appearances}/{quote.total_runs} | {rate_pct}% | {stability} |"


def format_metrics_inline(result: "ConsensusResult", precision: int = 2) -> str:
    """
    Format metrics as inline text for embedding in prose.

    Returns something like:
    "Effect size β=0.38 (95% CI: [0.34, 0.42], 🟢 HIGH stability)"
    """
    if not result.metrics:
        return ""

    parts = []
    for name, metric in result.metrics.items():
        if not metric.values:
            continue

        value = round(metric.mean, precision)
        ci_low = round(metric.ci_lower, precision)
        ci_high = round(metric.ci_upper, precision)
        emoji = stability_emoji(metric.stability)

        parts.append(
            f"{name}={value} (95% CI: [{ci_low}, {ci_high}], {emoji} {metric.stability.value.upper()})"
        )

    return "; ".join(parts)


def format_stability_summary(result: "ConsensusResult") -> str:
    """
    Format a brief stability summary for status displays.

    Returns something like:
    "🟢 HIGH (3 metrics, 5 quotes, 0 flags)"
    """
    overall = stability_label(result.overall_stability)
    n_metrics = len(result.metrics) if result.metrics else 0
    n_quotes = len(result.quotes) if result.quotes else 0
    n_flags = len(result.flagged_items)

    parts = []
    if n_metrics:
        parts.append(f"{n_metrics} metrics")
    if n_quotes:
        parts.append(f"{n_quotes} quotes")
    if n_flags:
        parts.append(f"{n_flags} flags")

    detail = ", ".join(parts) if parts else "no data"
    return f"{overall} ({detail})"


def format_quote_list_with_stability(
    quotes: List["QuoteConsensus"],
    show_low_stability: bool = True,
    warn_low_stability: bool = True,
) -> str:
    """
    Format quotes as a markdown list with stability indicators.

    Suitable for embedding in findings sections.
    """
    if not quotes:
        return "*No quotes extracted*"

    lines = []

    for quote in quotes:
        if not show_low_stability and quote.stability == StabilityRating.LOW:
            continue

        emoji = stability_emoji(quote.stability)
        stability_note = ""

        if warn_low_stability and quote.stability == StabilityRating.LOW:
            stability_note = " ⚠️ *verify manually*"

        # Format: > "Quote text" — Informant (emoji STABILITY)
        lines.append(f'> "{quote.text}"')
        lines.append(f'> — {quote.informant} ({emoji} {quote.stability.value.upper()}{stability_note})')
        lines.append("")

    return "\n".join(lines)


def format_flagged_items_callout(result: "ConsensusResult") -> str:
    """
    Format flagged items as a warning callout box.

    Returns markdown for a callout/admonition block.
    """
    if not result.flagged_items:
        return ""

    lines = [
        "> **⚠️ Items Flagged for Manual Review**",
        ">",
    ]

    for flag in result.flagged_items:
        lines.append(f"> - {flag}")

    lines.append(">")
    lines.append("> *Low stability items should be verified against raw data before publication.*")

    return "\n".join(lines)
