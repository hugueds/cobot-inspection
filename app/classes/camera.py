import yaml
from threading import Thread
from datetime import datetime
import cv2 as cv
from imutils.video.webcamvideostream import WebcamVideoStream
class Camera:

    src = 0
    frame = None
    window_name = 'Main'
    openned = False
    stopped = False
    frame_counter = 0

    def __init__(self, config_path='config.yml'):        
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        self.image_folder = config['camera']['folder']
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

    def save_image(self, filename=''):
        dt = datetime.now()
        file_name = dt.strftime(f"%Y%m%d_%h%M%s_{filename}")
        path = f'{self.image_folder}/{file_name}'
        cv.imwrite(path, self.frame)

    def display(self):
        self.openned = not self.openned
