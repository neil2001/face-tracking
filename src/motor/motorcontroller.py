from FaceTracker.src.motor.byj_motor_control import BYJMotor

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

    def rotate(self, angle):
        if self.current_angle == self.max_angle and angle > 0:
            return
        if self.current_angle == self.min_angle and angle < 0: 
            return

        next_angle = max(self.min_angle, min(self.max_angle, self.current_angle + angle))
        
        print("angle to move", angle)
        print("current angle", self.current_angle)
        print("next angle", next_angle)
        steps = int(self.gear_ratio * ((next_angle - self.current_angle) / FULL_ROTATION_DEGREES) * 512)
        print("steps to move", steps)
        self.motor.motor_run(self.pins, steps=abs(steps), ccwise=steps<0)
        self.current_angle = next_angle
        print("new_angle", self.current_angle)