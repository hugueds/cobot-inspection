from typing import List
from dataclasses import dataclass
from models.pose import Pose

@dataclass
class Component:
    number: int
    component_unit: str
    sequence: int
    poses: List[Pose]
