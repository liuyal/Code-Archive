import numpy as np
import operator
from fer import FER
import cv2

cap = cv2.VideoCapture(0)

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
detector = FER()

while (True):
    ret, frame = cap.read()
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    faces = faceCascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
    results = detector.detect_emotions(image)

    for item in results:
        bounding_box = item["box"]
        emotions = sorted(item["emotions"].items(), key=operator.itemgetter(1))
        emotions.reverse()
        cv2.rectangle(frame, (bounding_box[0], bounding_box[1]), (bounding_box[0] + bounding_box[2], bounding_box[1] + bounding_box[3]), (0, 255, 0), 2)
        cv2.putText(frame, str(emotions[0]), (bounding_box[0] + 5, bounding_box[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow('frame', frame)

    print("Found {0} faces!".format(len(faces)))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
