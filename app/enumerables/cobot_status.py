from enum import Enum

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
    NONE = None
