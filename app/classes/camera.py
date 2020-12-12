from time import sleep
from models.camera_info import CameraInfo
import yaml
from threading import Thread
from datetime import datetime
import cv2 as cv
import numpy as np
from imutils.video.webcamvideostream import WebcamVideoStream
from models import Prediction
class Camera:

    src = 0
    frame = np.zeros((480,640), dtype=np.uint8)
    window_name = 'Main'
    openned = False
    stopped = False
    frame_counter = 0
    info_opened = False

    def __init__(self, config_path='config.yml'):        
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        self.image_folder = config['camera']['folder']
        self.results_folder = config['camera']['results_folder']
        self.src = int(config['camera']['src'])
        self.debug = config['camera']['debug']
        if not self.debug:
            self.stream = WebcamVideoStream(self.src, 'WebCam').start()


    def config_camera(self, config='config.yml'):
        self.brightness = 0
        self.sharpness = 0
        self.hue = 0
        self.contrast = 0        

    def start(self):
        self.thread = Thread(target=self.update, args=(), daemon=True)
        self.thread.start()

    def update(self):
        try:        
            self.frame_counter = 0

            if not self.debug:
                self.frame = self.stream.read()

            while not self.stopped:
                if not self.debug:
                    self.frame = self.stream.read()

                flipped = cv.flip(self.frame, 0)
                cv.imshow('main', flipped)
                self.frame_counter += 1

                key = cv.waitKey(1) & 0xFF
                if key == ord('q'):
                    self.stopped = True

        except Exception as e:
            print(e)
            self.stream.stop()
            sleep(5)
            print('Trying to reopen the camera')
            self.start()

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
        date_str = dt.strftime('%Y%m%d_%H%M%S')
        filename =  f'{date_str}_{filename}'
        path = f'{self.image_folder}/{filename}.jpg'
        print('Saving File: ', filename)
        cv.imwrite(path, self.frame)   

    def save_screenshot(self, filename=''):
        dt = datetime.now()
        date_str = dt.strftime('%Y%m%d_%H%M%S')
        filename =  f'{date_str}_{filename}'
        path = f'screenshots/{filename}.jpg'
        print('Saving File: ', filename)
        cv.imwrite(path, self.frame)  

    def write_results(self, image: np.ndarray, prediction: Prediction):
        edited_image = image.copy()
        rows, _, _ = image.shape
        edited_image[int(rows * 0.93):, :, :] = 0
        font = cv.FONT_HERSHEY_SIMPLEX
        color = (0,200,200)
        text = f"LABEL: {prediction.label}, ACCURACY: {round( (prediction.confidence * 100), 2)}%"
        cv.putText(edited_image, text, (20, int(rows * 0.98)), font, 0.70, color, 2)
        return edited_image
        
    def save_result(self, image: np.ndarray, save_path, file):
        path = f'results/{save_path}/{file}'
        cv.imwrite(path, image)

    def display(self):
        self.openned = not self.openned

    def display_info(self, info: CameraInfo):

        info_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        font = cv.FONT_HERSHEY_SIMPLEX
        p = 20
        o = 25        
        cv.putText(info_frame, 'POPID: ' + info.popid, (10, p+0*o), font, 0.7, 255, 2)
        cv.putText(info_frame, 'STATE: ' + info.state, (10, p+1*o), font, 0.7, 255, 2)
        cv.putText(info_frame, 'CU: ' + info.cu, (10, p+2*o), font, 0.7, 255, 2)
        cv.putText(info_frame, 'PARAMETER: ' + info.parameter, (10, p+3*o), font, 0.7, 255, 2)
        cv.putText(info_frame, 'PROGRAM: ' + info.program, (10, p+4*o), font, 0.7, 255, 2)
        cv.putText(info_frame, f'POSE: {info.program_index} / {info.total_programs}' , (10, p+5*o), font, 0.7, 255, 2)
        cv.putText(info_frame, 'MANUAL: ' + info.manual, (10, p+6*o), font, 0.7, 255, 2)
        cv.putText(info_frame, 'LIFE BEAT: ' + info.life_beat_cobot, (10, p+7*o), font, 0.7, 255, 2)        
        cv.putText(info_frame, 'JOB TIME: ' + info.jobtime, (10, p+8*o), font, 0.7, 255, 2)
        cv.putText(info_frame, 'UPTIME TIME: ' + info.uptime, (10, p+9*o), font, 0.7, 255, 2)
        if len(info.results == info.parameters):
            for i in range(len(info.parameter)):
                color = (0,255,0) if info.parameter[i] == info.results[i] else (0,0,255)
                cv.putText(info_frame, info.parameter[i], (10, p+12*o + i * o), font, 0.7, color, 2)
        cv.imshow('info', info_frame)
        cv.waitKey(1) & 0xFF

        if not self.info_opened:
            cv.moveWindow('info', 0, 0)
            self.info_opened = True

