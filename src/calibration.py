from state import State, TrackerState

class CalibrationState(State):
    def enter_state(self, context):
        print("beginning calibration")
        
    def execute(self, context):
        print("calibrating device")
        context.change_state(TrackerState.IDLE)
        
    def exit_state(self, context):
        print("finished calibration")
