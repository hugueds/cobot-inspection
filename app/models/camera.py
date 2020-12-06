from datetime import datetime
import cv2 as cv
from imutils.video.webcamvideostream import WebcamVideoStream

image_folder = 'captures'

class Camera:

    src = 0
    frame = None
    window_name = 'Main'

    def __init__(self, config=None):
        self.stream = WebcamVideoStream(self.src, 'WebCam')

    def config_camera(self, config):
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

    def draw_on_image(self):
        pass

    def save_image(self, parameter=''):
        dt = datetime.now()
        file_name = dt.strftime("%Y-%m-%d_%h-%M-%s_" + parameter)
        path = image_folder + '/' + file_name
        cv.imwrite(file_name, self.frame)        

    def display(self):
        cv.imshow(self.window_name, self.frame)    
