from time import sleep
from models.camera_info import CameraInfo
import yaml
from threading import Thread
from datetime import datetime
import cv2 as cv
import numpy as np
from imutils.video.webcamvideostream import WebcamVideoStream
from models import Prediction, prediction

red = (0,0,255)
green = (0, 255, 0)
yellow = (0,200,200)
white = (255,255,255)
cyan = (255,255,0)

font = cv.FONT_HERSHEY_SIMPLEX
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

            while not self.stream.stopped:
                cut_frame = self.frame
                if not self.debug:
                    frame = self.stream.read()
                    cut_frame = frame
                    # cut_frame = frame[:, 70:-70] if use the teablemachine models

                self.frame = cut_frame
                flipped = cv.flip(cut_frame, 0)
                flipped = cv.flip(flipped, 1)                
                cv.imshow('main', flipped)
                self.frame_counter += 1

                if cv.waitKey(1) & 0xFF == ord('q'):
                    self.stopped = True

        except Exception as e:
            print(e)
            self.stream.stop()
            sleep(5)
            print('Trying to reopen the camera')            
            self.stream = WebcamVideoStream(self.src, 'WebCam').start()
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
        flipped = cv.flip(self.frame, 1)
        cv.imwrite(path, flipped)   

    def save_screenshot(self, filename=''):
        dt = datetime.now()
        date_str = dt.strftime('%Y%m%d_%H%M%S')
        filename =  f'{date_str}_{filename}'
        path = f'screenshots/{filename}.jpg'
        print('Saving File: ', filename)
        cv.imwrite(path, self.frame)  

    def create_subtitle(self, image: np.ndarray, prediction: Prediction):
        edited_image = image.copy()
        rows, _, _ = edited_image.shape
        edited_image[int(rows * 0.93):, :, :] = 0                
        text = f"LABEL: {prediction.label}, ACCURACY: {round( (prediction.confidence * 100), 2)}%"
        cv.putText(edited_image, text, (20, int(rows * 0.98)), font, 0.70, yellow, 2)
        return edited_image
        
        
    def save_result(self, image: np.ndarray, save_path, file):
        path = f'results/{save_path}/{file}'
        cv.imwrite(path, image)

    def display(self):
        self.openned = not self.openned

    def display_info(self, info: CameraInfo):        
        info_frame = np.zeros((720, 640, 3), dtype=np.uint8)        
        s = 10
        p = 20
        o = 25
        cv.putText(info_frame, 'POPID: ' + info.popid, (s, p+0*o), font, 0.7, white, 2)
        cv.putText(info_frame, 'STATE: ' + info.state, (s, p+1*o), font, 0.7, white, 2)
        cv.putText(info_frame, 'CU: ' + info.cu, (s, p+2*o), font, 0.7, white, 2)
        cv.putText(info_frame, 'PARAMETER: ' + info.parameter, (s, p+3*o), font, 0.7, white, 2)
        cv.putText(info_frame, 'PROGRAM: ' + info.program, (s, p+4*o), font, 0.7, white, 2)
        cv.putText(info_frame, f'POSE: {info.program_index} / {info.total_programs}' , (s, p+5*o), font, 0.7, white, 2)
        cv.putText(info_frame, 'MANUAL: ' + info.manual, (s, p+6*o), font, 0.7, white, 2)
        cv.putText(info_frame, 'LIFE BEAT: ' + info.life_beat_cobot, (s, p+7*o), font, 0.7, white, 2)        
        cv.putText(info_frame, 'JOB TIME: ' + info.jobtime, (s, p+8*o), font, 0.7, white, 2)
        cv.putText(info_frame, 'UPTIME TIME: ' + info.uptime, (s, p+9*o), font, 0.7, white, 2)
        cv.putText(info_frame, "LAST RESULTS: ", (s, p + 11*o ), font, 0.5, cyan, 2)
        
        if len(info.predictions) and len(info.results) and len(info.results) == len(info.predictions):
            for i in range(len(info.parameters)):                
                color = green if info.results[i] else red
                parameter = info.parameters[i]
                prediction = info.predictions[i].label
                cv.putText(info_frame, f"PARAMETER: {parameter}, RESULT: {prediction}", (s, p + (12+i)*o ), font, 0.6, color, 2)
        
        cv.imshow('info', info_frame)
        cv.waitKey(1) & 0xFF

        if not self.info_opened:
            cv.moveWindow('info', 0, 0)
            self.info_opened = True

