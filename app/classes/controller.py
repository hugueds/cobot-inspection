import os
import cv2 as cv
from pathlib import Path
from threading import Thread
from datetime import datetime
from time import sleep
from enumerables import AppState
from classes.cobot import Cobot
from classes.camera import Camera

debug = True
class Controller:

    state = AppState.INITIAL      
    operation_result = 0 # 0 -> None, 1 -> OK, 2 -> NOT_OK
    total_programs = 0
    program_list = []
    parameter_list = []
    program = 0
    program_index = 0
    start_datetime = datetime.now()
    final_datetime = start_datetime
    pose_times = []
    component_unit = '0000'
    parameters_found = False
    manual_mode = False
    waiting_program = 0
    home_program = 99
    popid = '999999'
    model_name = '0000'

    def __init__(self, cobot: Cobot = None, camera: Camera = None) -> None:
        self.cobot = cobot
        self.camera = camera
        self.camera.start()

        if not debug:
            from classes.TFModel import TFModel
        # self.cobot.connect()
        # self.thread_cobot = Thread(target=self.update_cobot_interface, daemon=True)
        # self.cobot.start_read_thread()
        # self.thread_camera = Thread(target=self.update_camera_interface, daemon=True)
        # self.thread_cobot.start()
        # self.thread_camera.start()


    def new_product(self):
        self.start_datetime = datetime.now()
        self.operation_result = 0
        self.program_index = 0
        self.pose_times = []
        self.popid = '999999'        

    def load_parameters(self): # Fazer download do SQL
        self.parameter_list = self.get_parameter_list()
        self.program_list = [int(x[5:7]) for x in self.parameter_list] # carrega a lista de LTs e separa a lista de parametros
        self.total_programs = len(self.program_list)

    def get_parameter_list(self): # Simulate parameters
        return ['PV110011', 'PV110021', 'PV110031', 'PV110041', 'PV110051', 'PV110061'] # Example
    
    def modbus_update(self):
        while self.modbus_thread:
            self.cobot.update_interface()            
            sleep(1)

    def load_images(self):
        pass

    def next_pose(self):
        self.program_index += 1
        program = self.program_list[self.program_index]
        self.set_program(program)

    def set_program(self, program):
        self.program = program
        self.cobot.set_program(program)

    def set_state(self, state: AppState):
        self.state = state

    def update_cobot_interface(self):
        print('Starting Cobot Update Interface')
        while self.cobot.thread_running and self.cobot.modbus_client.is_socket_open:
            self.cobot.read_interface()
            self.cobot.update_interface(self.state)
            sleep(0.25)
        else:
            print('Update has ended')

    def update_camera_interface(self):
        print('Starting Camera Update Interface')
        while True:
            print('Camera Thread')
            sleep(1)
            pass
        
    def start_camera(self):
        self.camera.display = True
        self.camera.start()

    def clear_folder(self):
        folder = self.camera.image_folder
        files = os.listdir(folder)
        for f in files:
            os.remove(f'{folder}/{f}')

    def process_images(self):
        model = TFModel(self.model_name)
        folder = self.camera.image_folder
        for image_file in os.listdir(folder):
            if image_file.split('.')[-1] in ['png', 'jpg']:                
                image = cv.imread(f'{folder}/{image_file}')
                prediction = model.predict(image)
                edited_image = self.camera.write_results(image, prediction)                
                path = f'results/{self.popid}/{self.component_unit}/'
                Path(path).mkdir(parents=True, exist_ok=True)                
                path = f'{path}/{image_file}'
                cv.imwrite(path, edited_image)
                
        
    def save_image(self):
        parameter = self.parameter_list[self.program_index]
        filename = f'{self.program_index}_{parameter}'
        self.camera.save_image(filename)
        