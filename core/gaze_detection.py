import mediapipe as mp
import numpy as np

mp_mesh = mp.solutions.face_mesh
mesh = mp_mesh.FaceMesh(refine_landmarks=True)

def detect_gaze(frame):
    rgb = frame[:, :, ::-1]
    result = mesh.process(rgb)

    if not result.multi_face_landmarks:
        return "UNKNOWN"

    lm = result.multi_face_landmarks[0].landmark
    nose = lm[1]
    left_iris = lm[468]
    right_iris = lm[473]

    avg_x = ((left_iris.x + right_iris.x) / 2) - nose.x
    avg_y = ((left_iris.y + right_iris.y) / 2) - nose.y

    if abs(avg_x) < 0.02 and abs(avg_y) < 0.02:
        return "CENTER"
    if avg_x < -0.02:
        return "LEFT"
    if avg_x > 0.02:
        return "RIGHT"
    if avg_y > 0.02:
        return "DOWN"

    return "CENTER"
