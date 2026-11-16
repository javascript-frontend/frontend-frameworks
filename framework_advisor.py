#!/usr/bin/env python3
"""Frontend Frameworks Advisor & Comparison CLI (2026).

Zero-dependency Python 3.9+ CLI for comparing verified frontend frameworks,
recommending the best stack for a concrete use case, exporting CSV, and
keeping root/docs datasets synchronized.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
from pathlib import Path
import sys
from typing import Any


ROOT_DIR = Path(__file__).resolve().parent
DATA_PATH = ROOT_DIR / "frameworks.json"
DOCS_DATA_PATH = ROOT_DIR / "docs" / "frameworks.json"

USE_CASE_LABELS = {
    "saas-dashboard": "Interactive SaaS Dashboard / Web App",
    "seo-content": "SEO Content Site, Docs, Blog or Marketing Landing",
    "enterprise-app": "Large Multi-Team Enterprise Platform",
    "lightweight-widget": "Embeddable Widget / Low-JS Enhancement",
    "ecommerce": "E-Commerce Storefront (Core Web Vitals + SEO)",
    "internal-tool": "Internal Admin Panel / CRUD Portal",
    "ai-app": "AI Streaming UI / Agent Workspace",
}


def load_dataset(path: Path = DATA_PATH) -> dict[str, Any]:
    """Load and parse the verified frameworks dataset."""
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def score_framework(
    fw: dict[str, Any],
    use_case: str,
    seo_critical: bool = False,
    low_bundle: bool = False,
    low_learning_curve: bool = False,
    prefer_category: str | None = None,
) -> tuple[int, list[str]]:
    """Score a framework against user constraints and explain why."""
    score = 0
    reasons: list[str] = []

    best_for = fw.get("best_for", [])
    if use_case in best_for:
        rank_bonus = max(40 - best_for.index(use_case) * 8, 16)
        score += rank_bonus
        reasons.append(f"strong fit for {use_case}")

    if seo_critical:
        ssr_score = int(fw.get("ssr_seo_score", 3))
        score += ssr_score * 6
        if ssr_score == 5:
            reasons.append("top-tier SSR/SSG SEO readiness")
        if fw.get("category") == "meta-framework":
            score += 12
            reasons.append("built-in SSR/SSG routing & metadata")

    if low_bundle:
        tier = fw.get("runtime_tier", "").lower()
        if "zero js" in tier or "tiny" in tier:
            score += 22
            reasons.append("minimal client JavaScript payload")
        elif "small" in tier:
            score += 10

    if low_learning_curve:
        curve = fw.get("learning_curve", "").lower()
        if "very low" in curve:
            score += 18
            reasons.append("minimal onboarding & zero/low boilerplate")
        elif curve == "low":
            score += 12
            reasons.append("gentle learning curve")

    if prefer_category and fw.get("category") == prefer_category:
        score += 10

    # Ecosystem adoption tie-breaker (bounded so niche winners still surface)
    downloads = int(fw.get("npm_weekly_downloads") or 0)
    if downloads >= 50_000_000:
        score += 8
    elif downloads >= 10_000_000:
        score += 5
    elif downloads >= 1_000_000:
        score += 2

    if fw.get("starter_path"):
        score += 3
        reasons.append(f"free starter at {fw['starter_path']}")

    return score, reasons


def recommend_frameworks(
    dataset: dict[str, Any],
    use_case: str,
    seo_critical: bool = False,
    low_bundle: bool = False,
    low_learning_curve: bool = False,
    category: str | None = None,
    limit: int = 5,
) -> list[dict[str, Any]]:
    """Return top ranked framework recommendations for a given scenario."""
    ranked: list[dict[str, Any]] = []
    for fw in dataset["frameworks"]:
        score, reasons = score_framework(
            fw,
            use_case=use_case,
            seo_critical=seo_critical,
            low_bundle=low_bundle,
            low_learning_curve=low_learning_curve,
            prefer_category=category,
        )
        ranked.append({**fw, "match_score": score, "match_reasons": reasons})

    ranked.sort(key=lambda item: (-item["match_score"], -item["npm_weekly_downloads"]))
    return ranked[:limit]


def format_number(value: int | None) -> str:
    """Format large integer metrics readably."""
    if value is None:
        return "N/A"
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"{value / 1_000:.1f}K"
    return str(value)


def render_table(frameworks: list[dict[str, Any]]) -> str:
    """Render a clean Markdown comparison table."""
    lines = [
        "| Framework | Category | Latest | GitHub Stars | npm Weekly | Rendering Model | SSR/SEO |",
        "| :--- | :--- | :--- | ---: | ---: | :--- | :---: |",
    ]
    for fw in frameworks:
        lines.append(
            f"| **{fw['name']}** (`{fw['npm_package']}`) | {fw['category']} | "
            f"`{fw['latest_version']}` | {fw['stars']:,} | "
            f"{format_number(fw['npm_weekly_downloads'])} | "
            f"{fw['rendering_model']} | {fw['ssr_seo_score']}/5 |"
        )
    return "\n".join(lines)


def export_csv(frameworks: list[dict[str, Any]]) -> str:
    """Export framework records as CSV text."""
    buf = io.StringIO()
    fields = [
        "id",
        "name",
        "category",
        "github_repo",
        "npm_package",
        "latest_version",
        "stars",
        "forks",
        "npm_weekly_downloads",
        "license",
        "rendering_model",
        "ssr_seo_score",
        "learning_curve",
        "official_url",
    ]
    writer = csv.DictWriter(buf, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    for fw in frameworks:
        writer.writerow(fw)
    return buf.getvalue()


def verify_sync() -> bool:
    """Verify root frameworks.json and docs/frameworks.json match byte-for-byte."""
    if not DATA_PATH.exists() or not DOCS_DATA_PATH.exists():
        return False
    return DATA_PATH.read_text(encoding="utf-8") == DOCS_DATA_PATH.read_text(encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    """Construct CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="framework_advisor",
        description="Compare 2026 frontend frameworks and pick the right stack for your project.",
    )
    parser.add_argument(
        "--use-case",
        choices=sorted(USE_CASE_LABELS.keys()),
        help="Target workload to rank frameworks against.",
    )
    parser.add_argument("--seo-critical", action="store_true", help="Prioritize SSR/SSG and zero-JS SEO.")
    parser.add_argument("--low-bundle", action="store_true", help="Prioritize minimal client JS payload.")
    parser.add_argument("--low-learning-curve", action="store_true", help="Prioritize fast team onboarding.")
    parser.add_argument(
        "--category",
        choices=["core-ui", "meta-framework"],
        help="Optional preference for core UI libraries vs full-stack meta-frameworks.",
    )
    parser.add_argument(
        "--compare",
        nargs="+",
        metavar="ID",
        help="Compare specific framework IDs side-by-side (e.g. --compare react vue svelte angular).",
    )
    parser.add_argument("--list", action="store_true", help="List all verified frameworks.")
    parser.add_argument("--export-csv", action="store_true", help="Export dataset as CSV to stdout.")
    parser.add_argument("--json", action="store_true", help="Output structured JSON.")
    parser.add_argument("--limit", type=int, default=5, help="Number of recommendations to display.")
    parser.add_argument("--verify-sync", action="store_true", help="Check root/docs JSON sync.")
    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.verify_sync:
        ok = verify_sync()
        print("OK: frameworks.json and docs/frameworks.json are synchronized." if ok else "ERROR: datasets out of sync.")
        return 0 if ok else 1

    dataset = load_dataset()
    frameworks = dataset["frameworks"]

    if args.export_csv:
        sys.stdout.write(export_csv(frameworks))
        return 0

    if args.compare:
        wanted = {item.lower() for item in args.compare}
        selected = [fw for fw in frameworks if fw["id"] in wanted]
        if not selected:
            print(f"No matching frameworks found for: {', '.join(args.compare)}", file=sys.stderr)
            return 1
        if args.json:
            print(json.dumps(selected, indent=2))
        else:
            print(render_table(selected))
        return 0

    if args.use_case:
        recs = recommend_frameworks(
            dataset,
            use_case=args.use_case,
            seo_critical=args.seo_critical,
            low_bundle=args.low_bundle,
            low_learning_curve=args.low_learning_curve,
            category=args.category,
            limit=args.limit,
        )
        if args.json:
            print(json.dumps({"use_case": args.use_case, "recommendations": recs}, indent=2))
            return 0
        print(f"Top Recommendations for: {USE_CASE_LABELS[args.use_case]}\n")
        for idx, fw in enumerate(recs, start=1):
            why = "; ".join(fw["match_reasons"]) if fw["match_reasons"] else fw["summary"]
            print(f"{idx}. {fw['name']} ({fw['latest_version']}) — score {fw['match_score']} | {why}")
        return 0

    if args.json:
        print(json.dumps(dataset, indent=2))
    else:
        print(f"Verified Frontend Frameworks ({dataset['metadata']['verified_at']}):\n")
        print(render_table(frameworks))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
