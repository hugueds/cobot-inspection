from enum import Enum

class OperationResult(Enum):
    NONE = 0
    OK = 1
    NOT_OK = 2
    REWORKED = 3
    ABORTED = 4