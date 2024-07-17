import sys
import os
import concurrent.futures

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.motor.motorcontroller import MotorController

pins = [17,18,27,22]
motor = MotorController(pins=pins, gear_ratio=3, min_angle=-90, max_angle=90)

pins2 = [6,13,19,26]
motor2 = MotorController(pins=pins2, gear_ratio=3, min_angle=-90, max_angle=90)

motor.rotate(45)
motor.rotate(-90)
motor.rotate(45)

motor2.rotate(45)
motor2.rotate(-90)
motor2.rotate(45)

motor.reset()
motor2.reset()

# ~ with concurrent.futures.ThreadPoolExecutor() as executor:
    # ~ executor.submit(motor.rotate, 90)
    # ~ executor.submit(motor2.rotate, 90)

# ~ with concurrent.futures.ThreadPoolExecutor() as executor:
    # ~ executor.submit(motor.reset)
    # ~ executor.submit(motor2.reset)
