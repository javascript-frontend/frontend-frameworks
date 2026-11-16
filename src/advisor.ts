import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

export type FrameworkCategory = "core-ui" | "meta-framework";

export type UseCase =
  | "saas-dashboard"
  | "seo-content"
  | "enterprise-app"
  | "lightweight-widget"
  | "ecommerce"
  | "internal-tool"
  | "ai-app";

export interface FrameworkRecord {
  id: string;
  name: string;
  category: FrameworkCategory;
  github_repo: string;
  legacy_github_repo?: string;
  legacy_stars?: number;
  npm_package: string;
  official_url: string;
  latest_version: string;
  github_latest_tag?: string;
  stars: number;
  forks: number;
  npm_weekly_downloads: number;
  license: string;
  rendering_model: string;
  reactivity: string;
  language: string;
  ssr_seo_score: number;
  learning_curve: string;
  runtime_tier: string;
  best_for: UseCase[];
  starter_path: string | null;
  summary: string;
}

export interface FrameworkDataset {
  metadata: {
    verified_at: string;
    sources: string[];
    notes: string;
  };
  frameworks: FrameworkRecord[];
}

export interface RecommendationOptions {
  useCase: UseCase;
  seoCritical?: boolean;
  lowBundle?: boolean;
  lowLearningCurve?: boolean;
  category?: FrameworkCategory;
  limit?: number;
}

export interface ScoredFramework extends FrameworkRecord {
  match_score: number;
  match_reasons: string[];
}

export const USE_CASE_LABELS: Record<UseCase, string> = {
  "saas-dashboard": "Interactive SaaS Dashboard / Web App",
  "seo-content": "SEO Content Site, Docs, Blog or Marketing Landing",
  "enterprise-app": "Large Multi-Team Enterprise Platform",
  "lightweight-widget": "Embeddable Widget / Low-JS Enhancement",
  "ecommerce": "E-Commerce Storefront (Core Web Vitals + SEO)",
  "internal-tool": "Internal Admin Panel / CRUD Portal",
  "ai-app": "AI Streaming UI / Agent Workspace",
};

export function loadDataset(customPath?: string): FrameworkDataset {
  const here = dirname(fileURLToPath(import.meta.url));
  const datasetPath = customPath ?? resolve(here, "..", "frameworks.json");
  return JSON.parse(readFileSync(datasetPath, "utf8")) as FrameworkDataset;
}

export function formatCompactNumber(value: number): string {
  if (value >= 1_000_000) return `${(value / 1_000_000).toFixed(1)}M`;
  if (value >= 1_000) return `${(value / 1_000).toFixed(1)}K`;
  return String(value);
}

export function scoreFramework(
  fw: FrameworkRecord,
  options: RecommendationOptions,
): { score: number; reasons: string[] } {
  let score = 0;
  const reasons: string[] = [];

  const idx = fw.best_for.indexOf(options.useCase);
  if (idx !== -1) {
    score += Math.max(40 - idx * 8, 16);
    reasons.push(`strong fit for ${options.useCase}`);
  }

  if (options.seoCritical) {
    score += fw.ssr_seo_score * 6;
    if (fw.ssr_seo_score === 5) {
      reasons.push("top-tier SSR/SSG SEO readiness");
    }
    if (fw.category === "meta-framework") {
      score += 12;
      reasons.push("built-in SSR/SSG routing & metadata");
    }
  }

  if (options.lowBundle) {
    const tier = fw.runtime_tier.toLowerCase();
    if (tier.includes("zero js") || tier.includes("tiny")) {
      score += 22;
      reasons.push("minimal client JavaScript payload");
    } else if (tier.includes("small")) {
      score += 10;
    }
  }

  if (options.lowLearningCurve) {
    const curve = fw.learning_curve.toLowerCase();
    if (curve.includes("very low")) {
      score += 18;
      reasons.push("minimal onboarding & zero/low boilerplate");
    } else if (curve === "low") {
      score += 12;
      reasons.push("gentle learning curve");
    }
  }

  if (options.category && fw.category === options.category) {
    score += 10;
  }

  if (fw.npm_weekly_downloads >= 50_000_000) score += 8;
  else if (fw.npm_weekly_downloads >= 10_000_000) score += 5;
  else if (fw.npm_weekly_downloads >= 1_000_000) score += 2;

  if (fw.starter_path) {
    score += 3;
    reasons.push(`free starter at ${fw.starter_path}`);
  }

  return { score, reasons };
}

export function recommendFrameworks(
  dataset: FrameworkDataset,
  options: RecommendationOptions,
): ScoredFramework[] {
  const limit = options.limit ?? 5;
  return dataset.frameworks
    .map((fw) => {
      const { score, reasons } = scoreFramework(fw, options);
      return { ...fw, match_score: score, match_reasons: reasons };
    })
    .sort((a, b) => b.match_score - a.match_score || b.npm_weekly_downloads - a.npm_weekly_downloads)
    .slice(0, limit);
}

