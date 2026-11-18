# Methodology and live data sources (verified 2026-11-16)

Every quantitative figure in `frameworks.json` was verified against live public APIs on `2026-11-16`:

1. GitHub stars and forks: `https://api.github.com/repos/{owner}/{repo}`
2. Latest npm release: `https://registry.npmjs.org/{package}/latest`
3. npm weekly downloads: `https://api.npmjs.org/downloads/point/last-week/{package}`

## Measurement notes

- Vue repository split: `vuejs/core` (`55,029` stars) is the active Vue 3+ codebase, whereas `vuejs/vue` (`212,519` stars) is the legacy Vue 2 repository.
- npm downloads context: React's `260.9M/week` includes CI pipelines, transitive dependencies, and meta-frameworks (`next`, `react-router`). Weigh adoption numbers alongside the code examples in `examples/same-app-task-tracker/` when picking a stack.
- htmx versioning: `htmx.org` on npm reports `2.0.11` latest while the GitHub releases API lists `v4.0.1` (`bigskysoftware/htmx`).
