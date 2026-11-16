"""Tests for frontend-frameworks dataset, CLI advisor, examples, starters, and SEO assets."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import framework_advisor  # noqa: E402


class TestFrontendFrameworksRepo(unittest.TestCase):
    def test_dataset_sync_and_schema(self) -> None:
        self.assertTrue(framework_advisor.verify_sync(), "frameworks.json and docs/frameworks.json must match")
        data = framework_advisor.load_dataset()
        self.assertEqual(len(data["frameworks"]), 15)
        for fw in data["frameworks"]:
            self.assertGreater(fw["stars"], 1000)
            self.assertGreater(fw["npm_weekly_downloads"], 1000)
            self.assertIn(fw["category"], {"core-ui", "meta-framework"})
            self.assertTrue(fw["official_url"].startswith("https://"))

    def test_recommendations_seo_content_ranks_astro_high(self) -> None:
        data = framework_advisor.load_dataset()
        recs = framework_advisor.recommend_frameworks(
            data,
            use_case="seo-content",
            seo_critical=True,
            low_bundle=True,
            limit=3,
        )
        top_ids = [r["id"] for r in recs]
        self.assertIn("astro", top_ids)

    def test_recommendations_saas_returns_react_or_nextjs(self) -> None:
        data = framework_advisor.load_dataset()
        recs = framework_advisor.recommend_frameworks(
            data,
            use_case="saas-dashboard",
            seo_critical=True,
            limit=3,
        )
        top_ids = [r["id"] for r in recs]
        self.assertTrue("nextjs" in top_ids or "react" in top_ids)

    def test_cli_compare_and_csv(self) -> None:
        res = subprocess.run(
            [sys.executable, str(ROOT / "framework_advisor.py"), "--compare", "react", "vue", "svelte"],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("React", res.stdout)
        self.assertIn("Vue", res.stdout)
        self.assertIn("Svelte", res.stdout)

        csv_res = subprocess.run(
            [sys.executable, str(ROOT / "framework_advisor.py"), "--export-csv"],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("github_repo,npm_package", csv_res.stdout)

    def test_examples_and_starters_exist(self) -> None:
        examples = [
            "examples/same-app-task-tracker/react/App.tsx",
            "examples/same-app-task-tracker/vue/App.vue",
            "examples/same-app-task-tracker/svelte/App.svelte",
            "examples/same-app-task-tracker/angular/app.component.ts",
            "examples/same-app-task-tracker/solid/App.tsx",
        ]
        for rel in examples:
            self.assertTrue((ROOT / rel).is_file(), f"Missing example: {rel}")

        starters = [
            "starters/react-vite-ts-saas/package.json",
            "starters/vue3-vite-ts-app/package.json",
            "starters/svelte5-vite-ts-app/package.json",
            "starters/astro-seo-landing/package.json",
        ]
        for rel in starters:
            pkg = json.loads((ROOT / rel).read_text(encoding="utf-8"))
            self.assertIn("dependencies", pkg)

    def test_seo_and_geo_files(self) -> None:
        self.assertTrue((ROOT / "llms.txt").is_file())
        self.assertTrue((ROOT / "docs" / "llms.txt").is_file())
        self.assertTrue((ROOT / "docs" / "robots.txt").is_file())
        self.assertTrue((ROOT / "docs" / "assets" / "preview.png").is_file())
        sitemap = (ROOT / "docs" / "sitemap.xml").read_text(encoding="utf-8")
        for html in (ROOT / "docs").glob("*.html"):
            if html.name == "index.html":
                self.assertIn("https://javascript-frontend.github.io/frontend-frameworks/</loc>", sitemap)
            else:
                self.assertIn(html.name, sitemap)


if __name__ == "__main__":
    unittest.main()
