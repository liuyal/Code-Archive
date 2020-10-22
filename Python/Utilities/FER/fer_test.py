import cv2
import os
from fer import FER

img = cv2.imread("test_images" + os.sep + "face2.jpg")
detector = FER()
detector.detect_emotions(img)

emotion, score = detector.top_emotion(img)

print(emotion)
print(score)