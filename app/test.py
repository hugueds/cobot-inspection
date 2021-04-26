from classes.barcode_scanner import BarcodeScanner
from models.pose import Pose, Joint
from enumerables.app_state import AppState
from time import sleep
from classes import Controller, Cobot
import sys

c = Controller()

first_component = c.component_list[0]

c.start_job(first_component)



