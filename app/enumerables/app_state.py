from enum import Enum, unique

@unique
class AppState(Enum):    
    INITIAL = 0
    WAITING_INPUT = 1
    WAITING_PARAMETER = 2
    PARAMETER_LOADED = 3
    MOVING_TO_WAITING = 4
    MOVING_TO_POSE = 5
    COLLECTING_IMAGES = 6
    PROCESSING_IMAGES = 7
    FINISHED = 8
    ERROR = -1
    DISCONNECTED = -2
    EMERGENCY_STOP = -3
    PARAMETER_NOT_FOUND = -4
