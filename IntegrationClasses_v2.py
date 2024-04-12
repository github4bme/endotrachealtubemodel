from abc import ABC, abstractmethod
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
from time import sleep
import cv2

# MAJOR QUESTION: How does the BME handle their loop of controlling the motors?
# Do we need to make our own timed frame-by-frame loop?

class AbstractState(ABC):
    currentServoX = 90
    currentServoY = 90
    increment = 1
    waitTime = 0.5
    goalWindowWidth = 0.1
    camera = None
    model = None
    xServo = None
    yServo = None
    iterations = 0

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
            self.iterations = oldState.iterations
        else:
            self.currentServoX = 90
            self.currentServoY = 90
            self.increment = increment
            self.waitTime = waitTime
            self.goalWindowWidth = goalWindowWidth
            self.camera = camera
            self.model = model
            self.xServo = xServo
            self.yServo = yServo
            self.iterations = 0

    def ManualOverride(self):
        return ManualState()

    def Execute(self, deltaTime):
        # LOGIC HERE WILL EVALUATE CAMERA FEED AND RETURN AN AIMING STATE
        ret, frame = self.camera.read()

        results = self.model.predict(frame, verbose=False, imgsz=320)
        for r in results:
            annotator = Annotator(frame)

            boxes = r.boxes
            for box in boxes:
                b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
                c = box.cls
                annotator.box_label(b, self.model.names[int(c)] + " " + str(box.conf))
        cv2.imshow('frame', annotator.result())

        normBox = None
        for box in results[0].boxes:
            if box.cls == 0:
                normBox = box.xywhn

        if normBox is not None:
            centerX = normBox[0][0]
            centerY = normBox[0][1]
            stepX = 0
            stepY = 0

            if centerX > 0.5 + self.goalWindowWidth:
                stepX = self.increment
            elif centerX < 0.5 - self.goalWindowWidth:
                stepX = self.increment * -1.0
            else:
                print("MIDDLE")

            if centerY > 0.5 + self.goalWindowWidth:
                stepY = self.increment * -1.0
            elif centerY < 0.5 - self.goalWindowWidth:
                stepY = self.increment

            targetX = self.currentServoX + stepX
            if targetX >= 180:
                targetX = 180
            elif targetX <= 0:
                targetX = 0

            targetY = self.currentServoY + stepY
            if targetY >= 180:
                targetY = 180
            elif targetY <= 0:
                targetY = 0
            self.currentServoX = targetX
            self.currentServoY = targetY
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
        self.iterations = oldState.iterations

        self.goalServoX = targetX
        self.goalServoY = targetY

    def ManualOverride(self):
        return ManualState()

    def Execute(self, deltaTime):
        if self.iterations % 3 != 0 or True:
            self.xServo.angle = self.goalServoX
            self.yServo.angle = self.goalServoY
        self.iterations += 1
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
