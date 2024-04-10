from IntegrationClasses import *
from dark_filter import *
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
import time
import cv2

# Initialize models and state
state = EvaluatingAnatomyState()
model = YOLO("runs/detect/train3/weights/best.pt")
model_aux = YOLO("runs/detect/train5/weights/best.pt")

def process_frame(frame, model):
    results = model.predict(frame, verbose=True, imgsz=320)
    annotator = Annotator(frame)
    for r in results:
        for box in r.boxes:
            b = box.xyxy[0]  # Box coordinates
            c = box.cls  # Class
            annotator.box_label(b, f"{model.names[int(c)]} {box.conf:.2f}")
    return annotator.result()

def start_execution(target_fps = 5):
    cap = cv2.VideoCapture("C:\\Users\\crlew\\PycharmProjects\\EndotrahealTubeModel\\images\\078280753_001.mp4")
    cap.set(3, 640)  # Width
    cap.set(4, 480)  # Height

    video_fps = cap.get(cv2.CAP_PROP_FPS)  # Get the video's original FPS
    frame_interval = int(round(video_fps / target_fps))
    frame_counter = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Stop if no frame is captured

        # Process only every nth frame (according to frame_interval)
        if frame_counter % frame_interval == 0:
            img = process_frame(frame, model_aux)
            cv2.imshow('frame', img)

        frame_counter += 1

        # Break loop if 'ESC' key is pressed
        if cv2.waitKey(1) & 0xFF == 27:
            break

start_execution()
cv2.destroyAllWindows()