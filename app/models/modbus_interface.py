# C = Cobot
# A = Application

from enum import Enum


class ModbusInterface(Enum):

    start_byte = 128

    set_program = 0 # A-> 1, C-> 0
    next_pose = 0 # A-> 1, C-> 0

    program_state = 0 # A
    selected_program = 0 # A
    cobot_status = 0 # C-> running, stopper, waiting
    camera_status = 0 # A ->
    
    running_pose = 0 # number

    component_unit = 0 
    valve_port = 0
    variant = 0

    pose_seconds = 0
    job_seconds = 0



