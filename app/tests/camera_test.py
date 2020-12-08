import cv2 as cv
from classes import Camera, Controller
from time import sleep

def run():

    cam = Camera()
    c = Controller(camera=cam)
    c.start_camera()
    c.load_parameters()

    c.process_images()

    # sleep(1)

    # for i in range(3):
    #     c.save_image()
    #     sleep(1)
    

