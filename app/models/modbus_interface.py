# 128-255 - General purpose 16 bit registers
# 258 - Disconnected=0, Confirm_safety=1, Booting=2, Power_off=3, Power_on=4, Idle=5, Backdrive=6, Running=7
# 261 - isSecurityStopped (coil)
# 262 - isEmergencyStopped (coil)

# C = Cobot
# A = Application

from enum import Enum


class ModbusInterface(Enum):

    START_BYTE = 128

    START_TRIGGER = 129  # A-> 1, C-> 0    

    LIFE_BEAT = 130  # A -> INCREASED BY 1
    PROGRAM_STATE = 131  # A -> STATE
    SELECTED_PROGRAM = 132  # A ->
    TOTAL_PROGRAMS = 133  # A ->
    CAMERA_STATUS = 134  # A -> 0 = CLOSED, 1 = OPENED

    COMPONENT_UNIT = 135  # -> A ->
    VALVE_PORT = 136  # ->
    VARIANT = 137  # ->

    POSITION_STATUS = 200 # C -> 0 - HOME, 1 - WAITING, 2 - POSE, 3 - MOVING
    COBOT_STATUS = 201  # C-> RUNNING, STOPPER, WAITING
    RUNNING_PROGRAM = 202  # C ->
    POSE_1 = 203  # C -> HOW TO GET PROPERLY
    POSE_2 = 204  # C -> HOW TO GET PROPERLY
    POSE_3 = 205  # C -> HOW TO GET PROPERLY
    POSE_4 = 206  # C -> HOW TO GET PROPERLY
    POSE_5 = 207  # C -> HOW TO GET PROPERLY
    POSE_6 = 208  # C -> HOW TO GET PROPERLY
    POSE_SECONDS = 209  # C ->
    JOB_SECONDS = 210  # C ->
    SPEED = 211  # C ->
