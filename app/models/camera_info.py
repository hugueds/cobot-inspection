from typing import List
from models.prediction import Prediction

class CameraInfo:

    state = ''
    cu = ''
    popid = ''
    parameter = ''
    program = ''
    program_index = ''
    total_programs = ''
    life_beat_cobot = ''
    manual = ''
    jobtime = ''
    uptime = ''
    message = ''
    final_result = ''
    parameters = []
    predictions: List[Prediction] = [] 
    results: List[bool] = []

    def __init__(self):
        pass
