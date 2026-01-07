import { useState, useEffect } from "react";

const API = "http://127.0.0.1:5000";

export default function Dashboard() {
  const [active, setActive] = useState(false);
  const [risk, setRisk] = useState(0);

  const start = async () => {
    await fetch(`${API}/start`, { method: "POST" });
    setActive(true);
  };

  const stop = async () => {
    await fetch(`${API}/stop`, { method: "POST" });
    setActive(false);
  };

  useEffect(() => {
    if (!active) return;

    const interval = setInterval(async () => {
      const res = await fetch(`${API}/tick`);
      const data = await res.json();
      setRisk(data.risk);
    }, 1000);

    return () => clearInterval(interval);
  }, [active]);

  return (
    <div style={{ padding: 40 }}>
      <h1>AI Proctoring System</h1>

      <button onClick={start} disabled={active}>
        ▶ Start Proctoring
      </button>

      <button onClick={stop} disabled={!active} style={{ marginLeft: 10 }}>
        ⏹ Stop Proctoring
      </button>

      <h2>Status: {active ? "ACTIVE" : "STOPPED"}</h2>
      <h2>Risk Score: {risk}</h2>
    </div>
  );
}
