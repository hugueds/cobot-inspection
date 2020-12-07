from threading import Thread
from datetime import datetime
import cv2 as cv
from imutils.video.webcamvideostream import WebcamVideoStream

image_folder = 'captures'

class Camera:

    src = 0
    frame = None
    window_name = 'Main'
    openned = False
    stopped = False
    frame_counter = 0

    def __init__(self, config=None):
        self.stream = WebcamVideoStream(self.src, 'WebCam').start()

    def config_camera(self, config='config.yml'):
        pass

    def start(self):
        self.thread = Thread(target=self.update, args=(), daemon=True)
        self.thread.start()

    def update(self):

        self.frame = self.stream.read()
        self.frame_counter = 0

        print(self.frame.shape)

        while not self.stopped:

            self.frame_counter += 1
            self.frame = self.stream.read()

            cv.imshow('main', self.frame)

            key = cv.waitKey(1) & 0xFF

            if key == ord('q'):
                self.stopped = True

        cv.destroyAllWindows()

    def pause(self):
        self.stream.stop()
        cv.destroyAllWindows()

    def read(self):
        return self.frame        

    def draw_on_image(self):
        pass

    def save_image(self, parameter=''):
        dt = datetime.now()
        file_name = dt.strftime("%Y-%m-%d_%h-%M-%s_" + parameter)
        path = image_folder + '/' + file_name
        cv.imwrite(path, self.frame)

    def display(self):
        self.openned = not self.openned
