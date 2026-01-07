import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
} from "chart.js";
import { Line } from "react-chartjs-2";

ChartJS.register(
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
);

export default function RiskChart({ history }) {
  return (
    <Line
      data={{
        labels: history.map((_, i) => i),
        datasets: [
          {
            label: "Risk Score",
            data: history.map(h => h.risk),
            borderColor: "#ef4444",
            borderWidth: 2,
            tension: 0.3,
            pointRadius: 0
          }
        ]
      }}
      options={{
        responsive: true,
        scales: {
          y: { beginAtZero: true }
        }
      }}
    />
  );
}
