from dataclasses import dataclass

@dataclass
class Prediction:
    label: str
    confidence: float