from datetime import datetime
from typing import List
from models.prediction import Prediction
from dataclasses import dataclass

@dataclass
class CameraInfo:
    state: str = ''
    component_unit: str = ''
    popid: str = ''
    parameter: str = ''
    program: str = ''
    program_index: int = 0
    total_programs: str = ''
    life_beat_cobot: int = 0
    manual: bool = False
    jobtime: datetime = datetime.now()
    uptime: datetime = datetime.now()
    message: str = ''
    final_result: str = ''
    parameters =  ''
    predictions = ''
    results = ''

    
