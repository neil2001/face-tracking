from state.state import State

class IdleState(State):
    def enter_state(self, context):
        print("entering idle state")
        
    def execute(self, context):
        print("idle")
        
    def exit_state(self, context):
        print("exiting idle state")
