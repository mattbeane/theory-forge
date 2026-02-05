"""
Consensus Engine for Paper Mining Agents

Provides statistical consensus through N-run execution with confidence intervals
and stability scoring.
"""

from .engine import (
    ConsensusEngine,
    ConsensusResult,
    MetricConsensus,
    QuoteConsensus,
    run_consensus,
)
from .stability import (
    StabilityRating,
    compute_stability,
    format_metric_for_paper,
    format_stability_badge,
    summarize_stabilities,
)
from .extractors import (
    extract_effect_sizes,
    extract_quotes,
    extract_claims,
    extract_cycle_time,
    get_extractor_for_stage,
)
from .config import (
    DEFAULT_CONFIG,
    get_stage_n,
    merge_config,
)
from .formatters import (
    format_confidence_section,
    format_metric_row,
    format_quote_row,
    format_metrics_inline,
    format_stability_summary,
    format_quote_list_with_stability,
    format_flagged_items_callout,
    stability_emoji,
    stability_label,
)

__all__ = [
    # Engine
    "ConsensusEngine",
    "ConsensusResult",
    "MetricConsensus",
    "QuoteConsensus",
    "run_consensus",
    # Stability
    "StabilityRating",
    "compute_stability",
    "format_metric_for_paper",
    "format_stability_badge",
    "summarize_stabilities",
    # Extractors
    "extract_effect_sizes",
    "extract_quotes",
    "extract_claims",
    "extract_cycle_time",
    "get_extractor_for_stage",
    # Config
    "DEFAULT_CONFIG",
    "get_stage_n",
    "merge_config",
    # Formatters (markdown output)
    "format_confidence_section",
    "format_metric_row",
    "format_quote_row",
    "format_metrics_inline",
    "format_stability_summary",
    "format_quote_list_with_stability",
    "format_flagged_items_callout",
    "stability_emoji",
    "stability_label",
]
