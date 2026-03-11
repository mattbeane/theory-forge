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


def extract_rubric_scores(response: str) -> Dict[str, float]:
    """
    Parse scored rubric output from eval stages.

    Handles formats:
        | Criterion Name | 4 |          (markdown table)
        Criterion Name: 4/5
        **Criterion Name**: 4
        criterion_name: 4

    Returns:
        {"criterion_name": 4.0, ...}
    """
    scores: Dict[str, float] = {}

    # Pattern 1: Markdown table row  — | Name | 4 |  or  | Name | 4/5 |
    table_pattern = r'\|\s*([^|]+?)\s*\|\s*(\d+(?:\.\d+)?)\s*(?:/\s*\d+)?\s*\|'
    for match in re.finditer(table_pattern, response):
        name = match.group(1).strip()
        # Skip header-like rows
        if name.startswith('-') or name.lower() in ('criterion', 'criteria', 'score', 'rating'):
            continue
        scores[name] = float(match.group(2))

    # Pattern 2: Criterion Name: 4/5  or  Criterion Name: 4
    colon_pattern = r'^([A-Z][A-Za-z\s]+?)\s*:\s*(\d+(?:\.\d+)?)\s*(?:/\s*\d+)?$'
    for match in re.finditer(colon_pattern, response, re.MULTILINE):
        name = match.group(1).strip()
        if name not in scores:
            scores[name] = float(match.group(2))

    # Pattern 3: **Criterion Name**: 4
    bold_pattern = r'\*\*([^*]+)\*\*\s*:\s*(\d+(?:\.\d+)?)'
    for match in re.finditer(bold_pattern, response):
        name = match.group(1).strip()
        if name not in scores:
            scores[name] = float(match.group(2))

    # Pattern 4: snake_case key: 4
    snake_pattern = r'^([a-z][a-z_]+)\s*:\s*(\d+(?:\.\d+)?)$'
    for match in re.finditer(snake_pattern, response, re.MULTILINE):
        name = match.group(1).strip()
        if name not in scores:
            scores[name] = float(match.group(2))

    return scores


def extract_verdict(response: str) -> Dict[str, float]:
    """
    Parse PASS/FAIL/CONDITIONAL verdicts from eval output.

    Handles formats:
        **Verdict:** PASS
        **Overall:** FAIL
        PASS ✓
        CONDITIONAL

    Returns:
        {"verdict": 1.0}  (PASS=1.0, FAIL=0.0, CONDITIONAL=0.5)
    """
    verdict_map = {
        'PASS': 1.0,
        'FAIL': 0.0,
        'CONDITIONAL': 0.5,
    }

    # Pattern 1: **Verdict:** PASS  or  **Overall:** PASS
    labeled_pattern = r'\*\*(?:Verdict|Overall)\s*:\*\*\s*(PASS|FAIL|CONDITIONAL)'
    match = re.search(labeled_pattern, response, re.IGNORECASE)
    if match:
        return {"verdict": verdict_map.get(match.group(1).upper(), 0.5)}

    # Pattern 2: PASS ✓  or  FAIL ✗
    check_pattern = r'\b(PASS|FAIL|CONDITIONAL)\s*[✓✗✔✘☑☒]?'
    match = re.search(check_pattern, response)
    if match:
        return {"verdict": verdict_map.get(match.group(1).upper(), 0.5)}

    # Pattern 3: standalone verdict word on its own line
    line_pattern = r'^\s*(PASS|FAIL|CONDITIONAL)\s*$'
    match = re.search(line_pattern, response, re.MULTILINE)
    if match:
        return {"verdict": verdict_map.get(match.group(1).upper(), 0.5)}

    return {"verdict": 0.5}  # Default to CONDITIONAL if unparseable


def extract_total_score(response: str) -> Dict[str, float]:
    """
    Extract total score from eval output.

    Handles formats:
        Total: 39/50
        **Total Score:** 39
        Score: 39 out of 50

    Returns:
        {"total": 39.0, "max_total": 50.0}  (max_total only if present)
    """
    result: Dict[str, float] = {}

    # Pattern 1: Total: 39/50  or  **Total:** 39/50
    slash_pattern = r'(?:\*\*)?(?:Total(?:\s*Score)?)\s*:?\s*(?:\*\*)?\s*(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)'
    match = re.search(slash_pattern, response, re.IGNORECASE)
    if match:
        result['total'] = float(match.group(1))
        result['max_total'] = float(match.group(2))
        return result

    # Pattern 2: Score: 39 out of 50
    out_of_pattern = r'(?:Total(?:\s*Score)?|Score)\s*:\s*(\d+(?:\.\d+)?)\s*(?:out\s*of|of)\s*(\d+(?:\.\d+)?)'
    match = re.search(out_of_pattern, response, re.IGNORECASE)
    if match:
        result['total'] = float(match.group(1))
        result['max_total'] = float(match.group(2))
        return result

    # Pattern 3: **Total Score:** 39  (no denominator)
    bare_pattern = r'(?:\*\*)?(?:Total(?:\s*Score)?)\s*:?\s*(?:\*\*)?\s*(\d+(?:\.\d+)?)'
    match = re.search(bare_pattern, response, re.IGNORECASE)
    if match:
        result['total'] = float(match.group(1))
        return result

    return result


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
    # Eval / test suite stages
    "eval_zuckerman": {
        "metrics": extract_rubric_scores,
        "quotes": None,
    },
    "eval_paper_quality": {
        "metrics": extract_rubric_scores,
        "quotes": None,
    },
    "eval_becker": {
        "metrics": extract_verdict,
        "quotes": None,
    },
    "eval_genre": {
        "metrics": extract_verdict,
        "quotes": None,
    },
    "eval_contribution": {
        "metrics": extract_rubric_scores,
        "quotes": None,
    },
    "eval_limitations": {
        "metrics": extract_verdict,
        "quotes": None,
    },
    "eval_citations": {
        "metrics": extract_total_score,
        "quotes": None,
    },
    "simulate_review": {
        "metrics": extract_verdict,
        "quotes": None,
    },
    "check_submission": {
        "metrics": extract_verdict,
        "quotes": None,
    },
    "test_counter_evidence": {
        "metrics": extract_verdict,
        "quotes": None,
    },
    "test_alt_interpretations": {
        "metrics": extract_verdict,
        "quotes": None,
    },
    "test_boundary_conditions": {
        "metrics": extract_verdict,
        "quotes": None,
    },
}


def get_extractor_for_stage(stage: str) -> Dict:
    """Get the appropriate extractors for a pipeline stage."""
    return STAGE_EXTRACTORS.get(stage, {"metrics": None, "quotes": None})
