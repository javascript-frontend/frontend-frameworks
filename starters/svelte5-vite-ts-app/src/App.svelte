<script lang="ts">
  let count = $state(0);
</script>

<main style="max-width: 720px; margin: 4rem auto; font-family: system-ui, sans-serif; padding: 0 1rem">
  <h1>Svelte 5 Runes + Vite + TypeScript Starter</h1>
  <p>Zero-boilerplate reactive baseline powered by $state and $derived runes.</p>
  <button onclick={() => count++}>Interactions: {count}</button>
</main>
