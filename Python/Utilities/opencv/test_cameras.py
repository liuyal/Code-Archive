import cv2 as cv

def testDevice(source):
   cap = cv.VideoCapture(source)
   if cap is None or not cap.isOpened():
       print('Warning: unable to open video source: ', source)

for i in range(0,10):
    testDevice(i)  # no printout