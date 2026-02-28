"""
Heuristic classifier for academic paper titles against the title grammar.

Uses pattern matching, keyword detection, and structural analysis to tag
each of the 1,000 titles across all grammar dimensions. Confidence scores
reflect how certain the heuristic is — low-confidence tags should be reviewed.

This is a first-pass classifier. For dimensions requiring deep semantic
judgment (e.g., lead concept for ambiguous titles), confidence will be lower.
"""

import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Keyword / pattern banks
# ---------------------------------------------------------------------------

NEGATIVE_WORDS = {
    "cost", "bias", "dark", "hidden", "fail", "failure", "harm", "harmful",
    "threat", "risk", "challenge", "tension", "paradox", "trap", "hurt",
    "hurts", "unintended", "loss", "inequality", "aversion", "penalty",
    "blind", "blindness", "precarious", "agony", "degrading", "dismantling",
    "toxic", "fake", "distrust", "hate", "harassment", "anxiety", "burnout",
    "overload", "surveillance", "manipulation", "deception", "deficit",
    "decline", "diminished", "obstacle", "barrier", "conflict", "dilemma",
    "vulnerability", "exploit", "unfair", "discrimination", "disparity",
    "adversarial", "noisy", "corrupt", "missing", "broken", "fragile",
    "collapse", "disruption",
}

POSITIVE_WORDS = {
    "improve", "improving", "improved", "enhance", "enhancing", "enhanced",
    "enable", "enabling", "empower", "empowering", "better", "advance",
    "advancing", "efficient", "optimal", "novel", "toward", "towards",
    "bridge", "bridging", "benefit", "sustainable", "resilient", "robust",
    "accurate", "superior", "precision", "collaborative", "enrichment",
    "accelerat", "breakthrough", "scalable", "generali",
}

EVIDENCE_PATTERNS = [
    r"evidence from",
    r"evidence of",
    r"evidence in",
    r"an empirical",
    r"empirical study",
    r"empirical examination",
    r"empirical analysis",
    r"a field experiment",
    r"a natural experiment",
    r"a randomized",
    r"a longitudinal",
    r"a case study of",
]

