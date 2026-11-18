#!/usr/bin/env python3
"""Generate and validate SEO comparison, alternatives, and workload HTML pages in docs/."""

from __future__ import annotations

from html import escape
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "frameworks.json"
DOCS_DIR = ROOT / "docs"
BASE_URL = "https://javascript-frontend.github.io/frontend-frameworks"
LASTMOD = "2026-11-18"

VS_PAIRS: list[dict[str, Any]] = [
    {
        "slug": "react-vs-vue",
        "a": "react",
        "b": "vue",
        "title": "React vs Vue (2026): Adoption, Syntax, Ecosystem and Performance",
        "desc": "React 19.3 vs Vue 3.5 in 2026: compare 260.9M vs 25.2M weekly npm downloads, Hooks vs Composition API, and Next.js vs Nuxt 4.",
        "h1": "React 19 vs Vue 3.5 in 2026.",
        "lead": "Verified adoption metrics, reactivity models, and identical Sprint Task Tracker line counts.",
        "loc_a": "82 lines",
        "loc_b": "76 lines",
        "win_a": "Pick React 19 for maximum hiring reach, third-party AI and UI ecosystems (Radix, shadcn/ui, TanStack), and Next.js full-stack conventions.",
        "win_b": "Pick Vue 3.5 for cohesive first-party tooling (Vue Router, Pinia, Nuxt 4), clear HTML single-file components, and fast team onboarding.",
        "faq_q": "Should I choose React or Vue in 2026?",
        "faq_a": "Choose React 19 if hiring pool, third-party UI libraries, and Next.js ecosystem breadth matter most. Choose Vue 3.5 if you want cleaner single-file components, faster onboarding, and official first-party routing and state via Vue Router, Pinia, and Nuxt 4.",
        "related": ["react-vs-svelte.html", "react-vs-angular.html", "vue-vs-svelte.html", "best-frontend-framework-for-seo.html"],
    },
    {
        "slug": "react-vs-svelte",
        "a": "react",
        "b": "svelte",
        "title": "React vs Svelte 5 (2026): Hooks vs Runes, Bundle Size and Adoption",
        "desc": "Compare React 19.3 vs Svelte 5.57 in 2026: Virtual DOM vs compiler Runes ($state, $derived), Next.js vs SvelteKit, and identical app line counts.",
        "h1": "React 19 vs Svelte 5 in 2026.",
        "lead": "Svelte 5 Runes bring explicit signals alongside React 19 Hooks.",
        "loc_a": "82 lines",
        "loc_b": "77 lines",
        "win_a": "Choose React 19 when your team relies on React-specific libraries, multi-vendor design systems, or large hiring pools.",
        "win_b": "Choose Svelte 5 for lean client bundles, zero Virtual DOM overhead, fewer re-render pitfalls, and cohesive SvelteKit full-stack delivery.",
        "faq_q": "Is Svelte 5 faster than React 19?",
        "faq_a": "Svelte 5 compiles templates into direct DOM updates with a 3 to 5 KB runtime overhead and no Virtual DOM diffing, making initial bundles smaller than React 19.",
        "related": ["react-vs-vue.html", "react-vs-angular.html", "svelte-vs-solidjs.html", "lightweight-frontend-frameworks.html"],
    },
    {
        "slug": "react-vs-angular",
        "a": "react",
        "b": "angular",
        "title": "React vs Angular (2026): Enterprise Architecture, Signals and Adoption",
        "desc": "Compare React 19.3 vs Angular 22.2 in 2026: library ecosystem vs TypeScript-first platform with Signals, dependency injection, and long-term maintenance.",
        "h1": "React 19 vs Angular 22 in 2026.",
        "lead": "Flexible UI library and meta-frameworks versus an all-in-one TypeScript Signals platform.",
        "loc_a": "82 lines",
        "loc_b": "93 lines",
        "win_a": "Choose React 19 for faster product iteration, composable third-party packages, and Next.js SSR defaults.",
        "win_b": "Choose Angular 22 when architectural uniformity across large multi-team monorepos outweighs ecosystem flexibility.",
        "faq_q": "Should enterprise teams choose React or Angular in 2026?",
        "faq_a": "Choose Angular 22 if you want built-in dependency injection, router, forms, and strict conventions across large teams; choose React 19 for broader hiring and composable libraries.",
        "related": ["react-vs-vue.html", "react-vs-svelte.html", "vue-vs-angular.html", "best-frontend-framework-for-seo.html"],
    },
    {
        "slug": "vue-vs-svelte",
        "a": "vue",
        "b": "svelte",
        "title": "Vue vs Svelte 5 (2026): Composition API vs Runes and Bundle Size",
        "desc": "Compare Vue 3.5 vs Svelte 5.57 in 2026: single-file components, proxy reactivity vs compiled Runes, Nuxt 4 vs SvelteKit 3, and identical app code.",
        "h1": "Vue 3.5 vs Svelte 5 in 2026.",
        "lead": "Two single-file component frameworks with minimal boilerplate and fast onboarding.",
        "loc_a": "76 lines",
        "loc_b": "77 lines",
        "win_a": "Pick Vue 3.5 for a larger third-party ecosystem, mature enterprise adoption, and Nuxt 4 Nitro hybrid rendering.",
        "win_b": "Pick Svelte 5 for smaller compiled runtime bundles, cleaner $state syntax without .value refs, and lean SvelteKit apps.",
        "faq_q": "How close are Vue 3.5 and Svelte 5 in code size?",
        "faq_a": "In our identical Sprint Task Tracker benchmark, Vue 3.5 takes 76 lines and Svelte 5 takes 77 lines, while Svelte 5 ships a smaller runtime overhead.",
        "related": ["react-vs-vue.html", "react-vs-svelte.html", "nuxt-vs-sveltekit.html", "lightweight-frontend-frameworks.html"],
    },
    {
        "slug": "vue-vs-angular",
        "a": "vue",
        "b": "angular",
        "title": "Vue vs Angular (2026): Progressive SFCs vs Enterprise Signals Platform",
        "desc": "Compare Vue 3.5 vs Angular 22.2 in 2026: learning curve, TypeScript ergonomics, Pinia vs Signals, and Nuxt vs Angular SSR.",
        "h1": "Vue 3.5 vs Angular 22 in 2026.",
        "lead": "Progressive single-file components versus an opinionated TypeScript enterprise platform.",
        "loc_a": "76 lines",
        "loc_b": "93 lines",
        "win_a": "Pick Vue 3.5 for faster onboarding, lighter runtime bundles, and flexible adoption from small widgets to Nuxt apps.",
        "win_b": "Pick Angular 22 when strict multi-team architecture, dependency injection, and standardized CLI tooling are mandatory.",
        "faq_q": "Is Vue easier to learn than Angular?",
        "faq_a": "Yes. Vue 3.5 uses standard HTML templates and concise Composition API primitives, whereas Angular 22 requires learning decorators, DI, RxJS, and Signals.",
        "related": ["react-vs-vue.html", "react-vs-angular.html", "angular-vs-svelte.html", "best-frontend-framework-for-enterprise.html"],
    },
    {
        "slug": "angular-vs-svelte",
        "a": "angular",
        "b": "svelte",
        "title": "Angular vs Svelte 5 (2026): Enterprise Platform vs Compiled UI",
        "desc": "Compare Angular 22.2 vs Svelte 5.57 in 2026: Signals vs Runes, runtime size, TypeScript tooling, and team scale tradeoffs.",
        "h1": "Angular 22 vs Svelte 5 in 2026.",
        "lead": "Full-featured enterprise platform versus lightweight compiled Runes reactivity.",
        "loc_a": "93 lines",
        "loc_b": "77 lines",
        "win_a": "Pick Angular 22 for regulated enterprise portals, large frontend orgs, and built-in forms, validation, and routing.",
        "win_b": "Pick Svelte 5 for fast product shipping, tiny JavaScript payloads, and low ceremony.",
        "faq_q": "When should a team pick Svelte 5 instead of Angular 22?",
        "faq_a": "Choose Svelte 5 for small to mid-size teams optimizing bundle size and speed of iteration; keep Angular 22 for standardized large enterprise monorepos.",
        "related": ["react-vs-angular.html", "vue-vs-angular.html", "svelte-vs-solidjs.html", "best-frontend-framework-for-enterprise.html"],
    },
    {
        "slug": "react-vs-solidjs",
        "a": "react",
        "b": "solid",
        "title": "React vs SolidJS (2026): Virtual DOM Hooks vs Fine-Grained Signals",
        "desc": "Compare React 19.3 vs SolidJS 1.9 in 2026: JSX ergonomics, re-rendering vs single-run components, npm downloads, and bundle size.",
        "h1": "React 19 vs SolidJS 1.9 in 2026.",
        "lead": "Identical JSX syntax backed by two fundamentally different execution models.",
        "loc_a": "82 lines",
        "loc_b": "88 lines",
        "win_a": "Pick React 19 for massive library compatibility, hiring pool, and Next.js or React Router production maturity.",
        "win_b": "Pick SolidJS for raw DOM update throughput, 7 KB runtime size, and zero Virtual DOM re-render overhead.",
        "faq_q": "Why does SolidJS feel like React but run faster?",
        "faq_a": "SolidJS uses JSX like React, but runs each component function once and compiles reactive expressions into fine-grained signal subscriptions instead of diffing a Virtual DOM.",
        "related": ["svelte-vs-solidjs.html", "react-vs-svelte.html", "lightweight-frontend-frameworks.html", "react-alternatives.html"],
    },
    {
        "slug": "svelte-vs-solidjs",
        "a": "svelte",
        "b": "solid",
        "title": "Svelte 5 vs SolidJS (2026): Runes SFC vs Compiled Signal JSX",
        "desc": "Compare Svelte 5.57 vs SolidJS 1.9 in 2026: fine-grained reactivity without Virtual DOM, bundle overhead, and template style.",
        "h1": "Svelte 5 vs SolidJS 1.9 in 2026.",
        "lead": "Two zero-VDOM reactive compilers compared on syntax, bundle size, and tooling.",
        "loc_a": "77 lines",
        "loc_b": "88 lines",
        "win_a": "Pick Svelte 5 for HTML single-file components, scoped CSS, and a mature full-stack framework in SvelteKit 3.",
        "win_b": "Pick SolidJS if your team prefers TypeScript JSX and predictable signal getter semantics without compiler magic.",
        "faq_q": "Which has a smaller learning curve for React developers: Svelte 5 or SolidJS?",
        "faq_a": "SolidJS keeps familiar JSX syntax, though React developers must unlearn component re-execution; Svelte 5 uses HTML templates with explicit $state and $derived runes.",
        "related": ["react-vs-solidjs.html", "react-vs-svelte.html", "vue-vs-svelte.html", "lightweight-frontend-frameworks.html"],
    },
    {
        "slug": "react-vs-preact",
        "a": "react",
        "b": "preact",
        "title": "React vs Preact (2026): Full Ecosystem vs 4 KB Drop-In Runtime",
        "desc": "Compare React 19.3 vs Preact 11.2 in 2026: 45 KB vs 4 KB runtime, preact/compat, Signals, and when to switch.",
        "h1": "React 19 vs Preact 11 in 2026.",
        "lead": "Full-featured React ecosystem versus a 4 KB lightweight Virtual DOM runtime.",
        "win_a": "Pick React 19 for React Server Components, Next.js 16 features, and full compatibility with complex third-party UI kits.",
        "win_b": "Pick Preact 11 for embeddable widgets, performance-sensitive storefronts, and strict client bundle budgets.",
        "faq_q": "Can Preact replace React without rewriting code?",
        "faq_a": "For most client-side SPAs and widgets, preact/compat maps React APIs to Preact's 4 KB core, though React 19 Server Components require React.",
        "related": ["lightweight-frontend-frameworks.html", "react-alternatives.html", "lit-vs-react.html", "react-vs-solidjs.html"],
    },
    {
        "slug": "react-vs-nextjs",
        "a": "react",
        "b": "nextjs",
        "title": "React vs Next.js (2026): Client Library vs Full-Stack Framework",
        "desc": "Understand React 19.3 vs Next.js 16.4 in 2026: when a Vite React SPA beats Next.js, and when SSR, RSC, and SEO demand Next.js.",
        "h1": "React 19 vs Next.js 16 in 2026.",
        "lead": "Choosing between a pure client-side React SPA and a full-stack SSR framework.",
        "win_a": "Pick plain React 19 with Vite for authenticated dashboards, internal tools, and static SPAs without server maintenance.",
        "win_b": "Pick Next.js 16 when SEO indexing, server rendering, streaming, and integrated API routes matter.",
        "faq_q": "Is Next.js replacing standalone React in 2026?",
        "faq_a": "Next.js builds on top of React 19; standalone React with Vite remains simpler for behind-login apps, while Next.js leads for SSR and SEO-critical web products.",
        "related": ["nextjs-vs-react-router.html", "nextjs-vs-astro.html", "best-frontend-framework-for-seo.html", "best-frontend-framework-for-saas.html"],
    },
    {
        "slug": "nextjs-vs-astro",
        "a": "nextjs",
        "b": "astro",
        "title": "Next.js vs Astro (2026): Full-Stack React SSR vs Zero-JS Islands",
        "desc": "Compare Next.js 16.4 vs Astro 7.4 in 2026: React Server Components vs Islands Architecture, Core Web Vitals, SEO, and bundle weight.",
        "h1": "Next.js 16 vs Astro 7 in 2026.",
        "lead": "Dynamic React application rendering versus zero-JS content and marketing delivery.",
        "win_a": "Pick Next.js 16 for interactive logged-in SaaS products, user-specific dynamic pages, and heavy React state.",
        "win_b": "Pick Astro 7 for blogs, documentation, marketing sites, and comparison directories needing 0 KB default JS.",
        "faq_q": "Is Astro better than Next.js for SEO?",
        "faq_a": "For content, docs, and marketing pages, Astro 7 ships zero client JavaScript by default and achieves faster Core Web Vitals; Next.js wins for dynamic data-driven apps.",
        "related": ["best-frontend-framework-for-seo.html", "astro-vs-nuxt.html", "astro-vs-sveltekit.html", "nextjs-alternatives.html"],
    },
    {
        "slug": "nextjs-vs-nuxt",
        "a": "nextjs",
        "b": "nuxt",
        "title": "Next.js vs Nuxt (2026): React App Router vs Vue Nitro Engine",
        "desc": "Compare Next.js 16.4 vs Nuxt 4.6 in 2026: SSR, hybrid caching, Server Components vs Vue SFCs, and ecosystem adoption.",
        "h1": "Next.js 16 vs Nuxt 4 in 2026.",
        "lead": "The flagship full-stack meta-frameworks for React 19 and Vue 3.5 compared.",
        "win_a": "Pick Next.js 16 for React talent availability, Vercel/edge ecosystem support, and React Server Components.",
        "win_b": "Pick Nuxt 4 for Nitro universal deployment, auto-imports, cleaner configuration, and Vue 3.5 ergonomics.",
        "faq_q": "Which is simpler to configure: Next.js 16 or Nuxt 4?",
        "faq_a": "Many teams find Nuxt 4's Nitro engine, built-in modules, and route rules more cohesive out of the box, while Next.js 16 offers a larger third-party React ecosystem.",
        "related": ["react-vs-vue.html", "nuxt-vs-sveltekit.html", "nextjs-vs-sveltekit.html", "best-frontend-framework-for-seo.html"],
    },
    {
        "slug": "nextjs-vs-sveltekit",
        "a": "nextjs",
        "b": "sveltekit",
        "title": "Next.js vs SvelteKit (2026): React Server Components vs Lean Svelte SSR",
        "desc": "Compare Next.js 16.4 vs SvelteKit 3.2 in 2026: hydration weight, form actions, deployment adapters, and developer experience.",
        "h1": "Next.js 16 vs SvelteKit 3 in 2026.",
        "lead": "Enterprise React meta-framework versus lean progressive full-stack Svelte.",
        "win_a": "Pick Next.js 16 when hiring React engineers and relying on React-first SaaS SDKs and UI libraries.",
        "win_b": "Pick SvelteKit 3 for smaller client payloads, progressive HTML form actions, and fast full-stack iteration.",
        "faq_q": "Why do indie teams switch from Next.js to SvelteKit?",
        "faq_a": "Teams cite smaller client bundles, simpler mental models without Server/Client component boundaries, and straightforward Vite-based adapters.",
        "related": ["react-vs-svelte.html", "nuxt-vs-sveltekit.html", "astro-vs-sveltekit.html", "nextjs-alternatives.html"],
    },
    {
        "slug": "nextjs-vs-react-router",
        "a": "nextjs",
        "b": "react-router",
        "title": "Next.js vs React Router (2026): RSC App Router vs Web Standards SSR",
        "desc": "Compare Next.js 16.4 vs React Router 8.5 (formerly Remix) in 2026: loaders and actions vs React Server Components, Vite support, and lock-in.",
        "h1": "Next.js 16 vs React Router 8.",
        "lead": "Comparing the two leading full-stack React frameworks on routing, Vite, and SSR.",
        "win_a": "Pick Next.js 16 for built-in image/font optimization, React Server Components, and managed edge caching.",
        "win_b": "Pick React Router 8 for standard Web Fetch loaders/actions, native Vite speed, and portable Node or Cloudflare hosting.",
        "faq_q": "What happened to Remix vs Next.js in 2026?",
        "faq_a": "Remix merged its full-stack framework capabilities into React Router (now v8.5.1), offering Vite-based SSR, SPA, and nested data loaders as a direct alternative to Next.js.",
        "related": ["react-vs-nextjs.html", "nextjs-alternatives.html", "react-alternatives.html", "best-frontend-framework-for-saas.html"],
    },
    {
        "slug": "nuxt-vs-sveltekit",
        "a": "nuxt",
        "b": "sveltekit",
        "title": "Nuxt vs SvelteKit (2026): Full-Stack Vue 3.5 vs Svelte 5 Runes",
        "desc": "Compare Nuxt 4.6 vs SvelteKit 3.2 in 2026: Nitro server engine vs SvelteKit adapters, bundle size, and developer ergonomics.",
        "h1": "Nuxt 4 vs SvelteKit 3 in 2026.",
        "lead": "Two cohesive non-React full-stack frameworks built on Vite and standard web APIs.",
        "win_a": "Pick Nuxt 4 if your team knows Vue 3.5, wants rich module presets, and values Nitro's hybrid caching.",
        "win_b": "Pick SvelteKit 3 for minimal client runtime overhead and clean form-first progressive enhancement.",
        "faq_q": "Is Nuxt 4 heavier than SvelteKit 3?",
        "faq_a": "SvelteKit 3 compiles components without a Virtual DOM runtime, producing slightly smaller client bundles than Nuxt 4, though both offer strong SSR performance.",
        "related": ["vue-vs-svelte.html", "nextjs-vs-nuxt.html", "nextjs-vs-sveltekit.html", "astro-vs-nuxt.html"],
    },
    {
        "slug": "astro-vs-nuxt",
        "a": "astro",
        "b": "nuxt",
        "title": "Astro vs Nuxt (2026): Content Islands vs Full-Stack Vue Apps",
        "desc": "Compare Astro 7.4 vs Nuxt 4.6 in 2026: zero-JS static sites vs hybrid Vue SSR applications, SEO, and Vue Islands.",
        "h1": "Astro 7 vs Nuxt 4 in 2026.",
        "lead": "Zero-JS static Islands versus full-stack reactive Vue routing and state.",
        "win_a": "Pick Astro 7 for content marketing, documentation, and blogs where you can embed Vue islands only where needed.",
        "win_b": "Pick Nuxt 4 for interactive Vue applications requiring shared client state across routes and dynamic SSR.",
        "faq_q": "Can I use Vue components inside Astro?",
        "faq_a": "Yes. Astro 7 supports Vue 3 components as isolated interactive islands while keeping the rest of the page pure zero-JS HTML.",
        "related": ["nextjs-vs-astro.html", "best-frontend-framework-for-seo.html", "nuxt-vs-sveltekit.html", "astro-alternatives.html"],
    },
    {
        "slug": "astro-vs-sveltekit",
        "a": "astro",
        "b": "sveltekit",
        "title": "Astro vs SvelteKit (2026): Zero-JS Content vs Full-Stack Svelte",
        "desc": "Compare Astro 7.4 vs SvelteKit 3.2 in 2026: content collections and zero-JS defaults vs full SPA transitions and form actions.",
        "h1": "Astro 7 vs SvelteKit 3 in 2026.",
        "lead": "Content-first Islands architecture versus full-stack interactive Svelte applications.",
        "win_a": "Pick Astro 7 for editorial sites, docs, and SEO landing directories with minimal client interactivity.",
        "win_b": "Pick SvelteKit 3 for authenticated dashboards, dynamic web apps, and stateful multi-step flows.",
        "faq_q": "When is SvelteKit better than Astro?",
        "faq_a": "Choose SvelteKit 3 when your site behaves like an interactive web application with shared state across page navigations rather than a content publication.",
        "related": ["nextjs-vs-astro.html", "nextjs-vs-sveltekit.html", "best-frontend-framework-for-seo.html", "astro-alternatives.html"],
    },
    {
        "slug": "astro-vs-qwik",
        "a": "astro",
        "b": "qwik",
        "title": "Astro vs Qwik (2026): Islands Architecture vs Resumability",
        "desc": "Compare Astro 7.4 vs Qwik 1.20 in 2026: partial island hydration vs zero-hydration resumability for Core Web Vitals and SEO.",
        "h1": "Astro 7 vs Qwik 1.20 in 2026.",
        "lead": "Two architectures designed to eliminate upfront JavaScript hydration bottlenecks.",
        "win_a": "Pick Astro 7 for content-rich sites, docs, and multi-framework islands backed by a huge 12.0M/wk ecosystem.",
        "win_b": "Pick Qwik 1.20 when a heavily interactive application (such as a complex storefront) still demands near-zero initial JS.",
        "faq_q": "How do Astro Islands differ from Qwik Resumability?",
        "faq_a": "Astro isolates interactive components as separate islands inside static HTML, while Qwik serializes application state into HTML and lazy-loads handlers only on user interaction.",
        "related": ["best-frontend-framework-for-seo.html", "best-frontend-framework-for-ecommerce.html", "lightweight-frontend-frameworks.html", "astro-alternatives.html"],
    },
    {
        "slug": "alpinejs-vs-htmx",
        "a": "alpine",
        "b": "htmx",
        "title": "Alpine.js vs htmx (2026): Client Directives vs Hypermedia HTML",
        "desc": "Compare Alpine.js 3.17 vs htmx 2.0 in 2026: zero-build client state vs server HTML partials for Django, Rails, Laravel, and Go.",
        "h1": "Alpine.js 3 vs htmx in 2026.",
        "lead": "Two zero-build libraries that enhance server-rendered HTML without a JavaScript SPA.",
        "win_a": "Pick Alpine.js for local UI state like dropdowns, modals, tabs, and client toggles directly inside HTML.",
        "win_b": "Pick htmx to fetch and swap server-rendered HTML fragments over AJAX using declarative attributes.",
        "faq_q": "Can Alpine.js and htmx be used together?",
        "faq_a": "Yes. Many Rails, Django, Laravel, and Go teams pair htmx for server HTML updates with Alpine.js for lightweight client UI state.",
        "related": ["htmx-vs-react.html", "lightweight-frontend-frameworks.html", "jquery-alternatives.html", "htmx-alternatives.html"],
    },
    {
        "slug": "htmx-vs-react",
        "a": "htmx",
        "b": "react",
        "title": "htmx vs React (2026): Server Hypermedia vs Client JSON SPA",
        "desc": "Compare htmx vs React 19.3 in 2026: backend-driven HTML partials without a build step vs rich client-side state management.",
        "h1": "htmx vs React 19 in 2026.",
        "lead": "Server-rendered HTML fragments versus client-side Virtual DOM applications.",
        "win_a": "Pick htmx when your team works in Python, Go, Ruby, or PHP and wants dynamic forms and tables without maintaining a separate JS build.",
        "win_b": "Pick React 19 for offline-capable apps, complex client editors, drag-and-drop canvases, and rich interactive dashboards.",
        "faq_q": "When does htmx fall short compared to React?",
        "faq_a": "htmx depends on server round-trips for state updates, making React a better choice for dense client-side editors, spreadsheets, and offline-first workspaces.",
        "related": ["alpinejs-vs-htmx.html", "htmx-alternatives.html", "jquery-alternatives.html", "react-alternatives.html"],
    },
    {
        "slug": "lit-vs-react",
        "a": "lit",
        "b": "react",
        "title": "Lit vs React (2026): Web Components vs Component Ecosystem",
        "desc": "Compare Lit 3.3 vs React 19.3 in 2026: browser-native Custom Elements for multi-framework design systems vs React app development.",
        "h1": "Lit 3 vs React 19 in 2026.",
        "lead": "Standards-based Web Components versus the dominant application UI ecosystem.",
        "win_a": "Pick Lit 3 to publish design system components or embeddable widgets that run inside React, Vue, Angular, and static HTML alike.",
        "win_b": "Pick React 19 when building full applications that benefit from React hooks, routing, and React Server Components.",
        "faq_q": "Does React 19 support Web Components built with Lit?",
        "faq_a": "Yes. React 19 added full support for Custom Elements properties and events, making Lit Web Components clean to consume inside React apps.",
        "related": ["react-vs-preact.html", "lightweight-frontend-frameworks.html", "react-alternatives.html", "best-frontend-framework-for-enterprise.html"],
    },
]

