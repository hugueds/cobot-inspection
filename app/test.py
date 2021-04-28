from models.component import Component
from enumerables.position_status import PositionStatus
from enumerables.cobot_status import CobotStatus
from classes.barcode_scanner import BarcodeScanner
from models.pose import Pose, Joints
from enumerables.app_state import AppState
from time import sleep
from classes import Controller, Cobot


# c = Controller()

# c.popid = '999999'

# c.load_parameters()

# print(c.parameter_list)

# c.start_job('7500')

# co = Component('1', 0, [[1,2,3,4,5,6], [9,9,9,9,9,9]])
# print(co.poses[0].get_joint_list())