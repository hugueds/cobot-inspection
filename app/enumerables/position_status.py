from enum import Enum

class PositionStatus(Enum):
    HOME = 0
    WAITING = 1
    POSE = 2
    MOVING = 3
    NOT_FOUND = 4
    NOT_FOUND2 = 5
    NOT_DEFINED = -1
    None = None