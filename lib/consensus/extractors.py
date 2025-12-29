"""
Metric and quote extractors for consensus analysis.

These functions parse LLM responses to extract structured data
that can be aggregated across N runs.
"""

import re
from typing import Dict, List, Optional


def extract_effect_sizes(response: str) -> Dict[str, float]:
    """
    Extract effect sizes and statistics from pattern hunting output.

    Looks for patterns like:
        β = 0.21
        OR = 2.3
        r = 0.45
        R² = 0.34
        p < 0.001
        p = 0.023
        difference = 15.3
        effect size = 0.8

    Returns:
        {"beta": 0.21, "p_value": 0.001, "r_squared": 0.34, ...}
    """
    metrics = {}

    # Beta coefficients
    beta_patterns = [
        r'β\s*=\s*([-+]?\d*\.?\d+)',
        r'beta\s*=\s*([-+]?\d*\.?\d+)',
        r'coefficient\s*[=:]\s*([-+]?\d*\.?\d+)',
    ]
    for pattern in beta_patterns:
        match = re.search(pattern, response, re.IGNORECASE)
        if match:
            metrics['beta'] = float(match.group(1))
            break

    # Odds ratios
    or_patterns = [
        r'OR\s*=\s*([-+]?\d*\.?\d+)',
        r'odds\s*ratio\s*[=:]\s*([-+]?\d*\.?\d+)',
    ]
    for pattern in or_patterns:
        match = re.search(pattern, response, re.IGNORECASE)
        if match:
            metrics['odds_ratio'] = float(match.group(1))
            break

    # Correlation coefficients
    r_patterns = [
        r'\br\s*=\s*([-+]?\d*\.?\d+)',
        r'correlation\s*[=:]\s*([-+]?\d*\.?\d+)',
    ]
    for pattern in r_patterns:
        match = re.search(pattern, response, re.IGNORECASE)
        if match:
            metrics['correlation'] = float(match.group(1))
            break

    # R-squared
    r2_patterns = [
        r'R²\s*=\s*([-+]?\d*\.?\d+)',
        r'R\^2\s*=\s*([-+]?\d*\.?\d+)',
        r'r-squared\s*[=:]\s*([-+]?\d*\.?\d+)',
        r'r_squared\s*[=:]\s*([-+]?\d*\.?\d+)',
    ]
    for pattern in r2_patterns:
        match = re.search(pattern, response, re.IGNORECASE)
        if match:
            metrics['r_squared'] = float(match.group(1))
            break

    # P-values
    p_patterns = [
        r'p\s*<\s*(0?\.\d+)',  # p < 0.001
        r'p\s*=\s*(0?\.\d+)',  # p = 0.023
        r'p-value\s*[=<]\s*(0?\.\d+)',
    ]
    for pattern in p_patterns:
        match = re.search(pattern, response, re.IGNORECASE)
        if match:
            metrics['p_value'] = float(match.group(1))
            break

    # Sample size
    n_patterns = [
        r'[nN]\s*=\s*(\d+)',
        r'sample\s*size\s*[=:]\s*(\d+)',
        r'observations?\s*[=:]\s*(\d+)',
    ]
    for pattern in n_patterns:
        match = re.search(pattern, response)
        if match:
            metrics['sample_size'] = float(match.group(1))
            break

    # Generic effect size
    effect_patterns = [
        r'effect\s*size\s*[=:]\s*([-+]?\d*\.?\d+)',
        r"cohen'?s?\s*d\s*[=:]\s*([-+]?\d*\.?\d+)",
    ]
    for pattern in effect_patterns:
        match = re.search(pattern, response, re.IGNORECASE)
        if match:
            metrics['effect_size'] = float(match.group(1))
            break

    # Percentage differences
    pct_pattern = r'(\d+\.?\d*)\s*%\s*(?:difference|change|increase|decrease)'
    match = re.search(pct_pattern, response, re.IGNORECASE)
    if match:
        metrics['percentage_change'] = float(match.group(1))

    # Mean differences
    diff_pattern = r'difference\s*(?:of|=|:)\s*([-+]?\d*\.?\d+)'
    match = re.search(diff_pattern, response, re.IGNORECASE)
    if match:
        metrics['difference'] = float(match.group(1))

    return metrics


