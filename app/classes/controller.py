from models.pose import Joint, Pose
import os
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
from classes.barcode_scanner import BarcodeScanner
from classes.camera import Camera
from classes.cobot import Cobot
from classes.tf_predictor import TFPredictor        
from models import CameraInfo, Prediction, Job, Component, prediction
from enumerables import CobotStatus, OperationResult
from logger import logger
from database import DAO


HOME_JOINTS = [-1.582, -1.261, -2.269, -1.107, 1.588, 0]
HOME_JOINTS = [1000,1000,1000,1000,1000, 0]
PRG_WAITING = 0
PRG_HOME = 99
AFTERPOSE_TRIGGER = 2


class Controller:

    state: AppState = AppState.INITIAL
    operation_result: OperationResult = OperationResult.NONE
    job: Job = None
    dao: DAO()
    barcode = BarcodeScanner()
    cobot = Cobot()
    camera = Camera()
    tf_predictor = TFPredictor()    
    program_list = []
    parameter_list = []
    program = 0
    program_index = 0
    start_datetime = datetime.now()
    pose_times = []
    parameters_found = False
    manual_mode = False
    auto_mode = True
    flag_new_product = False
    predictions: List[Prediction] = []
    results = []
    popid = ''
    running = True
    popid_buffer = []
    component_list = []
    parameter: str = ''
    selected_component = ''
    component_index = 0
    pose_index = 0
    total_poses = 0
    param_index = 0
    total_param = 0

    def __init__(self, debug=False, config='config.yml') -> None:        
        self.debug = debug        
        self.load_component_list()
        self.barcode.start()        
        # self.display_info()
        keyboard.on_press(self.on_event)  # Verificar se o Leitor pode vir aqui

    def load_component_list(self):
        with open('data/component_list.yml') as f:
            logger.info('Loading Component List')
            component_list = yaml.safe_load(f)['component_list']
            component_list = sorted(component_list, key=lambda x: x['sequence'])
            self.component_list = component_list
            self.component_index = 0
            self.total_components = len(self.component_list)
            logger.info(f"Components Loaded: {[x['number'] for x in component_list]}")
            # Convert component_list to Class of Components

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
        self.operation_result = OperationResult.NONE
        self.param_index = 0        
        self.component_index = 0
        self.pose_times = []
        self.parameters_found = False        
        logger.info(f'New Popid in Station: {self.popid}')

    def load_parameters(self):  # Fazer download do SQL
        # TODO Flag de loading para nao rodar duas vezes as consultas
        logger.info(f"Collecting parameters for POPID {self.popid}")        
        # Print all Component Units Found on Database        
        self.job.parameter_list = self.get_parameter_list(self.popid, debug=True, index=0)
        # self.parameters_found = True
        # self.parameter = self.parameter_list[0]

    def start_job(self, component_unit):
        # TODO: Log the component loaded
        self.job = Job(self.popid, component_unit['number'])
        self.selected_component = list(filter(lambda x: x['number'] == component_unit['number'], self.component_list))[0]
        self.tf_predictor.load_single_model(component_unit['number'])
        self.job.status = 1 # Create a enumerable for jobs
        self.pose_index = 0
        self.param_index = 0
        self.predictions = []
        self.total_poses = len(self.selected_component['poses'])
        pose = self.get_pose(component_unit, self.pose_index)
        self.cobot.set_pose(pose)
        logger.info(f'Job for component {self.selected_component["number"]} started')
    
    def job_done(self):
        self.job.status = 2 # Create a enumerable for jobs
        # TODO: Create a report using the job results        
        if self.component_index < self.total_components - 1:
            self.component_index = self.component_index + 1
            component = self.component_list[self.component_index]
            self.start_job(component)

    def abort_job(self):
        self.job.status = 3 # Create a enumerable for jobs     

    def get_pose(self, component_unit, index) -> Pose:        
        pose_array = component_unit['poses'][index]        
        pose = Pose(pose_array['joints'], speed=pose_array['speed'], acc=pose_array['acc'])        
        return pose
        
    def check_inspection(self):
        index = self.component_index
        return self.component_list[index]['has_inspection']

    def next_pose(self): # NEW:
        self.param_result = False        
        if self.pose_index < self.total_poses - 1:
            self.pose_index = self.pose_index + 1
            logger.info(f'Moving to POSE: {self.pose_index}/{self.total_poses}')
            pose = self.get_pose(self, self.pose_index)
            self.cobot.set_pose(pose)

    def set_home_pose(self):
        home_pose = Pose(HOME_JOINTS, speed=1, acc=1)
        self.cobot.set_pose(home_pose)

    def set_state(self, state: AppState):
        self.state = state

    def update_cobot_interface(self):
        logger.info('Starting Cobot Data Update...')
        while self.running and self.cobot.modbus_client.is_socket_open:
            self.cobot.read_interface()
            self.cobot.update_interface(self.state.value)
            sleep(0.2)  # TODO Get via config
        else:
            logger.error('Cobot Data Update has stopped')

    def update_camera_interface(self):
        logger.info('Starting Camera Update Interface')
        info = CameraInfo()

        while self.running:
            # info.state = self.state.name
            # info.parameter = self.parameter
            # info.program = str(self.program)
            # info.program_index = str(self.program_index)
            # info.total_programs = str(self.total_programs)
            # info.life_beat_cobot = str(self.cobot.life_beat)
            # info.manual = str(self.manual_mode)

            # # Create a class with all kind of images
            # info.message = '[INFO] Message Test'
            # info.predictions = self.predictions
            # info.results = self.results

            if self.job:
                info.cu = self.job.component_unit
                info.popid = self.job.popid
                info.parameters = self.job.parameter_list
                jt = str((datetime.now() - self.job.start_time).seconds)
                info.jobtime = jt
                ut = str((datetime.now() - self.start_datetime).seconds)
                info.uptime = ut

            self.camera.display_info(info)

    def clear_folder(self):
        folder = self.camera.image_folder
        files = os.listdir(folder)
        for f in files:
            os.remove(f'{folder}/{f}')

    def process_image(self):        
        expected_pred = self.job.parameter_list[self.param_index]        
        prediction = self.classify()
        if prediction.label == expected_pred and prediction.confidence > 0.6: # Update confidence offset later
            self.param_index = self.param_index + 1
            self.param_result = True
            logger.info('Inspection Result OK')
        else:
            self.param_result = False
            logger.info('Inspection Result NOK')
            logger.info(f'Expected: {expected_pred}, Received: {prediction.label}')
            # path = f'results/{self.popid}/{self.component_unit}/' IF OK
            # Path(path).mkdir(parents=True, exist_ok=True)
            # path = f'{path}/{image_file}'
            # cv.imwrite(path, edited_image)

    def process_images_v1(self):
        self.predictions = []        
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

    def get_parameter_list(self, popid='', debug=False, index=0):  # Simulate parameters
        self.dao.get_parameters(popid)
        
        if debug:
            with open('./data/mock_request.json') as f:
                file = json.load(f)
            self.popid = file['data'][index]['popid']  # Only in tests
            return file['data'][index]['lts']

    def classify(self) -> Prediction:
        image = self.camera.frame.copy()
        prediction = self.tf_predictor.predict(image)
        logger.info(f'{prediction.label}, {prediction.confidence}')
        return prediction

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
        total_time = (datetime.now() - self.start_datetime).seconds        
        logger.info(f"Total operation time: {total_time}")

    def on_event(self, e: keyboard.KeyboardEvent):
        logger.info(f'[EVENT] Key: {e.name} was pressed')
        if e.name == 'm':
            self.set_state(AppState.WAITING_INPUT)
            self.change_auto_man()
        elif e.name == 'q':
            logger.info('[COMMAND] Closing the camera and quiting application')
            self.camera.stop()
            self.running = False
        elif e.name.isdigit() and self.manual_mode:
            logger.info('[COMMAND] Set Manual Program ' + e.name)
            self.set_program(int(e.name))
        elif e.name == 't':
            logger.info('[COMMAND] Trigger After Pose')
            self.trigger_after_pose()
        elif e.name == 's':
            logger.info('[COMMAND] Saving ScreenShot...')
            self.camera.save_screenshot(str(self.program))
        elif e.name == 'n':
            logger.info('[COMMAND] New Flag')
            self.flag_new_product = True
        elif e.name == 'z':
            logger.info('[COMMAND] Classifing Image...')
            self.classify()

    def get_cobot_status(self):
        return self.cobot.status

    def get_position_status(self):
        return self.cobot.position_status

    def check_cobot_status(self):
        status = True
        if self.cobot.status == CobotStatus.EMERGENCY_STOPPED.value:
            logger.warning(
                f"Cobot is under Emergency Stop... Status: {self.cobot.status}")
            status = False
        elif self.cobot.status != CobotStatus.RUNNING.value:
            logger.warning(
                f"Cobot is not ready for work... Status: {self.cobot.status}")
            status = False
        sleep(1)
        return status

    def wait_new_product(self):
        popid = self.barcode.get_buffer()
        if popid:
            self.popid = popid
            self.flag_new_product = True
