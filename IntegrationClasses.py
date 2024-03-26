from abc import ABC, abstractmethod

# MAJOR QUESTION: How does the BME handle their loop of controlling the motors?
# Do we need to make our own timed frame-by-frame loop?

class AbstractState(ABC):
    @abstractmethod
    def ManualOverride(self):
        pass

    @abstractmethod
    def Execute(self):
        pass


class EvaluatingAnatomyState(AbstractState):
    def ManualOverride(self):
        return ManualState()

    def Execute(self):
        # LOGIC HERE WILL EVALUATE CAMERA FEED AND RETURN AN AIMING STATE
        return AimingState()


class AimingState(AbstractState):
    currentMotorX = 0
    currentMotorY = 0
    goalMotorX = 0
    goalMotorY = 0

    def ManualOverride(self):
        return ManualState()

    def Execute(self):
        # LOGIC HERE WILL MANIPULATE MOTORS TO THE DESIRED ANGLE, THEN RETURN A MOVING STATE
        # IF VALID FURTHER PATH IS FOUND
        return MovingState()


class MovingState(AbstractState):
    def ManualOverride(self):
        return ManualState()

    def Execute(self):
        # LOGIC HERE WILL MOVE THE LINEAR ACTUATOR FURTHER DOWN THE THROAT A SPECIFIED DISTANCE,
        # THEN RETURN AND EvaluatingAnatomyState
        return EvaluatingAnatomyState()


class RetractingState(AbstractState):
    def ManualOverride(self):
        return ManualState()

    def Execute(self):
        # LOGIC HERE WILL MOVE THE LINEAR ACTUATOR OUT OF THE THROAT A SPECIFIED DISTANCE,
        # THEN RETURN AND EvaluatingAnatomyState
        return EvaluatingAnatomyState()


class ManualState(AbstractState):
    def ManualOverride(self):
        return self

    def Execute(self):
        # LOGIC HERE WILL CONTROL THE LINEAR ACTUATOR AND MOTORS BASED OFF OF USER INPUT
        return self
