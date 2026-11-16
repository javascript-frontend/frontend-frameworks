import { Component, computed, effect, signal } from "@angular/core";
import { FormsModule } from "@angular/forms";

type Priority = "high" | "med" | "low";
type Filter = "all" | "active" | "done";

interface Task {
  id: string;
  title: string;
  priority: Priority;
  done: boolean;
}

const STORAGE_KEY = "ff-task-tracker-v1";

@Component({
  selector: "app-root",
  standalone: true,
  imports: [FormsModule],
  template: `
    <main>
      <h1>Sprint Tasks ({{ remaining() }} open)</h1>
      <form (ngSubmit)="addTask()">
        <input [(ngModel)]="title" name="title" placeholder="Add task..." />
        <select [(ngModel)]="priority" name="priority">
          <option value="high">High</option>
          <option value="med">Medium</option>
          <option value="low">Low</option>
        </select>
        <button type="submit">Add</button>
      </form>
      <div>
        @for (f of filters; track f) {
          <button (click)="filter.set(f)" [attr.aria-pressed]="filter() === f">{{ f }}</button>
        }
      </div>
      <ul>
        @for (t of visible(); track t.id) {
          <li>
            <label>
              <input type="checkbox" [checked]="t.done" (change)="toggle(t.id)" />
              <span>[{{ t.priority }}] {{ t.title }}</span>
            </label>
            <button (click)="remove(t.id)">Delete</button>
          </li>
        }
      </ul>
    </main>
  `,
})
export class AppComponent {
  readonly filters: Filter[] = ["all", "active", "done"];
  tasks = signal<Task[]>(this.load());
  filter = signal<Filter>("all");
  title = "";
  priority: Priority = "med";

  remaining = computed(() => this.tasks().filter((t) => !t.done).length);
  visible = computed(() => {
    const f = this.filter();
    const list = this.tasks();
    if (f === "active") return list.filter((t) => !t.done);
    if (f === "done") return list.filter((t) => t.done);
    return list;
  });

  constructor() {
    effect(() => localStorage.setItem(STORAGE_KEY, JSON.stringify(this.tasks())));
  }

  private load(): Task[] {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
    } catch {
      return [];
    }
  }

  addTask() {
    const clean = this.title.trim();
    if (!clean) return;
    this.tasks.update((prev) => [{ id: crypto.randomUUID(), title: clean, priority: this.priority, done: false }, ...prev]);
    this.title = "";
  }

  toggle(id: string) {
    this.tasks.update((prev) => prev.map((t) => (t.id === id ? { ...t, done: !t.done } : t)));
  }

  remove(id: string) {
    this.tasks.update((prev) => prev.filter((t) => t.id !== id));
  }
}
