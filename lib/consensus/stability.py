"""
Stability calculations for consensus results.

Computes coefficient of variation (CV), confidence intervals,
and assigns stability ratings based on configurable thresholds.
"""

from enum import Enum
from typing import TYPE_CHECKING
import statistics
import math

if TYPE_CHECKING:
    from .engine import MetricConsensus

from .config import DEFAULT_CONFIG


class StabilityRating(Enum):
    """Stability classification based on coefficient of variation."""

    HIGH = "high"  # CV < 10% - defensible
    MEDIUM = "medium"  # CV 10-25% - mostly defensible, note variance
    LOW = "low"  # CV > 25% - ambiguous, flag for review
    UNKNOWN = "unknown"  # Insufficient data


def compute_stability(
    metric: "MetricConsensus",
    config: dict = None,
) -> "MetricConsensus":
    """
    Compute statistical measures and stability rating for a metric.

    Args:
        metric: MetricConsensus with values populated
        config: Thresholds for stability ratings

    Returns:
        Same MetricConsensus with statistics filled in
    """
    config = config or DEFAULT_CONFIG
    values = metric.values

    if not values:
        metric.stability = StabilityRating.UNKNOWN
        return metric

    n = len(values)

    # Basic statistics
    metric.mean = statistics.mean(values)
    metric.median = statistics.median(values)

    if n > 1:
        metric.std = statistics.stdev(values)

        # 95% confidence interval
        # CI = mean ± (t * std / sqrt(n))
        # Using z=1.96 for large n, t-value for small n
        if n >= 30:
            t_value = 1.96
        else:
            # Approximate t-value for 95% CI
            # More accurate would use scipy.stats.t.ppf
            t_values = {
                2: 12.71, 3: 4.30, 4: 3.18, 5: 2.78,
                6: 2.57, 7: 2.45, 8: 2.36, 9: 2.31, 10: 2.26,
                15: 2.14, 20: 2.09, 25: 2.06,
            }
            t_value = t_values.get(n, 2.0)

        margin = t_value * (metric.std / math.sqrt(n))
        metric.ci_lower = metric.mean - margin
        metric.ci_upper = metric.mean + margin

        # Coefficient of variation (CV = std / mean)
        # Only meaningful for ratio scales where 0 is meaningful
        if metric.mean != 0:
            metric.cv = abs(metric.std / metric.mean)
        else:
            metric.cv = float('inf') if metric.std > 0 else 0.0

    else:
        # Single value - can't compute variance
        metric.std = 0.0
        metric.ci_lower = metric.mean
        metric.ci_upper = metric.mean
        metric.cv = 0.0

    # Assign stability rating based on CV
    high_threshold = config.get("high_stability_cv", 0.10)
    medium_threshold = config.get("medium_stability_cv", 0.25)

    if n < 3:
        metric.stability = StabilityRating.UNKNOWN
    elif metric.cv < high_threshold:
        metric.stability = StabilityRating.HIGH
    elif metric.cv < medium_threshold:
        metric.stability = StabilityRating.MEDIUM
    else:
        metric.stability = StabilityRating.LOW

    return metric


def format_metric_for_paper(metric: "MetricConsensus", precision: int = 2) -> str:
    """
    Format a metric consensus for inclusion in a paper.

    Returns strings like:
        "β = 0.21 (±0.03 SD, 95% CI: [0.18, 0.24], n=25)"
    """
    if not metric.values:
        return "[No data]"

    n = len(metric.values)
    mean = round(metric.mean, precision)
    std = round(metric.std, precision)
    ci_low = round(metric.ci_lower, precision)
    ci_high = round(metric.ci_upper, precision)
    cv_pct = round(metric.cv * 100, 1)

    if n == 1:
        return f"{mean} (single run)"

    return (
        f"{mean} (±{std} SD, 95% CI: [{ci_low}, {ci_high}], "
        f"CV={cv_pct}%, n={n})"
    )


def format_stability_badge(stability: StabilityRating) -> str:
    """Return a text badge for stability rating."""
    badges = {
        StabilityRating.HIGH: "HIGH ✓",
        StabilityRating.MEDIUM: "MEDIUM ~",
        StabilityRating.LOW: "LOW ⚠️",
        StabilityRating.UNKNOWN: "UNKNOWN ?",
    }
    return badges.get(stability, "?")


def summarize_stabilities(metrics: dict) -> dict:
    """
    Summarize stability ratings across all metrics.

    Returns:
        {
            "high": 5,
            "medium": 2,
            "low": 1,
            "overall": "MEDIUM",
            "defensible": True/False
        }
    """
    counts = {
        StabilityRating.HIGH: 0,
        StabilityRating.MEDIUM: 0,
        StabilityRating.LOW: 0,
        StabilityRating.UNKNOWN: 0,
    }

    for metric in metrics.values():
        counts[metric.stability] += 1

    # Overall is determined by worst non-unknown rating
    if counts[StabilityRating.LOW] > 0:
        overall = "LOW"
        defensible = False
    elif counts[StabilityRating.MEDIUM] > 0:
        overall = "MEDIUM"
        defensible = True  # Mostly defensible
    elif counts[StabilityRating.HIGH] > 0:
        overall = "HIGH"
        defensible = True
    else:
        overall = "UNKNOWN"
        defensible = False

    return {
        "high": counts[StabilityRating.HIGH],
        "medium": counts[StabilityRating.MEDIUM],
        "low": counts[StabilityRating.LOW],
        "unknown": counts[StabilityRating.UNKNOWN],
        "overall": overall,
        "defensible": defensible,
    }
