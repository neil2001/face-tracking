import cv2
from state.state import State

class TrackState(State):
    def enter_state(self, context):
        print("entering tracking state")
        
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

            print("Pose landmarks", results.pose_landmarks)

        # Display the image.
        cv2.imshow('MediaPipe Pose', image)

        cv2.waitKey(5)
        return
        
    def exit_state(self, context):
        print("exiting tracking state")
