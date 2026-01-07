# 🎥 AI-Based Online Proctoring System

An end-to-end **AI-powered online proctoring system** built using **Python, Flask, OpenCV, MediaPipe, YOLO**, and **React**.  
The system performs **real-time monitoring**, **risk scoring**, **cheating detection**, **event logging**, and **evidence capture** (snapshots), with downloadable **audit logs (CSV/JSON)**.

---

## 📌 Features Implemented

### ✅ Live Proctoring
- Real-time webcam streaming
- Face count detection
- Head pose / gaze tracking
- Mobile phone detection (YOLO-based)
- Tab-switch / window-blur monitoring (frontend → backend)

### ✅ Intelligent Risk Engine
- Time-based penalties
- Cooldown-based scoring
- Risk decay for good behavior
- Permanent penalties for serious violations
- Delta-based event confirmation

### ✅ Evidence & Logging
- Snapshot capture on confirmed cheating events
- Event timeline with timestamps
- Downloadable CSV & JSON reports
- Snapshot URLs embedded inside CSV

### ✅ Frontend Dashboard
- Start / Stop proctoring
- Live video feed with overlays
- Risk-over-time graph
- Download CSV / JSON buttons

---
Frontend (React)
|
| REST API (JSON)
↓
Backend (Flask)
|
├── Camera Stream (OpenCV)
├── AI Detection Modules
├── Risk Engine
├── Event Logger
├── Snapshot Manager
└── Report Exporter

## 🧠 System Architecture

---

## 🧩 Technologies Used

### 🔹 Backend
| Technology | Purpose |
|----------|--------|
| Flask | REST API & streaming |
| Flask-CORS | Cross-origin requests |
| OpenCV | Camera capture & frame processing |
| MediaPipe FaceMesh | Head pose estimation |
| YOLO (Phone Detection) | Mobile phone detection |
| Python | Core logic |

### 🔹 Frontend
| Technology | Purpose |
|----------|--------|
| React + Vite | Dashboard UI |
| Chart.js / Recharts | Risk graph |
| Fetch API | Backend communication |

---

## 📁 Project Structure

ai_proctoring_system/
│
├── backend/
│ ├── app.py
│ ├── core/
│ │ ├── camera.py
│ │ ├── face_detection.py
│ │ ├── face_mesh.py
│ │ ├── phone_detection.py
│ │ └── risk_engine.py
│ └── snapshots/
│
├── frontend/
│ ├── src/
│ │ ├── App.jsx
│ │ ├── components/
│ │ │ ├── VideoFeed.jsx
│ │ │ └── RiskChart.jsx
│
└── README.md

---

## 🎯 Detection Modules Explained

### 👤 Face Detection
- Counts number of faces per frame
- Detects:
  - `NO_FACE`
  - `MULTIPLE_FACES`

### 👀 Head Pose / Looking Away
- Uses facial landmarks (yaw angle)
- Flags when user looks away continuously

### 📱 Phone Detection
- YOLO-based detection
- Triggered every N frames (performance optimized)
- Penalized only if visible continuously

### 🖥️ Tab Switch Detection
- Frontend listens to:
  - `document.visibilitychange`
  - `window.blur`
- Sends events to backend (`/tab-event`)

---

## ⚠️ Risk Engine Design

### 🔸 Why a Risk Engine?
Instead of binary cheating detection, we use **behavioral risk accumulation**, just like real exam platforms.

### 🔸 Risk Types
- **Temporary Risk**
  - Decays over time
  - Encourages good behavior recovery
- **Permanent Risk**
  - Serious violations
  - Never decays

---

### 🧮 Risk Logic Summary

| Event | Condition | Penalty |
|----|----|----|
| No Face | > 2 sec | +5 |
| Multiple Faces | > 2 sec | +10 |
| Looking Away | > 3 sec | +6 |
| Phone Detected | > 5 sec | +15 (permanent) |
| Tab Switch | Immediate | +5 (permanent) |

✔ Risk decays by **1 point per second** if no violation.

---

## 📸 Snapshot Capture System

- Snapshots are taken **only when risk increases**
- Stored in `/snapshots/`
- Publicly accessible via Flask route
- Snapshot URL saved inside event log

Example:

---

## 🎯 Detection Modules Explained

### 👤 Face Detection
- Counts number of faces per frame
- Detects:
  - `NO_FACE`
  - `MULTIPLE_FACES`

### 👀 Head Pose / Looking Away
- Uses facial landmarks (yaw angle)
- Flags when user looks away continuously

### 📱 Phone Detection
- YOLO-based detection
- Triggered every N frames (performance optimized)
- Penalized only if visible continuously

### 🖥️ Tab Switch Detection
- Frontend listens to:
  - `document.visibilitychange`
  - `window.blur`
- Sends events to backend (`/tab-event`)

---

## ⚠️ Risk Engine Design

### 🔸 Why a Risk Engine?
Instead of binary cheating detection, we use **behavioral risk accumulation**, just like real exam platforms.

### 🔸 Risk Types
- **Temporary Risk**
  - Decays over time
  - Encourages good behavior recovery
- **Permanent Risk**
  - Serious violations
  - Never decays

---

### 🧮 Risk Logic Summary

| Event | Condition | Penalty |
|----|----|----|
| No Face | > 2 sec | +5 |
| Multiple Faces | > 2 sec | +10 |
| Looking Away | > 3 sec | +6 |
| Phone Detected | > 5 sec | +15 (permanent) |
| Tab Switch | Immediate | +5 (permanent) |

✔ Risk decays by **1 point per second** if no violation.

---

## 📸 Snapshot Capture System

- Snapshots are taken **only when risk increases**
- Stored in `/snapshots/`
- Publicly accessible via Flask route
- Snapshot URL saved inside event log

Example:
snapshots/LOOKING_AWAY_1767788935191.jpg


---

## 📑 Event Logging Format

Each cheating event stores:

```json
{
  "time_24h": "2026-01-07 17:59:23",
  "unix_time": 1767788963.51,
  "event": "LOOKING_AWAY",
  "risk_delta": 6,
  "risk_total": 24,
  "phone_detected": 0,
  "looking_away": 1,
  "face_count": 1,
  "snapshot_url": "http://127.0.0.1:5000/snapshots/LOOKING_AWAY_..."
}
```
## 📤 Exported Reports

### CSV Export
- Timestamp (24-hour format)
- Unix time
- Event name
- Risk delta
- Total risk
- Detection flags
- Snapshot URL

### JSON Export
- Session start time
- Full risk history
- Complete event timeline

---

## 🖥️ Frontend Dashboard Features

- ▶ **Start Proctoring**
- ■ **Stop Proctoring**
- 🎥 **Live Camera Feed**
- 📈 **Risk Over Time Graph**
- 📥 **Download CSV / JSON**
- 🚨 **Real-time Overlay Warnings**

---

## 🚀 How to Run

### Backend
```bash
cd backend
python app.py
```
### Frontend
```bash
cd frontend
npm install
npm run dev
```


