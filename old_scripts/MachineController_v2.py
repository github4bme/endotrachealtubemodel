from IntegrationClasses import *
from gpiozero import DigitalOutputDevice, Servo
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
import time
import cv2


def start_execution():
    state = EvaluatingAnatomyState()

    # servo and motor config
    direction_pin_stepper = DigitalOutputDevice(21)
    pulse_pin_stepper = DigitalOutputDevice(20)
    cw_direction_stepper = 0
    ccw_direction_stepper = 1

    servo_pin1 = 14
    servo_pin2 = 17
    servo1 = Servo(servo_pin1, min_pulse_width=0.0001, max_pulse_width=0.00275)
    servo2 = Servo(servo_pin2, min_pulse_width=0.0001, max_pulse_width=0.00275)
    servo1.mid()
    servo2.mid()
    global_inc= 0.00000000000001
    print(global_inc)
    

    model = YOLO("best.pt")
    #model_aux = YOLO("runs/detect/train5/weights/best.pt")

    cap = cv2.VideoCapture(0)
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

        img, results = image_process_model(frame, model)

        normBoxes = results[0].boxes.xywhn
        if len(normBoxes) > 0:
            centerX = normBoxes[0][0]
            centerY = normBoxes[0][1]

            if centerY > 0.5:
                move_servo_right(servo1, global_inc)
                print("RIGHT")
            else:
                move_servo_left(servo1, global_inc)
                print("LEFT")

            print(centerY)

            if centerX > 0.5:
                move_servo_right(servo2, global_inc)
            else:
                move_servo_left(servo2, global_inc)
        #img = image_process_aux(frame, model_aux)
        #img = image_process_darkness(frame)
        cv2.imshow('frame', img)

        k = cv2.waitKey(30) & 0xff
        if k == 27:  # press 'ESC' to quit
            return_servo(servo1)
            return_servo(servo2)
            break

def image_process_model(frame, model):
    # imgsz=288 seems to be the lowest size the model can still reliably recognize
    results = model.predict(frame, verbose=True, imgsz=288)

    for r in results:
        annotator = Annotator(frame)

        boxes = r.boxes
        for box in boxes:
            b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
            c = box.cls
            annotator.box_label(b, model.names[int(c)] + " " + str(box.conf))

    return annotator.result(), results

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

def move_servo_right(servo, global_inc):
    inc = global_inc
    if servo.value + inc <= .8:
        servo.value += inc
    else:
        print("limit reached")

def move_servo_left(servo, global_inc):
    inc = -global_inc
    if servo.value + inc >= -.8:
        servo.value += inc
    else:
        print("limit reached")

def return_servo(servo):
    servo.mid()


start_execution()
