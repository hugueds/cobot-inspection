from enum import Enum, unique

@unique
class State(Enum):    
    INITIAL = 0
    WAITING_PARAMETER = 1
    PARAMETER_LOADED = 1
    MOVING_TO_WAITING = 2
    MOVING_TO_POSE = 2
    COLLECTING_IMAGES = 3
    PROCESSING_IMAGES = 3
    FINISHED = 3
    ERROR = -1
    DISCONNECTED = -2
    EMERGENCY_STOP = -3
    PARAMETER_NOT_FOUND = -4
