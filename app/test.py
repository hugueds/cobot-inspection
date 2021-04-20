from classes.barcode_scanner import BarcodeScanner
from models.pose import Pose
from enumerables.app_state import AppState
from time import sleep
from classes import Controller, Cobot
import sys

cb = Cobot(ip='10.8.66.212', port=502)
# cb.connect()

pose = Pose()


poses = [
    Pose(4693, 5567, 3881, 4856, 1542,  6279),
    Pose(3777, 4479, 4404, 5308, 1543,  6279),
    Pose(3827, 4248, 4330, 5616, 1447,  4310),
    Pose(3692, 4416, 4066, 5588, 1321,  4747),
    Pose(3989, 4712, 3817, 5219, 1610,  6060),
    Pose(4540, 4788, 3724, 5648, 1893,  1246),
    Pose(3757, 4699, 4081, 3872, 3728,  181),
]

index = 0
bc = BarcodeScanner()
bc.start()

while True:
    sleep(1)
    # print(index)
    # pose = poses[index]
    # cb.set_pose(pose)
    # index = index + 1 if index < len(poses) - 1 else 0
    # sleep(5)
