import sys
import os
import concurrent.futures

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.motor.motorcontroller import MotorController

pins = [17,18,27,22]
motor = MotorController(pins=pins, gear_ratio=3, min_angle=-90, max_angle=90)

pins2 = [17,18,27,22]
motor2 = MotorController(pins=pins2, gear_ratio=3, min_angle=-90, max_angle=90)

motor.rotate(90)
motor.rotate(-180)
motor.rotate(90)

motor2.rotate(90)
motor2.rotate(-180)
motor2.rotate(90)

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.submit(motor.rotate, 90)
    executor.submit(motor2.rotate, 90)
    executor.submit(motor.rotate, -90)
    executor.submit(motor2.rotate, -90)

