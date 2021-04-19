from datetime import datetime
from dataclasses import dataclass
from typing import List

@dataclass
class Job:
    popid: str = ''
    component_unit: str = ''
    size: int = 0
    model_name: str = ''
    parameter_list = []
    start_time: datetime = datetime.now()