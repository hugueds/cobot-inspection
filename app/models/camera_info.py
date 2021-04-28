from datetime import datetime
from models.pose import Pose
from typing import List
from models.prediction import Prediction
from dataclasses import dataclass


@dataclass
class CameraInfo:
    state: str = ''
    popid: str = ''
    component_unit: str = ''
    cobot_status: str = ''
    position_status: str = ''
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
    component_index = ''
    component_total = ''
    parameter_index = ''
    parameter_total = ''
    pose_index = ''
    pose_total = ''
