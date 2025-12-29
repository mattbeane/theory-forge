"""
Default configuration for consensus analysis.

These values can be overridden in state.json per-project.
"""

DEFAULT_CONFIG = {
    # Number of runs per stage
    "default_n": 10,

    # Per-stage N overrides (higher N for more critical stages)
    "stage_n": {
        "hunt_patterns": 25,  # Effect sizes need high confidence
        "mine_qual": 15,  # Quote stability
        "verify_claims": 10,  # Final verification
    },

    # CV thresholds for stability ratings (for numeric metrics)
    "high_stability_cv": 0.10,  # CV < 10% = HIGH stability
    "medium_stability_cv": 0.25,  # CV < 25% = MEDIUM stability
    # CV >= 25% = LOW stability

    # Quote appearance thresholds (for qualitative mining)
    "quote_high_stability": 0.75,  # Appeared in 75%+ of runs
    "quote_medium_stability": 0.50,  # Appeared in 50%+ of runs
    # < 50% = LOW stability

    # Execution settings
    "max_concurrent_runs": 10,  # Limit parallel API calls
    "timeout_per_run_seconds": 120,

    # Provider settings
    "default_provider": "anthropic",
    "default_model": {
        "anthropic": "claude-sonnet-4-20250514",
        "openai": "gpt-4o-mini",
    },

    # Cost optimization
    "use_batch_api": False,  # OpenAI batch API (50% savings, async)
}


def get_stage_n(stage: str, config: dict = None) -> int:
    """Get the N value for a specific stage."""
    config = config or DEFAULT_CONFIG
    stage_n = config.get("stage_n", {})
    return stage_n.get(stage, config.get("default_n", 10))


def merge_config(base: dict, override: dict) -> dict:
    """Merge override config into base, preserving nested structure."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_config(result[key], value)
        else:
            result[key] = value
    return result
