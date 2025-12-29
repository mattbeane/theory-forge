"""
Consensus Engine for Paper Mining Agents

Runs LLM prompts N times in parallel, extracts metrics, and computes
statistical aggregates with confidence intervals and stability scores.

Based on the workflow-analysis-platform architecture.
"""

import asyncio
import json
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

# Support both OpenAI and Anthropic
try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from anthropic import AsyncAnthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

from .stability import compute_stability, StabilityRating
from .config import DEFAULT_CONFIG


@dataclass
class ConsensusResult:
    """Result of N-run consensus analysis."""

    # Raw outputs
    raw_responses: List[str]
    n_runs: int

    # Extracted metrics with statistics
    metrics: Dict[str, "MetricConsensus"]

    # Extracted quotes with stability (for qual mining)
    quotes: Optional[List["QuoteConsensus"]] = None

    # Overall stability assessment
    overall_stability: StabilityRating = StabilityRating.UNKNOWN
    flagged_items: List[str] = field(default_factory=list)

    # Execution metadata
    model: str = ""
    total_tokens: int = 0
    execution_time_seconds: float = 0.0
    estimated_cost_usd: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for JSON storage."""
        return {
            "n_runs": self.n_runs,
            "metrics": {k: v.to_dict() for k, v in self.metrics.items()},
            "quotes": [q.to_dict() for q in self.quotes] if self.quotes else None,
            "overall_stability": self.overall_stability.value,
            "flagged_items": self.flagged_items,
            "model": self.model,
            "total_tokens": self.total_tokens,
            "execution_time_seconds": self.execution_time_seconds,
            "estimated_cost_usd": self.estimated_cost_usd,
            "timestamp": self.timestamp,
        }


@dataclass
class MetricConsensus:
    """Statistical consensus for a single metric."""

    name: str
    values: List[float]

    # Statistics
    mean: float = 0.0
    median: float = 0.0
    std: float = 0.0
    ci_lower: float = 0.0
    ci_upper: float = 0.0
    cv: float = 0.0  # Coefficient of variation

    # Stability
    stability: StabilityRating = StabilityRating.UNKNOWN

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "values": self.values,
            "mean": self.mean,
            "median": self.median,
            "std": self.std,
            "ci_lower": self.ci_lower,
            "ci_upper": self.ci_upper,
            "cv": self.cv,
            "stability": self.stability.value,
        }


@dataclass
class QuoteConsensus:
    """Stability tracking for extracted quotes."""

    text: str
    informant: str
    context: str

    # How many runs extracted this quote
    appearances: int = 0
    total_runs: int = 0

    # Stability
    appearance_rate: float = 0.0
    stability: StabilityRating = StabilityRating.UNKNOWN

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "informant": self.informant,
            "context": self.context,
            "appearances": self.appearances,
            "total_runs": self.total_runs,
            "appearance_rate": self.appearance_rate,
            "stability": self.stability.value,
        }


class ConsensusEngine:
    """
    Execute prompts N times and aggregate results with statistical confidence.
    """

    def __init__(
        self,
        provider: str = "anthropic",
        model: str = None,
        api_key: str = None,
    ):
        self.provider = provider

        if provider == "anthropic":
            if not ANTHROPIC_AVAILABLE:
                raise ImportError("anthropic package not installed. Run: pip install anthropic")
            self.model = model or "claude-sonnet-4-20250514"
            self.client = AsyncAnthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
        elif provider == "openai":
            if not OPENAI_AVAILABLE:
                raise ImportError("openai package not installed. Run: pip install openai")
            self.model = model or "gpt-4o-mini"
            self.client = AsyncOpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        else:
            raise ValueError(f"Unknown provider: {provider}. Use 'anthropic' or 'openai'.")

    async def run_single(self, system_prompt: str, user_prompt: str) -> tuple[str, int]:
        """Run a single LLM call. Returns (response_text, token_count)."""

        if self.provider == "anthropic":
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
            )
            text = response.content[0].text
            tokens = response.usage.input_tokens + response.usage.output_tokens
            return text, tokens

        elif self.provider == "openai":
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )
            text = response.choices[0].message.content
            tokens = response.usage.total_tokens
            return text, tokens

    async def run_n_times(
        self,
        system_prompt: str,
        user_prompt: str,
        n: int,
        max_concurrent: int = 10,
    ) -> List[tuple[str, int]]:
        """Run the prompt N times with concurrency control."""

        semaphore = asyncio.Semaphore(max_concurrent)

        async def bounded_call():
            async with semaphore:
                return await self.run_single(system_prompt, user_prompt)

        tasks = [bounded_call() for _ in range(n)]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions, log them
        valid_results = []
        for i, r in enumerate(results):
            if isinstance(r, Exception):
                print(f"Run {i+1} failed: {r}")
            else:
                valid_results.append(r)

        return valid_results

    async def run_with_consensus(
        self,
        system_prompt: str,
        user_prompt: str,
        n: int = 10,
        extract_metrics_fn: Callable[[str], Dict[str, float]] = None,
        extract_quotes_fn: Callable[[str], List[Dict]] = None,
        config: Dict = None,
    ) -> ConsensusResult:
        """
        Run prompt N times, extract metrics/quotes, compute consensus statistics.

        Args:
            system_prompt: System message for the LLM
            user_prompt: User message (includes data context)
            n: Number of runs
            extract_metrics_fn: Function to extract numeric metrics from response
            extract_quotes_fn: Function to extract quotes from response (for qual mining)
            config: Override default thresholds

        Returns:
            ConsensusResult with statistics, stability ratings, and flags
        """
        import time
        start_time = time.time()

        config = config or DEFAULT_CONFIG

        # Run N times
        results = await self.run_n_times(system_prompt, user_prompt, n)

        raw_responses = [r[0] for r in results]
        total_tokens = sum(r[1] for r in results)

        # Extract and aggregate metrics
        metrics = {}
        if extract_metrics_fn:
            all_extractions = [extract_metrics_fn(resp) for resp in raw_responses]

            # Collect all metric names across runs
            all_metric_names = set()
            for extraction in all_extractions:
                all_metric_names.update(extraction.keys())

            # Aggregate each metric
            for metric_name in all_metric_names:
                values = [
                    extraction.get(metric_name)
                    for extraction in all_extractions
                    if extraction.get(metric_name) is not None
                ]

                if values:
                    mc = MetricConsensus(name=metric_name, values=values)
                    mc = compute_stability(mc, config)
                    metrics[metric_name] = mc

        # Extract and aggregate quotes
        quotes = None
        if extract_quotes_fn:
            all_quotes = [extract_quotes_fn(resp) for resp in raw_responses]
            quotes = self._aggregate_quotes(all_quotes, len(raw_responses), config)

        # Determine overall stability
        flagged = []
        stabilities = []

        for name, mc in metrics.items():
            stabilities.append(mc.stability)
            if mc.stability == StabilityRating.LOW:
                flagged.append(f"Metric '{name}' has LOW stability (CV={mc.cv:.1%})")

        if quotes:
            for q in quotes:
                stabilities.append(q.stability)
                if q.stability == StabilityRating.LOW:
                    flagged.append(
                        f"Quote '{q.text[:50]}...' has LOW stability "
                        f"({q.appearances}/{q.total_runs} runs)"
                    )

        # Overall = worst stability found
        if StabilityRating.LOW in stabilities:
            overall = StabilityRating.LOW
        elif StabilityRating.MEDIUM in stabilities:
            overall = StabilityRating.MEDIUM
        elif stabilities:
            overall = StabilityRating.HIGH
        else:
            overall = StabilityRating.UNKNOWN

        execution_time = time.time() - start_time

        # Estimate cost (rough, varies by model)
        cost = self._estimate_cost(total_tokens)

        return ConsensusResult(
            raw_responses=raw_responses,
            n_runs=len(raw_responses),
            metrics=metrics,
            quotes=quotes,
            overall_stability=overall,
            flagged_items=flagged,
            model=self.model,
            total_tokens=total_tokens,
            execution_time_seconds=execution_time,
            estimated_cost_usd=cost,
        )

    def _aggregate_quotes(
        self,
        all_quotes: List[List[Dict]],
        n_runs: int,
        config: Dict,
    ) -> List[QuoteConsensus]:
        """Aggregate quotes across runs, computing appearance rates."""

        # Normalize quotes for comparison (lowercase, strip whitespace)
        def normalize(text: str) -> str:
            return " ".join(text.lower().split())

        # Count appearances of each unique quote
        quote_counts = {}  # normalized_text -> {quote_data, count}

        for run_quotes in all_quotes:
            seen_in_run = set()
            for q in run_quotes:
                norm = normalize(q.get("text", ""))
                if norm and norm not in seen_in_run:
                    seen_in_run.add(norm)
                    if norm not in quote_counts:
                        quote_counts[norm] = {
                            "text": q.get("text", ""),
                            "informant": q.get("informant", ""),
                            "context": q.get("context", ""),
                            "count": 0,
                        }
                    quote_counts[norm]["count"] += 1

        # Convert to QuoteConsensus objects
        results = []
        high_threshold = config.get("quote_high_stability", 0.75)
        medium_threshold = config.get("quote_medium_stability", 0.50)

        for norm, data in quote_counts.items():
            rate = data["count"] / n_runs

            if rate >= high_threshold:
                stability = StabilityRating.HIGH
            elif rate >= medium_threshold:
                stability = StabilityRating.MEDIUM
            else:
                stability = StabilityRating.LOW

            results.append(QuoteConsensus(
                text=data["text"],
                informant=data["informant"],
                context=data["context"],
                appearances=data["count"],
                total_runs=n_runs,
                appearance_rate=rate,
                stability=stability,
            ))

        # Sort by appearance rate (most stable first)
        results.sort(key=lambda q: q.appearance_rate, reverse=True)

        return results

    def _estimate_cost(self, tokens: int) -> float:
        """Rough cost estimate based on model."""

        # Approximate costs per 1M tokens (input+output average)
        costs = {
            # Anthropic
            "claude-sonnet-4-20250514": 6.0,
            "claude-3-5-haiku-20241022": 1.0,
            # OpenAI
            "gpt-4o-mini": 0.3,
            "gpt-4o": 5.0,
        }

        per_million = costs.get(self.model, 3.0)  # Default $3/M
        return (tokens / 1_000_000) * per_million


# Convenience function for simple usage
async def run_consensus(
    prompt: str,
    data_context: str,
    n: int = 10,
    extract_fn: Callable = None,
    provider: str = "anthropic",
    model: str = None,
) -> ConsensusResult:
    """
    Simple interface to run consensus analysis.

    Example:
        result = await run_consensus(
            prompt="Analyze this workflow for bottlenecks...",
            data_context="[workflow data here]",
            n=25,
            extract_fn=extract_effect_sizes,
        )
        print(f"Mean cycle time: {result.metrics['cycle_time'].mean} ± {result.metrics['cycle_time'].std}")
    """
    engine = ConsensusEngine(provider=provider, model=model)

    system_prompt = (
        "You are a research analysis assistant. "
        "Provide exact numbers, show calculations explicitly. "
        "Use consistent output format."
    )

    user_prompt = f"{prompt}\n\n---\n\nDATA:\n{data_context}"

    return await engine.run_with_consensus(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        n=n,
        extract_metrics_fn=extract_fn,
    )
