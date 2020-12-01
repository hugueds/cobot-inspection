import cv2 as cv
from imutils.video.webcamvideostream import WebcamVideoStream

class Camera:

    src = 0
    frame = None
    window_name = 'Main'

    def __init__(self, config=None):
        self.stream = WebcamVideoStream(self.src, 'WebCam')

    def config_camera(config):
        pass

    def start(self):
        self.stream.start()
        self.frame = self.read()

    def pause(self):
        self.stream.stop()
        cv.destroyAllWindows()

    def read(self):
        self.frame = self.stream.read()
        return self.frame

    def display(self):
        cv.imshow(self.window_name, self.frame)    

    def classify(self, model): # should it be in this class?
        pass
