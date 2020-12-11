from datetime import datetime
from time import sleep
from logger import logger
from classes import Controller, controller
from enumerables import PositionStatus, AppState, CobotStatus
from models.result import Result


controller = Controller()

controller.connect_to_cobot()
controller.start_camera()

# check if robot is on running State
while controller.cobot.status != CobotStatus.RUNNING:
    logger.warning(f"Cobot is not ready for work... Status: {controller.cobot.status}")
    sleep(5)

while not controller.cobot.position_status == PositionStatus.HOME:
    print("Waiting Cobot reach the Home position")
    logger.info("Waiting Cobot reach in Home position")
    sleep(5)

controller.set_state(AppState.WAITING_INPUT)

while True:  # Put another condition

    # read a break condition / keyboard
    if controller.cobot.status != CobotStatus.RUNNING:
        logger.warning(f"Cobot is not ready for work... Status: {controller.cobot.status}")
        sleep(1)
        continue

    if controller.cobot.emergency == CobotStatus.EMERGENCY_STOPPED:
        logger.warning(f"Cobot is under Emergency Stop... Status: {controller.cobot.status}")
        sleep(5)
        continue

    if controller.manual_mode and controller.state == AppState.WAITING_INPUT:
        if datetime.now().second % 10 == 0:
            print("Cobot is on Manual mode")        
        continue

    if not controller.manual_mode and controller.state == AppState.WAITING_INPUT:    
        if datetime.now().second % 10 == 0:    
            print("Waiting a new Input...")
        if controller.flag_new_product:
            logger.info(f'New Popid in Station: {controller.popid}')
            start = False
            controller.new_product()
            controller.set_state(AppState.LOADING_PARAMETERS)

    elif controller.state == AppState.LOADING_PARAMETERS:
        logger.info(f"Collecting parameters for POPID {controller.popid}")
        controller.load_parameters()
        if controller.parameters_found:
            logger.info(f'Parameters for CU: {controller.component_unit} loaded')
            controller.set_state(AppState.PARAMETER_LOADED)
        else:
            logger.error(f'Parameters for POPID {controller.popid}, CU: {controller.component_unit} not found')
            controller.set_state(AppState.PARAMETER_NOT_FOUND)

    elif controller.state == AppState.PARAMETER_LOADED:
        controller.clear_folder()
        controller.set_waiting_program()
        sleep(1)
        controller.set_state(AppState.MOVING_TO_WAITING)

    elif controller.state == AppState.MOVING_TO_WAITING:
        print("Moving to Waiting...")
        if controller.cobot.position_status == PositionStatus.WAITING:
            if controller.program_index < controller.total_programs:
                controller.next_pose()
                logger.info(f'Moving to POSE: {controller.program_index}/{controller.total_programs}')
                logger.info(f'Running Program: {controller.program}')
                controller.set_state(AppState.MOVING_TO_POSE)
            else:
                controller.set_state(AppState.PROCESSING_IMAGES)

    elif controller.state == AppState.MOVING_TO_POSE:
        print("Moving to Pose...")
        if controller.cobot.position_status == PositionStatus.POSE:
            controller.set_state(AppState.COLLECTING_IMAGE)

    elif controller.state == AppState.COLLECTING_IMAGE:
        # print("Collecting Image")
        logger.info("Collecting and Saving Image")
        controller.save_image()
        controller.trigger_after_pose()
        controller.set_state(AppState.MOVING_TO_AFTER_POSE)

    elif controller.state == AppState.MOVING_TO_AFTER_POSE:
        print("Moving to after pose...")
        if controller.cobot.position_status == PositionStatus.AFTER_POSE:
            controller.pose_times.append(datetime.now())
            controller.set_waiting_program()
            controller.set_state(AppState.MOVING_TO_WAITING)

    elif controller.state == AppState.PROCESSING_IMAGES:
        logger.info('Start Processing the saved images')                
        controller.process_images()
        controller.operation_result = 1 if True else False
        controller.final_datetime = datetime.now()
        total_time = (controller.start_datetime - controller.final_datetime).seconds        
        logger.info(f"Total operation time: {total_time}")
        controller.set_state(AppState.WAITING_INPUT)

    sleep(0.25)


# def main():
#     pass

  


# if __name__ == "__main__":
#     try:
#         main()
#     except Exception as e:
#         logger.info("Finishing program due error")
#         logger.info("Last State")
#         logger.error(e)
