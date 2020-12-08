from datetime import datetime
from time import sleep
from logger import logger
from classes import Cobot, Camera, Controller
from models.result import Result
from enumerables import PositionStatus, AppState, CobotStatus


def main():

    camera = Camera()
    cobot = Cobot()
    controller = Controller(cobot, camera)

    # cobot.read_interface()
    # cobot.update_interface(controller.state)

    controller.set_state(AppState.INITIAL)

    # check if robot is on running State
    while cobot.status != CobotStatus.RUNNING:
        logger.warning(f'Cobot is not ready for work... Status: {cobot.status}')
        sleep(5)

    # check if robot is in Home Position if not move there
    if not cobot.position_status == PositionStatus.HOME:
        controller.set_state(AppState.MOVING)
        controller.set_program(controller.home_program)

    while not cobot.position_status == PositionStatus.HOME:
        print('Waiting Cobot reach the Home position')
        logger.info('Waiting Cobot reach in Home position')
        sleep(5)

    controller.set_state(AppState.WAITING_INPUT)

    while True:  # Put another condition

        # read and write modbus
        # cobot.read_interface()
        # cobot.update_interface(controller.state)

        # read a break condition / keyboard
        if controller.cobot.status != CobotStatus.RUNNING:
            logger.warning(f'Cobot is not ready for work... Status: {cobot.status}')
            sleep(1)
            continue

        if controller.cobot.emergency == CobotStatus.EMERGENCY_STOPPED:            
            logger.warning(f'Cobot is under Emergency Stop... Status: {cobot.status}')
            sleep(5)
            continue

        if controller.manual_mode and controller.state == AppState.WAITING_INPUT:
            print('Cobot is on Manual mode')
            sleep(5)
            continue        

        if controller.state == AppState.WAITING_INPUT and not controller.manual_mode:
            # Change to manual
            print('Waiting a new Input...')
            start = 0
            if start:
                start = False
                controller.new_product()
                controller.set_state(AppState.WAITING_PARAMETER)

        # wait for a new product
        elif controller.state == AppState.WAITING_PARAMETER:            
            logger.info(f'Collecting parameters for POPID {controller.popid}')
            controller.load_parameters()
            if controller.parameters_found:
                controller.set_state(AppState.PARAMETER_LOADED)
            else:
                controller.set_state(AppState.PARAMETER_NOT_FOUND)

        elif controller.state == AppState.PARAMETER_LOADED:
            # move to identify CU model (optional)
            controller.clear_folder()
            controller.set_program(controller.waiting_program)  # move to waiting position
            controller.set_state(AppState.MOVING_TO_WAITING)

        elif controller.state == AppState.MOVING_TO_WAITING:
            print('Moving to Waiting...')
            if controller.cobot.position_status == PositionStatus.WAITING:
                if controller.program_index < controller.total_programs:                    
                    controller.next_pose()
                    controller.set_state(AppState.MOVING_TO_POSE)
                else:
                    controller.set_state(AppState.PROCESSING_IMAGES)

        elif controller.state == AppState.MOVING_TO_POSE:
            print('Moving to Pose...')
            if controller.cobot.position_status == PositionStatus.POSE:
                controller.set_state(AppState.COLLECTING_IMAGES)

        elif controller.state == AppState.COLLECTING_IMAGES:  
            print('Collecting Image')
            controller.save_image()
            controller.set_program(controller.waiting_program)
            controller.pose_times.append(datetime.now())
            controller.set_state(AppState.MOVING_TO_WAITING)

        elif controller.state == AppState.PROCESSING_IMAGES:
            # TODO: write a footer on picture describing the results            
            # TODO: save logger to database
            controller.process_images()
            controller.operation_result = 1 if True else False
            controller.final_datetime = datetime.now()
            total_time = (controller.start_datetime -
                          controller.final_datetime).seconds
            print('Total operation time: %d', total_time)
            logger.info('Total operation time: %d', total_time)            
            controller.set_state(AppState.WAITING_INPUT)

    logger.info('Finishing Program')  # In case of breaking


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.info('Finishing program due error')
        logger.error(e)
