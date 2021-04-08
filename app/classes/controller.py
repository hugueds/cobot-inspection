from enumerables import cobot_status
from enumerables.cobot_status import CobotStatus
import os
import json
import yaml
from typing import List
import cv2 as cv
from PIL import Image, ImageOps
from pathlib import Path
from threading import Thread
from datetime import datetime
from time import sleep
from enumerables import AppState
from classes.cobot import Cobot
from classes.camera import Camera
from models import CameraInfo, Prediction
import keyboard
from logger import logger

with open('config.yml') as f:
    config = yaml.safe_load(f)
    debug = config['controller']['debug_model']

# debug = False
# debug = True

if not debug:
    from classes.TFModel import TFModel

waiting_program = 0
home_program = 99
trigger_afterpose = 2


class Controller:

    state: AppState = AppState.INITIAL
    operation_result = 0  # 0 -> None, 1 -> OK, 2 -> NOT_OK
    total_programs = 0
    program_list = []
    parameter_list = []
    program = 0
    program_index = 0
    start_datetime = datetime.now()
    job_datetime = datetime.now()    
    pose_times = []
    parameters_found = False
    manual_mode = False
    auto_mode = False
    popid = ''
    component_unit = '0000'
    model_name = '0000'
    parameter = ''
    flag_new_product = False

    predictions: List[Prediction] = []
    results = []

    def __init__(self, cobot: Cobot = None, camera: Camera = None, debug=False) -> None:
        self.cobot = cobot if cobot else Cobot()
        self.camera = camera if camera else Camera()
        self.display_info()
        keyboard.on_press(self.on_event)
        self.debug = debug

    def connect_to_cobot(self):
        self.cobot.connect()
        self.thread_cobot = Thread(target=self.update_cobot_interface, daemon=True)
        self.thread_cobot.start()

    def start_camera(self):
        self.camera.start()        

    def display_info(self):
        self.thread_camera = Thread(target=self.update_camera_interface, args=(), daemon=True)
        self.thread_camera.start()

    def new_product(self):
        self.flag_new_product = False
        self.job_datetime = datetime.now()
        self.operation_result = 0
        self.program_index = 0
        self.parameter_list = []
        self.program_list = []
        self.pose_times = []        
        self.parameters_found = False
        self.total_programs = 0
        logger.info(f'New Popid in Station: {self.popid}')

    def load_parameters(self):  # Fazer download do SQL
        logger.info(f"Collecting parameters for POPID {self.popid}")
        self.parameter_list = self.get_parameter_list()        
        self.program_list = [int(x[5:7]) for x in self.parameter_list]
        self.total_programs = len(self.program_list)
        self.parameters_found = True
        self.parameter = self.parameter_list[0]

    def next_pose(self):
        self.program = self.program_list[self.program_index]
        self.parameter = self.parameter_list[self.program_index]
        self.set_program(self.program)
        self.program_index += 1
        logger.info(f'Moving to POSE: {self.program_index}/{self.total_programs}')
        logger.info(f'Running Program: {self.program}')

    def trigger_after_pose(self):
        self.cobot.set_trigger(trigger_afterpose)

    def set_program(self, program):
        self.program = program
        self.cobot.set_program(program)

    def set_waiting_program(self):
        self.program = waiting_program
        self.cobot.set_program(waiting_program)
        sleep(0.2)

    def set_state(self, state: AppState):
        self.state = state

    def update_cobot_interface(self):
        print('Starting Cobot Update Interface')
        while self.cobot.modbus_client.is_socket_open:
            self.cobot.read_interface()
            self.cobot.update_interface(self.state)
            sleep(0.2)
        else:
            print('Update Cobot Interface has stopped')

    def update_camera_interface(self):
        print('Starting Camera Update Interface')
        info = CameraInfo()
        while True:
            info.state = self.state.name
            info.cu = self.component_unit
            info.popid = self.popid
            info.parameter = self.parameter
            info.program = str(self.program)
            info.program_index = str(self.program_index)
            info.total_programs = str(self.total_programs)
            info.life_beat_cobot = str(self.cobot.life_beat)
            info.manual = str(self.manual_mode)
            info.jobtime = str((datetime.now() - self.job_datetime).seconds)
            info.uptime = str((datetime.now() - self.start_datetime).seconds)
            info.message = '[INFO] Message Test'
            info.parameters = self.parameter_list
            info.predictions = self.predictions
            info.results = self.results
            self.camera.display_info(info)

    def clear_folder(self):
        folder = self.camera.image_folder
        files = os.listdir(folder)
        for f in files:
            os.remove(f'{folder}/{f}')

    def process_images(self):
        self.predictions = []
        model = TFModel(self.model_name)
        folder = self.camera.image_folder
        for image_file in os.listdir(folder):
            if image_file.split('.')[-1] in ['png', 'jpg']:
                image = cv.imread(f'{folder}/{image_file}')
                prediction = model.predict(image)
                print(prediction.label, prediction.confidence)
                self.predictions.append(prediction)
                # edited_image = self.camera.create_subtitle(image, prediction)
                edited_image = image
                path = f'results/{self.popid}/{self.component_unit}/'
                Path(path).mkdir(parents=True, exist_ok=True)
                path = f'{path}/{image_file}'
                # cv.imwrite(path, edited_image)

    def save_image(self):
        sleep(0.2)
        parameter = self.parameter_list[self.program_index - 1]
        filename = f'{self.program_index}_{parameter}'
        self.camera.save_image(filename)

    def get_parameter_list(self, index=0, debug=False):  # Simulate parameters        
        with open('./data/mock_request.json') as f:
            file = json.load(f)
        self.popid = file['data'][index]['popid'] # Only in tests
        return file['data'][index]['lts']

    def classify(self):
        model = TFModel(self.model_name)
        image = self.camera.frame
        prediction = model.predict(image)
        print(f'{prediction.label}, {prediction.confidence}')

    def change_auto_man(self):
        self.manual_mode = not self.manual_mode
        if self.manual_mode:
            print('Set to manual')
            self.set_state(AppState.WAITING_INPUT)            
        else:
            print('Set to automatic')

    def generate_report(self):
        print('Generating Results...')
        self.results = []
        i = 0
        for p in self.parameter_list:
            prediction_label = self.predictions[i].label.split('_')[0]
            print('Parameter: ', p)
            print('Predicted: ', prediction_label)
            if p[4:] == prediction_label:
                self.results.append(True)
            elif prediction_label == 'NOK':
                self.results.append(False)
            else:
                self.results.append(False)
            i += 1

    def on_event(self, e: keyboard.KeyboardEvent):
        print(f'[EVENT] Key: {e.name} was pressed')
        if e.name == 'm':
            self.set_state(AppState.WAITING_INPUT)
            self.change_auto_man()
        elif e.name.isdigit():
            print('Set Manual Program ' + e.name)
            self.set_program(int(e.name))
        elif e.name == 't':
            self.trigger_after_pose()
        elif e.name == 's':
            print('Saving Screen Shot...')
            self.camera.save_screenshot(str(self.program))
        elif e.name == 'n':
            print('New Flag')
            self.flag_new_product = True
        elif e.name == 'z':
            print('Classifing Image...')
            self.classify()


    def get_cobot_status(self):
        return self.cobot.status

    def get_position_status(self):
        return self.cobot.position_status

    def check_cobot_status(self):         
        error = False
        if cobot_status == CobotStatus.EMERGENCY_STOPPED:
            logger.warning(f"Cobot is under Emergency Stop... Status: {self.cobot.status}")            
            error = True
        elif cobot_status != CobotStatus.RUNNING:
            logger.warning(f"Cobot is not ready for work... Status: {self.cobot.status}")
            error = True
        sleep(2)
        return error