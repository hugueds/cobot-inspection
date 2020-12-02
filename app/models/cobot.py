from enum import Enum
import yaml
from pymodbus.client.sync import ModbusTcpClient
from .modbus_interface import ModbusInterface


class Pose:
    def __init__(self, base, shoulder, elbow, wrist_1, wrist_2, wrist_3) -> None:
        self.base = base
        self.shoulder = shoulder
        self.elbow = elbow
        self.wrist_1 = wrist_1
        self.wrist_2 = wrist_2
        self.wrist_3 = wrist_3

class PositionStatus(Enum):
    HOME = 0
    WAITING = 1
    POSE = 2
    MOVING = 3
    NOT_DEFINED = -1

class CobotStatus(Enum):
    DISCONNECTED = 0
    CONFIRM_SAFETY = 1
    BOOTING = 2
    POWER_OFF = 3
    POWER_ON = 4
    IDLE = 5
    BACKDRIVE = 6
    RUNNING = 7
    SECURE_STOPPED = 8
    EMERGENCY_STOPPED = 9


class Cobot:

    status = 0
    selected_program = 0
    running_program = 0
    modbus_client = None

    position_status = PositionStatus.NOT_DEFINED

    pose_seconds = 0
    job_seconds = 0
    pose = Pose(0, 0, 0, 0, 0, 0)

    def __init__(self, config_path='config.yml') -> None:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        self.ip = config['cobot']['ip']
        self.port = int(config['port'])

    def connect(self):
        try:
            self.modbus_client = ModbusTcpClient(self.ip, self.port)
            print(f'Robot {self.ip} connected')  # Replace with log
        except Exception as e:
            print(e)

    def disconnect(self):
        self.modbus_client.close()

    def set_program(self, program):
        self.selected_program = program
        self.__write_register(ModbusInterface.SELECTED_PROGRAM, program)
        trigger = self.__read_register(ModbusInterface.START_TRIGGER)
        if not trigger:
            self.__write_register(ModbusInterface.START_TRIGGER, 1)
            return
        print('Trigger is SET on Cobot') # debug
        

    def move_to_waiting(self):
        self.selected_program = 0
        self.set_program(self.selected_program)

    def next_pose(self):
        # write_register
        pass

    def previous_pose(self):
        # write_register
        pass

    def move(self, move_type, pose: Pose):
        if move_type == 'joint':
            pass
        elif move_type == 'linear':
            pass

    def __read_register(self, address):
        try:
            return self.modbus_client.read_holding_registers(address, count=1)
        except Exception as e:
            return print(e)

    def __write_register(self, address, value):
        try:
            self.modbus_client.write_register(address, value)
        except Exception as e:
            print(e)

    def read_interface(self):
        self.position_status = self.__read_register(ModbusInterface.POSITION_STATUS)

    def update_interface(self, life_beat, state):
        self.__write_register(ModbusInterface.LIFE_BEAT, life_beat)
        self.__write_register(ModbusInterface.POSITION_STATUS, state)