ALTERNATIVES_PAGES: list[dict[str, Any]] = [
    {
        "slug": "react-alternatives",
        "target_name": "React",
        "target_id": "react",
        "title": "Best React Alternatives in 2026 (Lighter, Faster, Lower Boilerplate)",
        "desc": "Top React alternatives in 2026 verified by GitHub stars and npm downloads: Vue 3.5, Svelte 5, SolidJS, Preact 11, Angular 22, and htmx.",
        "h1": "Best React alternatives in 2026.",
        "lead": "Compare faster, lighter, or more opinionated UI frameworks when React feels heavy.",
        "picks": ["vue", "svelte", "solid", "preact", "angular", "htmx"],
        "reasons": {
            "vue": "Clean HTML single-file components with official routing and Pinia state.",
            "svelte": "Compiled Runes reactivity with 3 to 5 KB runtime and no Virtual DOM.",
            "solid": "React-like JSX without re-renders or Virtual DOM overhead.",
            "preact": "4 KB React-compatible drop-in runtime for strict bundle budgets.",
            "angular": "Batteries-included TypeScript platform for large enterprise squads.",
            "htmx": "Zero-build hypermedia attributes when backend templates render HTML.",
        },
        "faq_q": "What is the closest lightweight alternative to React?",
        "faq_a": "Preact (11.2.0, ~4 KB) offers near drop-in React compatibility, while SolidJS (1.9.19, ~7 KB) keeps JSX syntax with signal-based DOM updates.",
        "related": ["react-vs-vue.html", "react-vs-svelte.html", "react-vs-solidjs.html", "react-vs-preact.html"],
    },
    {
        "slug": "vue-alternatives",
        "target_name": "Vue",
        "target_id": "vue",
        "title": "Best Vue Alternatives in 2026 (Svelte, React, SolidJS, Alpine.js)",
        "desc": "Compare the top Vue 3 alternatives in 2026: Svelte 5 Runes, React 19, SolidJS, Alpine.js for drop-in HTML, and Angular 22.",
        "h1": "Best Vue alternatives in 2026.",
        "lead": "Frameworks that match Vue's ergonomics or expand hiring and performance headroom.",
        "picks": ["svelte", "react", "solid", "alpine", "angular"],
        "reasons": {
            "svelte": "Closest single-file component DX with smaller compiled runtime output.",
            "react": "Largest job market and UI library ecosystem (260.9M weekly npm downloads).",
            "solid": "Signal-driven JSX for maximum DOM benchmark throughput.",
            "alpine": "Vue-inspired x-data and x-model directives with zero build tooling.",
            "angular": "Strict enterprise architecture with Signals and dependency injection.",
        },
        "faq_q": "Which framework feels closest to Vue 3?",
        "faq_a": "Svelte 5 uses single-file components with scoped styles like Vue, while Alpine.js offers Vue-style HTML directives without a build step.",
        "related": ["vue-vs-svelte.html", "react-vs-vue.html", "vue-vs-angular.html", "alpinejs-vs-htmx.html"],
    },
    {
        "slug": "angular-alternatives",
        "target_name": "Angular",
        "target_id": "angular",
        "title": "Best Angular Alternatives in 2026 (React, Vue, SvelteKit, Next.js)",
        "desc": "Top Angular alternatives in 2026 for TypeScript teams seeking lighter bundles and faster onboarding: React, Vue 3.5, Next.js, SvelteKit, and Lit.",
        "h1": "Best Angular alternatives in 2026.",
        "lead": "TypeScript-ready alternatives when Angular's ceremony and baseline bundle feel heavy.",
        "picks": ["react", "vue", "nextjs", "sveltekit", "lit"],
        "reasons": {
            "react": "Flexible TypeScript UI ecosystem with broad enterprise hiring.",
            "vue": "Gentle onboarding with strong TypeScript support in <script setup>.",
            "nextjs": "Full-stack React routing, SSR, and data conventions out of the box.",
            "sveltekit": "Opinionated full-stack TypeScript routing with tiny client bundles.",
            "lit": "Standards-based TypeScript Web Components for multi-team design systems.",
        },
        "faq_q": "What is the best alternative to Angular for large TypeScript teams?",
        "faq_a": "Next.js 16 (with React 19 and strict TypeScript) or Nuxt 4 (with Vue 3.5) provide full-stack routing and conventions with lighter client footprints.",
        "related": ["react-vs-angular.html", "vue-vs-angular.html", "angular-vs-svelte.html", "best-frontend-framework-for-enterprise.html"],
    },
    {
        "slug": "svelte-alternatives",
        "target_name": "Svelte",
        "target_id": "svelte",
        "title": "Best Svelte Alternatives in 2026 (SolidJS, Vue, Preact, Astro, Qwik)",
        "desc": "Top Svelte 5 alternatives in 2026 for lean bundles and reactive UI: SolidJS, Vue 3.5, Preact 11, Astro 7, and Qwik.",
        "h1": "Best Svelte alternatives in 2026.",
        "lead": "Low-overhead UI frameworks and compilers compared against Svelte 5 Runes.",
        "picks": ["solid", "vue", "preact", "astro", "qwik"],
        "reasons": {
            "solid": "Compiled fine-grained signals with TypeScript JSX instead of SFCs.",
            "vue": "Single-file components with a larger ecosystem and Nuxt 4 support.",
            "preact": "4 KB Virtual DOM runtime compatible with existing React packages.",
            "astro": "Zero-JS Islands architecture ideal for content and SEO landings.",
            "qwik": "Resumable execution avoiding hydration on heavy interactive pages.",
        },
        "faq_q": "What matches Svelte's small bundle size?",
        "faq_a": "SolidJS (~7 KB), Preact (~4 KB), Lit (~5 KB), and Astro (0 KB default JS for static content) all keep client payloads minimal.",
        "related": ["svelte-vs-solidjs.html", "react-vs-svelte.html", "vue-vs-svelte.html", "lightweight-frontend-frameworks.html"],
    },
    {
        "slug": "nextjs-alternatives",
        "target_name": "Next.js",
        "target_id": "nextjs",
        "title": "Best Next.js Alternatives in 2026 (React Router 8, Astro, SvelteKit, Nuxt)",
        "desc": "Compare the top Next.js alternatives in 2026: React Router 8 (Remix), Astro 7, SvelteKit 3, Nuxt 4, and Qwik.",
        "h1": "Best Next.js alternatives in 2026.",
        "lead": "Portable, Vite-native, and zero-JS alternatives to Next.js App Router.",
        "picks": ["react-router", "astro", "sveltekit", "nuxt", "qwik"],
        "reasons": {
            "react-router": "React SSR and SPA powered by Vite and standard Web Request loaders.",
            "astro": "Zero-JS static defaults for docs, blogs, and marketing sites.",
            "sveltekit": "Lean full-stack SSR with adapters for Node, Cloudflare, and static hosts.",
            "nuxt": "Vue 3.5 full-stack framework with Nitro universal deployment.",
            "qwik": "Zero-hydration resumability for fast e-commerce Core Web Vitals.",
        },
        "faq_q": "What is the best React alternative to Next.js?",
        "faq_a": "React Router 8 (the evolution of Remix) gives React 19 teams Vite-native SSR, nested data loaders, and portable server adapters without Next.js lock-in.",
        "related": ["nextjs-vs-react-router.html", "nextjs-vs-astro.html", "nextjs-vs-sveltekit.html", "nextjs-vs-nuxt.html"],
    },
    {
        "slug": "nuxt-alternatives",
        "target_name": "Nuxt",
        "target_id": "nuxt",
        "title": "Best Nuxt Alternatives in 2026 (Astro, SvelteKit, Next.js, Vue + Vite)",
        "desc": "Compare top Nuxt 4 alternatives in 2026: Astro 7 for content sites, SvelteKit 3, Next.js 16, and standalone Vue 3.5 with Vite.",
        "h1": "Best Nuxt alternatives in 2026.",
        "lead": "Lighter SSR and static options when Nuxt 4 is more server framework than you need.",
        "picks": ["astro", "sveltekit", "nextjs", "vue", "react-router"],
        "reasons": {
            "astro": "Zero-JS static Islands that still render Vue 3 components where needed.",
            "sveltekit": "Smaller compiled client bundles with progressive form actions.",
            "nextjs": "Largest full-stack React ecosystem and SaaS SDK compatibility.",
            "vue": "Simpler client-only Vite SPA when SEO is not needed behind login.",
            "react-router": "Web-standard Vite SSR and SPA routing for React teams.",
        },
        "faq_q": "Should I use Astro instead of Nuxt for a Vue marketing site?",
        "faq_a": "If the site is mostly static content with occasional Vue widgets, Astro 7 ships less client JS than Nuxt 4; choose Nuxt for full-stack Vue apps.",
        "related": ["astro-vs-nuxt.html", "nuxt-vs-sveltekit.html", "nextjs-vs-nuxt.html", "best-frontend-framework-for-seo.html"],
    },
    {
        "slug": "astro-alternatives",
        "target_name": "Astro",
        "target_id": "astro",
        "title": "Best Astro Alternatives in 2026 (Next.js, SvelteKit, Nuxt, Qwik, htmx)",
        "desc": "Compare top Astro 7 alternatives in 2026 when your site needs dynamic SSR or full SPA transitions: Next.js, SvelteKit, Nuxt, Qwik, and htmx.",
        "h1": "Best Astro alternatives in 2026.",
        "lead": "Full-stack SSR and hypermedia options when static Islands are not dynamic enough.",
        "picks": ["nextjs", "sveltekit", "nuxt", "qwik", "htmx"],
        "reasons": {
            "nextjs": "Full-stack React streaming SSR and dynamic app routes.",
            "sveltekit": "Fast prerendering plus stateful SPA transitions and tiny JS.",
            "nuxt": "Hybrid static and SSR caching for Vue 3.5 sites via Nitro.",
            "qwik": "Zero-hydration resumability for deeply interactive SEO pages.",
            "htmx": "Dynamic server-rendered HTML partials from any backend language.",
        },
        "faq_q": "When should I pick SvelteKit or Next.js over Astro?",
        "faq_a": "Choose SvelteKit 3 or Next.js 16 when persistent client state across page navigations and complex interactive workflows dominate over static content.",
        "related": ["nextjs-vs-astro.html", "astro-vs-sveltekit.html", "astro-vs-nuxt.html", "astro-vs-qwik.html"],
    },
    {
        "slug": "htmx-alternatives",
        "target_name": "htmx",
        "target_id": "htmx",
        "title": "Best htmx Alternatives in 2026 (Alpine.js, Astro, Svelte, Preact)",
        "desc": "Compare htmx alternatives in 2026: Alpine.js for client directives, Astro 7, Svelte 5, Preact 11, and React 19 for rich client state.",
        "h1": "Best htmx alternatives in 2026.",
        "lead": "Client-side and zero-JS alternatives when server HTML partials hit limits.",
        "picks": ["alpine", "astro", "svelte", "preact", "react"],
        "reasons": {
            "alpine": "Zero-build client state directly in HTML without server round-trips.",
            "astro": "Zero-JS static HTML paired with isolated interactive component islands.",
            "svelte": "Tiny compiled client UI when rich local interactions become complex.",
            "preact": "4 KB React-compatible islands for dropping interactivity into HTML pages.",
            "react": "Full client ecosystem for offline-ready editors and complex dashboards.",
        },
        "faq_q": "What is the closest zero-build alternative to htmx?",
        "faq_a": "Alpine.js (3.17.5) also requires no build step and drops directly into server templates, focusing on client UI state rather than server HTML swaps.",
        "related": ["alpinejs-vs-htmx.html", "htmx-vs-react.html", "jquery-alternatives.html", "lightweight-frontend-frameworks.html"],
    },
    {
        "slug": "jquery-alternatives",
        "target_name": "jQuery (Legacy)",
        "target_id": None,
        "title": "Best jQuery Alternatives in 2026 (Alpine.js, htmx, Preact, Vue, Lit)",
        "desc": "Modern 2026 replacements for jQuery: Alpine.js and htmx with zero build step, plus Preact 11, Vue 3.5, and Lit Web Components.",
        "h1": "Best jQuery alternatives in 2026.",
        "lead": "Zero-build HTML enhancers and lightweight libraries replacing legacy DOM scripts.",
        "picks": ["alpine", "htmx", "preact", "vue", "lit"],
        "reasons": {
            "alpine": "Declarative reactivity via HTML attributes with no build step.",
            "htmx": "AJAX HTML updates via hx-get and hx-post without manual DOM code.",
            "preact": "4 KB component library when state outgrows inline DOM manipulation.",
            "vue": "Easy progressive drop-in for legacy server apps via CDN or Vite.",
            "lit": "Standards-based Custom Elements for reusable cross-page widgets.",
        },
        "faq_q": "What is the easiest drop-in replacement for jQuery without a build step?",
        "faq_a": "Native browser DOM APIs cover most selectors and fetch calls; for declarative state and AJAX partials without Webpack or Vite, pair Alpine.js and htmx.",
        "related": ["alpinejs-vs-htmx.html", "htmx-vs-react.html", "lightweight-frontend-frameworks.html", "htmx-alternatives.html"],
    },
    {
        "slug": "create-react-app-alternatives",
        "target_name": "Create React App (Deprecated)",
        "target_id": None,
        "title": "Best Create React App Alternatives in 2026 (Vite, Next.js, React Router 8)",
        "desc": "Modern replacements for deprecated Create React App (CRA) in 2026: Vite + React 19, Next.js 16, React Router 8, and Astro 7.",
        "h1": "Create React App alternatives (2026).",
        "lead": "Fast, supported toolchains replacing deprecated CRA for React 19 projects.",
        "picks": ["react", "nextjs", "react-router", "astro", "preact"],
        "reasons": {
            "react": "Vite + React 19 + TypeScript (free starter included in this repo) replaces CRA SPAs directly.",
            "nextjs": "Official React full-stack choice when SSR, SEO, and API routes are needed.",
            "react-router": "Vite-native React framework with SSR, SPA mode, and nested loaders.",
            "astro": "Zero-JS static pages that still render React 19 islands on demand.",
            "preact": "4 KB alternative with Vite preset when client bundle size is critical.",
        },
        "faq_q": "What replaced Create React App in 2026?",
        "faq_a": "React recommends full-stack frameworks like Next.js 16 and React Router 8 for new apps, or Vite with React 19 for pure client-side SPAs.",
        "related": ["react-vs-nextjs.html", "nextjs-vs-react-router.html", "best-frontend-framework-for-saas.html", "react-alternatives.html"],
    },
]

