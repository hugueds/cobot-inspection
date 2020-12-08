from enum import Enum

class PositionStatus(Enum):
    HOME = 0
    WAITING = 1
    POSE = 2
    AFTER_POSE = 3
    MOVING = 4
    NOT_FOUND = 5
    NOT_FOUND2 = 6
    NOT_DEFINED = -1
    NONE = None