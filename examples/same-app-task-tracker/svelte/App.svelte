<script lang="ts">
  type Priority = "high" | "med" | "low";
  type Filter = "all" | "active" | "done";

  interface Task {
    id: string;
    title: string;
    priority: Priority;
    done: boolean;
  }

  const STORAGE_KEY = "ff-task-tracker-v1";
  const initial = (): Task[] => {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
    } catch {
      return [];
    }
  };

  let tasks = $state<Task[]>(initial());
  let title = $state("");
  let priority = $state<Priority>("med");
  let filter = $state<Filter>("all");

  const remaining = $derived(tasks.filter((t) => !t.done).length);
  const visible = $derived(
    filter === "active" ? tasks.filter((t) => !t.done)
    : filter === "done" ? tasks.filter((t) => t.done)
    : tasks
  );

  $effect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks));
  });

  function addTask(e: SubmitEvent) {
    e.preventDefault();
    const clean = title.trim();
    if (!clean) return;
    tasks.unshift({ id: crypto.randomUUID(), title: clean, priority, done: false });
    title = "";
  }

  const remove = (id: string) => {
    tasks = tasks.filter((t) => t.id !== id);
  };
</script>

<main>
  <h1>Sprint Tasks ({remaining} open)</h1>
  <form onsubmit={addTask}>
    <input bind:value={title} placeholder="Add task..." />
    <select bind:value={priority}>
      <option value="high">High</option>
      <option value="med">Medium</option>
      <option value="low">Low</option>
    </select>
    <button type="submit">Add</button>
  </form>
  <div>
    {#each ["all", "active", "done"] as const as f}
      <button onclick={() => (filter = f)} aria-pressed={filter === f}>{f}</button>
    {/each}
  </div>
  <ul>
    {#each visible as t (t.id)}
      <li>
        <label>
          <input type="checkbox" bind:checked={t.done} />
          <span>[{t.priority}] {t.title}</span>
        </label>
        <button onclick={() => remove(t.id)}>Delete</button>
      </li>
    {/each}
  </ul>
</main>
