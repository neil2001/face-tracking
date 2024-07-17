import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.motor.byj_motor_control import BYJMotor
from src.motor.motorcontroller import MotorController

pins = [17,18,27,22]

# ================= initial_test ===============
# motor = BYJMotor()
# steps = 512*3
# motor.motor_run(pins, wait=0.001, steps=steps)

motor = MotorController(pins=pins, gear_ratio=3, min_angle=-90, max_angle=90)
motor.rotate(90, verbose=True)
motor.rotate(-180, verbose=True)
motor.rotate(90, verbose=True)
motor.rotate(45, verbose=True)
motor.rotate(-90, verbose=True)
motor.rotate(45, verbose=True)
motor.reset()
