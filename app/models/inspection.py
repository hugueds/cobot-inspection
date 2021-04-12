from typing import List
from dataclasses import dataclass
from .pose import Pose

@dataclass
class Inspection: 
    cobot_pose: List[Pose]
    pose_order: int
    popid: str
    component_unit: str
    image_model: str



    