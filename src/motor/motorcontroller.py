import threading
from motor.byj_motor_control import BYJMotor

STEPS_PER_ROTATION = 512
FULL_ROTATION_STEPS = 512*3
FULL_ROTATION_DEGREES = 360

class MotorController(object):
    def __init__(self, pins, gear_ratio, min_angle, max_angle):
        self.pins = pins
        self.motor = BYJMotor()
        self.gear_ratio = gear_ratio # 3:1
        self.current_angle = 0
        self.min_angle = min_angle
        self.max_angle = max_angle
        
        self.motor_thread = None
        self.lock = threading.Lock()
        
    def join_motor(self, verbose=False):
        self.motor_thread.join()
        steps_taken = self.motor.steps_taken
        angle_traversed = steps_taken / STEPS_PER_ROTATION / self.gear_ratio * FULL_ROTATION_DEGREES
        self.current_angle += angle_traversed
        if verbose:
            print("angle traversed", angle_traversed)
            print("new angle", self.current_angle)

    def rotate(self, angle, verbose=False, reset=False):
        self.motor.motor_stop() # DOES THIS WORK WITH MULTITHREADING?
        
        with self.lock:
                
            if self.motor_thread is not None:
                self.join_motor(verbose=verbose)
                    
            if reset:
                angle = -self.current_angle
            
            if self.current_angle == self.max_angle and angle > 0:
                print("max angle reached")
                return
            if self.current_angle == self.min_angle and angle < 0: 
                print("min angle reached")
                return

            next_angle = max(self.min_angle, min(self.max_angle, self.current_angle + angle))

            if verbose: 
                print("angle to move", angle)
                print("current angle", self.current_angle)
                print("next angle", next_angle)
            steps = int(self.gear_ratio * ((next_angle - self.current_angle) / FULL_ROTATION_DEGREES) * STEPS_PER_ROTATION)
            if verbose: 
                print("steps to move", steps)
                
            self.motor_thread = threading.Thread(
                target=self.motor.motor_run, 
                args=(self.pins,), 
                kwargs={
                    'steps': abs(steps), 
                    'ccwise':steps<0,
                    'initdelay': 0
                    }
                )
                
            self.motor_thread.start()
            
            # ~ steps_taken = self.motor.motor_run(self.pins, steps=abs(steps), ccwise=steps<0)
            
            # ~ angle_traversed = steps_taken / STEPS_PER_ROTATION / self.gear_ratio * FULL_ROTATION_DEGREES
            # ~ if verbose:
                # ~ print("angle traversed", angle_traversed)
                
            # ~ self.current_angle = next_angle
            
            # ~ if verbose:
                # ~ print("new_angle", self.current_angle)
                # ~ print("\n")

    def reset(self):
        # ~ with self.lock:
            # ~ angle = -self.current_angle
        self.rotate(None, reset=True)
        self.join_motor()
        with self.lock:
            print("end angle", self.current_angle)
            assert(self.current_angle == 0)
            
