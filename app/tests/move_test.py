from enumerables.position_status import PositionStatus
from enumerables.cobot_status import CobotStatus
from classes.barcode_scanner import BarcodeScanner
from models.pose import Pose, Joints
from enumerables.app_state import AppState
from time import sleep
from classes import Controller, Cobot


c = Controller()

c.connect_to_cobot()
c.set_home_pose()

index = 0
poses = c.component_list[0]['poses']
total_poses = len(poses) 

while True:
    print(c.get_position_status())
    if c.get_position_status() == PositionStatus.POSE:
        p = Pose(poses[index]['joints'])
        c.cobot.set_pose(p)
        index = index + 1
        if index >= total_poses:
            index = 0    
            c.set_home_pose()
    sleep(1)
