import { For, createEffect, createMemo, createSignal } from "solid-js";

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

export default function App() {
  const [tasks, setTasks] = createSignal<Task[]>(load());
  const [title, setTitle] = createSignal("");
  const [priority, setPriority] = createSignal<Priority>("med");
  const [filter, setFilter] = createSignal<Filter>("all");

  createEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks()));
  });

  const remaining = createMemo(() => tasks().filter((t) => !t.done).length);
  const visible = createMemo(() => {
    const f = filter();
    if (f === "active") return tasks().filter((t) => !t.done);
    if (f === "done") return tasks().filter((t) => t.done);
    return tasks();
  });

  function addTask(e: SubmitEvent) {
    e.preventDefault();
    const clean = title().trim();
    if (!clean) return;
    setTasks((prev) => [{ id: crypto.randomUUID(), title: clean, priority: priority(), done: false }, ...prev]);
    setTitle("");
  }

  const toggle = (id: string) =>
    setTasks((prev) => prev.map((t) => (t.id === id ? { ...t, done: !t.done } : t)));
  const remove = (id: string) => setTasks((prev) => prev.filter((t) => t.id !== id));

  return (
    <main>
      <h1>Sprint Tasks ({remaining()} open)</h1>
      <form onSubmit={addTask}>
        <input value={title()} onInput={(e) => setTitle(e.currentTarget.value)} placeholder="Add task..." />
        <select value={priority()} onChange={(e) => setPriority(e.currentTarget.value as Priority)}>
          <option value="high">High</option>
          <option value="med">Medium</option>
          <option value="low">Low</option>
        </select>
        <button type="submit">Add</button>
      </form>
      <div>
        <For each={["all", "active", "done"] as Filter[]}>
          {(f) => (
            <button onClick={() => setFilter(f)} aria-pressed={filter() === f}>
              {f}
            </button>
          )}
        </For>
      </div>
      <ul>
        <For each={visible()}>
          {(t) => (
            <li>
              <label>
                <input type="checkbox" checked={t.done} onChange={() => toggle(t.id)} />
                <span>[{t.priority}] {t.title}</span>
              </label>
              <button onClick={() => remove(t.id)}>Delete</button>
            </li>
          )}
        </For>
      </ul>
    </main>
  );
}
