from enum import Enum

class PositionStatus(Enum):
    HOME = 0
    WAITING = 1
    POSE = 2
    MOVING = 3
    AFTER_POSE = 4
    NOT_FOUND = 5
    NOT_FOUND2 = 6
    NOT_DEFINED = -1
    NONE = None