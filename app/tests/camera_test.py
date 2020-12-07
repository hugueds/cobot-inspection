import cv2 as cv
from classes import Camera, Controller
from time import sleep

def run():

    cam = Camera()
    ctrl = Controller(camera=cam)
    ctrl.start_camera()
    while True:
        msg = 'Collecting images'
                
        print(msg)
        sleep(1)

