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

# create the servos that will be controlled
kit = ServoKit(channels=16)
servo1 = kit.servo[0]
servo2 = kit.servo[1]

def start_execution():
    # load most recent model
    model = YOLO("runs/detect/train3/weights/best.pt")

    # set servo angles to middle (arm pointing straight down)
    servo1.angle = 90
    servo2.angle = 90

    # set up camera frame capture
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)  # set Width
    cap.set(4, 480)  # set Height
    lastFrameTime = None

    # create machine state (will be updated in a state-machine-like flow)
    state = EvaluatingAnatomyState(None, 3, 0, 0.15, cap, model, servo1, servo2)

    while (True):
        # determine time elapsed since last frame evaluated
        # NOT used but could be useful for timekeeping during the procedure
        currentTime = time.time()
        if lastFrameTime is not None:
            dt = currentTime - lastFrameTime
        else:
            dt = 0
        lastFrameTime = currentTime

        # execute action on the machine based on its current state, and update the state
        state = state.Execute(dt)

        # manual override detection
        k = cv2.waitKey(30) & 0xff
        if k == 27:  # press 'ESC' to quit
            state = state.ManualOverride()

start_execution()
