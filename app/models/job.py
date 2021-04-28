from datetime import datetime
from dataclasses import dataclass


class Job:
    popid: str = ''
    component_unit: str = ''
    status: int = 0
    parameter_list: list = []
    results: list = []
    start_time: datetime = datetime.now()

    def __init__(self, popid, component_unit) -> None:
        self.popid = popid
        self.component_unit = component_unit