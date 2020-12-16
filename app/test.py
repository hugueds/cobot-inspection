from enumerables.app_state import AppState
from tests import camera_test
from time import sleep
from classes import Controller, Camera

c = Controller()

c.load_parameters()
c.start_camera()

# s = 0

# sleep(1)

# # c.process_images()
# # c.generate_report()

while True:
    print('Main Thread')
    sleep(5)

