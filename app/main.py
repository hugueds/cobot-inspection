import os
from datetime import datetime
from time import sleep
import logging
import cv2 as cv
from controller import Controller
from models import Camera, Cobot
from enumerables import ModbusInterface, PositionStatus, AppState, CobotStatus


FORMAT = ('%(asctime)-15s %(threadName)-15s %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()


def main():            

    controller = Controller()
    camera = Camera()
    camera.start()

    cobot = Cobot()
    cobot.connect()

    cobot.read_interface()
    cobot.update_interface(controller.state)

    # check if robot is on running State
    while cobot.status != CobotStatus.RUNNING:
        # print('Cobot is not ready for work... Status: %d', cobot.status)
        log.warning(f'Cobot is not ready for work... Status: {cobot.status}')
        sleep(2)

    # check if robot is in Home Position if not move there
    if not cobot.position_status == PositionStatus.HOME:
        controller.state = AppState.MOVING
        home_program = 99
        cobot.set_program(home_program)

    while not cobot.position_status == PositionStatus.HOME:
        cobot.read_interface()
        print('Waiting Cobot in Home position')
        log.info('Waiting Cobot in Home position')
        sleep(5)

    controller.state = AppState.WAITING_PARAMETER

    while True: # Put another condition

        # read and write modbus
        cobot.read_interface()        
        cobot.update_interface(controller.state)
        
        # read a break condition / keyboard
        if cobot.status != CobotStatus.RUNNING:
            log.warning(f'Cobot is not ready for work... Status: {cobot.status}')
            sleep(1)
            continue

        if cobot.emergency == CobotStatus.EMERGENCY_STOPPED:
            # print('Emergency stop')
            log.warning(f'Cobot is under Emergency Stop... Status: {cobot.status}')
            sleep(5)
            continue                 
        
        # write information on camera window

        if controller.state == AppState.WAITING_INPUT:
            # Change to manual            
            controller.state = AppState.WAITING_PARAMETER

        # wait for a new product    
        elif controller.state == AppState.WAITING_PARAMETER:
            log.info('Collecting parameters for POPID')
            controller.load_parameters()                         
            if controller.parameters_found:
                controller.state = AppState.PARAMETER_LOADED
            else:
                controller.state = AppState.PARAMETER_NOT_FOUND
            
        elif controller.state == AppState.PARAMETER_LOADED:
            controller.operation_result = 0
            controller.program_index = 0
            controller.pose_times = []
            controller.start_datetime = datetime.now()
            # move to identify CU model (optional)
            # load keras model for the CU     
            # clear the pictures folder
            controller.program = 0
            cobot.set_program(controller.program)  # move to waiting position
            controller.state = AppState.MOVING_TO_WAITING
            
        elif controller.state == AppState.MOVING_TO_WAITING:
            if cobot.position_status == PositionStatus.WAITING:
                if controller.program_index < controller.total_programs:
                    program = controller.program_list[controller.program_index]
                    cobot.set_program(program)
                    controller.state = AppState.MOVING_TO_POSE        
                else:
                    controller.state = AppState.PROCESSING_IMAGES

        elif controller.state == AppState.MOVING_TO_POSE:
            if cobot.position_status == PositionStatus.POSE:
                controller.state = AppState.COLLECTING_IMAGES
        
        elif controller.state == AppState.COLLECTING_IMAGES:
            parameter = controller.parameter_list[controller.program_index]
            camera.read()
            camera.save_image(parameter)
            cobot.move_to_waiting()            
            controller.pose_times.append(datetime.now())
            controller.state = AppState.MOVING_TO_WAITING

        elif controller.state == AppState.PROCESSING_IMAGES:
            # Load all pictures inside a folder ... Load the model here?
            pictures = []            
            results = []

            for file in os.listdir('captures'):
                if file.split('.')[-1] in ['jpg', 'png']:
                    pictures.append(cv.imread(file))

            # Classify every picture and store into array
            for pic in pictures:                
                result = 0
                results.append(result)
                
            # compare each picture prediction to 0000XXXX - CU, Position, Port, Variant
            # if all pictures are correct, send an OK report
            # write a footer on picture describing the results
            # save all picures to a folder containing POPID and CU
            # save log to database
            controller.operation_result = 1 if True else False
            controller.final_datetime = datetime.now()
            total_time = (controller.start_datetime - controller.final_datetime).seconds
            # print('Total operation time: %d', total_time)
            log.info('Total operation time: %d', total_time)
            controller.program_index += 1                    
            controller.state = AppState.WAITING_INPUT                  

    log.info('Finishing Program')
        

if __name__ == '__main__':
    try:
        main()        
    except Exception as e:
        log.error('Finishing program due error')
        log.error(e)