WORKLOAD_PAGES: list[dict[str, Any]] = [
    {
        "slug": "best-frontend-framework-for-seo",
        "title": "Best Frontend Frameworks for SEO and Core Web Vitals (2026)",
        "desc": "Ranking the best frontend frameworks for Google SEO and AI search in 2026: Astro 7 Islands, Next.js 16, Nuxt 4, SvelteKit 3, and Qwik resumability.",
        "h1": "Best frontend frameworks for SEO.",
        "lead": "Server-rendered HTML and zero-JS Islands improve crawlability, LCP, and INP.",
        "picks": ["astro", "nextjs", "nuxt", "sveltekit", "qwik"],
        "reasons": {
            "astro": "Zero-JS static and Islands for content sites, docs, blogs, and programmatic SEO.",
            "nextjs": "SSR, SSG, and React Server Components for dynamic SaaS and e-commerce.",
            "nuxt": "Hybrid SSR and SSG (Nitro) for Vue-based SEO storefronts and portals.",
            "sveltekit": "SSR, prerender, and progressive forms for fast interactive web apps.",
            "qwik": "Resumability (zero hydration) for large interactive e-commerce catalogs.",
        },
        "panel_a_title": "Public marketing and docs",
        "panel_a_body": "Use Astro 7 or static prerendering so Googlebot and AI crawlers receive complete semantic HTML with minimal client script.",
        "panel_b_title": "Dynamic catalogs and SaaS",
        "panel_b_body": "Use Next.js 16, Nuxt 4, or SvelteKit 3 when product availability, user pricing, or per-request metadata must stream from the server.",
        "related": ["react-vs-vue.html", "lightweight-frontend-frameworks.html", "nextjs-vs-astro.html", "astro-vs-qwik.html"],
    },
    {
        "slug": "lightweight-frontend-frameworks",
        "title": "Lightweight Frontend Frameworks (2026): Smallest Bundle and Zero-Build",
        "desc": "Compare lightweight JavaScript frameworks in 2026: Svelte 5, SolidJS, Preact 11, Lit 3, Alpine.js, and htmx for minimal client JS payloads.",
        "h1": "Lightweight frontend frameworks in 2026.",
        "lead": "Six low-overhead tools for embeddable widgets, tight JS budgets, and server-rendered backends.",
        "picks": ["preact", "solid", "lit", "svelte", "alpine", "htmx"],
        "reasons": {
            "preact": "~4 KB min+gz; React-compatible widgets and fast storefronts.",
            "solid": "~7 KB min+gz; high-frequency UI updates and real-time dashboards.",
            "lit": "~5 KB min+gz; cross-framework Web Components design systems.",
            "svelte": "~3 to 5 KB overhead; full SPAs and SvelteKit apps with tiny bundles.",
            "alpine": "~15 KB, no build; progressive enhancement on Rails, Django, Laravel.",
            "htmx": "~14 KB, no build; server-driven HTML partials without JSON SPAs.",
        },
        "panel_a_title": "Client SPAs and islands",
        "panel_a_body": "Pick Preact, SolidJS, or Svelte 5 when you need rich client state with a minimal bundle budget.",
        "panel_b_title": "Zero-build server HTML",
        "panel_b_body": "Pick Alpine.js or htmx when Rails, Django, Laravel, or Go templates already render your pages.",
        "related": ["react-vs-svelte.html", "best-frontend-framework-for-seo.html", "svelte-vs-solidjs.html", "alpinejs-vs-htmx.html"],
    },
    {
        "slug": "best-frontend-framework-for-saas",
        "title": "Best Frontend Frameworks for SaaS Dashboards (2026)",
        "desc": "Compare the best frontend frameworks for SaaS web apps and dashboards in 2026: React 19, Next.js 16, Vue 3.5, SvelteKit 3, and Angular 22.",
        "h1": "Best frontend frameworks for SaaS.",
        "lead": "Choose the right UI stack for dashboards, billing workflows, and multi-tenant apps.",
        "picks": ["react", "nextjs", "vue", "sveltekit", "angular"],
        "reasons": {
            "react": "Deepest ecosystem for tables, charts, auth SDKs, and AI workspaces.",
            "nextjs": "Unified SSR marketing routes plus authenticated SaaS app routes.",
            "vue": "Clean component state with Pinia and rapid product iteration.",
            "sveltekit": "Fast full-stack forms and small client bundles for lean teams.",
            "angular": "Structured platform for complex B2B admin portals.",
        },
        "panel_a_title": "Behind-login dashboards",
        "panel_a_body": "A Vite + React 19, Vue 3.5, or Svelte 5 SPA avoids SSR complexity when your app sits behind authentication.",
        "panel_b_title": "Unified marketing and app",
        "panel_b_body": "Pick Next.js 16, Nuxt 4, or SvelteKit 3 when public SEO pages and logged-in dashboards share one codebase.",
        "related": ["react-vs-nextjs.html", "react-vs-vue.html", "create-react-app-alternatives.html", "best-frontend-framework-for-ai-apps.html"],
    },
    {
        "slug": "best-frontend-framework-for-ecommerce",
        "title": "Best Frontend Frameworks for E-Commerce Storefronts (2026)",
        "desc": "Compare the best frontend frameworks for e-commerce SEO and Core Web Vitals in 2026: Next.js 16, Astro 7, Nuxt 4, Qwik 1.20, and React Router 8.",
        "h1": "Best frameworks for e-commerce.",
        "lead": "Balance dynamic cart state with fast LCP, INP, and product catalog SEO.",
        "picks": ["nextjs", "astro", "nuxt", "qwik", "react-router"],
        "reasons": {
            "nextjs": "Proven commerce starter kits, streaming SSR, and React ecosystem.",
            "astro": "Zero-JS product pages with interactive cart and filter islands.",
            "nuxt": "Hybrid route caching via Nitro for Vue storefronts.",
            "qwik": "Resumable hydration keeps mobile INP low on large catalogs.",
            "react-router": "Fast nested loaders and progressive checkout forms on Vite.",
        },
        "panel_a_title": "Conversion and Core Web Vitals",
        "panel_a_body": "Shipping less client JavaScript on product detail pages directly improves mobile LCP and checkout conversion.",
        "panel_b_title": "Dynamic pricing and inventory",
        "panel_b_body": "Use streaming SSR or edge caching in Next.js, Nuxt, or React Router when stock and currency change per request.",
        "related": ["best-frontend-framework-for-seo.html", "astro-vs-qwik.html", "nextjs-vs-astro.html", "nextjs-vs-nuxt.html"],
    },
    {
        "slug": "best-frontend-framework-for-enterprise",
        "title": "Best Frontend Frameworks for Enterprise Teams (2026)",
        "desc": "Compare frontend frameworks for large multi-team enterprise platforms in 2026: Angular 22, React 19 + TypeScript, Vue 3.5, Next.js 16, and Lit 3.",
        "h1": "Best enterprise frontend frameworks.",
        "lead": "Evaluate long-term maintainability, TypeScript strictness, and multi-squad standards.",
        "picks": ["angular", "react", "nextjs", "vue", "lit"],
        "reasons": {
            "angular": "Built-in dependency injection, router, forms, and Signals across large monorepos.",
            "react": "Broadest global hiring pool and mature enterprise component libraries.",
            "nextjs": "Standardized full-stack React conventions for customer-facing portals.",
            "vue": "Predictable upgrade path and lower training cost for mixed-seniority teams.",
            "lit": "Framework-agnostic Web Components for shared cross-org design systems.",
        },
        "panel_a_title": "Standardized internal platforms",
        "panel_a_body": "Angular 22 reduces architectural drift across dozens of squads by shipping official patterns for routing, DI, and forms.",
        "panel_b_title": "Cross-framework design systems",
        "panel_b_body": "Pair React or Angular applications with Lit Web Components when multiple teams share UI primitives.",
        "related": ["react-vs-angular.html", "vue-vs-angular.html", "angular-alternatives.html", "lit-vs-react.html"],
    },
    {
        "slug": "best-frontend-framework-for-ai-apps",
        "title": "Best Frontend Frameworks for AI Apps and Streaming UIs (2026)",
        "desc": "Compare frontend frameworks for AI chat, streaming UIs, and agent workspaces in 2026: React 19, Next.js 16, SvelteKit 3, SolidJS, and Vue 3.5.",
        "h1": "Best frameworks for AI apps.",
        "lead": "Build token-streaming interfaces, artifact panels, and responsive agent workspaces.",
        "picks": ["react", "nextjs", "sveltekit", "solid", "vue"],
        "reasons": {
            "react": "First-class SDK support (Vercel AI SDK, CopilotKit, Assistant UI) and rich markdown libraries.",
            "nextjs": "Streaming route handlers, server actions, and React Server Components.",
            "sveltekit": "Smooth high-frequency token updates with minimal runtime overhead.",
            "solid": "Fine-grained signal updates avoid diffing large chat histories on each streamed token.",
            "vue": "Fast reactive streaming UIs with clean single-file component structure.",
        },
        "panel_a_title": "SDK and ecosystem speed",
        "panel_a_body": "React 19 and Next.js 16 ship first-party hooks and streaming primitives across most AI developer SDKs.",
        "panel_b_title": "High-frequency token streaming",
        "panel_b_body": "SolidJS and Svelte 5 update only the active text node during fast token streams without re-diffing old messages.",
        "related": ["best-frontend-framework-for-saas.html", "react-vs-solidjs.html", "nextjs-vs-sveltekit.html", "react-vs-svelte.html"],
    },
]


