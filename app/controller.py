from datetime import datetime
from time import sleep
from models.cobot import Cobot
from enumerables import AppState
from threading import Thread

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
    component_unit = ''
    parameters_found = False
    manual_mode = False

    def __init__(self, cobot: Cobot = None) -> None:
        self.cobot = cobot        

    def start_modbus_thread(self, cobot: Cobot):
        self.modbus_thread = True
        self.thread = Thread(target=self.modbus_update,  daemon=True)
        self.thread.start()
        print('Start Reading Modbus')
    
    def stop_modbus_thread(self):
        self.modbus_thread = False

    def load_parameters(self):        
        self.parameter_list = self.get_parameter_list()
        self.program_list = [int(x[5:7]) for x in self.parameter_list] # carrega a lista de LTs e separa a lista de parametros
        self.total_programs = len(self.program_list) 
        self.program_index = 0

    def get_parameter_list(self): # Simulate parameters
        return ['PV110011', 'PV110021', 'PV110031', 'PV110041', 'PV110051', 'PV110061'] # Example
    
    def modbus_update(self):
        while self.modbus_thread:
            self.cobot.update_interface()
            sleep(1)

