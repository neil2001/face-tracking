import cv2
import mediapipe as mp
# ~ import time
from picamera2 import Picamera2, Preview

picam = Picamera2()

config = picam.create_preview_configuration()
picam.configure(config)

# ~ picam.start_preview(Preview.QTGL)

picam.start()
# ~ time.sleep(10)
# ~ picam.capture_file("test-python.jpg")

# ~ picam.close()

# Initialize MediaPipe Pose.
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Initialize the webcam.
# ~ cap = cv2.VideoCapture(0)

# ~ while cap.isOpened():
    # ~ success, frame = cap.read()
    # ~ if not success:
        # ~ print("Ignoring empty camera frame.")
        # ~ continue
        
while True:
# ~ for i in range(10):
    frame = picam.capture_array()
        
    # Convert the BGR image to RGB.
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # To improve performance, mark the image as not writeable.
    image.flags.writeable = False
    
    # Process the image and perform pose detection.
    results = pose.process(image)
    
    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
        )
        
        print(results.pose_landmarks.landmark[0].x, results.pose_landmarks.landmark[0].y)

    # Display the image.
    cv2.imshow('MediaPipe Pose', image)

    # Break the loop if 'q' is pressed.
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows.
# ~ cap.release()
cv2.destroyAllWindows()
