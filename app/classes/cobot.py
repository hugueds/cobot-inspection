from enum import Enum
from threading import Thread
import yaml
from models import Pose
from pymodbus.client.sync import ModbusTcpClient
from enumerables import ModbusInterface, PositionStatus, AppState, CobotStatus
from time import sleep

class Cobot:

    life_beat = -1
    status = 0
    move_status = 0
    selected_program = 0
    running_program = 0
    modbus_client = None
    emergency = False

    position_status = PositionStatus.NOT_DEFINED

    pose_seconds = 0
    job_seconds = 0
    pose = Pose(0, 0, 0, 0, 0, 0)
    thread_running = False    
    home_program = 99

    def __init__(self, config_path='config.yml') -> None:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        self.ip = config['cobot']['ip']
        self.port = int(config['cobot']['modbus_port'])
        self.connect()

    def connect(self):
        try:
            print(f'Robot {self.ip} trying to connect')  # Replace with log
            self.modbus_client = ModbusTcpClient(self.ip, self.port)
        except Exception as e:
            return print('Cobot::connect::', str(e))

    def disconnect(self):
        self.modbus_client.close()

    def start_read_thread(self):         
        self.thread_running = True
        self.thread = Thread(target=self.read_interface_2, daemon=True)
        self.thread.start()

    def stop_thread(self):
        self.thread_running = False

    def set_program(self, program):
        self.selected_program = program
        self.__write_register(ModbusInterface.SELECTED_PROGRAM.value, program)
        trigger = self.__read_register(ModbusInterface.START_TRIGGER.value)
        if not trigger:
            self.__write_register(ModbusInterface.START_TRIGGER.value, 1)            
        
    def move_to_waiting(self):
        self.selected_program = 0
        self.set_program(self.selected_program)

    def move(self, move_type, pose):        
        if move_type == 'joint':
            pass
        elif move_type == 'linear':
            pass    

    def __read_register(self, address):
        try:
            reg = self.modbus_client.read_holding_registers(address, count=1)
            return reg.registers[0]
        except Exception as e:
            return print('Cobot::__read_register::', str(e))

    def __write_register(self, address, value):
        try:
            self.modbus_client.write_register(address, value)
        except Exception as e:
            print('Cobot::__write_register::', str(e))

    def read_interface(self):
        self.status = CobotStatus(self.__read_register(ModbusInterface.COBOT_STATUS.value))
        self.position_status = PositionStatus(self.__read_register(ModbusInterface.POSITION_STATUS.value))
        self.running_program = self.__read_register(ModbusInterface.RUNNING_PROGRAM.value)
        # self.move_status = PositionStatus(self.__read_register(ModbusInterface.MOVE_STATUS.value))

    def read_interface_2(self):        
        while self.thread_running and self.modbus_client.is_socket_open:
            self.read_interface()
            sleep(1)
        else:
            print('Disconnected')


    def update_interface(self, state: AppState):
        self.life_beat = self.life_beat + 1 if self.life_beat <= 1000 else 0
        self.__write_register(ModbusInterface.LIFE_BEAT.value, self.life_beat)
        self.__write_register(ModbusInterface.PROGRAM_STATE.value, state.value)
        self.__write_register(ModbusInterface.POSITION_STATUS.value, state.value)

        
    def next_pose(self):
        # write_register
        pass

    def previous_pose(self):
        # write_register
        pass