def fmt_num(n: int) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return str(n)


def render_head(title: str, desc: str, slug: str, faq_q: str | None = None, faq_a: str | None = None) -> str:
    url = f"{BASE_URL}/{slug}.html"
    faq_block = ""
    if faq_q and faq_a:
        faq_json = json.dumps(
            {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": faq_q,
                        "acceptedAnswer": {"@type": "Answer", "text": faq_a},
                    }
                ],
            },
            indent=2,
        )
        faq_block = f'\n  <script type="application/ld+json">\n{faq_json}\n  </script>'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(desc)}" />
  <link rel="canonical" href="{escape(url)}" />
  <meta property="og:title" content="{escape(title)}" />
  <meta property="og:description" content="{escape(desc)}" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="{escape(url)}" />
  <meta property="og:image" content="{BASE_URL}/assets/preview.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Host+Grotesk:wght@400;500&family=Atkinson+Hyperlegible+Mono:wght@400;500&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="styles/site.css" />{faq_block}
</head>"""


def render_nav(active_slug: str) -> str:
    links = [
        ("./", "All frameworks", "index"),
        ("comparisons.html", "Directory", "comparisons"),
        ("react-vs-vue.html", "React vs Vue", "react-vs-vue"),
        ("react-vs-svelte.html", "React vs Svelte", "react-vs-svelte"),
        ("best-frontend-framework-for-seo.html", "Best for SEO", "best-frontend-framework-for-seo"),
        ("https://github.com/javascript-frontend/frontend-frameworks", "GitHub", ""),
    ]
    rendered = []
    for href, label, slug in links:
        cur = ' aria-current="page"' if slug == active_slug else ""
        rendered.append(f'        <a href="{href}"{cur}>{escape(label)}</a>')
    return f"""  <header class="site-nav">
    <div class="container site-nav__inner">
      <a class="brand" href="./">javascript-frontend</a>
      <nav class="nav-links" aria-label="Primary navigation">
{chr(10).join(rendered)}
      </nav>
    </div>
  </header>"""


def render_footer(related: list[str], titles: dict[str, str]) -> str:
    links_html = []
    for rel in related:
        label = titles.get(rel, rel.replace(".html", "").replace("-", " ").title())
        links_html.append(f'          <a href="{rel}">{escape(label)}</a>')
    links_html.append('          <a href="comparisons.html">All comparisons</a>')
    links_html.append('          <a href="https://github.com/javascript-frontend/frontend-frameworks">GitHub repository</a>')
    return f"""  <footer class="site-footer">
    <div class="container">
      <div class="site-footer__top">
        <a class="site-footer__wordmark" href="./">javascript-frontend</a>
        <div class="footer-links">
{chr(10).join(links_html)}
        </div>
      </div>
      <div class="site-footer__bottom">
        <span>Data verified 2026-11-16</span>
        <span>MIT License</span>
      </div>
    </div>
  </footer>"""


def render_related_section(related: list[str], label_map: dict[str, str], faq_q: str | None = None, faq_a: str | None = None) -> str:
    rows = []
    for rel in related:
        title = label_map.get(rel, rel.replace(".html", "").replace("-", " ").title())
        rows.append(
            f"""          <a class="index-row" href="{rel}">
            <span class="index-row__title">{escape(title)}</span>
            <span class="index-row__desc">Verified metrics and architecture breakdown.</span>
            <span class="index-row__action">Read</span>
          </a>"""
        )
    faq_html = ""
    if faq_q and faq_a:
        faq_html = f"""
        <div class="faq-list">
          <article class="faq-item">
            <h3>{escape(faq_q)}</h3>
            <p>{escape(faq_a)}</p>
          </article>
        </div>"""
    return f"""    <section class="section">
      <div class="container">
        <div class="section__head">
          <h2>Related comparisons.</h2>
          <p>Explore neighboring frameworks or jump back to the interactive selector.</p>
        </div>{faq_html}
        <div class="index-rows">
{chr(10).join(rows)}
        </div>
      </div>
    </section>"""


def build_vs_page(spec: dict[str, Any], fws: dict[str, dict[str, Any]], label_map: dict[str, str]) -> str:
    fa = fws[spec["a"]]
    fb = fws[spec["b"]]
    col_a = f"{fa['name']} {fa['latest_version']}"
    col_b = f"{fb['name']} {fb['latest_version']}"
    a_stars = f"{fa['stars']:,}" + (f" (legacy vuejs/vue: {fa['legacy_stars']:,})" if "legacy_stars" in fa else "")
    b_stars = f"{fb['stars']:,}" + (f" (legacy vuejs/vue: {fb['legacy_stars']:,})" if "legacy_stars" in fb else "")
    extra_rows = ""
    if "loc_a" in spec and "loc_b" in spec:
        extra_rows = f"""
              <tr>
                <td data-label="Dimension">Identical app LOC</td>
                <td data-label="{escape(col_a)}" class="measured">{escape(spec['loc_a'])}</td>
                <td data-label="{escape(col_b)}" class="measured">{escape(spec['loc_b'])}</td>
              </tr>"""
    head = render_head(spec["title"], spec["desc"], spec["slug"], spec.get("faq_q"), spec.get("faq_a"))
    nav = render_nav(spec["slug"])
    related_sec = render_related_section(spec["related"], label_map, spec.get("faq_q"), spec.get("faq_a"))
    footer = render_footer(spec["related"], label_map)
    return f"""{head}
