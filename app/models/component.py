from dataclasses import dataclass
from typing import List
from models import Pose

@dataclass
class Component:
    number: str    
    sequence: int    

    def __init__(self, number, sequence, poses) -> None:
        self.number = number
        self.sequence = sequence
        self.poses = [Pose(x) for x in poses]