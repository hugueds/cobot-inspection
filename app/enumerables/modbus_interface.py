from enum import Enum

# 128-255 - General purpose 16 bit hold registers
# 258 - Default cobot status Coil
# 261 - isSecurityStopped (coil)
# 262 - isEmergencyStopped (coil)

# C = Cobot Writes
# A = Application Writes

class ModbusInterface(Enum):    

    START_BYTE = 128
    LIFE_BEAT = 129             # A -> INCREASED BY 1
    START_TRIGGER = 130         # A -> 1 = Request, C -> 0 = Request ACK
    PROGRAM_STATE = 131         # A -> STATE
    SELECTED_PROGRAM = 132      # A -> 
    TOTAL_PROGRAMS = 133        # A -> 
    CAMERA_STATUS = 134         # A -> 0 = CLOSED, 1 = OPENED

    COMPONENT_UNIT = 135        # A ->
    VALVE_PORT = 136            # A ->
    VARIANT = 137               # A ->

    LIFE_BEAT_COBOT = 200   # C -> 0 - 65535 incremental
    POSITION_STATUS = 201   # C -> 0 - HOME, 1 - WAITING, 2 - POSE, 3 - MOVING, 4 - POSITION NOT FOUND
    MOVE_STATUS = 202       # C -> MOVING, STOPPED, WAITING
    RUNNING_PROGRAM = 203   # C ->
    POSE_BASE = 204         # A -> HOW TO SET PROPERLY
    POSE_SHOULDER = 205     # A -> HOW TO SET PROPERLY
    POSE_ELBOW = 206        # A -> HOW TO SET PROPERLY
    POSE_WRIST_1 = 207      # A -> HOW TO SET PROPERLY
    POSE_WRIST_2 = 208      # A -> HOW TO SET PROPERLY
    POSE_WRIST_3 = 209      # A -> HOW TO SET PROPERLY
    SET_POSE = 210          # A -> SET TO 1 C -> SET TO 0
    POSE_SECONDS = 211      # C ->
    JOB_SECONDS = 212       # C ->
    SPEED = 213             # C -> JOINT SPEED

    COBOT_STATUS = 258              # C -> Disconnected=0, Confirm_safety=1, Booting=2, Power_off=3, Power_on=4, Idle=5, Backdrive=6, Running=7
    IS_POWER_ON_ROBOT  = 260        # C -> 
    IS_SECURITY_STOPPED  = 261      # C ->
    IS_EMERGENCY_STOPPED  = 262     # C ->
    IS_TEACHING_PRESSED  = 263      # C ->
    BASE_JOINT  = 270               # C -> Angle in MRAD
    SHOULDER_JOINT = 271            # C ->
    ELBOW_JOINT = 272               # C ->
    WRIST_1_JOINT = 273             # C ->
    WRIST_2_JOINT = 274             # C ->
    WRIST_3_JOINT = 275             # C ->
    
