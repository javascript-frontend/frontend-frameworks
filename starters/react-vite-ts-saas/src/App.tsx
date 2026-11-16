import { useState } from "react";

export default function App() {
  const [count, setCount] = useState(0);
  return (
    <main style={{ maxWidth: 720, margin: "4rem auto", fontFamily: "system-ui, sans-serif", padding: "0 1rem" }}>
      <h1>React 19 + Vite + TypeScript Starter</h1>
      <p>Clean baseline ready for SaaS dashboards, authentication, and API data fetching.</p>
      <button onClick={() => setCount((c) => c + 1)}>Interactions: {count}</button>
    </main>
  );
}