<body>
{nav}

  <main>
    <section class="hero-banner">
      <div class="container">
        <h1>{escape(spec['h1'])}</h1>
        <p class="lead">{escape(spec['lead'])}</p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section__head">
          <h2>Compare verified metrics side by side.</h2>
          <p>Data verified on 2026-11-16 from GitHub and npm registries.</p>
        </div>
        <div class="table-wrap">
          <table class="table-responsive">
            <thead>
              <tr>
                <th>Dimension</th>
                <th>{escape(col_a)}</th>
                <th>{escape(col_b)}</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td data-label="Dimension">GitHub stars</td>
                <td data-label="{escape(col_a)}" class="measured">{escape(a_stars)}</td>
                <td data-label="{escape(col_b)}" class="measured">{escape(b_stars)}</td>
              </tr>
              <tr>
                <td data-label="Dimension">npm weekly downloads</td>
                <td data-label="{escape(col_a)}" class="measured">{fa['npm_weekly_downloads']:,}</td>
                <td data-label="{escape(col_b)}" class="measured">{fb['npm_weekly_downloads']:,}</td>
              </tr>
              <tr>
                <td data-label="Dimension">Rendering model</td>
                <td data-label="{escape(col_a)}">{escape(fa['rendering_model'])}</td>
                <td data-label="{escape(col_b)}">{escape(fb['rendering_model'])}</td>
              </tr>
              <tr>
                <td data-label="Dimension">Reactivity</td>
                <td data-label="{escape(col_a)}">{escape(fa['reactivity'])}</td>
                <td data-label="{escape(col_b)}">{escape(fb['reactivity'])}</td>
              </tr>
              <tr>
                <td data-label="Dimension">Runtime tier</td>
                <td data-label="{escape(col_a)}">{escape(fa['runtime_tier'])}</td>
                <td data-label="{escape(col_b)}">{escape(fb['runtime_tier'])}</td>
              </tr>
              <tr>
                <td data-label="Dimension">Server SEO score</td>
                <td data-label="{escape(col_a)}" class="measured">{fa['ssr_seo_score']}/5</td>
                <td data-label="{escape(col_b)}" class="measured">{fb['ssr_seo_score']}/5</td>
              </tr>{extra_rows}
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <section class="section section--band">
      <div class="container">
        <div class="section__head">
          <h2>Choose by project constraint.</h2>
          <p>Match framework strengths to team hiring, runtime budget, and rendering architecture.</p>
        </div>
        <div class="panels-grid panels-grid--3">
          <article>
            <h3>When {escape(fa['name'])} wins</h3>
            <p class="muted-copy">{escape(spec['win_a'])}</p>
          </article>
          <article>
            <h3>When {escape(fb['name'])} wins</h3>
            <p class="muted-copy">{escape(spec['win_b'])}</p>
          </article>
          <article>
            <h3>Compare via CLI</h3>
            <p class="muted-copy">Inspect both frameworks in your terminal or inspect the identical Sprint Task Tracker implementations.</p>
            <div class="cmd-box">
              <code>node src/advisor.ts --compare {escape(spec['a'])} {escape(spec['b'])}</code>
            </div>
          </article>
        </div>
      </div>
    </section>

