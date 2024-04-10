from abc import ABC, abstractmethod
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
from time import sleep
import cv2

# MAJOR QUESTION: How does the BME handle their loop of controlling the motors?
# Do we need to make our own timed frame-by-frame loop?

class AbstractState(ABC):
    currentServoX = 0
    currentServoY = 0
    increment = 0
    waitTime = 0
    goalWindowWidth = 0
    camera = None
    model = None
    xServo = None
    yServo = None

    @abstractmethod
    def ManualOverride(self):
        pass

    @abstractmethod
    def Execute(self, deltaTime):
        pass


class EvaluatingAnatomyState(AbstractState):
    def __init__(self, oldState=None, increment=None, waitTime=None, goalWindowWidth = None,camera=None, model=None, xServo=None, yServo=None):
        if oldState is not None:
            self.currentServoX = oldState.currentServoX
            self.currentServoY = oldState.currentServoY
            self.increment = oldState.increment
            self.waitTime = oldState.waitTime
            self.goalWindowWidth = oldState.goalWindowWidth
            self.camera = oldState.camera
            self.model = oldState.model
            self.xServo = oldState.xServo
            self.yServo = oldState.yServo
        else:
            self.currentServoX = 0.0
            self.currentServoY = 0.0
            self.increment = increment
            self.waitTime = waitTime
            self.goalWindowWidth = goalWindowWidth
            self.camera = camera
            self.model = model
            self.xServo = xServo
            self.yServo = yServo

    def ManualOverride(self):
        return ManualState()

    def Execute(self, deltaTime):
        # LOGIC HERE WILL EVALUATE CAMERA FEED AND RETURN AN AIMING STATE
        ret, frame = self.camera.read()

        results = self.model.predict(frame, verbose=True, imgsz=288)
        for r in results:
            annotator = Annotator(frame)

            boxes = r.boxes
            for box in boxes:
                b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
                c = box.cls
                annotator.box_label(b, self.model.names[int(c)] + " " + str(box.conf))
        cv2.imshow('frame', annotator.result())

        normBoxes = results[0].boxes.xywhn
        if len(normBoxes) > 0:
            centerX = normBoxes[0][0]
            centerY = normBoxes[0][1]
            stepX = 0
            stepY = 0

            if centerX > 0.5 + self.goalWindowWidth:
                stepX = self.increment
            elif centerX < 0.5 - self.goalWindowWidth:
                stepX = self.increment * -1.0

            if centerY > 0.5 + self.goalWindowWidth:
                stepY = self.increment * -1.0
            elif centerY < 0.5 - self.goalWindowWidth:
                stepY = self.increment

            targetX = self.currentServoX + stepX
            if targetX >= 1.0:
                targetX = 1.0
            elif targetX <= -1.0:
                targetX = -1.0

            targetY = self.currentServoY + stepY
            if targetY >= 1.0:
                targetY = 1.0
            elif targetY <= -1.0:
                targetY = -1.0

            return AimingState(self, targetX, targetY)

        return AimingState(self, self.currentServoX, self.currentServoY)


class AimingState(AbstractState):
    goalServoX = 0
    goalServoY = 0

    def __init__(self, oldState, targetX, targetY):
        self.currentServoX = oldState.currentServoX
        self.currentServoY = oldState.currentServoY
        self.increment = oldState.increment
        self.waitTime = oldState.waitTime
        self.goalWindowWidth = oldState.goalWindowWidth
        self.camera = oldState.camera
        self.model = oldState.model
        self.xServo = oldState.xServo
        self.yServo = oldState.yServo

        self.goalServoX = targetX
        self.goalServoY = targetY

    def ManualOverride(self):
        return ManualState()

    def Execute(self, deltaTime):
        self.xServo.value = self.goalServoX
        self.yServo.value = self.goalServoY
        sleep(self.waitTime)
        return EvaluatingAnatomyState(self)


class MovingState(AbstractState):
    currentDistance = 0
    goalDistance = 0

    def ManualOverride(self):
        return ManualState()

    def Execute(self, deltaTime):
        # LOGIC HERE WILL MOVE THE LINEAR ACTUATOR FURTHER DOWN THE THROAT A SPECIFIED DISTANCE,
        # THEN RETURN AND EvaluatingAnatomyState
        return EvaluatingAnatomyState()


class RetractingState(AbstractState):
    currentDistance = 0
    goalDistance = 0

    def ManualOverride(self):
        return ManualState()

    def Execute(self, deltaTime):
        # LOGIC HERE WILL MOVE THE LINEAR ACTUATOR OUT OF THE THROAT A SPECIFIED DISTANCE,
        # THEN RETURN AND EvaluatingAnatomyState
        return EvaluatingAnatomyState()


class ManualState(AbstractState):
    def ManualOverride(self):
        return self

    def Execute(self, deltaTime):
        # LOGIC HERE WILL CONTROL THE LINEAR ACTUATOR AND MOTORS BASED OFF OF USER INPUT
        return self
