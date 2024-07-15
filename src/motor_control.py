# ========================== IMPORTS ======================
# Import the system modules needed to run rpiMotorlib.py
import sys
import time
import RPi.GPIO as GPIO

# ==================== CLASS SECTION ===============================

class StopMotorInterrupt(Exception):
    """ Stop the motor """
    pass

class BYJMotor(object):
    """class to control a 28BYJ-48 stepper motor with ULN2003 controller
    by a raspberry pi"""
    def __init__(self, name="BYJMotorX", motor_type="28BYJ"):
        self.name = name
        self.motor_type = motor_type
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.stop_motor = False

    def motor_stop(self):
        """ Stop the motor """
        self.stop_motor = True

    def motor_run(self, gpiopins, wait=.001, steps=512, ccwise=False,
                  verbose=False, steptype="half", initdelay=.001):
        """motor_run,  moves stepper motor based on 7 inputs

         (1) GPIOPins, type=list of ints 4 long, help="list of
         4 GPIO pins to connect to motor controller
         These are the four GPIO pins we will
         use to drive the stepper motor, in the order
         they are plugged into the controller board. So,
         GPIO 18 is plugged into Pin 1 on the stepper motor.
         (2) wait, type=float, default=0.001, help=Time to wait
         (in seconds) between steps.
         (3) steps, type=int, default=512, help=Number of steps sequence's
         to execute. Default is one revolution , 512 (for a 28BYJ-48)
         (4) counterclockwise, type=bool default=False
         help="Turn stepper counterclockwise"
         (5) verbose, type=bool  type=bool default=False
         help="Write pin actions",
         (6) steptype, type=string , default=half help= type of drive to
         step motor 3 options full step half step or wave drive
         where full = fullstep , half = half step , wave = wave drive.
         (7) initdelay, type=float, default=1mS, help= Intial delay after
         GPIO pins initialized but before motor is moved.

        """
        if steps < 0:
            print("Error BYJMotor 101: Step number must be greater than 0")
            quit()
                
        try:
            self.stop_motor = False
            for pin in gpiopins:
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, False)
            time.sleep(initdelay)

            # select step based on user input
            # Each step_sequence is a list containing GPIO pins that should be set to High
            if steptype == "half":  # half stepping.
                step_sequence = list(range(0, 8))
                step_sequence[0] = [gpiopins[0]]
                step_sequence[1] = [gpiopins[0], gpiopins[1]]
                step_sequence[2] = [gpiopins[1]]
                step_sequence[3] = [gpiopins[1], gpiopins[2]]
                step_sequence[4] = [gpiopins[2]]
                step_sequence[5] = [gpiopins[2], gpiopins[3]]
                step_sequence[6] = [gpiopins[3]]
                step_sequence[7] = [gpiopins[3], gpiopins[0]]
            elif steptype == "full":  # full stepping.
                step_sequence = list(range(0, 4))
                step_sequence[0] = [gpiopins[0], gpiopins[1]]
                step_sequence[1] = [gpiopins[1], gpiopins[2]]
                step_sequence[2] = [gpiopins[2], gpiopins[3]]
                step_sequence[3] = [gpiopins[0], gpiopins[3]]
            elif steptype == "wave":  # wave driving
                step_sequence = list(range(0, 4))
                step_sequence[0] = [gpiopins[0]]
                step_sequence[1] = [gpiopins[1]]
                step_sequence[2] = [gpiopins[2]]
                step_sequence[3] = [gpiopins[3]]
            else:
                print("Error: BYJMotor 102 : unknown step type : half, full or wave")
                print(steptype)
                quit()

            #  To run motor in reverse we flip the sequence order.
            if ccwise:
                step_sequence.reverse()

            def display_degree():
                """ display the degree value at end of run if verbose"""
                if self.motor_type == "28BYJ":
                    degree = 1.422222
                    print("Size of turn in degrees = {}".format(round(steps/degree, 2)))
                elif self.motor_type == "Nema":
                    degree = 7.2
                    print("Size of turn in degrees = {}".format(round(steps*degree, 2)))
                else:
                    # Unknown Motor type
                    print("Warning 201 : Unknown Motor Type : {}".format(self.motor_type))
                    print("Size of turn in degrees = N/A")

            def print_status(enabled_pins):
                """   Print status of pins."""
                if verbose:
                    print("Next Step: Step sequence remaining : {} ".format(steps_remaining))
                    for pin_print in gpiopins:
                        if pin_print in enabled_pins:
                            print("GPIO pin on {}".format(pin_print))
                        else:
                            print("GPIO pin off {}".format(pin_print))

            # Iterate through the pins turning them on and off.
            steps_remaining = steps
            while steps_remaining > 0:
                for pin_list in step_sequence:
                    for pin in gpiopins:
                        if self.stop_motor:
                            raise StopMotorInterrupt
                        else:
                            if pin in pin_list:
                                GPIO.output(pin, True)
                            else:
                                GPIO.output(pin, False)
                    print_status(pin_list)
                    time.sleep(wait)
                steps_remaining -= 1

        except KeyboardInterrupt:
            print("User Keyboard Interrupt : RpiMotorLib: ")
        except StopMotorInterrupt:
            print("Stop Motor Interrupt : RpiMotorLib: ")
        except Exception as motor_error:
            print(sys.exc_info()[0])
            print(motor_error)
            print("Error : BYJMotor 103 : RpiMotorLib  : Unexpected error:")
        else:
            # print report status if everything went well
            if verbose:
                print("\nRpiMotorLib, Motor Run finished, Details:.\n")
                print("Motor type = {}".format(self.motor_type))
                print("Initial delay = {}".format(initdelay))
                print("GPIO pins = {}".format(gpiopins))
                print("Wait time = {}".format(wait))
                print("Number of step sequences = {}".format(steps))
                print("Size of step sequence = {}".format(len(step_sequence)))
                print("Number of steps = {}".format(steps*len(step_sequence)))
                display_degree()
                print("Counter clockwise = {}".format(ccwise))
                print("Verbose  = {}".format(verbose))
                print("Steptype = {}".format(steptype))
        finally:
            # switch off pins at end
            for pin in gpiopins:
                GPIO.output(pin, False)
