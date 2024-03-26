from abc import ABC, abstractmethod


class AbstractState(ABC):
    @abstractmethod
    def ManualOverride(self):
        pass

    @abstractmethod
    def EvaluateAnatomy(self):
        pass

    @abstractmethod
    def AimAtAnatomy(self):
        pass

    @abstractmethod
    def MoveDeeper(self):
        pass

    @abstractmethod
    def MoveBackwards(self):
        pass


class AimingState(AbstractState):
    def ManualOverride(self):
        pass

    def EvaluateAnatomy(self):
        pass

    def AimAtAnatomy(self):
        pass

    def MoveDeeper(self):
        pass

    def MoveBackwards(self):
        pass


class MovingState(AbstractState):
    def ManualOverride(self):
        pass

    def EvaluateAnatomy(self):
        pass

    def AimAtAnatomy(self):
        pass

    def MoveDeeper(self):
        pass

    def MoveBackwards(self):
        pass


class ManualState(AbstractState):
    def ManualOverride(self):
        pass

    def EvaluateAnatomy(self):
        pass

    def AimAtAnatomy(self):
        pass

    def MoveDeeper(self):
        pass

    def MoveBackwards(self):
        pass


class RetractingState(AbstractState):
    def ManualOverride(self):
        pass

    def EvaluateAnatomy(self):
        pass

    def SeekAnatomy(self):
        pass

    def MoveDeeper(self):
        pass

    def MoveBackwards(self):
        pass
