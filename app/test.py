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

c.load_parameters()
