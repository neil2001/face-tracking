import cv2

SENSITIVITY = 5
SCALE = 1.05

RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)

# detector = cv2.HOGDescriptor()
# detector.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def detect_and_bound(frame):
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    boxes = detector.detectMultiScale(
        gray_img, scaleFactor=SCALE, minNeighbors=SENSITIVITY, minSize=(75, 75)
    )
    # boxes, _ = detector.detectMultiScale(frame, winStride=(8,8))

    for x,y,w,h in boxes:
        x_o, y_o = (x + w//2, y + h//2)
        cv2.circle(frame, (x_o, y_o), 5, RED, -1)
        cv2.rectangle(frame, (x, y), (x + w, y + h), GREEN, 4)
    return


video_capture = cv2.VideoCapture(0)

while True:

    result, video_frame = video_capture.read()  # read frames from the video
    if result is False:
        break  # terminate the loop if the frame is not read successfully

    detect_and_bound(video_frame)  

    cv2.imshow("Face Detection Test", video_frame)  

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()