HOW_SUBTITLE_PATTERN = re.compile(r"^how\b", re.IGNORECASE)
TOWARD_SUBTITLE_PATTERN = re.compile(r"^towards?\b", re.IGNORECASE)
FRAMEWORK_SUBTITLE_PATTERN = re.compile(
    r"^(a|an)\s+(framework|model|method|approach|tool|system|benchmark|dataset|survey|taxonomy|pipeline)\b",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Structure classifier
# ---------------------------------------------------------------------------

def classify_structure(title):
    """Determine the physical structure of the title."""
    has_colon = ":" in title
    has_question = "?" in title

    if has_colon:
        headline = title.split(":", 1)[0].strip()

        # Check for tool/system name pattern: single proper noun before colon
        if re.match(r"^[A-Z][A-Za-z0-9\-\.]+$", headline) and len(headline.split()) <= 3:
            return "name_description", 0.9

        # Check for quoted phrase before colon
        if headline.startswith('"') or headline.startswith("\u201c") or headline.startswith("'"):
            # Still headline_subtitle, but with quotation rhetorical move
            if has_question and "?" in headline:
                return "question_answer", 0.8
            return "headline_subtitle", 0.85

        if has_question and "?" in headline:
            return "question_answer", 0.85

        return "headline_subtitle", 0.95

    if has_question:
        return "question_only", 0.85

    return "headline_only", 0.95


# ---------------------------------------------------------------------------
# Rhetorical move classifier
# ---------------------------------------------------------------------------

def classify_rhetorical(title, headline, subtitle, structure):
    """Determine the rhetorical framing device."""
    title_lower = title.lower()
    headline_lower = headline.lower() if headline else title.lower()

    # Naming: tool/system name
    if structure == "name_description":
        return "naming", 0.95

    # Quotation: starts with quote marks
    if headline and (headline.startswith('"') or headline.startswith("\u201c") or
                     headline.startswith("'") or headline.startswith("\u2018")):
        return "quotation", 0.95

    # Question
    if "?" in (headline or title):
        return "question", 0.95

    # Paradox
    if "paradox" in title_lower:
        return "paradox", 0.95

    # Beyond X (contrast)
    if headline_lower.startswith("beyond "):
        return "contrast", 0.90

    # X as Y (reframing)
    if re.search(r"\bas\b", headline_lower) and not headline_lower.startswith("as "):
        # Check it's actually a reframing and not incidental "as"
        if re.search(r"\w+ as \w+", headline_lower) and len(headline_lower.split()) <= 8:
            return "reframing", 0.70

    # Gerund/process
    if headline and re.match(r"^[A-Z]\w+ing\b", headline):
        return "process_gerund", 0.85

    if not headline and re.match(r"^[A-Z]\w+ing\b", title):
        return "process_gerund", 0.85

    # Metaphor detection — figurative language heuristics
    metaphor_signals = ["lure", "shadow", "weight", "footprint", "landscape",
                        "ecosystem", "bridge", "lens", "telescope", "mirror",
                        "fabric", "dance", "wave", "storm", "fire", "web",
                        "sword", "shield", "anchor", "compass", "path"]
    if any(w in headline_lower.split() for w in metaphor_signals):
        return "metaphor", 0.60

    # Coinage detection — capitalized multi-word terms, or unusual compounds
    # Look for title-case words that aren't standard
    if headline:
        words = headline.split()
        if len(words) <= 4:
            # Short headlines with unusual terms might be coinages
            # Hard to detect reliably — mark with lower confidence
            pass

    # Declaration / Descriptive (fallback)
    # If no rhetorical device detected, check if it's truly descriptive
    # (no figurative language, just states the topic) or a declaration
    # (asserts something about the topic)

    # "The X of Y" is typically a declaration
    if re.match(r"^The \w+", headline_lower):
        return "declaration", 0.70

    # Very short, purely technical titles are descriptive
    word_count = len(title.split())
    if word_count <= 6 and structure == "headline_only":
        return "descriptive", 0.70

    # Default: descriptive for STEM venues, declaration for social science
    # (We don't have venue info here, so default to declaration for colon
    # titles and descriptive for standalone)
    if structure in ("headline_subtitle", "question_answer"):
        return "declaration", 0.50
    return "descriptive", 0.50


# ---------------------------------------------------------------------------
# Valence classifier
# ---------------------------------------------------------------------------

def classify_valence(title):
    """Determine the evaluative orientation."""
    title_lower = title.lower()
    words = set(title_lower.split())

    neg_hits = sum(1 for w in words if w in NEGATIVE_WORDS or
                   any(w.startswith(nw) for nw in NEGATIVE_WORDS if len(nw) > 4))
    pos_hits = sum(1 for w in words if w in POSITIVE_WORDS or
                   any(w.startswith(pw) for pw in POSITIVE_WORDS if len(pw) > 4))

    # Check for phrase-level patterns
    neg_phrases = ["dark side", "hidden cost", "unintended consequence", "at what cost",
                   "double-edged", "too much", "too little", "when.*hurts",
                   "when.*fails", "downside"]
    pos_phrases = ["toward a", "towards a", "better than", "more efficient"]

    for phrase in neg_phrases:
        if re.search(phrase, title_lower):
            neg_hits += 2
    for phrase in pos_phrases:
        if re.search(phrase, title_lower):
            pos_hits += 1

    if neg_hits > pos_hits and neg_hits >= 1:
        confidence = min(0.9, 0.6 + neg_hits * 0.1)
        return "negative", confidence
    elif pos_hits > neg_hits and pos_hits >= 1:
        confidence = min(0.85, 0.55 + pos_hits * 0.1)
        return "positive", confidence
    else:
        return "neutral", 0.75


# ---------------------------------------------------------------------------
# Lead concept classifier
# ---------------------------------------------------------------------------

def classify_lead(title, headline, subtitle, structure, rhetorical, venue):
    """Determine what concept occupies the headline position."""
    h = headline.lower() if headline else title.lower()
    t = title.lower()

    # Artifact: already caught by naming rhetorical move
    if rhetorical == "naming":
        return "artifact", 0.95

    # Process: already caught by gerund rhetorical move
    if rhetorical == "process_gerund":
        return "process", 0.85

    # Method indicators
    method_words = ["framework", "method", "metric", "measure", "measuring",
                    "algorithm", "model", "estimation", "detection",
                    "inference", "prediction", "classification", "learning",
                    "network", "neural", "deep", "training", "optimization"]
    if venue in ("NeurIPS",) and any(w in h.split() for w in method_words):
        return "method", 0.75

    # Reconceptualization: coinage or reframing rhetorical moves
    if rhetorical in ("coinage", "reframing"):
        return "reconceptualization", 0.70

    # Finding: for Nature/Science, most titles report findings
    if venue in ("Nature", "Science"):
        return "finding", 0.70

    # Site: empirical context as draw (look for geographic/org names, "in China", etc.)
    site_patterns = [r"in china", r"in india", r"in the u\.?s\.?", r"at nasa",
                     r"in japan", r"in europe", r"at google", r"at amazon",
                     r"in africa", r"in brazil"]
    if any(re.search(p, t) for p in site_patterns) and structure == "headline_only":
        return "site", 0.55

    # Implication: design-forward
    impl_words = ["design", "guideline", "recommendation", "implications", "toward"]
    if any(w in h.split() for w in impl_words):
        return "implication", 0.55

    # Question titles in ManSci/OrgSci often lead with phenomena
    if rhetorical == "question":
        if re.match(r"^(does|do|can|is|are|will|should|how|what|when|why)\b", h):
            return "phenomenon", 0.60

    # Paradox titles typically lead with a finding or phenomenon
    if rhetorical == "paradox":
        return "finding", 0.65

    # Default by venue
    if venue in ("ASQ", "OrgSci"):
        return "phenomenon", 0.45
    elif venue in ("ManSci",):
        return "phenomenon", 0.45
    elif venue in ("CHI", "TOCHI", "HRI"):
        return "phenomenon", 0.40
    elif venue in ("NeurIPS",):
        return "method", 0.50
    else:
        return "finding", 0.40


# ---------------------------------------------------------------------------
# Subtitle function classifier
# ---------------------------------------------------------------------------

def classify_subtitle_fn(title, headline, subtitle, structure):
    """Determine what work the subtitle does."""
    if not subtitle or structure in ("headline_only", "question_only"):
        return "none", 0.95

    sub_lower = subtitle.lower().strip()

    # "How X does Y"
    if HOW_SUBTITLE_PATTERN.match(sub_lower):
        return "how_mechanism", 0.85

    # "Toward(s) X"
    if TOWARD_SUBTITLE_PATTERN.match(sub_lower):
        return "specification", 0.70

    # "A Framework/Method/System for..."
    if FRAMEWORK_SUBTITLE_PATTERN.match(sub_lower):
        return "specification", 0.85

    # "Evidence from X"
    for pat in EVIDENCE_PATTERNS:
        if re.search(pat, sub_lower):
            return "empirical_grounding", 0.90

    # Narrative: "How [proper noun] did X while Y"
    if re.search(r"how [A-Z]", subtitle) and re.search(r"\b(while|despite|although|yet)\b", sub_lower):
        return "narrative", 0.80

    # Mechanism: verb triad or process description
    if re.search(r"(and|,)\s+\w+ing\b.*\band\b", sub_lower):
        return "mechanism", 0.60

    # Scoping: often starts with a domain or context
    scoping_patterns = [
        r"^the (role|case|effect|impact|influence) of",
        r"^(insights|lessons|perspectives) from",
        r"^(a|the) (study|analysis|investigation|survey|review) of",
    ]
    for pat in scoping_patterns:
        if re.search(pat, sub_lower):
            return "scoping", 0.70

    # Causal claim: "X affects/shapes/drives/determines Y"
    causal_verbs = ["affects", "shapes", "drives", "determines", "influences",
                    "leads to", "causes", "predicts", "explains", "mediates",
                    "moderates"]
    for verb in causal_verbs:
        if verb in sub_lower:
            return "causal_claim", 0.70

    # Domain grounding: mentions specific domain/context
    if re.search(r"in (online|digital|virtual|mobile|social|health|financial|organizational)", sub_lower):
        return "domain_grounding", 0.55

    # For name_description structure, subtitle describes the artifact
    if structure == "name_description":
        return "specification", 0.75

    # Default
    return "scoping", 0.35


# ---------------------------------------------------------------------------
# Relation classifier
# ---------------------------------------------------------------------------

def classify_relation(structure, rhetorical, subtitle_fn):
    """Determine how headline and subtitle connect."""
    if structure in ("headline_only", "question_only") or subtitle_fn == "none":
        return "none", 0.95

    # Question → Answer
    if structure == "question_answer":
        return "answers", 0.90

    # Name → Describes
    if structure == "name_description":
        return "describes", 0.90

    # Paradox → Resolves
    if rhetorical == "paradox":
        return "resolves", 0.75

    # Contrast → Supersedes
    if rhetorical == "contrast":
        return "supersedes", 0.75

    # How-mechanism subtitle → Explains
    if subtitle_fn == "how_mechanism":
        return "explains", 0.75

    # Narrative subtitle → Illustrates
    if subtitle_fn == "narrative":
        return "illustrates", 0.80

    # Empirical grounding → Locates
    if subtitle_fn == "empirical_grounding":
        return "locates", 0.75

    # Specification → Operationalizes or Instantiates
    if subtitle_fn == "specification":
        return "operationalizes", 0.55

    # Mechanism → Unpacks
    if subtitle_fn == "mechanism":
        return "unpacks", 0.70

    # Causal claim → Explains
    if subtitle_fn == "causal_claim":
        return "explains", 0.65

    # Scoping → Locates
    if subtitle_fn == "scoping":
        return "locates", 0.55

    # Default
    return "evokes", 0.35


# ---------------------------------------------------------------------------
# Main classifier
# ---------------------------------------------------------------------------

def classify_title(entry):
    """Classify a single title entry across all dimensions."""
    title = entry["title"]
    venue = entry["venue"]

    # Split headline/subtitle
    if ":" in title:
        parts = title.split(":", 1)
        headline = parts[0].strip()
        subtitle = parts[1].strip()
    else:
        headline = title
        subtitle = None

    # Classify each dimension
    structure, s_conf = classify_structure(title)
    rhetorical, r_conf = classify_rhetorical(title, headline, subtitle, structure)
    valence, v_conf = classify_valence(title)
    lead, l_conf = classify_lead(title, headline, subtitle, structure, rhetorical, venue)
    subtitle_fn, sf_conf = classify_subtitle_fn(title, headline, subtitle, structure)
    relation, rel_conf = classify_relation(structure, rhetorical, subtitle_fn)

    avg_confidence = (s_conf + r_conf + v_conf + l_conf + sf_conf + rel_conf) / 6

    return {
        "title": title,
        "venue": venue,
        "cluster": entry.get("cluster", ""),
        "year": entry.get("year"),
        "doi": entry.get("doi"),
        "headline": headline,
        "subtitle": subtitle,
        # Dimensions
        "structure": structure,
        "lead": lead,
        "rhetorical": rhetorical,
        "valence": valence,
        "subtitle_fn": subtitle_fn,
        "relation": relation,
        # Confidence
        "confidence": round(avg_confidence, 3),
        "confidence_detail": {
            "structure": round(s_conf, 2),
            "lead": round(l_conf, 2),
            "rhetorical": round(r_conf, 2),
            "valence": round(v_conf, 2),
            "subtitle_fn": round(sf_conf, 2),
            "relation": round(rel_conf, 2),
        },
        "method": "heuristic",
    }


# ---------------------------------------------------------------------------
# Batch processing and summary
# ---------------------------------------------------------------------------

def run_classification(input_path, output_path):
    """Classify all titles and write results."""
    with open(input_path) as f:
        data = json.load(f)

    titles = data["titles"]
    results = [classify_title(t) for t in titles]

    # Summary statistics
    summary = compute_summary(results)

    output = {
        "metadata": {
            "source": str(input_path),
            "total": len(results),
            "method": "heuristic",
            "grammar_version": "1.0",
            "description": "1,000 academic titles classified against the title grammar",
        },
        "summary": summary,
        "titles": results,
    }

    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    return results, summary


def compute_summary(results):
    """Compute distribution summaries across all dimensions."""
    n = len(results)

    def dist(key):
        counts = {}
        for r in results:
            val = r[key]
            counts[val] = counts.get(val, 0) + 1
        return {k: {"count": v, "pct": round(v / n * 100, 1)} for k, v in sorted(counts.items(), key=lambda x: -x[1])}

    def dist_by_venue(key):
        by_venue = {}
        for r in results:
            venue = r["venue"]
            val = r[key]
            if venue not in by_venue:
                by_venue[venue] = {}
            by_venue[venue][val] = by_venue[venue].get(val, 0) + 1
        # Convert to pct
        out = {}
        for venue, counts in sorted(by_venue.items()):
            total = sum(counts.values())
            out[venue] = {k: round(v / total * 100, 1) for k, v in sorted(counts.items(), key=lambda x: -x[1])}
        return out

    # Average confidence by dimension
    conf_dims = ["structure", "lead", "rhetorical", "valence", "subtitle_fn", "relation"]
    avg_conf = {}
    for dim in conf_dims:
        vals = [r["confidence_detail"][dim] for r in results]
        avg_conf[dim] = round(sum(vals) / len(vals), 3)

    return {
        "overall_distributions": {
            "structure": dist("structure"),
            "lead": dist("lead"),
            "rhetorical": dist("rhetorical"),
            "valence": dist("valence"),
            "subtitle_fn": dist("subtitle_fn"),
            "relation": dist("relation"),
        },
        "by_venue": {
            "structure": dist_by_venue("structure"),
            "rhetorical": dist_by_venue("rhetorical"),
            "lead": dist_by_venue("lead"),
            "valence": dist_by_venue("valence"),
        },
        "confidence": {
            "overall_mean": round(sum(r["confidence"] for r in results) / n, 3),
            "by_dimension": avg_conf,
            "low_confidence_count": sum(1 for r in results if r["confidence"] < 0.5),
            "high_confidence_count": sum(1 for r in results if r["confidence"] >= 0.7),
        },
    }


def print_summary(summary):
    """Print a human-readable summary."""
    print("\n" + "=" * 70)
    print("TITLE GRAMMAR CLASSIFICATION — SUMMARY")
    print("=" * 70)

    for dim_name, dist in summary["overall_distributions"].items():
        print(f"\n--- {dim_name.upper()} ---")
        for val, info in dist.items():
            bar = "#" * int(info["pct"] / 2)
            print(f"  {val:25s} {info['count']:4d} ({info['pct']:5.1f}%) {bar}")

    print(f"\n--- CONFIDENCE ---")
    conf = summary["confidence"]
    print(f"  Overall mean: {conf['overall_mean']:.3f}")
    for dim, val in conf["by_dimension"].items():
        print(f"  {dim:15s}: {val:.3f}")
    print(f"  Low confidence (<0.5):  {conf['low_confidence_count']}")
    print(f"  High confidence (>=0.7): {conf['high_confidence_count']}")

    # By-venue breakdowns for key dimensions
    for dim_name in ["structure", "rhetorical"]:
        print(f"\n--- {dim_name.upper()} BY VENUE ---")
        bv = summary["by_venue"][dim_name]
        # Get all possible values
        all_vals = set()
        for venue_data in bv.values():
            all_vals.update(venue_data.keys())
        all_vals = sorted(all_vals)

        # Header
        header = f"  {'Venue':>8}"
        for v in all_vals[:8]:  # limit columns
            header += f" {v[:12]:>12}"
        print(header)

        for venue in ["ASQ", "OrgSci", "ManSci", "CHI", "TOCHI", "NeurIPS", "HRI", "Nature", "Science"]:
            if venue not in bv:
                continue
            row = f"  {venue:>8}"
            for v in all_vals[:8]:
                pct = bv[venue].get(v, 0)
                row += f" {pct:>11.1f}%"
            print(row)


if __name__ == "__main__":
    input_path = Path(__file__).parent / "title_dataset.json"
    output_path = Path(__file__).parent / "title_dataset_classified.json"

    print(f"Classifying titles from: {input_path}")
    results, summary = run_classification(input_path, output_path)
    print_summary(summary)
    print(f"\nFull results written to: {output_path}")
    print(f"File size: {output_path.stat().st_size / 1024:.1f} KB")
