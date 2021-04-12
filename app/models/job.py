from datetime import datetime
from dataclasses import dataclass
from typing import List

@dataclass
class Job:
    popid: str
    component_unit: str
    size: int
    model_name: str
    parameter_list: List[str]
    start_time: datetime = datetime.now()