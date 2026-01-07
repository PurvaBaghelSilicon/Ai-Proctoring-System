import cv2
import numpy as np

def detect_head_pose(landmarks, frame_shape):
    h, w = frame_shape[:2]

    image_points = np.array([
        (landmarks[1].x * w, landmarks[1].y * h),   # Nose
        (landmarks[152].x * w, landmarks[152].y * h), # Chin
        (landmarks[33].x * w, landmarks[33].y * h), # Left eye
        (landmarks[263].x * w, landmarks[263].y * h), # Right eye
        (landmarks[61].x * w, landmarks[61].y * h), # Left mouth
        (landmarks[291].x * w, landmarks[291].y * h) # Right mouth
    ], dtype="double")

    model_points = np.array([
        (0, 0, 0),
        (0, -330, -65),
        (-225, 170, -135),
        (225, 170, -135),
        (-150, -150, -125),
        (150, -150, -125)
    ])

    focal_length = w
    cam_matrix = np.array([
        [focal_length, 0, w / 2],
        [0, focal_length, h / 2],
        [0, 0, 1]
    ], dtype="double")

    dist = np.zeros((4, 1))
    _, rvec, _ = cv2.solvePnP(model_points, image_points, cam_matrix, dist)
    angles, _, _, _, _, _ = cv2.RQDecomp3x3(cv2.Rodrigues(rvec)[0])

    yaw, pitch = angles[1], angles[0]

    if abs(yaw) > 20 or abs(pitch) > 20:
        return True, yaw, pitch

    return False, yaw, pitch
