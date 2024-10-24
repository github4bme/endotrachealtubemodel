from IntegrationClasses import *
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
from gpiozero import DigitalOutputDevice, Servo
import time
import cv2

#deepsparse: https://docs.ultralytics.com/integrations/neural-magic/

def start_execution():
    model = YOLO("runs/detect/train3/weights/best.pt")

    # set the pin values as hooked up with the Raspberry Pi's gpio pins to control the servos
    servo_pin1 = 14
    servo_pin2 = 17
    servo1 = Servo(servo_pin1, min_pulse_width=0.0001, max_pulse_width=0.00275)
    servo2 = Servo(servo_pin2, min_pulse_width=0.0001, max_pulse_width=0.00275)

    # create the camera feed capture (will allow pulling of individual frames)
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)  # set Width
    cap.set(4, 480)  # set Height
    lastFrameTime = None

    # create a new state
    # the current states in use are only Evaluating and Aiming, and executing each state in the below
    # while loop leads to the state flipping between the two as we try and aim at our target
    state = EvaluatingAnatomyState(None, 0.2, 1, 0.1, cap, model, servo2, servo1)

    while (True):
        # update the amount of time since the last frame of evaluation and aiming
        # (this is not currently used, but could be useful when
        currentTime = time.time()
        if lastFrameTime is not None:
            dt = currentTime - lastFrameTime
        else:
            dt = 0
        lastFrameTime = currentTime

        # call for the execution of the current state and update the state
        # the behavior corresponding to each state can be seen in Integration classes
        state = state.Execute(dt)

        k = cv2.waitKey(30) & 0xff
        if k == 27:  # press 'ESC' to quit
            break

start_execution()