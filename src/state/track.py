from state.state import State

class TrackState(State):
    def enter_state(self, context):
        print("entering tracking state")
        
    def execute(self, context):
        print("tracking")
        return
        
    def exit_state(self, context):
        print("exiting tracking state")
