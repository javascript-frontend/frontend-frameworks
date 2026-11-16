# Same App Across 5 Frontend Frameworks (Sprint Task Tracker)

To compare real-world ergonomics instead of synthetic "Hello World" snippets, every folder here implements the **exact same Sprint Task Tracker specification**:

1. Add task with text input + priority (`high` / `med` / `low`).
2. Filter tasks (`all` / `active` / `done`).
3. Toggle task completion and delete tasks.
4. Compute live remaining open-task count.
5. Persist and restore tasks via `localStorage`.

## Side-by-Side Comparison

| Framework | File | Lines | State Primitive | Derived State | Side Effect | Template Style |
| :--- | :--- | ---: | :--- | :--- | :--- | :--- |
| **Vue 3.5** | [`vue/App.vue`](vue/App.vue) | 76 | `ref()` | `computed()` | `watch(..., { deep: true })` | HTML SFC (`v-model`, `v-for`) |
| **Svelte 5** | [`svelte/App.svelte`](svelte/App.svelte) | 77 | `$state()` | `$derived()` | `$effect()` | HTML SFC (`bind:value`, `{#each}`) |
| **React 19** | [`react/App.tsx`](react/App.tsx) | 82 | `useState()` | `useMemo()` | `useEffect()` | JSX (`onChange`, `.map()`) |
| **SolidJS 1.9** | [`solid/App.tsx`](solid/App.tsx) | 88 | `createSignal()` | `createMemo()` | `createEffect()` | JSX (`<For>`, getter calls) |
| **Angular 22** | [`angular/app.component.ts`](angular/app.component.ts) | 93 | `signal()` | `computed()` | `effect()` | Standalone Class + `@for` |

## Key Engineering Takeaways

- **React vs SolidJS:** Look similar in JSX, but React re-executes the component function on state updates (requiring `useMemo` / dependency arrays), while Solid executes the component once and tracks signal getters (`tasks()`, `remaining()`).
- **Vue 3.5 vs Svelte 5:** Nearly identical line counts (`76` vs `77`); Svelte 5 Runes (`$state`, `$derived`) eliminate `.value` unwrapping while Vue gives explicit `ref` objects.
- **Angular 22:** Slightly more ceremony (`@Component` decorator + `FormsModule` import), but built-in Signals (`signal`, `computed`, `effect`) and `@for` control flow keep standalone components concise without RxJS boilerplate for local UI state.
