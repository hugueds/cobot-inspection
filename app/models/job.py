from datetime import datetime
from dataclasses import dataclass
from typing import List

@dataclass
class Job:
    popid: str = ''
    component_unit: str = ''
    parameter_list = []
    start_time: datetime = datetime.now()