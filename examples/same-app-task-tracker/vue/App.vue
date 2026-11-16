<script setup lang="ts">
import { computed, ref, watch } from "vue";

type Priority = "high" | "med" | "low";
type Filter = "all" | "active" | "done";

interface Task {
  id: string;
  title: string;
  priority: Priority;
  done: boolean;
}

const STORAGE_KEY = "ff-task-tracker-v1";
const load = (): Task[] => {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
  } catch {
    return [];
  }
};

const tasks = ref<Task[]>(load());
const title = ref("");
const priority = ref<Priority>("med");
const filter = ref<Filter>("all");

watch(tasks, (val) => localStorage.setItem(STORAGE_KEY, JSON.stringify(val)), { deep: true });

const remaining = computed(() => tasks.value.filter((t) => !t.done).length);
const visible = computed(() => {
  if (filter.value === "active") return tasks.value.filter((t) => !t.done);
  if (filter.value === "done") return tasks.value.filter((t) => t.done);
  return tasks.value;
});

function addTask() {
  const clean = title.value.trim();
  if (!clean) return;
  tasks.value.unshift({ id: crypto.randomUUID(), title: clean, priority: priority.value, done: false });
  title.value = "";
}

const remove = (id: string) => {
  tasks.value = tasks.value.filter((t) => t.id !== id);
};
</script>

<template>
  <main>
    <h1>Sprint Tasks ({{ remaining }} open)</h1>
    <form @submit.prevent="addTask">
      <input v-model="title" placeholder="Add task..." />
      <select v-model="priority">
        <option value="high">High</option>
        <option value="med">Medium</option>
        <option value="low">Low</option>
      </select>
      <button type="submit">Add</button>
    </form>
    <div>
      <button v-for="f in (['all', 'active', 'done'] as const)" :key="f" :aria-pressed="filter === f" @click="filter = f">
        {{ f }}
      </button>
    </div>
    <ul>
      <li v-for="t in visible" :key="t.id">
        <label>
          <input type="checkbox" v-model="t.done" />
          <span>[{{ t.priority }}] {{ t.title }}</span>
        </label>
        <button @click="remove(t.id)">Delete</button>
      </li>
    </ul>
  </main>
</template>
