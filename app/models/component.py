import csv
from dataclasses import dataclass
from os import name
from models.pose import Pose


@dataclass
class Component:
    
    number: str
    sequence: int

    def __init__(self, number, sequence, poses=[]) -> None:
        self.number = number
        self.sequence = sequence
        self.poses = [Pose(x) for x in poses]

    def load_from_file(self, path='data/poses'):
        with open(f'{path}/{self.number}.csv') as file:
            reader = csv.DictReader(file)
            for row in reader:
                seq = int(row['sequence'])
                hi = True if row['has_inspection'].lower == 'yes' else False
                speed = float(row['speed'])
                acc = float(row['acc'])
                joints = [float(row['j1']), float(row['j2']), float(row['j3']),
                          float(row['j4']), float(row['j5']), float(row['j6'])]

                pose = Pose(joints=joints, acc=acc, has_inspection=hi,
                            speed=speed, sequence=seq, name=row['name'])

                self.poses.append(pose)
