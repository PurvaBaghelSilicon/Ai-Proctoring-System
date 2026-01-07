import { useEffect, useState } from "react";
import RiskChart from "./components/RiskChart";
import VideoFeed from "./components/VideoFeed";

function App() {
  const [running, setRunning] = useState(false);
  const [riskHistory, setRiskHistory] = useState([]);

  // 🔁 Poll risk history
  useEffect(() => {
    if (!running) return;

    const interval = setInterval(() => {
      fetch("http://127.0.0.1:5000/risk-history")
        .then(res => res.json())
        .then(data => setRiskHistory(data))
        .catch(() => {});
    }, 1000);

    return () => clearInterval(interval);
  }, [running]);

  // 🟡 TAB SWITCH / VISIBILITY LOGGING
  useEffect(() => {
    const handleVisibilityChange = () => {
      if (document.hidden) {
        fetch("http://127.0.0.1:5000/tab-event", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ event: "TAB_HIDDEN" })
        });
      }
    };

    document.addEventListener("visibilitychange", handleVisibilityChange);

    return () => {
      document.removeEventListener("visibilitychange", handleVisibilityChange);
    };
  }, []);

  // 🟡 WINDOW BLUR LOGGING
  useEffect(() => {
    const handleBlur = () => {
      fetch("http://127.0.0.1:5000/tab-event", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ event: "WINDOW_BLUR" })
      });
    };

    window.addEventListener("blur", handleBlur);

    return () => {
      window.removeEventListener("blur", handleBlur);
    };
  }, []);

  const startProctoring = async () => {
    await fetch("http://127.0.0.1:5000/start", { method: "POST" });
    setRunning(true);
  };

  const stopProctoring = () => {
    setRunning(false);
  };

  return (
    <div style={page}>
      <h1>AI Proctoring Dashboard</h1>
      <p style={{ color: "#94a3b8" }}>
        Real-time monitoring using face analysis, head pose & phone detection
      </p>

      <div style={controls}>
        <button onClick={startProctoring} style={startBtn}>
          ▶ Start Proctoring
        </button>
        <button onClick={stopProctoring} style={stopBtn}>
          ■ Stop
        </button>
      </div>

      <div style={grid}>
        <div>
          <h3>Live Camera Feed</h3>
          <VideoFeed running={running} />
        </div>

        <div>
          <h3>Risk Over Time</h3>
          <RiskChart history={riskHistory} />
        </div>
      </div>

      <div style={downloads}>
        <a href="http://127.0.0.1:5000/export/csv" target="_blank">
          <button style={downloadBtn}>Download CSV</button>
        </a>
        <a
          href="http://127.0.0.1:5000/export/json"
          target="_blank"
          style={{ marginLeft: "12px" }}
        >
          <button style={downloadBtn}>Download JSON</button>
        </a>
      </div>
    </div>
  );
}

export default App;

/* ---------- STYLES ---------- */

const page = {
  minHeight: "100vh",
  background: "#020617",
  color: "white",
  padding: "30px",
  fontFamily: "Arial"
};

const controls = {
  margin: "20px 0"
};

const grid = {
  display: "grid",
  gridTemplateColumns: "1fr 1fr",
  gap: "30px"
};

const downloads = {
  marginTop: "25px"
};

const startBtn = {
  background: "#16a34a",
  color: "white",
  padding: "10px 16px",
  border: "none",
  borderRadius: "6px",
  marginRight: "10px",
  cursor: "pointer"
};

const stopBtn = {
  background: "#dc2626",
  color: "white",
  padding: "10px 16px",
  border: "none",
  borderRadius: "6px",
  cursor: "pointer"
};

const downloadBtn = {
  background: "#334155",
  color: "white",
  padding: "8px 14px",
  border: "none",
  borderRadius: "6px",
  cursor: "pointer"
};
