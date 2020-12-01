import cv2 as cv
from imutils.video import VideoStream
from time import sleep

vs = VideoStream(src=0)
vs.start()

sleep(0.2)

while True:

    frame = vs.read()

    cv.imshow('Main', frame)

    key = cv.waitKey(10) & 0xFF

    if key == ord('q'):
        break

cv.destroyAllWindows()