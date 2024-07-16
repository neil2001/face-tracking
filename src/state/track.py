import cv2
from state.state import State
from dataclasses import dataclass
import numpy as np

# ============ Constants =============
TILT_THRESHOLD = 0.15
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

    def move_camera(self, landmarks, context):
        centroid = self.compute_centroid(landmarks)

        y_diff = centroid.y - 0.5
        sign = -1 if y_diff < 0 else 1

        if abs(y_diff) < TILT_THRESHOLD:
            return
        
        context.tilt_motor.rotate(sign * 10)
        
    def execute(self, context):
        print("tracking")
        frame = context.camera.capture_array()
        
        # Convert the BGR image to RGB.
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # To improve performance, mark the image as not writeable.
        image.flags.writeable = False
        
        # Process the image and perform pose detection.
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
