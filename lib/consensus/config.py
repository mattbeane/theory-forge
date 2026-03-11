"""
Default configuration for consensus analysis.

These values can be overridden in state.json per-project.
"""

DEFAULT_CONFIG = {
    # Number of runs per stage (eval stages use consensus by default)
    "default_n": 5,

    # Per-stage N overrides (higher N for more critical stages)
    "stage_n": {
        "hunt_patterns": 10,  # Effect sizes need high confidence
        "mine_qual": 10,  # Quote stability
        "verify_claims": 10,  # Final verification

        # Eval / test suite stages (consensus by default)
        "eval_zuckerman": 5,
        "eval_paper_quality": 5,
        "eval_becker": 5,
        "eval_genre": 5,
        "eval_contribution": 5,
        "eval_limitations": 5,
        "eval_citations": 5,
        "simulate_review": 5,
        "check_submission": 7,  # Slightly higher for the aggregate runner
        "test_counter_evidence": 5,
        "test_alt_interpretations": 5,
        "test_boundary_conditions": 5,
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
