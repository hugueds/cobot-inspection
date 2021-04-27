from datetime import datetime
from dataclasses import dataclass
from typing import List

@dataclass
class Job:
    popid: str = ''
    component_unit: str = ''
    status: int = 0
    parameter_list = []
    results = []
    start_time: datetime = datetime.now()