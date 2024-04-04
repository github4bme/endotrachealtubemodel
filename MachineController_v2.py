from IntegrationClasses import *
from dark_filter import *
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
import time
import cv2


def start_execution():
    state = EvaluatingAnatomyState()

    model = YOLO("runs/detect/train3/weights/best.pt")
    model_aux = YOLO("runs/detect/train5/weights/best.pt")

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

        #img = image_process_model(frame, model)
        img = image_process_aux(frame, model_aux)
        #img = image_process_darkness(frame)
        cv2.imshow('frame', img)

        k = cv2.waitKey(30) & 0xff
        if k == 27:  # press 'ESC' to quit
            break

def image_process_model(frame, model):
    # imgsz=288 seems to be the lowest size the model can still reliably recognize
    results = model.predict(frame, verbose=True, imgsz=320)

    for r in results:
        annotator = Annotator(frame)

        boxes = r.boxes
        for box in boxes:
            b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
            c = box.cls
            annotator.box_label(b, model.names[int(c)] + " " + str(box.conf))

    return annotator.result()

def image_process_darkness(frame):
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    threshold_value = 50

    ret, thresh = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    result_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(result_image, contours, -1, (0, 255, 0), 2)
    return result_image

def image_process_aux(frame, model):
    # imgsz=288 seems to be the lowest size the model can still reliably recognize
    results = model.predict(frame, verbose=True, imgsz=320)

    for r in results:
        annotator = Annotator(frame)

        boxes = r.boxes
        for box in boxes:
            b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
            c = box.cls
            annotator.box_label(b, model.names[int(c)] + " " + str(box.conf))

    return annotator.result()

start_execution()