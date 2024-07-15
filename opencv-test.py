import cv2

SENSITIVITY = 5
SCALE = 1.05

RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)


face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def detect_faces(frame):
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(
        gray_img, scaleFactor=SCALE, minNeighbors=SENSITIVITY, minSize=(75, 75)
    )

    for x,y,w,h in faces:
        x_o, y_o = (x + w//2, y + h//2)
        cv2.circle(frame, (x_o, y_o), 5, RED, -1)
        cv2.rectangle(frame, (x, y), (x + w, y + h), GREEN, 4)
    return faces


video_capture = cv2.VideoCapture(0)

while True:

    result, video_frame = video_capture.read()  # read frames from the video
    if result is False:
        break  # terminate the loop if the frame is not read successfully

    faces = detect_faces(video_frame)  

    cv2.imshow("Face Detection Test", video_frame)  

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()