def extract_quotes(response: str) -> List[Dict]:
    """
    Extract quotes with informant information from qualitative mining output.

    Looks for patterns like:
        > "This is a quote"
        > — Informant 12, Manager, [Context]

    Or:
        "[Quote text]" (Informant 5, Worker)

    Returns:
        [{"text": "...", "informant": "...", "context": "..."}, ...]
    """
    quotes = []

    # Pattern 1: Markdown blockquote style
    # > "Quote text"
    # > — Informant info
    blockquote_pattern = r'>\s*"([^"]+)"\s*\n>\s*[-—]\s*([^,\n]+)(?:,\s*([^\n]+))?'
    for match in re.finditer(blockquote_pattern, response):
        quotes.append({
            "text": match.group(1).strip(),
            "informant": match.group(2).strip(),
            "context": (match.group(3) or "").strip(),
        })

    # Pattern 2: Inline quote style
    # "Quote text" (Informant 5, Worker)
    inline_pattern = r'"([^"]{20,})"[^(]*\(([^)]+)\)'
    for match in re.finditer(inline_pattern, response):
        informant_parts = match.group(2).split(',')
        quotes.append({
            "text": match.group(1).strip(),
            "informant": informant_parts[0].strip(),
            "context": ','.join(informant_parts[1:]).strip() if len(informant_parts) > 1 else "",
        })

    # Pattern 3: Quote with attribution on same line
    # "Quote text" — Informant 12
    dash_pattern = r'"([^"]{20,})"\s*[-—]+\s*([^\n]+)'
    for match in re.finditer(dash_pattern, response):
        # Skip if already captured
        text = match.group(1).strip()
        if not any(q["text"] == text for q in quotes):
            quotes.append({
                "text": text,
                "informant": match.group(2).strip(),
                "context": "",
            })

    return quotes


def extract_claims(response: str) -> List[Dict]:
    """
    Extract quantitative claims from verification output.

    Looks for structured claim blocks like:
        Claim 1: Effect of X on Y
        Statement: "Effect is positive"
        Value: β = 0.21

    Returns:
        [{"id": "1", "statement": "...", "value": 0.21, "metric": "beta"}, ...]
    """
    claims = []

    # Pattern: Claim N: Description
    claim_blocks = re.split(r'(?:###\s*)?Claim\s+(\d+)[:\s]', response)

    # Process pairs (id, content)
    for i in range(1, len(claim_blocks), 2):
        if i + 1 >= len(claim_blocks):
            break

        claim_id = claim_blocks[i]
        content = claim_blocks[i + 1]

        # Extract statement
        stmt_match = re.search(r'Statement[:\s]*"?([^"\n]+)"?', content, re.IGNORECASE)
        statement = stmt_match.group(1).strip() if stmt_match else ""

        # Extract expected value
        value_match = re.search(
            r'(?:Expected\s*value|Value)[:\s]*([^\n]+)',
            content,
            re.IGNORECASE
        )
        value_str = value_match.group(1).strip() if value_match else ""

        # Parse numeric value from value string
        effect_sizes = extract_effect_sizes(value_str)

        claims.append({
            "id": claim_id,
            "statement": statement,
            "value_string": value_str,
            "metrics": effect_sizes,
        })

    return claims


def extract_cycle_time(response: str) -> Dict[str, float]:
    """
    Extract cycle time metrics (specialized for workflow analysis).

    Returns:
        {"total_days": X, "active_pct": Y, "wait_pct": Z, "handoffs": N}
    """
    metrics = {}

    # Total cycle time
    time_patterns = [
        r'(?:total\s*)?cycle\s*time[:\s]*(\d+\.?\d*)\s*days?',
        r'(\d+\.?\d*)\s*days?\s*(?:total|elapsed)',
    ]
    for pattern in time_patterns:
        match = re.search(pattern, response, re.IGNORECASE)
        if match:
            metrics['total_days'] = float(match.group(1))
            break

    # Active vs wait percentages
    active_match = re.search(r'active[:\s]*(\d+\.?\d*)\s*%', response, re.IGNORECASE)
    if active_match:
        metrics['active_pct'] = float(active_match.group(1))

    wait_match = re.search(r'wait(?:ing)?[:\s]*(\d+\.?\d*)\s*%', response, re.IGNORECASE)
    if wait_match:
        metrics['wait_pct'] = float(wait_match.group(1))

    # Handoff count
    handoff_match = re.search(r'handoffs?[:\s]*(\d+)', response, re.IGNORECASE)
    if handoff_match:
        metrics['handoffs'] = float(handoff_match.group(1))

    return metrics


# Registry of extractors by stage
STAGE_EXTRACTORS = {
    "hunt_patterns": {
        "metrics": extract_effect_sizes,
        "quotes": None,
    },
    "mine_qual": {
        "metrics": None,
        "quotes": extract_quotes,
    },
    "verify_claims": {
        "metrics": extract_effect_sizes,
        "quotes": None,
    },
}


def get_extractor_for_stage(stage: str) -> Dict:
    """Get the appropriate extractors for a pipeline stage."""
    return STAGE_EXTRACTORS.get(stage, {"metrics": None, "quotes": None})
