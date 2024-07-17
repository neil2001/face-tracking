import sys
import os
import concurrent.futures
import threading
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.motor.motorcontroller import MotorController

pins = [17,18,27,22]
motor = MotorController(pins=pins, gear_ratio=3, min_angle=-90, max_angle=90)

pins2 = [6,13,19,26]
motor2 = MotorController(pins=pins2, gear_ratio=3, min_angle=-90, max_angle=90)

# ~ motor_thread = threading.Thread(target=motor.rotate, args=(90,))
# ~ motor2_thread = threading.Thread(target=motor2.rotate, args=(90,))

# ~ motor_thread.start()
# ~ motor2_thread.start()

# ~ motor_thread.join()
# ~ motor2_thread.join()

# ~ motor2_thread2 = threading.Thread(target=motor2.rotate, args=(-90,True))
# ~ motor2_thread3 = threading.Thread(target=motor2.rotate, args=(45,True))

# ~ motor2_thread2.start()
# ~ time.sleep(2)
# ~ motor2_thread3.start()

# ~ motor2_thread2.join()
# ~ motor2_thread3.join()

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.submit(motor.reset)
    executor.submit(motor2.reset)
