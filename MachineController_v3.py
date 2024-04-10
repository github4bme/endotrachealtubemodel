from IntegrationClasses import *
from dark_filter import *
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
from gpiozero import DigitalOutputDevice, Servo
import time
import cv2

#deepsparse: https://docs.ultralytics.com/integrations/neural-magic/

def start_execution():
    model = YOLO("runs/detect/train3/weights/best.pt")

    servo_pin1 = 14
    servo_pin2 = 17
    servo1 = Servo(servo_pin1, min_pulse_width=0.0001, max_pulse_width=0.00275)
    servo2 = Servo(servo_pin2, min_pulse_width=0.0001, max_pulse_width=0.00275)

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)  # set Width
    cap.set(4, 480)  # set Height
    lastFrameTime = None

    state = EvaluatingAnatomyState(None, 0.1, 1, 0.1, cap, model, servo2, servo1)

    while (True):
        currentTime = time.time()
        if lastFrameTime is not None:
            dt = currentTime - lastFrameTime
        else:
            dt = 0
        lastFrameTime = currentTime

        state = state.Execute(dt)

        k = cv2.waitKey(30) & 0xff
        if k == 27:  # press 'ESC' to quit
            break

start_execution()