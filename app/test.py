from classes.barcode_scanner import BarcodeScanner
from models.pose import Pose, Joints
from enumerables.app_state import AppState
from time import sleep
from classes import Controller, Cobot
import sys

c = Controller()

c.connect_to_cobot()
c.set_home_pose()


