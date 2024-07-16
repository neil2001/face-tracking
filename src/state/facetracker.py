import cv2
import mediapipe as mp
from picamera2 import Picamera2, Preview

from state.calibration import CalibrationState
from state.idle import IdleState
from state.track import TrackState
from state.state import TrackerState


from motor.motorcontroller import MotorController

# =========== Constants ============
TILT_MOTOR_PINS = [17,18,27,22]
TILT_GEAR_RATIO = 3
TILT_MAX_ANGLE = 90
TILT_MIN_ANGLE = -90

class FaceTracker:
    def __init__(self):
        self.state_map = {
            TrackerState.CALIBRATION: CalibrationState(),
            TrackerState.IDLE: IdleState(),
            TrackerState.TRACK: TrackState()
        }

        self.state = None
        self.state_class = None
        self.change_state(TrackerState.CALIBRATION)

        # Setting up camera
        self.camera = Picamera2()
        config = self.camera.create_preview_configuration()
        self.camera.configure(config)
        self.camera.start() # TODO: comment out to disable gui (maybe make this a cli arg)

        # Setting up motor
        self.tilt_motor = MotorController(
            pins=TILT_MOTOR_PINS, 
            gear_ratio=TILT_GEAR_RATIO, 
            min_angle=TILT_MIN_ANGLE, 
            max_angle=TILT_MAX_ANGLE
        )

        # Setting up mediapipe
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.mp_drawing = mp.solutions.drawing_utils

    def change_state(self, state):
        if self.state_class is not None:
            self.state_class.exit_state(self)
        self.state = state
        self.state_class = self.state_map[state]
        self.state_class.enter_state(self)

    def execute(self):
        self.state_class.execute(self)

    def cleanup(self):
        self.tilt_motor.reset()
        cv2.destroyAllWindows()

        
