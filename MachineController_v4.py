from IntegrationClasses_v2 import *
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
from gpiozero import DigitalOutputDevice, Servo
import time
import cv2
from adafruit_servokit import ServoKit
import board
from adafruit_pca9685 import PCA9685

#deepsparse: https://docs.ultralytics.com/integrations/neural-magic/
kit = ServoKit(channels=16)
servo1 = kit.servo[0]
servo2 = kit.servo[1]

def start_execution():
    model = YOLO("runs/detect/train3/weights/best.pt")

    servo1.angle = 90
    servo2.angle = 90

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)  # set Width
    cap.set(4, 480)  # set Height
    lastFrameTime = None

    state = EvaluatingAnatomyState(None, 5, 0, 0.15, cap, model, servo1, servo2)

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
