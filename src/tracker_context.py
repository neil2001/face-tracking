from calibration import CalibrationState
from idle import IdleState
from state import TrackerState

class FaceTracker:
    def __init__(self):
        self.state_map = {
            TrackerState.CALIBRATION: CalibrationState(),
            TrackerState.IDLE: IdleState()
        }

        self.state = None
        self.state_class = None
        self.change_state(TrackerState.CALIBRATION)

    def change_state(self, state):
        if self.state_class is not None:
            self.state_class.exit_state(self)
        self.state = state
        self.state_class = self.state_map[state]
        self.state_class.enter_state(self)

    def execute(self):
        self.state_class.execute(self)
        
