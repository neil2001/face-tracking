from abc import ABC, abstractmethod
from enum import Enum, auto

class TrackerState(Enum):
    CALIBRATION = auto()
    TRACK = auto()
    IDLE = auto()

class State(ABC):
    @abstractmethod
    def enter_state(self, context):
        pass
        
    @abstractmethod
    def execute(self, context):
        pass
        
    @abstractmethod
    def exit_state(self, context):
        pass
