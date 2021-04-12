from typing import List
from models.prediction import Prediction
from dataclasses import dataclass

@dataclass
class CameraInfo:
    state: str
    component_unit: str
    popid: str
    parameter: str
    program: str
    program_index: str
    total_programs: str
    life_beat_cobot: str
    manual: str
    jobtime: str
    uptime: str
    message: str
    final_result: str
    parameters: List[str]
    predictions: List[Prediction]
    results: List[bool]

    
