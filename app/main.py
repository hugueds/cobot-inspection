import os
from datetime import datetime
from time import sleep
import cv2 as cv
from classes import Cobot, Camera, Controller
from enumerables import PositionStatus, AppState, CobotStatus
from logger import logger


def main():

    camera = Camera()
    cobot = Cobot()
    controller = Controller(cobot, camera)

    cobot.read_interface()
    cobot.update_interface(controller.state)

    # check if robot is on running State
    while cobot.status != CobotStatus.RUNNING:
        logger.warning(f'Cobot is not ready for work... Status: {cobot.status}')
        sleep(5)

    # check if robot is in Home Position if not move there
    if not cobot.position_status == PositionStatus.HOME:
        controller.set_state(AppState.MOVING)
        cobot.set_program(cobot.home_program)

    while not cobot.position_status == PositionStatus.HOME:
        cobot.read_interface()
        print('Waiting Cobot in Home position')
        logger.info('Waiting Cobot in Home position')
        sleep(5)

    controller.set_state(AppState.WAITING_PARAMETER)

    while True:  # Put another condition

        # read and write modbus
        cobot.read_interface()
        cobot.update_interface(controller.state)

        # read a break condition / keyboard
        if cobot.status != CobotStatus.RUNNING:
            logger.warning(f'Cobot is not ready for work... Status: {cobot.status}')
            sleep(1)
            continue

        if cobot.emergency == CobotStatus.EMERGENCY_STOPPED:            
            logger.warning(f'Cobot is under Emergency Stop... Status: {cobot.status}')
            sleep(5)
            continue

        # write information on camera window

        if controller.state == AppState.WAITING_INPUT:
            # Change to manual
            controller.set_state(AppState.WAITING_PARAMETER)

        # wait for a new product
        elif controller.state == AppState.WAITING_PARAMETER:
            logger.info('Collecting parameters for POPID')
            controller.load_parameters()
            if controller.parameters_found:
                controller.set_state(AppState.PARAMETER_LOADED)
            else:
                controller.set_state(AppState.PARAMETER_NOT_FOUND)

        elif controller.state == AppState.PARAMETER_LOADED:
            controller.operation_result = 0
            controller.program_index = 0
            controller.pose_times = []
            controller.start_datetime = datetime.now()
            # move to identify CU model (optional)
            # load keras model for the CU
            # clear the pictures folder
            cobot.set_program(controller.program)  # move to waiting position
            controller.set_state(AppState.MOVING_TO_WAITING)

        elif controller.state == AppState.MOVING_TO_WAITING:
            if cobot.position_status == PositionStatus.WAITING:
                if controller.program_index < controller.total_programs:
                    program = controller.program_list[controller.program_index]
                    controller.set_program(program)
                    controller.set_state(AppState.MOVING_TO_POSE)
                else:
                    controller.set_state(AppState.PROCESSING_IMAGES)

        elif controller.state == AppState.MOVING_TO_POSE:
            if cobot.position_status == PositionStatus.POSE:
                controller.set_state(AppState.COLLECTING_IMAGES)

        elif controller.state == AppState.COLLECTING_IMAGES:
            parameter = controller.parameter_list[controller.program_index]
            camera.read()
            camera.save_image(parameter)
            cobot.move_to_waiting()
            controller.pose_times.append(datetime.now())
            controller.set_state(AppState.MOVING_TO_WAITING)

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
            # save logger to database
            controller.operation_result = 1 if True else False
            controller.final_datetime = datetime.now()
            total_time = (controller.start_datetime -
                          controller.final_datetime).seconds
            # print('Total operation time: %d', total_time)
            logger.info('Total operation time: %d', total_time)
            controller.program_index += 1
            controller.set_state(AppState.WAITING_INPUT)

    logger.info('Finishing Program')  # In case of breaking


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.info('Finishing program due error')
        logger.error(e)
