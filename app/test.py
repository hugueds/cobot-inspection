# from tests import test_cobot_interface_v1 as tci
from classes.TFModel import TFModel
from classes import Controller
import tests.test_cobot_interface_v2 as tci2
from tests import camera_test
import cv2
import os

if __name__ == '__main__':   
    # tci.run()    
    # tci2.run()
    # cobot_w_thread.run()
    # logger_test.run()
    # camera_test.run()

    c = Controller()
    m = TFModel('0000')
    
    for file in os.listdir('temp'):
        if file.split('.')[-1] in ['jpg', 'png']:
            i = cv2.imread(f'temp/{file}')
            r = m.predict(i)
            print(r)

    

