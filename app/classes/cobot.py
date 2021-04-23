from logging import log
import yaml
from threading import Thread
from time import sleep
from pymodbus.client.sync import ModbusTcpClient
from models import Pose, Joint
from enumerables import ModbusInterface, PositionStatus, CobotStatus
from logger import logger

class Cobot:

    status = CobotStatus.NONE
    pose: Pose
    life_beat = -1
    move_status = 0
    modbus_client = None
    emergency = False
    selected_program = 0
    running_program = 0

    position_status = PositionStatus.NOT_DEFINED

    pose_seconds = 0
    job_seconds = 0
    thread_running = True    
    home_program = 99

    trigger = 0

    def __init__(self, config_path='config.yml', ip:str = '', port:int = 0) -> None:
        if ip != '' and port != 0:
            self.ip = ip
            self.port = port
        elif config_path != '':
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
            self.ip = config['cobot']['ip']
            self.port = int(config['cobot']['modbus_port'])        

    def connect(self):
        try:
            logger.info(f'Robot {self.ip} trying to connect')  # Replace with log
            self.modbus_client = ModbusTcpClient(self.ip, self.port)
        except Exception as e:
            return logger.error(e)

    def disconnect(self):
        self.modbus_client.close()    

    def set_program(self, program: int):
        self.selected_program = program
        self.__write_register(ModbusInterface.SELECTED_PROGRAM.value, program)
        self.set_trigger()

    def set_trigger(self, value=1):
        trigger = self.__read_register(ModbusInterface.START_TRIGGER.value)
        if value != trigger:
            self.trigger = value
            self.__write_register(ModbusInterface.START_TRIGGER.value, value)    

    def move_to_waiting(self):
        self.selected_program = 0
        self.set_program(self.selected_program)

    def get_pose(self) -> Pose:
        pose = Pose()
        first_address = ModbusInterface.BASE_JOINT.value
        pose_array = self.__read_register(first_address, 6)        
        pose.joint.base     = pose_array[0]
        pose.joint.shoulder = pose_array[1]
        pose.joint.elbow    = pose_array[2]
        pose.joint.wrist_1  = pose_array[3]
        pose.joint.wrist_2  = pose_array[4]
        pose.joint.wrist_3  = pose_array[5]
        self.pose.joint = pose.joint
        return pose

    def set_pose(self, pose: Pose):
        first_address = ModbusInterface.POSE_BASE.value
        joints = pose.get_joint_list()
        pose_array = [joints, pose.speed, pose.acc]
        self.__write_register(first_address, pose_array)
        self.__write_register(ModbusInterface.SET_POSE.value, 1)
    
    def __read_register(self, address: int, count=1):
        try:
            reg = self.modbus_client.read_holding_registers(address, count=count)
            return reg.registers
        except Exception as e:
            logger.error(e)            

    def __write_register(self, address: int, values):
        try:
            self.modbus_client.write_registers(address, values)
        except Exception as e:            
            logger.error(e)

    def read_interface(self):
        status = self.__read_register(ModbusInterface.COBOT_STATUS.value)
        position_status = self.__read_register(ModbusInterface.POSITION_STATUS.value)
        running_program = self.__read_register(ModbusInterface.RUNNING_PROGRAM.value)
        self.status = CobotStatus(0) if status is None else CobotStatus(status[0])
        self.position_status = PositionStatus(0) if position_status is None else PositionStatus(position_status[0])
        self.running_program = 0 if running_program is None else running_program
        # self.move_status = PositionStatus(self.__read_register(ModbusInterface.MOVE_STATUS.value))

    def update_interface(self, state: int):
        self.life_beat = self.life_beat + 1 if self.life_beat <= 1000 else 0
        self.__write_register(ModbusInterface.LIFE_BEAT.value, self.life_beat)
        self.__write_register(ModbusInterface.PROGRAM_STATE.value, state)
    
    def start_read_thread(self):         
        self.thread_running = True
        self.thread = Thread(target=self.read_interface_2, daemon=True)
        self.thread.start()

    def stop_thread(self):
        self.thread_running = False

    def read_interface_2(self):        
        while self.thread_running and self.modbus_client.is_socket_open:
            self.read_interface()
            sleep(1)
        else:
            logger.error('Modbus Interface Disconnected')
      




    def get_test(self):
        return self.__read_register(200, 6)
