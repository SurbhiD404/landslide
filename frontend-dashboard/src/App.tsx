import { useState } from "react";

function App() {
  const [health, setHealth] = useState<string>("");

  const checkHealth = async () => {
    try {
      const res = await fetch("/health");
      const data = await res.json();
      setHealth(JSON.stringify(data));
    } catch {
      setHealth("Backend unreachable");
    }
  };

  return (
    <div style={{ fontFamily: "system-ui, sans-serif", padding: "2rem" }}>
      <h1>Landslide Early Warning System</h1>
      <h2>District Disaster Management Dashboard</h2>
      <p>SIH26001 — AI-Based Early Warning and Landslide Risk Monitoring System in NER</p>

      <section style={{ marginTop: "2rem", padding: "1rem", border: "1px solid #ccc", borderRadius: "8px" }}>
        <h3>System Status</h3>
        <button onClick={checkHealth} style={{ padding: "0.5rem 1rem", cursor: "pointer" }}>
          Check Backend Health
        </button>
        {health && <pre style={{ marginTop: "1rem", background: "#f5f5f5", padding: "1rem" }}>{health}</pre>}
      </section>

      <section style={{ marginTop: "2rem" }}>
        <h3>Components (Phase 3)</h3>
        <ul>
          <li>RiskHeatmap — React + Leaflet color-coded risk zones</li>
          <li>RoadStatusPanel — Road connectivity overlay</li>
          <li>ForecastPanel — Weather forecast per zone</li>
          <li>AlertConsole — Recent alerts with explanations</li>
        </ul>
      </section>
    </div>
  );
}

export default App;
