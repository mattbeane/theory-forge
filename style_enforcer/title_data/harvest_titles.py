"""
Harvest ~1000 academic paper titles from OpenAlex across multiple disciplines.

Venues selected to span:
- Technical HCI/AI: CHI, TOCHI, NeurIPS, HRI
- Managerial/Org: ASQ, OrgSci, Management Science
- Generalist: Nature, Science

Strategy: Pull recent articles (2015-2025), sample ~100-130 per venue,
output a single JSON dataset tagged by venue and discipline cluster.
"""

import json
import time
import urllib.request
import urllib.parse
from pathlib import Path

# OpenAlex source IDs and metadata
VENUES = [
    # Technical HCI/AI
    {
        "id": "S4363607743",
        "name": "CHI",
        "full_name": "CHI Conference on Human Factors in Computing Systems",
        "cluster": "technical-hci",
    },
    {
        "id": "S89276529",
        "name": "TOCHI",
        "full_name": "ACM Transactions on Computer-Human Interaction",
        "cluster": "technical-hci",
    },
    {
        "id": "S4306420609",
        "name": "NeurIPS",
        "full_name": "Neural Information Processing Systems",
        "cluster": "technical-ai",
    },
    {
        "id": "S4306418552",
        "name": "HRI",
        "full_name": "Human-Robot Interaction",
        "cluster": "technical-hci",
    },
    # Managerial / Organizational
    {
        "id": "S143668711",
        "name": "ASQ",
        "full_name": "Administrative Science Quarterly",
        "cluster": "managerial",
    },
    {
        "id": "S206124708",
        "name": "OrgSci",
        "full_name": "Organization Science",
        "cluster": "managerial",
    },
    {
        "id": "S33323087",
        "name": "ManSci",
        "full_name": "Management Science",
        "cluster": "managerial",
    },
    # Generalist
    {
        "id": "S137773608",
        "name": "Nature",
        "full_name": "Nature",
        "cluster": "generalist",
    },
    {
        "id": "S3880285",
        "name": "Science",
        "full_name": "Science",
        "cluster": "generalist",
    },
]

# Target ~1000 total. Distribute by venue size and discipline coverage.
# Smaller venues (CHI conf, HRI, TOCHI) get fewer; bigger ones get more.
TARGETS = {
    "CHI": 120,
    "TOCHI": 100,
    "NeurIPS": 120,
    "HRI": 100,
    "ASQ": 100,
    "OrgSci": 100,
    "ManSci": 120,
    "Nature": 120,
    "Science": 120,
}

BASE_URL = "https://api.openalex.org/works"
# polite pool: add email for faster rate limit
MAILTO = "mattbeane@ucsb.edu"


def fetch_titles(venue, target_n):
    """Fetch up to target_n article titles from a venue via OpenAlex."""
    source_id = venue["id"]
    titles = []
    page = 1
    per_page = min(target_n, 200)

    while len(titles) < target_n:
        params = {
            "filter": f"primary_location.source.id:{source_id},type:article,from_publication_date:2015-01-01,to_publication_date:2025-12-31",
            "per_page": per_page,
            "page": page,
            "select": "id,title,publication_year,doi",
            "sort": "cited_by_count:desc",  # get well-cited papers first
            "mailto": MAILTO,
        }
        url = f"{BASE_URL}?{urllib.parse.urlencode(params)}"

        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode())
        except Exception as e:
            print(f"  ERROR on page {page}: {e}")
            break

        results = data.get("results", [])
        if not results:
            break

        for work in results:
            title = work.get("title")
            if not title:
                continue
            titles.append({
                "title": title,
                "year": work.get("publication_year"),
                "doi": work.get("doi"),
                "openalex_id": work.get("id"),
                "venue": venue["name"],
                "venue_full": venue["full_name"],
                "cluster": venue["cluster"],
            })

        total_available = data.get("meta", {}).get("count", 0)
        print(f"  Page {page}: got {len(results)} works (total available: {total_available}, collected: {len(titles)})")

        if len(titles) >= target_n:
            break
        if len(results) < per_page:
            break

        page += 1
        time.sleep(0.15)  # polite rate limiting

    return titles[:target_n]


def main():
    all_titles = []

    for venue in VENUES:
        target = TARGETS[venue["name"]]
        print(f"\n{'='*60}")
        print(f"Fetching {target} titles from {venue['name']} ({venue['full_name']})")
        print(f"{'='*60}")

        titles = fetch_titles(venue, target)
        all_titles.extend(titles)
        print(f"  -> Collected {len(titles)} titles")
        time.sleep(0.2)

    # Summary
    print(f"\n{'='*60}")
    print(f"TOTAL: {len(all_titles)} titles")
    print(f"{'='*60}")

    by_cluster = {}
    by_venue = {}
    for t in all_titles:
        by_cluster.setdefault(t["cluster"], []).append(t)
        by_venue.setdefault(t["venue"], []).append(t)

    print("\nBy cluster:")
    for cluster, items in sorted(by_cluster.items()):
        print(f"  {cluster}: {len(items)}")

    print("\nBy venue:")
    for venue, items in sorted(by_venue.items()):
        print(f"  {venue}: {len(items)}")

    # Write output
    out_path = Path(__file__).parent / "title_dataset.json"
    with open(out_path, "w") as f:
        json.dump({
            "metadata": {
                "description": "Academic paper titles from OpenAlex for title grammar validation",
                "venues": [v["name"] for v in VENUES],
                "date_range": "2015-2025",
                "sort": "cited_by_count:desc",
                "total": len(all_titles),
                "harvested_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            },
            "titles": all_titles,
        }, f, indent=2)

    print(f"\nDataset written to: {out_path}")
    print(f"File size: {out_path.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