export function exportCsv(frameworks: FrameworkRecord[]): string {
  const fields: Array<keyof FrameworkRecord> = [
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
  ];
  const escapeCell = (raw: unknown): string => {
    const str = String(raw ?? "");
    return /[",\n]/.test(str) ? `"${str.replace(/"/g, "\"\"")}"` : str;
  };
  const lines = [fields.join(",")];
  for (const fw of frameworks) {
    lines.push(fields.map((key) => escapeCell(fw[key])).join(","));
  }
  return `${lines.join("\n")}\n`;
}

export function renderMarkdownTable(frameworks: FrameworkRecord[]): string {
  const header = [
    "| Framework | Category | Latest | GitHub Stars | npm Weekly | Rendering Model | SSR/SEO |",
    "| :--- | :--- | :--- | ---: | ---: | :--- | :---: |",
  ];
  const rows = frameworks.map(
    (fw) =>
      `| **${fw.name}** (\`${fw.npm_package}\`) | ${fw.category} | \`${fw.latest_version}\` | ${fw.stars.toLocaleString("en-US")} | ${formatCompactNumber(fw.npm_weekly_downloads)} | ${fw.rendering_model} | ${fw.ssr_seo_score}/5 |`,
  );
  return [...header, ...rows].join("\n");
}

function parseCliArgs(argv: string[]) {
  let useCase: UseCase | undefined;
  let seoCritical = false;
  let lowBundle = false;
  let lowLearningCurve = false;
  let category: FrameworkCategory | undefined;
  let jsonOutput = false;
  let exportCsvFlag = false;
  let limit = 5;
  const compare: string[] = [];

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--use-case" && argv[i + 1]) {
      useCase = argv[++i] as UseCase;
    } else if (arg === "--seo-critical") {
      seoCritical = true;
    } else if (arg === "--low-bundle") {
      lowBundle = true;
    } else if (arg === "--low-learning-curve") {
      lowLearningCurve = true;
    } else if (arg === "--category" && argv[i + 1]) {
      category = argv[++i] as FrameworkCategory;
    } else if (arg === "--limit" && argv[i + 1]) {
      limit = Number.parseInt(argv[++i], 10) || 5;
    } else if (arg === "--json") {
      jsonOutput = true;
    } else if (arg === "--export-csv") {
      exportCsvFlag = true;
    } else if (arg === "--compare") {
      while (argv[i + 1] && !argv[i + 1].startsWith("--")) {
        compare.push(argv[++i].toLowerCase());
      }
    }
  }
  return { useCase, seoCritical, lowBundle, lowLearningCurve, category, jsonOutput, exportCsvFlag, limit, compare };
}

function main(): number {
  const args = parseCliArgs(process.argv.slice(2));
  const dataset = loadDataset();

  if (args.exportCsvFlag) {
    process.stdout.write(exportCsv(dataset.frameworks));
    return 0;
  }

  if (args.compare.length > 0) {
    const wanted = new Set(args.compare);
    const selected = dataset.frameworks.filter((fw) => wanted.has(fw.id));
    if (selected.length === 0) {
      console.error(`No matching frameworks found for: ${args.compare.join(", ")}`);
      return 1;
    }
    console.log(args.jsonOutput ? JSON.stringify(selected, null, 2) : renderMarkdownTable(selected));
    return 0;
  }

  if (args.useCase) {
    if (!(args.useCase in USE_CASE_LABELS)) {
      console.error(`Unknown use-case: ${args.useCase}`);
      return 1;
    }
    const recs = recommendFrameworks(dataset, {
      useCase: args.useCase,
      seoCritical: args.seoCritical,
      lowBundle: args.lowBundle,
      lowLearningCurve: args.lowLearningCurve,
      category: args.category,
      limit: args.limit,
    });
    if (args.jsonOutput) {
      console.log(JSON.stringify({ use_case: args.useCase, recommendations: recs }, null, 2));
      return 0;
    }
    console.log(`Top Recommendations for: ${USE_CASE_LABELS[args.useCase]}\n`);
    recs.forEach((fw, index) => {
      const why = fw.match_reasons.length > 0 ? fw.match_reasons.join("; ") : fw.summary;
      console.log(`${index + 1}. ${fw.name} (${fw.latest_version}) — score ${fw.match_score} | ${why}`);
    });
    return 0;
  }

  console.log(
    args.jsonOutput
      ? JSON.stringify(dataset, null, 2)
      : `Verified Frontend Frameworks (${dataset.metadata.verified_at}):\n\n${renderMarkdownTable(dataset.frameworks)}`,
  );
  return 0;
}

const isMain = process.argv[1] && fileURLToPath(import.meta.url) === resolve(process.argv[1]);
if (isMain) {
  process.exitCode = main();
}
