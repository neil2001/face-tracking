import cv2
from state.state import State
from dataclasses import dataclass
import numpy as np
import concurrent.futures
from simple_pid import PID
import time

# ============ Constants =============

PAN_THRESHOLD = 0.15
TILT_THRESHOLD = 0.15

FIXED_PAN_AMOUNT = 10
FIXED_TILT_AMOUNT = 10

TOP_BOTTOM_ANGLE = 60
LEFT_RIGHT_ANGLE = 90

VELOCITY_BUFFER_SIZE = 2

# ====================================

# TODO: Move to util?
@dataclass
class Point:
    x: float
    y: float

class TrackState(State):
    def __init__(self):
        self.velocity = Point(0, 0)
        self.locations = np.zeros((VELOCITY_BUFFER_SIZE,2))
        self.times = np.zeros(VELOCITY_BUFFER_SIZE)
        self.index = 0

    def enter_state(self, context):
        print("entering tracking state")

    def compute_centroid(self, landmarks):
        x_vals = [l.x for l in landmarks]
        y_vals = [l.y for l in landmarks]

        return Point(np.mean(x_vals), np.mean(y_vals))
    
    # def compute_angle(self, loc, context):

    def update_velocity(self, centroid):
        self.locations[self.index] = [centroid.x, centroid.y]
        self.times[self.index] = time.time()

        roll_amt = VELOCITY_BUFFER_SIZE - self.index - 1
        times_rolled = np.roll(self.times, roll_amt)
        locations_rolled = np.roll(self.locations, roll_amt, axis=0)

        # ~ print("times", times_rolled % 1000)

        displacements = np.diff(locations_rolled, axis=0)
        time_diffs = np.diff(times_rolled)
        velocities = displacements / time_diffs[:, None]

        # ~ print("velocities", velocities)

        average_velocity = np.mean(velocities, axis=0)
        self.velocity.x = average_velocity[0]
        self.velocity.y = average_velocity[1]
        
        print("average velocity", average_velocity)

        self.index = (self.index + 1) % VELOCITY_BUFFER_SIZE


    def move_camera(self, centroid, context):
        x_angle, y_angle = 0, 0

        x_diff = centroid.x - 0.5
        if abs(x_diff) > PAN_THRESHOLD:
            # x_angle = np.sign(x_diff) * FIXED_PAN_AMOUNT
            x_angle = x_diff * LEFT_RIGHT_ANGLE * abs(self.velocity.x) * 10

        y_diff = centroid.y - 0.5
        if abs(y_diff) > TILT_THRESHOLD:
            # y_angle = np.sign(y_diff) * FIXED_TILT_AMOUNT
            y_angle = y_diff * TOP_BOTTOM_ANGLE * abs(self.velocity.y) * 10
            
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(context.pan_motor.rotate, x_angle)
            executor.submit(context.tilt_motor.rotate, y_angle)
        
    def execute(self, context):
        frame = context.camera.capture_array()
        
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False # performance optimization
        results = context.pose.process(image)
        
        # Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.pose_landmarks:
            context.mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                context.mp_pose.POSE_CONNECTIONS,
                context.mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                context.mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
            )

            nose_landmark = results.pose_landmarks.landmark[0]

            centroid = self.compute_centroid([nose_landmark])

            self.move_camera(centroid, context)
            self.update_velocity(centroid)

        # Display the image.
        cv2.imshow('MediaPipe Pose', image)

        cv2.waitKey(5)
        return
        
    def exit_state(self, context):
        print("exiting tracking state")
