#!/usr/bin/env python3
"""
Consensus-mode evaluation runner for theory-forge.

Runs scored evaluations N times via the consensus engine, computes
stability statistics (CV, CI), and updates state.json with results.

Usage:
    # Run all scored evals with consensus (requires ANTHROPIC_API_KEY)
    ANTHROPIC_API_KEY=sk-... python3 lib/consensus/run_evals.py --project /path/to/paper

    # Run specific eval
    ANTHROPIC_API_KEY=sk-... python3 lib/consensus/run_evals.py --project /path/to/paper --eval zuckerman

    # Dry run (construct prompts, don't call API)
    python3 lib/consensus/run_evals.py --project /path/to/paper --dry-run

    # Quick mode (N=1, for plumbing validation)
    ANTHROPIC_API_KEY=sk-... python3 lib/consensus/run_evals.py --project /path/to/paper --quick
"""

import argparse
import asyncio
import hashlib
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add parent dirs to path for imports
SCRIPT_DIR = Path(__file__).resolve().parent
THEORY_FORGE_ROOT = SCRIPT_DIR.parent.parent
sys.path.insert(0, str(THEORY_FORGE_ROOT))

from lib.consensus.engine import ConsensusEngine, ConsensusResult
from lib.consensus.stability import StabilityRating, format_metric_for_paper
from lib.consensus.extractors import extract_rubric_scores, extract_verdict, extract_total_score
from lib.consensus.config import DEFAULT_CONFIG, get_stage_n


# ── Eval definitions ──────────────────────────────────────────────────

EVAL_REGISTRY = {
    "zuckerman": {
        "rubric_file": "rubrics/zuckerman_criteria.json",
        "manuscript_file": "submission/main.tex",
        "extractor": extract_rubric_scores,
        "stage_key": "eval_zuckerman",
        "state_key": "zuckerman",
        "scored": True,
        "system_prompt": (
            "You are an expert academic paper reviewer applying Zuckerman's "
            "'Tips to Article-Writers' criteria. Score each criterion on a 0-5 scale. "
            "For each criterion, cite specific evidence from the paper. "
            "End with a total score in the format: Total: XX/50\n\n"
            "Output each score in a markdown table row: | Criterion Name | Score |\n"
            "Use the exact criterion names from the rubric."
        ),
    },
    "paper_quality": {
        "rubric_file": "rubrics/paper_quality.json",
        "manuscript_file": "submission/main.tex",
        "extractor": extract_rubric_scores,
        "stage_key": "eval_paper_quality",
        "state_key": "paper_quality",
        "scored": True,
        "system_prompt": (
            "You are an expert academic reviewer evaluating a draft paper for a "
            "top-tier social science journal. Score each dimension on a 0-10 scale. "
            "For each dimension, cite specific evidence from the paper. "
            "End with a total score in the format: Total: XX/50\n\n"
            "Output each score in a markdown table row: | Dimension Name | Score |\n"
            "Use the exact dimension names from the rubric."
        ),
    },
    "becker": {
        "rubric_file": None,
        "manuscript_file": "submission/main.tex",
        "extractor": extract_verdict,
        "stage_key": "eval_becker",
        "state_key": "becker",
        "scored": False,
        "system_prompt": (
            "You are applying Becker's 'Tricks of the Trade' (1998) generalization test. "
            "1) Identify all domain-specific nouns in the paper's claims. "
            "2) Reformulate the core claim without domain nouns. "
            "3) Test whether the abstracted claim transfers to at least 3 other domains. "
            "4) If it transfers: output '**Verdict:** PASS'. "
            "If it doesn't: output '**Verdict:** FAIL'."
        ),
    },
    "genre": {
        "rubric_file": None,
        "manuscript_file": "submission/main.tex",
        "extractor": extract_verdict,
        "stage_key": "eval_genre",
        "state_key": "genre",
        "scored": False,
        "system_prompt": (
            "You are an expert at identifying the methodological genre of academic papers. "
            "Check whether the paper uses language consistent with its empirical approach:\n"
            "- Inductive/discovery papers should NOT use hypo-deductive language "
            "(e.g., 'we hypothesize', 'we test', 'derive observable implications').\n"
            "- Deductive/testing papers should NOT claim emergent findings.\n"
            "If the genre framing is consistent: output '**Verdict:** PASS'.\n"
            "If there are red flags: output '**Verdict:** FAIL' and list them."
        ),
    },
    "limitations": {
        "rubric_file": None,
        "manuscript_file": "submission/main.tex",
        "extractor": extract_verdict,
        "stage_key": "eval_limitations",
        "state_key": "limitations",
        "scored": False,
        "system_prompt": (
            "You are evaluating the limitations section of an academic paper. Check:\n"
            "1. Is it <=400 words? (over 400 = FAIL)\n"
            "2. Does it have <=2 enumerated items? (>2 = FAIL)\n"
            "3. Does it include a generalizability/transferability paragraph? (missing = FAIL)\n"
            "4. Does it avoid over-disclosure of non-threatening limitations?\n\n"
            "If all checks pass: output '**Verdict:** PASS'.\n"
            "If any fail: output '**Verdict:** FAIL' and explain which."
        ),
    },
}


