# Design: javascript-frontend / frontend-frameworks

The locked system. Every Hallmark run reads this first and pages share it. Change it on purpose; the file is the rule.

## System
- Genre: modern-minimal
- Shape of the first page: Map / Diagram (Stage hero on index, Banner hero on comparison pages)
- Theme: Console (deal 1/3, seed `frontend-frameworks-comparison-workload-823d·60348198·2026-11-16·r0`)
- Axes: dark/grotesk-sans/chromatic-amber · posture: restrained

## Tokens
`docs/styles/tokens.css` is the source of truth.
- Paper steps: `--color-paper` `oklch(17% 0.008 250)`, `--color-paper-2` `oklch(21% 0.009 250)`, `--color-paper-3` `oklch(13.5% 0.007 250)`
- Ink & rules: `--color-ink` `oklch(95% 0.005 250)`, `--color-ink-2` `oklch(83% 0.008 250)`, `--color-muted` `oklch(71% 0.01 250)`, `--color-rule` `oklch(31% 0.01 250)`, `--color-rule-2` `oklch(42% 0.012 250)`
- Signals: `--color-accent` `oklch(82% 0.15 80)` (amber: person/primary action), `--color-cool` `oklch(77% 0.12 245)` (cool blue: instrument/reading), `--color-ok` / `--color-bad`
- Typography: `--font-display` & `--font-body` `"Host Grotesk", ui-sans-serif, system-ui, sans-serif`; `--font-outlier` `"Atkinson Hyperlegible Mono", ui-monospace, monospace` (strictly for measured figures, versions, and code)
- Geometry: `--radius-card: 10px`, `--radius-pill: 6px`, `--rule-hair: 1px`, `--shadow-card: none`

## Controls
- Primary: amber fill (`--color-accent` with `--color-accent-ink`) · `6px` radius · `48px` height (`min-height: 44px` on inline filter controls)
- Secondary: `1px` `--color-rule-2` outline on `--color-paper-2` · same radius and height

## Motion
- Character: still; instant `:focus-visible`, short `220ms` color transitions on controls, full `prefers-reduced-motion: reduce` support.

## Exports
`docs/styles/tokens.css`, `docs/styles/base.css`, and `docs/styles/site.css`.
