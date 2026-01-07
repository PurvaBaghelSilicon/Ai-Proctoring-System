print(">>> phone_detection.py LOADED <<<")

from ultralytics import YOLO


# Load lightweight YOLOv8 model
model = YOLO("yolov8n.pt")  # nano = fast on CPU

PHONE_CLASS_ID = 67  # COCO class ID for 'cell phone'

def detect_phone(frame):
    print(">>> detect_phone CALLED <<<")
    results = model(frame, conf=0.25, verbose=False)

    for r in results:
        if r.boxes is None:
            continue
        for cls in r.boxes.cls:
            if int(cls) == PHONE_CLASS_ID:
                print(">>> RETURNING True <<<")
                return True

    print(">>> RETURNING False <<<")
    return False


