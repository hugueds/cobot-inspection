from datetime import datetime
from models.pose import Pose
from typing import List
from models.prediction import Prediction
from dataclasses import dataclass


@dataclass
class CameraInfo:
    state: str = ''
    cobot_status: str = ''
    component_unit: str = ''
    popid: str = ''
    parameter: str = ''
    life_beat_cobot: str = ''
    manual: str = ''
    jobtime: str = '0'
    uptime: str = '0'
    message: str = ''
    final_result: str = ''
    parameters = ''
    predictions = ''
    results = ''
    joints = ''
