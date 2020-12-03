from enum import Enum


class ModbusInterface(Enum):

    # 128-255 - General purpose 16 bit registers
    # 258 - 
    # 261 - isSecurityStopped (coil)
    # 262 - isEmergencyStopped (coil)
    
    # C = Cobot
    # A = Application

    START_BYTE = 128

    LIFE_BEAT = 129  # A -> INCREASED BY 1
    START_TRIGGER = 130  # A-> 1, C-> 0    
    PROGRAM_STATE = 131  # A -> STATE
    SELECTED_PROGRAM = 132  # A ->
    TOTAL_PROGRAMS = 133  # A ->
    CAMERA_STATUS = 134  # A -> 0 = CLOSED, 1 = OPENED

    COMPONENT_UNIT = 135  # -> A ->
    VALVE_PORT = 136  # ->
    VARIANT = 137  # ->

    LIFE_BEAT_COBOT = 200
    POSITION_STATUS = 201 # C -> 0 - HOME, 1 - WAITING, 2 - POSE, 3 - MOVING, 4 - POSITION NOT FOUND
    MOVE_STATUS = 202  # C-> RUNNING, STOPPED, WAITING
    RUNNING_PROGRAM = 203  # C ->
    POSE_1 = 204  # C -> HOW TO GET PROPERLY
    POSE_2 = 205  # C -> HOW TO GET PROPERLY
    POSE_3 = 206  # C -> HOW TO GET PROPERLY
    POSE_4 = 207  # C -> HOW TO GET PROPERLY
    POSE_5 = 208  # C -> HOW TO GET PROPERLY
    POSE_6 = 209  # C -> HOW TO GET PROPERLY
    POSE_SECONDS = 210  # C ->
    JOB_SECONDS = 211  # C ->
    SPEED = 212  # C ->

    COBOT_STATUS = 258 # C -> Disconnected=0, Confirm_safety=1, Booting=2, Power_off=3, Power_on=4, Idle=5, Backdrive=6, Running=7
    IS_SECURITY_STOPPED  = 261 # C ->
    IS_EMERGENCY_STOPPED  = 262 # C ->
    
