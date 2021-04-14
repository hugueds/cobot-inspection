import argparse
from datetime import datetime
from time import sleep
from logger import logger
from classes import Controller
from enumerables import PositionStatus, AppState

parser = argparse.ArgumentParser()
parser.add_argument('--debug', default=False, action='store_true')
args = parser.parse_args()

debug = args.debug

controller = Controller(debug)

while True:       
    
    if not controller.check_cobot_status():        
        continue

    if controller.state == AppState.INITIAL:
        logger.log('Starting Program...')
        controller.connect_to_cobot()
        controller.start_camera()        
        controller.set_state(AppState.WAITING_INPUT)
        logger.log('Waiting for an Input...')
        sleep(1)

    if controller.manual_mode and controller.state == AppState.WAITING_INPUT:
        continue        

    if controller.state == AppState.WAITING_INPUT:
        if controller.flag_new_product: # Quem alterará esta Flag?
            controller.new_product()
            controller.set_state(AppState.LOADING_PARAMETERS)

    elif controller.state == AppState.LOADING_PARAMETERS:
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
        controller.set_state(AppState.MOVING_TO_WAITING)

    elif controller.state == AppState.MOVING_TO_WAITING:
        logger.info("Moving to Waiting...")
        if controller.get_position_status() == PositionStatus.WAITING:
            if controller.program_index < controller.total_programs:
                controller.next_pose()                
                controller.set_state(AppState.MOVING_TO_POSE)
            else:
                controller.set_state(AppState.PROCESSING_IMAGES)

    elif controller.state == AppState.MOVING_TO_POSE:
        logger.info("Moving to Pose...")
        if controller.get_position_status() == PositionStatus.POSE:
            controller.set_state(AppState.COLLECTING_IMAGE)

    elif controller.state == AppState.COLLECTING_IMAGE:        
        logger.info("Collecting and Saving Image")
        controller.save_image()
        controller.trigger_after_pose()
        controller.set_state(AppState.MOVING_TO_AFTER_POSE)

    elif controller.state == AppState.MOVING_TO_AFTER_POSE:
        logger.info("Moving to after pose...")
        if controller.cobot.position_status == PositionStatus.AFTER_POSE:
            controller.pose_times.append(datetime.now())
            controller.set_waiting_program()
            controller.set_state(AppState.MOVING_TO_WAITING)

    elif controller.state == AppState.PROCESSING_IMAGES:
        logger.info('Start Processing the saved images')                
        controller.process_images()
        controller.generate_report()
        controller.operation_result = 1 if True else False        
        total_time = (datetime.now() - controller.start_datetime).seconds        
        logger.info(f"Total operation time: {total_time}")
        controller.set_state(AppState.WAITING_INPUT)

    sleep(0.2)


# def main():
#     pass

  


# if __name__ == "__main__":
#     try:
#         main()
#     except Exception as e:
#         logger.info("Finishing program due error")
#         logger.info("Last State")
#         logger.error(e)
