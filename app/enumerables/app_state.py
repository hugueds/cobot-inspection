from enum import Enum, unique

@unique
class AppState(Enum):    
    INITIAL = 0
    WAITING_PARAMETER = 2
    WAITING_INPUT = 3
    PARAMETER_LOADED = 4
    MOVING_TO_WAITING = 5
    MOVING_TO_POSE = 6
    COLLECTING_IMAGES = 7
    PROCESSING_IMAGES = 8
    FINISHED = 9
    ERROR = -1
    DISCONNECTED = -2
    EMERGENCY_STOP = -3
    PARAMETER_NOT_FOUND = -4