{related_sec}
  </main>

{footer}
</body>
</html>
"""


def build_alternatives_page(spec: dict[str, Any], fws: dict[str, dict[str, Any]], label_map: dict[str, str]) -> str:
    rows = []
    for fid in spec["picks"]:
        fw = fws[fid]
        rows.append(
            f"""              <tr>
                <td data-label="Alternative"><a href="{escape(fw['official_url'])}" target="_blank" rel="noopener">{escape(fw['name'])}</a></td>
                <td data-label="Latest" class="measured">{escape(fw['latest_version'])}</td>
                <td data-label="Stars" class="num">{fw['stars']:,}</td>
                <td data-label="npm weekly" class="num">{fmt_num(fw['npm_weekly_downloads'])}</td>
                <td data-label="Runtime tier">{escape(fw['runtime_tier'])}</td>
                <td data-label="Why teams switch">{escape(spec['reasons'][fid])}</td>
              </tr>"""
        )
    head = render_head(spec["title"], spec["desc"], spec["slug"], spec.get("faq_q"), spec.get("faq_a"))
    nav = render_nav(spec["slug"])
    related_sec = render_related_section(spec["related"], label_map, spec.get("faq_q"), spec.get("faq_a"))
    footer = render_footer(spec["related"], label_map)
    return f"""{head}
