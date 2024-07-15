from motor_control import BYJMotor

motor = BYJMotor()

pins = [17,18,27,22]

steps = 512*3

motor.motor_run(pins, wait=0.001, steps=steps)
