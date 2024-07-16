import cv2
from state.state import State
from dataclasses import dataclass
import numpy as np
import concurrent.futures

# ============ Constants =============

PAN_THRESHOLD = 0.15
TILT_THRESHOLD = 0.15

FIXED_PAN_AMOUNT = 10
FIXED_TILT_AMOUNT = 10

# ====================================

# TODO: Move to util?
@dataclass
class Point:
    x: float
    y: float

class TrackState(State):
    def enter_state(self, context):
        print("entering tracking state")

    def compute_centroid(self, landmarks):
        x_vals = [l.x for l in landmarks]
        y_vals = [l.y for l in landmarks]

        return Point(np.mean(x_vals), np.mean(y_vals))
    
    # def compute_angle(self, loc, context):

    def move_camera(self, landmarks, context):
        centroid = self.compute_centroid(landmarks)

        x_angle, y_angle = 0, 0

        x_diff = centroid.x - 0.5
        if abs(x_diff) > PAN_THRESHOLD:
            x_angle = np.sign(x_diff) * FIXED_PAN_AMOUNT

        y_diff = centroid.y - 0.5
        if abs(y_diff) > TILT_THRESHOLD:
            y_angle = np.sign(y_diff) * FIXED_TILT_AMOUNT
            
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(context.pan_motor.rotate, x_angle)
            executor.submit(context.tilt_motor.rotate, y_angle)
        
    def execute(self, context):
        print("tracking")
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

            self.move_camera([nose_landmark], context)

        # Display the image.
        cv2.imshow('MediaPipe Pose', image)

        cv2.waitKey(5)
        return
        
    def exit_state(self, context):
        print("exiting tracking state")