<body>
{nav}

  <main>
    <section class="hero-banner">
      <div class="container">
        <h1>{escape(spec['h1'])}</h1>
        <p class="lead">{escape(spec['lead'])}</p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section__head">
          <h2>Compare verified {escape(spec['target_name'])} alternatives.</h2>
          <p>GitHub stars, npm adoption, and runtime tiers verified on 2026-11-16.</p>
        </div>
        <div class="table-wrap">
          <table class="table-responsive">
            <thead>
              <tr>
                <th>Alternative</th>
                <th>Latest</th>
                <th class="num">Stars</th>
                <th class="num">npm weekly</th>
                <th>Runtime tier</th>
                <th>Why teams switch</th>
              </tr>
            </thead>
            <tbody>
{chr(10).join(rows)}
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <section class="section section--band">
      <div class="container">
        <div class="section__head">
          <h2>How to migrate cleanly.</h2>
          <p>Test one route or widget before committing a full rewrite.</p>
        </div>
        <div class="panels-grid panels-grid--3">
          <article>
            <h3>Start with free starters</h3>
            <p class="muted-copy">Copy minimal Vite or Astro templates from this repository and benchmark bundle size against your existing app.</p>
          </article>
          <article>
            <h3>Compare identical app logic</h3>
            <p class="muted-copy">Review our 5-framework Sprint Task Tracker examples to check real state and template ergonomics before migrating.</p>
          </article>
          <article>
            <h3>Filter by workload</h3>
            <p class="muted-copy">Rank all 15 frameworks for your constraints using the interactive selector or CLI.</p>
            <div class="cmd-box">
              <code>node src/advisor.ts --use-case saas-dashboard --seo-critical</code>
            </div>
          </article>
        </div>
      </div>
    </section>

