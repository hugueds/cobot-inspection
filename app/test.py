from enumerables.app_state import AppState
from tests import camera_test
from time import sleep
from classes import Controller, Camera

c = Controller()

# c.start_camera()

s = 0

while True:
    print('Main Thread')
    sleep(5)

