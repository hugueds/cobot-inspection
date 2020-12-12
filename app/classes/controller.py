import os
import cv2 as cv
from pathlib import Path
from threading import Thread
from datetime import datetime
from time import sleep
from enumerables import AppState
from classes.cobot import Cobot
from classes.camera import Camera
from models import CameraInfo, prediction
import keyboard

debug = True

if not debug:
    from classes.TFModel import TFModel

waiting_program = 0
home_program = 99
trigger_afterpose = 2
class Controller:

    state = AppState.INITIAL      
    operation_result = 0 # 0 -> None, 1 -> OK, 2 -> NOT_OK
    total_programs = 0
    program_list = []
    parameter_list = []
    program = 0
    program_index = 0
    start_datetime = datetime.now()
    job_datetime = datetime.now()
    final_datetime = start_datetime
    pose_times = []
    component_unit = '0000'
    parameters_found = False
    manual_mode = False
    popid = '999999'
    model_name = '0000'
    parameter = ''
    flag_new_product = False
    predictions = []
    results = []


    def __init__(self, cobot: Cobot = None, camera: Camera = None) -> None:
        self.cobot = cobot if cobot else Cobot()
        self.camera = camera if camera else Camera()
        self.display_info()
        keyboard.on_press(self.on_event)

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
        self.job_datetime = datetime.now()
        self.operation_result = 0
        self.program_index = 0
        self.parameter_list = []
        self.program_list = []
        self.pose_times = []
        self.popid = '999999'        
        self.parameters_found = False
        self.total_programs = 0

    def load_parameters(self): # Fazer download do SQL
        self.parameter_list = self.get_parameter_list()
        self.program_list = [int(x[5:7]) for x in self.parameter_list] # carrega a lista de LTs e separa a lista de parametros
        self.total_programs = len(self.program_list)
        self.parameters_found = True
        self.parameter = self.parameter_list[0]    

    def load_images(self):
        pass

    def next_pose(self):
        self.program = self.program_list[self.program_index]
        self.parameter = self.parameter_list[self.program_index]
        self.set_program(self.program)
        self.program_index += 1

    def trigger_after_pose(self):
        self.cobot.set_trigger(2)

    def set_program(self, program):
        self.program = program
        self.cobot.set_program(program)

    def set_waiting_program(self):
        self.program = waiting_program
        self.cobot.set_program(waiting_program)

    def set_state(self, state: AppState):
        self.state = state

    def update_cobot_interface(self):
        print('Starting Cobot Update Interface')
        while self.cobot.modbus_client.is_socket_open:
            self.cobot.read_interface()
            self.cobot.update_interface(self.state)
            sleep(0.25)
        else:
            print('Update Cobot Interface has stopped')

    def update_camera_interface(self):
        print('Starting Camera Update Interface')
        info = CameraInfo()
        while True:
            info.state = self.state.name
            info.cu =  self.component_unit
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
            info.results = self.results
            info.parameters = self.parameter_list
            self.camera.display_info(info)        

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
        parameter = self.parameter_list[self.program_index - 1]
        filename = f'{self.program_index}_{parameter}'
        self.camera.save_image(filename)

    def get_parameter_list(self): # Simulate parameters
        return ['PV110011', 'PV110021', 'PV110031', 'PV110041', 'PV110051', 'PV110061'] # Example
        
    def classify(self):
        model = TFModel(self.model_name)
        image = self.camera.frame
        prediction = model.predict(image)
        print(f'{prediction.label}, {prediction.confidence}' )

    def on_event(self, e: keyboard.KeyboardEvent):
        print(f'button {e.name} pressed')
        if e.name == 'm':            
            self.change_auto_man()            
        elif e.name.isdigit():
            print('Set Program ' + e.name)
            self.set_program(int(e.name))
        elif e.name == 't':
            print('Trigger After Pose')
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

    def change_auto_man(self):
        self.manual_mode = not self.manual_mode
        if self.manual_mode:
            print('Set to manual')
            self.state == AppState.WAITING_INPUT
        else:
            print('Set to automatic')

    def generate_report(self):
        self.results = []
        i = 0
        for p in self.parameter_list:
            prediction_label = self.predictions[i].split('_')[0]
            print('Parameter: ', p)
            print('Predicted: ', prediction_label)
            if p[4:] == prediction_label:
                self.results.append(True)
            elif prediction_label == 'NOK':
                self.results.append(False)
            else:
                self.results.append(False)
            i += 1
   
