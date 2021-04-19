import os
import sys
import json
import yaml
import keyboard
import cv2 as cv
from typing import List
from pathlib import Path
from threading import Thread
from datetime import datetime
from time import sleep
from enumerables import AppState
from classes import Camera, Cobot
from models import CameraInfo, Prediction, Job
from enumerables import CobotStatus, OperationResult
from logger import logger

with open('config.yml') as f:
    config = yaml.safe_load(f)
    debug = config['controller']['debug_model']

if not debug:
    from classes import TFPredictor

PRG_WAITING = 0
PRG_HOME = 99
AFTERPOSE_TRIGGER = 2

class Controller:

    state: AppState = AppState.INITIAL
    operation_result: OperationResult = OperationResult.NONE
    job: Job = None
    total_programs: int = 0
    program_list = []
    parameter_list = []
    program = 0
    program_index = 0
    start_datetime = datetime.now()
    pose_times = []
    parameters_found = False
    manual_mode = False
    auto_mode = True
    parameter: str = ''
    flag_new_product = False
    predictions: List[Prediction] = []
    results = []
    popid = ''
    running = True

    def __init__(self, cobot: Cobot = None, camera: Camera = None, debug=False) -> None:
        self.cobot = cobot if cobot else Cobot()
        self.camera = camera if camera else Camera()
        self.tf_predictor = TFPredictor()
        self.display_info()
        self.debug = debug
        keyboard.on_press(self.on_event)  # Verificar se o Leitor pode vir aqui

    def connect_to_cobot(self):
        self.cobot.connect()
        self.thread_cobot = Thread(
            target=self.update_cobot_interface, daemon=True)
        self.thread_cobot.start()

    def start_camera(self):
        self.camera.start()

    def display_info(self):
        self.thread_camera = Thread(
            target=self.update_camera_interface, args=(), daemon=True)
        self.thread_camera.start()

    def new_product(self):
        self.flag_new_product = False
        self.operation_result = 0
        self.program_index = 0
        self.pose_times = []
        self.parameters_found = False
        self.total_programs = 0
        self.job = Job()
        logger.info(f'New Popid in Station: {self.popid}')

    def load_parameters(self):  # Fazer download do SQL
        # TODO Flag de loading para nao rodar duas vezes as consultas
        logger.info(f"Collecting parameters for POPID {self.popid}")
        self.job.parameter_list = self.get_parameter_list(debug=True, index=0)
        self.job.program_list = [int(x[5:7]) for x in self.parameter_list]
        self.total_programs = len(self.job.program_list)
        self.parameters_found = True
        self.parameter = self.parameter_list[0]
        # Load Model
        self.tf_predictor.load_single_model(self.job.component_unit)

    def next_pose(self):
        program = self.job.program_list[self.program_index]
        self.set_program(program)
        self.parameter = self.parameter_list[self.program_index]
        self.program_index += 1
        logger.info(
            f'Moving to POSE: {self.program_index}/{self.total_programs}')
        logger.info(f'Running Program: {self.program}')

    def trigger_after_pose(self):
        self.cobot.set_trigger(AFTERPOSE_TRIGGER)

    def set_program(self, program):
        self.program = program
        self.cobot.set_program(program)

    def set_waiting_program(self):
        self.program = PRG_WAITING
        self.cobot.set_program(PRG_WAITING)
        sleep(0.2)

    def set_state(self, state: AppState):
        self.state = state

    def update_cobot_interface(self):
        logger.info('Starting Cobot Data Update...')
        while self.running and self.cobot.modbus_client.is_socket_open:
            self.cobot.read_interface()
            self.cobot.update_interface(self.state)
            sleep(0.2)  # TODO Get via config
        else:
            logger.error('Cobot Data Update has stopped')

    def update_camera_interface(self):
        logger.info('Starting Camera Update Interface')
        info = CameraInfo()

        while self.running:
            info.state = self.state.name

            info.parameter = self.parameter
            info.program = str(self.program)
            info.program_index = str(self.program_index)
            info.total_programs = str(self.total_programs)
            info.life_beat_cobot = str(self.cobot.life_beat)
            info.manual = str(self.manual_mode)

            # Create a class with all kind of images
            info.message = '[INFO] Message Test'
            info.predictions = self.predictions
            info.results = self.results

            if self.job:
                info.cu = self.job.component_unit
                info.popid = self.job.popid
                info.parameters = self.job.parameter_list
                info.jobtime = str(
                    (datetime.now() - self.job.start_time).seconds)
                info.uptime = str(
                    (datetime.now() - self.start_datetime).seconds)

            self.camera.display_info(info)

    def clear_folder(self):
        folder = self.camera.image_folder
        files = os.listdir(folder)
        for f in files:
            os.remove(f'{folder}/{f}')

    def process_images(self):
        self.predictions = []
        self.tf_predictor.load_single_model(self.job.component_unit)
        folder = self.camera.image_folder
        for image_file in os.listdir(folder):
            if image_file.split('.')[-1] in ['png', 'jpg']:
                image = cv.imread(f'{folder}/{image_file}')
                prediction = self.tf_predictor.predict(image)
                logger.info(prediction.label, prediction.confidence)
                self.predictions.append(prediction)
                # edited_image = self.camera.create_subtitle(image, prediction)
                edited_image = image.copy()
                path = f'results/{self.popid}/{self.component_unit}/'
                Path(path).mkdir(parents=True, exist_ok=True)
                path = f'{path}/{image_file}'
                # cv.imwrite(path, edited_image)

    def save_image(self):
        sleep(0.2)
        parameter = self.job.parameter_list[self.program_index - 1]
        filename = f'{self.program_index}_{parameter}'
        self.camera.save_image(filename)

    def get_parameter_list(self, debug=False, index=0):  # Simulate parameters
        if debug:
            with open('./data/mock_request.json') as f:
                file = json.load(f)
            self.popid = file['data'][index]['popid']  # Only in tests
            return file['data'][index]['lts']

    def classify(self):
        model = self.tf_predictor.model
        image = self.camera.frame.copy()
        prediction = model.predict(image)
        logger.info(f'{prediction.label}, {prediction.confidence}')

    def change_auto_man(self):
        self.manual_mode = not self.manual_mode
        self.auto_mode = not self.auto_mode
        if self.manual_mode:
            logger.info('Set to Cobot to Manual mode')
            self.set_state(AppState.WAITING_INPUT)
        else:
            logger.info('Set Cobot to Automatic mode')

    def generate_report(self):
        logger.info('Generating Results...')
        self.results = []
        i = 0
        for p in self.parameter_list:
            prediction_label = self.predictions[i].label.split('_')[0]
            logger.info('Parameter: ', p)
            logger.info('Predicted: ', prediction_label)
            if p[4:] == prediction_label:
                self.results.append(True)
            elif prediction_label == 'NOK':
                self.results.append(False)
            else:
                self.results.append(False)
            i += 1

    def on_event(self, e: keyboard.KeyboardEvent):
        logger.info(f'[EVENT] Key: {e.name} was pressed')
        if e.name == 'm':
            self.set_state(AppState.WAITING_INPUT)
            self.change_auto_man()
        elif e.name == 'q':
            logger.info('[Command] Closing the camera and quiting application')            
            self.camera.pause()
            self.running = False
            exit(0)
        elif e.name.isdigit() and self.manual_mode:
            logger.info('[Command] Set Manual Program ' + e.name)
            self.set_program(int(e.name))
        elif e.name == 't':
            logger.info('[Command] Trigger After Pose')
            self.trigger_after_pose()
        elif e.name == 's':
            logger.info('[Command] Saving ScreenShot...')
            self.camera.save_screenshot(str(self.program))
        elif e.name == 'n':
            logger.info('[Command] New Flag')
            self.flag_new_product = True
        elif e.name == 'z':
            logger.info('[Command] Classifing Image...')
            self.classify()


    def get_cobot_status(self):
        return self.cobot.status

    def get_position_status(self):
        return self.cobot.position_status

    def check_cobot_status(self):
        status = False
        if self.cobot.status == CobotStatus.EMERGENCY_STOPPED:
            logger.warning(
                f"Cobot is under Emergency Stop... Status: {self.cobot.status}")
            status = True
        elif self.cobot.status != CobotStatus.RUNNING:
            logger.warning(
                f"Cobot is not ready for work... Status: {self.cobot.status}")
            status = True
        sleep(1)
        return status

    def wait_input(self):
        self.flag_new_product = False
