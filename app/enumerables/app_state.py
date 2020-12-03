from enum import Enum, unique

@unique
class AppState(Enum):    
    INITIAL = 0
    WAITING_PARAMETER = 1
    PARAMETER_LOADED = 2
    MOVING_TO_WAITING = 3
    MOVING_TO_POSE = 4
    COLLECTING_IMAGES = 5
    PROCESSING_IMAGES = 6
    FINISHED = 7
    ERROR = -1
    DISCONNECTED = -2
    EMERGENCY_STOP = -3
    PARAMETER_NOT_FOUND = -4
