from enum import Enum, unique

@unique
class AppState(Enum):    
    INITIAL = 0
    WAITING_INPUT = 1
    LOADING_PARAMETERS = 2
    PARAMETER_LOADED = 3
    MOVING_TO_WAITING = 4
    MOVING_TO_PRE_POSE = 5
    MOVING_TO_POSE = 6
    COLLECTING_IMAGE = 7
    PROCESSING_IMAGES = 8
    FINISHED = 9
    ERROR = -1
    DISCONNECTED = -2
    EMERGENCY_STOP = -3
    PARAMETER_NOT_FOUND = -4
    NONE = None
    