# ── Helpers ────────────────────────────────────────────────────────────

def sha256_file(path: Path) -> str:
    """Compute SHA-256 checksum of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return f"sha256:{h.hexdigest()}"


def load_state(project_dir: Path) -> dict:
    """Load state.json from project directory."""
    state_file = project_dir / "state.json"
    if not state_file.exists():
        raise FileNotFoundError(f"No state.json found at {state_file}")
    with open(state_file) as f:
        return json.load(f)


def save_state(project_dir: Path, state: dict):
    """Save state.json to project directory."""
    state_file = project_dir / "state.json"
    with open(state_file, "w") as f:
        json.dump(state, f, indent=2)
    print(f"  Updated {state_file}")


def build_user_prompt(project_dir: Path, eval_def: dict) -> str:
    """Build the user prompt from manuscript + rubric."""
    parts = []

    # Load rubric if specified
    if eval_def["rubric_file"]:
        rubric_path = project_dir / eval_def["rubric_file"]
        if not rubric_path.exists():
            # Try theory-forge root for rubrics
            rubric_path = THEORY_FORGE_ROOT / eval_def["rubric_file"]
        if rubric_path.exists():
            with open(rubric_path) as f:
                rubric = f.read()
            parts.append(f"RUBRIC:\n```json\n{rubric}\n```")
        else:
            print(f"  Warning: rubric not found at {rubric_path}")

    # Load manuscript
    manuscript_path = project_dir / eval_def["manuscript_file"]
    if manuscript_path.exists():
        with open(manuscript_path) as f:
            manuscript = f.read()
        parts.append(f"MANUSCRIPT:\n```latex\n{manuscript}\n```")
    else:
        raise FileNotFoundError(f"Manuscript not found: {manuscript_path}")

    parts.append(
        "Score this paper against the rubric criteria above. "
        "Be rigorous but fair. Cite specific evidence from the text."
    )

    return "\n\n---\n\n".join(parts)


def update_state_with_result(
    state: dict,
    eval_name: str,
    eval_def: dict,
    result: ConsensusResult,
    project_dir: Path,
) -> dict:
    """Update state.json eval_results with consensus result."""
    frame = str(state.get("current_frame", 1))
    state_key = eval_def["state_key"]

    # Compute upstream checksum
    manuscript_path = project_dir / eval_def["manuscript_file"]
    checksum = sha256_file(manuscript_path) if manuscript_path.exists() else ""

    # Build scores dict from consensus metrics
    scores = {}
    for metric_name, mc in result.metrics.items():
        scores[metric_name] = round(mc.mean, 2)

    # Compute total if this is a scored eval
    total = None
    max_total = None
    if eval_def["scored"]:
        total = round(sum(scores.values()), 1)
        if eval_name == "zuckerman":
            max_total = 50
        elif eval_name == "paper_quality":
            max_total = 50

    # Determine verdict
    verdict = "UNKNOWN"
    if eval_def["scored"]:
        threshold = 35  # default min_score
        verdict = "PASS" if (total or 0) >= threshold else "FAIL"
    else:
        # For verdict-based evals, use the mean verdict score
        v = result.metrics.get("verdict")
        if v:
            if v.mean >= 0.75:
                verdict = "PASS"
            elif v.mean >= 0.25:
                verdict = "CONDITIONAL"
            else:
                verdict = "FAIL"

    # Determine overall stability
    overall_stability = result.overall_stability.value

    # Build the consensus stats
    consensus_stats = {
        "n_runs": result.n_runs,
        "stability": overall_stability,
    }

    # Add per-metric consensus detail
    metric_consensus = {}
    for metric_name, mc in result.metrics.items():
        metric_consensus[metric_name] = {
            "values": mc.values,
            "mean": round(mc.mean, 2),
            "std": round(mc.std, 2),
            "cv": round(mc.cv, 4),
            "ci_lower": round(mc.ci_lower, 2),
            "ci_upper": round(mc.ci_upper, 2),
            "stability": mc.stability.value,
        }

    # Build eval_results entry
    entry = {
        "timestamp": datetime.now().isoformat(),
        "scores": scores,
        "total": total,
        "max_total": max_total,
        "verdict": verdict,
        "consensus": consensus_stats,
        "metric_consensus": metric_consensus,
        "stale": False,
        "stale_reason": None,
        "upstream_checksums": {
            eval_def["manuscript_file"]: checksum,
        },
        "output_file": None,
        "execution": {
            "model": result.model,
            "total_tokens": result.total_tokens,
            "time_seconds": round(result.execution_time_seconds, 1),
            "cost_usd": round(result.estimated_cost_usd, 4),
        },
    }

    # Ensure eval_results structure exists
    if "eval_results" not in state:
        state["eval_results"] = {}
    if state_key not in state["eval_results"]:
        state["eval_results"][state_key] = {}
    if f"frame_{frame}" not in state["eval_results"][state_key]:
        state["eval_results"][state_key][f"frame_{frame}"] = {}

    state["eval_results"][state_key][f"frame_{frame}"]["latest"] = entry

    return state


# ── Main runner ────────────────────────────────────────────────────────

async def run_eval(
    eval_name: str,
    project_dir: Path,
    engine: ConsensusEngine,
    n: int,
    dry_run: bool = False,
) -> Optional[ConsensusResult]:
    """Run a single evaluation with consensus."""
    eval_def = EVAL_REGISTRY[eval_name]

    print(f"\n{'='*60}")
    print(f"Running: {eval_name} (N={n})")
    print(f"{'='*60}")

    # Build prompts
    system_prompt = eval_def["system_prompt"]
    user_prompt = build_user_prompt(project_dir, eval_def)

    print(f"  System prompt: {len(system_prompt)} chars")
    print(f"  User prompt: {len(user_prompt)} chars")
    print(f"  Extractor: {eval_def['extractor'].__name__}")

    if dry_run:
        print(f"  [DRY RUN] Would fire {n} parallel API calls")
        print(f"  System prompt preview: {system_prompt[:100]}...")
        return None

    # Run consensus
    result = await engine.run_with_consensus(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        n=n,
        extract_metrics_fn=eval_def["extractor"],
    )

    # Print results
    print(f"\n  Results ({result.n_runs} runs, {result.execution_time_seconds:.1f}s):")
    print(f"  Model: {result.model}")
    print(f"  Tokens: {result.total_tokens:,}")
    print(f"  Est. cost: ${result.estimated_cost_usd:.4f}")
    print(f"  Overall stability: {result.overall_stability.value}")

    if result.flagged_items:
        print(f"\n  Flags:")
        for flag in result.flagged_items:
            print(f"    ⚠️  {flag}")

    print(f"\n  Metrics:")
    for name, mc in result.metrics.items():
        print(f"    {name}: {format_metric_for_paper(mc)}")
        print(f"      Stability: {mc.stability.value} (CV={mc.cv:.1%})")

    return result


async def main():
    parser = argparse.ArgumentParser(description="Run consensus evaluations")
    parser.add_argument("--project", required=True, help="Path to paper project directory")
    parser.add_argument("--eval", help="Run specific eval (default: all scored evals)")
    parser.add_argument("--dry-run", action="store_true", help="Build prompts without calling API")
    parser.add_argument("--quick", action="store_true", help="N=1 for all evals")
    parser.add_argument("--model", default=None, help="Override model (default: from config)")
    parser.add_argument("--provider", default="anthropic", help="API provider")
    parser.add_argument("--all", action="store_true", help="Run all evals including PASS/FAIL")
    args = parser.parse_args()

    project_dir = Path(args.project).resolve()
    if not project_dir.exists():
        print(f"Error: project directory not found: {project_dir}")
        sys.exit(1)

    # Load state
    state = load_state(project_dir)
    consensus_config = state.get("consensus", DEFAULT_CONFIG)

    # Determine which evals to run
    if args.eval:
        eval_names = [args.eval]
        if args.eval not in EVAL_REGISTRY:
            print(f"Error: unknown eval '{args.eval}'. Available: {list(EVAL_REGISTRY.keys())}")
            sys.exit(1)
    elif args.all:
        eval_names = list(EVAL_REGISTRY.keys())
    else:
        # Default: scored evals only (where consensus adds statistical value)
        eval_names = [name for name, defn in EVAL_REGISTRY.items() if defn["scored"]]

    print(f"Project: {project_dir}")
    print(f"Evals to run: {eval_names}")
    print(f"Provider: {args.provider}")
    print(f"Quick mode: {args.quick}")
    print(f"Dry run: {args.dry_run}")

    # Initialize engine (skip if dry run)
    engine = None
    if not args.dry_run:
        try:
            engine = ConsensusEngine(
                provider=args.provider,
                model=args.model,
            )
            print(f"Model: {engine.model}")
        except (ImportError, ValueError) as e:
            print(f"Error initializing engine: {e}")
            sys.exit(1)

    # Run evals
    results = {}
    total_cost = 0.0
    total_tokens = 0
    start_time = time.time()

    for eval_name in eval_names:
        eval_def = EVAL_REGISTRY[eval_name]
        stage_key = eval_def["stage_key"]

        # Get N from config
        n = 1 if args.quick else get_stage_n(
            stage_key,
            {"stage_n": {s["stage_key"]: consensus_config.get("stages", {}).get(s["stage_key"], {}).get("n", 5) for s in EVAL_REGISTRY.values()}, "default_n": 5}
        )

        result = await run_eval(eval_name, project_dir, engine, n, args.dry_run)

        if result:
            results[eval_name] = result
            total_cost += result.estimated_cost_usd
            total_tokens += result.total_tokens

            # Update state
            state = update_state_with_result(state, eval_name, eval_def, result, project_dir)

    # Save state
    if results and not args.dry_run:
        state["updated_at"] = datetime.now().isoformat()
        save_state(project_dir, state)

    # Summary
    elapsed = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Evals run: {len(results)}")
    print(f"Total tokens: {total_tokens:,}")
    print(f"Total cost: ${total_cost:.4f}")
    print(f"Total time: {elapsed:.1f}s")

    if results:
        print(f"\nStability summary:")
        for name, result in results.items():
            stability = result.overall_stability.value
            n_runs = result.n_runs
            emoji = {"high": "✅", "medium": "⚠️", "low": "❌", "unknown": "❓"}.get(stability, "❓")
            print(f"  {emoji} {name}: {stability.upper()} (N={n_runs})")

        # Flag any LOW stability results
        low_stability = [name for name, r in results.items()
                         if r.overall_stability == StabilityRating.LOW]
        if low_stability:
            print(f"\n⚠️  LOW stability evals (consider increasing N): {low_stability}")


if __name__ == "__main__":
    asyncio.run(main())
