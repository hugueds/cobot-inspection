from dataclasses import dataclass
from datetime import datetime

@dataclass
class Result:
    approved: bool  = False
    label: str = 'not_defined'
    confidence: float = 0.0
    date_time: datetime = datetime.now()