{related_sec}
  </main>

{footer}
</body>
</html>
"""


def build_workload_page(spec: dict[str, Any], fws: dict[str, dict[str, Any]], label_map: dict[str, str]) -> str:
    rows = []
    for fid in spec["picks"]:
        fw = fws[fid]
        rows.append(
            f"""              <tr>
                <td data-label="Framework"><a href="{escape(fw['official_url'])}" target="_blank" rel="noopener">{escape(fw['name'])}</a></td>
                <td data-label="Latest" class="measured">{escape(fw['latest_version'])}</td>
                <td data-label="npm weekly" class="num">{fmt_num(fw['npm_weekly_downloads'])}</td>
                <td data-label="Rendering model">{escape(fw['rendering_model'])}</td>
                <td data-label="Why it fits">{escape(spec['reasons'][fid])}</td>
              </tr>"""
        )
    head = render_head(spec["title"], spec["desc"], spec["slug"])
    nav = render_nav(spec["slug"])
    related_sec = render_related_section(spec["related"], label_map)
    footer = render_footer(spec["related"], label_map)
    return f"""{head}
<body>
{nav}

  <main>
    <section class="hero-banner">
      <div class="container">
        <h1>{escape(spec['h1'])}</h1>
        <p class="lead">{escape(spec['lead'])}</p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section__head">
          <h2>Top frameworks ranked by fit.</h2>
          <p>Verified versions and weekly npm downloads as of 2026-11-16.</p>
        </div>
        <div class="table-wrap">
          <table class="table-responsive">
            <thead>
              <tr>
                <th>Framework</th>
                <th>Latest</th>
                <th class="num">npm weekly</th>
                <th>Rendering model</th>
                <th>Why it fits</th>
              </tr>
            </thead>
            <tbody>
{chr(10).join(rows)}
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <section class="section section--band">
      <div class="container">
        <div class="section__head">
          <h2>Architecture guidelines.</h2>
          <p>Choose rendering strategy and client bundle boundaries early.</p>
        </div>
        <div class="panels-grid panels-grid--3">
          <article>
            <h3>{escape(spec['panel_a_title'])}</h3>
            <p class="muted-copy">{escape(spec['panel_a_body'])}</p>
          </article>
          <article>
            <h3>{escape(spec['panel_b_title'])}</h3>
            <p class="muted-copy">{escape(spec['panel_b_body'])}</p>
          </article>
          <article>
            <h3>Run CLI advisor</h3>
            <p class="muted-copy">Score all 15 verified frameworks locally with zero dependencies.</p>
            <div class="cmd-box">
              <code>node src/advisor.ts --use-case saas-dashboard --seo-critical</code>
            </div>
          </article>
        </div>
      </div>
    </section>

{related_sec}
  </main>

{footer}
</body>
</html>
"""


def build_directory_page(label_map: dict[str, str]) -> str:
    def render_rows(items: list[dict[str, Any]]) -> str:
        out = []
        for item in items:
            slug = item["slug"]
            href = f"{slug}.html"
            out.append(
                f"""          <a class="index-row" href="{href}">
            <span class="index-row__title">{escape(label_map[href])}</span>
            <span class="index-row__desc">{escape(item['lead'])}</span>
            <span class="index-row__action">Read guide</span>
          </a>"""
            )
        return "\n".join(out)

    head = render_head(
        "Frontend Framework Comparisons and Alternatives Directory (2026)",
        "Browse all 37 frontend framework comparisons, head-to-head matchups, alternatives guides, and workload recommendations.",
        "comparisons",
    )
    nav = render_nav("comparisons")
    footer = render_footer(
        ["react-vs-vue.html", "react-alternatives.html", "nextjs-alternatives.html", "best-frontend-framework-for-seo.html"],
        label_map,
    )
    return f"""{head}
<body>
{nav}

  <main>
    <section class="hero-banner">
      <div class="container">
        <h1>All 37 framework guides and comparisons.</h1>
        <p class="lead">Head-to-head matchups, migration alternatives, and workload guides backed by 2026 data.</p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section__head">
          <h2>Head-to-head comparisons.</h2>
          <p>21 direct matchups across React, Vue, Angular, Svelte, SolidJS, Next.js, Astro, and Nuxt.</p>
        </div>
        <div class="index-rows">
{render_rows(VS_PAIRS)}
        </div>
      </div>
    </section>

    <section class="section section--band">
      <div class="container">
        <div class="section__head">
          <h2>Framework alternatives.</h2>
          <p>10 migration guides for React, Vue, Angular, Svelte, Next.js, jQuery, and CRA.</p>
        </div>
        <div class="index-rows">
{render_rows(ALTERNATIVES_PAGES)}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section__head">
          <h2>Workload guides.</h2>
          <p>6 focused rankings for SEO, lightweight bundles, SaaS, e-commerce, enterprise, and AI apps.</p>
        </div>
        <div class="index-rows">
{render_rows(WORKLOAD_PAGES)}
        </div>
      </div>
    </section>
  </main>

{footer}
</body>
</html>
"""


def main() -> int:
    dataset = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    fws = {fw["id"]: fw for fw in dataset["frameworks"]}

    label_map: dict[str, str] = {}
    for item in VS_PAIRS:
        label_map[f"{item['slug']}.html"] = item["h1"].rstrip(".")
    for item in ALTERNATIVES_PAGES:
        label_map[f"{item['slug']}.html"] = item["h1"].rstrip(".")
    for item in WORKLOAD_PAGES:
        label_map[f"{item['slug']}.html"] = item["h1"].rstrip(".")

    generated_urls: list[tuple[str, str]] = [("", "1.0"), ("comparisons.html", "0.95")]

    for spec in VS_PAIRS:
        path = DOCS_DIR / f"{spec['slug']}.html"
        path.write_text(build_vs_page(spec, fws, label_map), encoding="utf-8")
        generated_urls.append((f"{spec['slug']}.html", "0.9"))

    for spec in ALTERNATIVES_PAGES:
        path = DOCS_DIR / f"{spec['slug']}.html"
        path.write_text(build_alternatives_page(spec, fws, label_map), encoding="utf-8")
        generated_urls.append((f"{spec['slug']}.html", "0.9"))

    for spec in WORKLOAD_PAGES:
        path = DOCS_DIR / f"{spec['slug']}.html"
        path.write_text(build_workload_page(spec, fws, label_map), encoding="utf-8")
        generated_urls.append((f"{spec['slug']}.html", "0.9"))

    (DOCS_DIR / "comparisons.html").write_text(build_directory_page(label_map), encoding="utf-8")

    url_entries = []
    for rel, prio in generated_urls:
        loc = f"{BASE_URL}/{rel}" if rel else f"{BASE_URL}/"
        url_entries.append(
            f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{LASTMOD}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{prio}</priority>
  </url>"""
        )

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(url_entries)}
</urlset>
"""
    (DOCS_DIR / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print(f"Generated {len(generated_urls)} pages in sitemap.xml")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
