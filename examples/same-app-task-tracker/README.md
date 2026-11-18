# Same app across 5 frontend frameworks (Sprint Task Tracker)

Every folder here implements the same Sprint Task Tracker:

1. Add a task with text input and priority (`high` / `med` / `low`).
2. Filter tasks (`all` / `active` / `done`).
3. Toggle task completion and delete tasks.
4. Compute live remaining open-task count.
5. Persist and restore tasks via `localStorage`.

## Side-by-side comparison

| Framework | File | Lines | State primitive | Derived state | Side effect | Template style |
| :--- | :--- | ---: | :--- | :--- | :--- | :--- |
| Vue 3.5 | [`vue/App.vue`](vue/App.vue) | 76 | `ref()` | `computed()` | `watch(..., { deep: true })` | HTML SFC (`v-model`, `v-for`) |
| Svelte 5 | [`svelte/App.svelte`](svelte/App.svelte) | 77 | `$state()` | `$derived()` | `$effect()` | HTML SFC (`bind:value`, `{#each}`) |
| React 19 | [`react/App.tsx`](react/App.tsx) | 82 | `useState()` | `useMemo()` | `useEffect()` | JSX (`onChange`, `.map()`) |
| SolidJS 1.9 | [`solid/App.tsx`](solid/App.tsx) | 88 | `createSignal()` | `createMemo()` | `createEffect()` | JSX (`<For>`, getter calls) |
| Angular 22 | [`angular/app.component.ts`](angular/app.component.ts) | 93 | `signal()` | `computed()` | `effect()` | Standalone Class + `@for` |

## Takeaways

- React and SolidJS share JSX syntax, yet React re-runs the component function on state updates (so hooks need dependency arrays) while Solid runs the component once and tracks signal getters (`tasks()`, `remaining()`).
- Vue 3.5 and Svelte 5 come within one line of each other (`76` vs `77`); Svelte 5 Runes (`$state`, `$derived`) skip `.value` unwrapping, while Vue keeps `ref` objects explicit.
- Angular 22 takes slightly more setup (`@Component` decorator and `FormsModule`), though built-in Signals (`signal`, `computed`, `effect`) and `@for` control flow avoid RxJS boilerplate for local UI state.
