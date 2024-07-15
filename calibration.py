from state import State

class Calibration(State):
    def enter_state(self, context):
        print("beginning calibration")
        
    def execute(self, context):
        print("calibrating device")
        context.set_state(IdleState())
        
    def exit_state(self, context):
        print("finished calibration")
