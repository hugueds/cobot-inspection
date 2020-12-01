from pymodbus.client.sync import ModbusTcpClient
from .modbus_interface import ModbusInterface

# 128-255 - General purpose 16 bit registers
# 258 - Disconnected=0, Confirm_safety=1, Booting=2, Power_off=3, Power_on=4, Idle=5, Backdrive=6, Running=7
# 261 - isSecurityStopped (coil)
# 262 - isEmergencyStopped (coil)

class Pose:
    def __init__(self, base, shoulder, elbow, wrist_1, wrist_2, wrist_3) -> None:
        self.base = base
        self.shoulder = shoulder
        self.elbow = elbow
        self.wrist_1 = wrist_1
        self.wrist_2 = wrist_2
        self.wrist_3 = wrist_3


class Cobot:

    status = 0
    selected_program = '00'
    modbus_client = None
    home_position = False
    wait_position = False
    pose_position = False
    pose_seconds = 0
    job_seconds = 0
    pose = Pose(0, 0, 0, 0, 0, 0)

    def __init__(self, ip, port=502) -> None:
        self.ip = ip
        self.port = port

    def connect(self):
        try:
            self.modbus_client = ModbusTcpClient(self.ip, self.port)
            print(f'Robot {self.ip} connected') # Replace with log
        except Exception as e:
            print(e)

    def disconnect(self):
        self.modbus_client.close()

    def set_program(self, program):
        self.selected_program = program
        self.__write_register(ModbusInterface.selected_program, self.selected_program)
        

    def move_to_waiting(self):
        self.wait_position = True
        self.selected_program = '00'
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
