from flask import (
    Flask, Response, jsonify, request,
    make_response, send_from_directory
)
from flask_cors import CORS
import cv2
import time
import csv
from io import StringIO
from datetime import datetime
import os

# -------------------- UTILITIES --------------------

def to_24hr(ts):
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

# -------------------- CORE IMPORTS --------------------

from core.camera import Camera
from core.face_detection import detect_faces
from core.face_mesh import get_head_pose
from core.phone_detection import detect_phone
from core.risk_engine import RiskEngine

risk_engine = RiskEngine()

# -------------------- GLOBAL STATE --------------------

frame_count = 0
phone_detected = False
show_phone_overlay = False

risk_history = []
event_log = []
session_start_time = None

camera = None

# -------------------- APP INIT --------------------

app = Flask(__name__)
CORS(app)

os.makedirs("snapshots", exist_ok=True)

# -------------------- SNAPSHOT --------------------

def save_snapshot(frame, event_name):
    timestamp = int(time.time() * 1000)
    filename = f"{event_name}_{timestamp}.jpg"
    path = os.path.join("snapshots", filename)

    cv2.imwrite(path, frame)

    return f"http://127.0.0.1:5000/snapshots/{filename}"

# -------------------- ROUTES --------------------

@app.route("/start", methods=["POST"])
def start():
    global camera, risk_history, event_log, session_start_time

    camera = Camera()
    risk_history = []
    event_log = []
    session_start_time = time.time()

    return jsonify({"status": "started"})


@app.route("/video")
def video():
    if camera is None:
        return "Camera not started. Call /start first.", 400

    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/risk-history")
def risk_history_api():
    return jsonify(risk_history)


@app.route("/events")
def events_api():
    return jsonify(event_log)


@app.route("/export/json")
def export_json():
    return jsonify({
        "session_start": session_start_time,
        "risk_history": risk_history,
        "events": event_log
    })


@app.route("/export/csv")
def export_csv():
    if not event_log:
        return jsonify({"error": "No events logged"}), 400

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "time_24h",
        "event",
        "risk_delta",
        "risk_total",
        "phone_detected",
        "looking_away",
        "face_count",
        "snapshot_url"
    ])

    for e in event_log:
        writer.writerow([
            e["time_24h"],
            e["event"],
            e["risk_delta"],
            e["risk_total"],
            e["phone_detected"],
            e["looking_away"],
            e["face_count"],
            e["snapshot_url"]
        ])

    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=proctoring_session.csv"
    response.headers["Content-Type"] = "text/csv"

    return response


@app.route("/tab-event", methods=["POST"])
def tab_event():
    data = request.json
    event = data.get("event")
    now = time.time()

    if event == "TAB_HIDDEN":
        new_risk = risk_engine.add_external_penalty(5)

        event_log.append({
            "time_24h": to_24hr(now),
            "unix_time": now,
            "event": "TAB_SWITCH",
            "risk_delta": 5,
            "risk_total": new_risk,
            "phone_detected": 0,
            "looking_away": 0,
            "face_count": None,
            "snapshot_url": ""
        })

    return jsonify({"status": "logged"})



@app.route("/snapshots/<filename>")
def serve_snapshot(filename):
    return send_from_directory("snapshots", filename)

# -------------------- VIDEO LOOP --------------------

def generate_frames():
    global frame_count, phone_detected, show_phone_overlay

    while True:
        ret, frame = camera.read()
        if not ret:
            break

        frame_count += 1

        # ---- PHONE (YOLO every 30 frames) ----
        if frame_count % 30 == 0:
            phone_detected = detect_phone(frame)
            show_phone_overlay = phone_detected

        # ---- FACE COUNT ----
        face_count = detect_faces(frame)
        cv2.putText(frame, f"Faces: {face_count}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # ---- HEAD POSE ----
        looking_away = False
        pitch, yaw = get_head_pose(frame)

        if pitch is not None and yaw is not None:
            if abs(yaw) > 15:
                looking_away = True
                status, color = "LOOKING AWAY", (0, 0, 255)
            else:
                status, color = "LOOKING FORWARD", (0, 255, 0)

            cv2.putText(frame, status, (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        # ---- RISK UPDATE ----
        risk, delta = risk_engine.update(
            face_count, looking_away, phone_detected
        )

        risk_history.append({
            "time": time.time(),
            "risk": risk
        })
        risk_history[:] = risk_history[-300:]

        cv2.putText(frame, f"Risk: {risk}", (20, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        # ---- EVENT LOGGING (ONLY ON DELTA) ----
        if delta > 0:
            if phone_detected:
                event_name = "PHONE_DETECTED"
            elif looking_away:
                event_name = "LOOKING_AWAY"
            elif face_count == 0:
                event_name = "NO_FACE"
            elif face_count > 1:
                event_name = "MULTIPLE_FACES"
            else:
                event_name = "UNKNOWN"

            snapshot_url = save_snapshot(frame, event_name)

            event_log.append({
                "time_24h": to_24hr(time.time()),
                "event": event_name,
                "risk_delta": delta,
                "risk_total": risk,
                "phone_detected": int(phone_detected),
                "looking_away": int(looking_away),
                "face_count": face_count,
                "snapshot_url": snapshot_url
            })

        # ---- OVERLAY ----
        if show_phone_overlay:
            cv2.putText(frame, "PHONE DETECTED", (20, 160),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # ---- STREAM ----
        ret, buffer = cv2.imencode(".jpg", frame)
        if not ret:
            continue

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" +
            buffer.tobytes() +
            b"\r\n"
        )

# -------------------- MAIN --------------------

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
