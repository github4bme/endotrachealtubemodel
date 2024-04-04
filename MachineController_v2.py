from IntegrationClasses import *
from dark_filter import *
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
import time
import cv2


def start_execution():
    state = EvaluatingAnatomyState()

    model = YOLO("runs/detect/train3/weights/best.pt")

    cap = cv2.VideoCapture("C:\\Users\\crlew\\PycharmProjects\\EndotrahealTubeModel\\images\\078280753_001.mp4")
    cap.set(3, 640)  # set Width
    cap.set(4, 480)  # set Height
    lastFrameTime = None

    while (True):
        currentTime = time.time()
        if lastFrameTime is not None:
            dt = currentTime - lastFrameTime
        else:
            dt = 0
        lastFrameTime = currentTime

        state = state.Execute(dt)

        ret, frame = cap.read()

        # imgsz=288 seems to be the lowest size the model can still reliably recognize
        results = model.predict(frame, verbose=True, imgsz=288)

        for r in results:

            annotator = Annotator(frame)

            boxes = r.boxes
            for box in boxes:
                b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
                c = box.cls
                annotator.box_label(b, model.names[int(c)] + " " + str(box.conf))

        img = annotator.result()
        cv2.imshow('frame', img)

        k = cv2.waitKey(30) & 0xff
        if k == 27:  # press 'ESC' to quit
            break


start_execution()