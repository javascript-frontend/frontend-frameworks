<script setup lang="ts">
import { ref } from "vue";
const count = ref(0);
</script>

<template>
  <main style="max-width: 720px; margin: 4rem auto; font-family: system-ui, sans-serif; padding: 0 1rem">
    <h1>Vue 3.5 + Vite + TypeScript Starter</h1>
    <p>Clean Composition API (&lt;script setup&gt;) baseline ready for Pinia and Vue Router.</p>
    <button @click="count++">Interactions: {{ count }}</button>
  </main>
</template>
