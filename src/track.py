from state import State

class TrackState(State):
    def enter_state(self, context):
        print("entering tracking state")
        
    def execute(self, context):
        
        return
        
    def exit_state(self, context):
        print("exiting tracking state")
