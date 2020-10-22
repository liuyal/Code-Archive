import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    color = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    cv2.imshow('frame',color)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()