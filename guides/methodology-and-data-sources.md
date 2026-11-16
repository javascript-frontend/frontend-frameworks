# Methodology & Live Data Sources (Verified 2026-11-16)

Older frontend popularity gists suffer from broken image links, dead survey charts, and stale 2018–2022 metrics. Every quantitative number in `frameworks.json` was verified directly against live public APIs on **2026-11-16**:

1. **GitHub Stars & Forks:** `https://api.github.com/repos/{owner}/{repo}`
2. **Latest npm Release:** `https://registry.npmjs.org/{package}/latest`
3. **npm Weekly Downloads:** `https://api.npmjs.org/downloads/point/last-week/{package}`

## Important Measurement Notes

- **Vue Repository Split:** `vuejs/core` (`55,029` stars) is the active Vue 3+ codebase, whereas `vuejs/vue` (`212,519` stars) is the legacy Vue 2 repository. Both are documented so historical comparisons remain transparent.
- **npm Downloads Context:** React's `260.9M/week` includes CI pipelines, transitive dependencies, and meta-frameworks (`next`, `react-router`). Compare frameworks alongside qualitative ergonomics in `examples/same-app-task-tracker/` rather than treating download counts as a single quality score.
- **htmx Versioning:** `htmx.org` on npm reports `2.0.11` latest while the GitHub releases API lists `v4.0.1` (`bigskysoftware/htmx`); both are noted transparently.
