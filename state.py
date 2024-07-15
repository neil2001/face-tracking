from abc import ABC, abstractmethod

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
