from enum import Enum

class PositionStatus(Enum):
    HOME = 0
    WAITING = 1
    POSE = 2
    MOVING = 3    
    AFTER_POSE = 5
    NOT_FOUND = 6
    NOT_FOUND2 = 7
    NOT_DEFINED = -1
    NONE = None