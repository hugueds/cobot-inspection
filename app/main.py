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

logger.info('Starting Program...')
controller = Controller(debug)

while controller.running:

    if controller.state != AppState.INITIAL and not controller.check_cobot_status():
        continue

    elif controller.manual_mode and controller.state == AppState.WAITING_INPUT:
        continue

    if controller.state == AppState.INITIAL:
        logger.info('Initial State')
        controller.connect_to_cobot()
        controller.start_camera()
        controller.set_state(AppState.WAITING_INPUT)
        logger.info('Waiting for an Input...')
        sleep(1)

    elif controller.state == AppState.WAITING_INPUT:
        controller.wait_new_product()
        if controller.flag_new_product:
            controller.new_product()
            controller.set_state(AppState.LOADING_PARAMETERS)

    elif controller.state == AppState.LOADING_PARAMETERS:
        controller.load_parameters()  # Check the parameters for ALL component units
        if controller.parameters_found:
            logger.info(f'Parameters loaded')
            controller.set_state(AppState.PARAMETER_LOADED)
        else:
            logger.error(f'Parameters not found')
            controller.set_state(AppState.PARAMETER_NOT_FOUND)

    elif controller.state == AppState.PARAMETER_LOADED:  # NEW
        first_component = controller.component_list[0]
        controller.start_job(first_component)
        controller.set_state(AppState.MOVING_TO_WAITING)

    elif controller.state == AppState.MOVING_TO_WAITING:
        logger.info("Moving to Waiting...")                  

        if controller.get_position_status() == PositionStatus.POSE:            
            # Check the index of the Pose to ensure is not empty
            if controller.component_index >= controller.total_components - 1:
                controller.set_state(AppState.FINISHED)        
            elif controller.total_poses > 0:
                controller.next_pose()
                controller.set_state(AppState.MOVING_TO_POSE)
            else:
                # Verify the amount of jobs remaining
                controller.job_done()

    elif controller.state == AppState.MOVING_TO_POSE:
        logger.info("Moving to Pose...")
        index = 0
        if controller.get_position_status() == PositionStatus.POSE:
            # Check the index of the Pose            
            if controller.pose_index > controller.total_poses:
                controller.job_done()
                controller.set_state(AppState.MOVING_TO_WAITING)
            else:
                if controller.component_list[index]['has_inspection']: # If current pose has a parameter por picture
                    controller.set_state(AppState.COLLECTING_IMAGE)
                else:
                    controller.next_pose()
                    sleep(0.2)
                    controller.set_state(AppState.MOVING_TO_POSE)

    elif controller.state == AppState.FINISHED:
        logger.info('All Component Jobs finished, Returning to Home Position')
        # Generate Report
        # Clear all variables
        # print all next popids in the queue
        controller.set_state(AppState.WAITING_INPUT)

    # elif controller.state == AppState.PARAMETER_LOADED: # OLD
    #     controller.clear_folder()
    #     controller.set_waiting_program()
    #     controller.set_state(AppState.MOVING_TO_WAITING)

    # elif controller.state == AppState.MOVING_TO_WAITING:
    #     logger.info("Moving to Waiting...")
    #     if controller.get_position_status() == PositionStatus.WAITING:
    #         if controller.program_index < controller.total_programs:
    #             controller.next_pose()
    #             controller.set_state(AppState.MOVING_TO_POSE)
    #         else:
    #             controller.set_state(AppState.PROCESSING_IMAGES)

    # elif controller.state == AppState.MOVING_TO_POSE:
    #     logger.info("Moving to Pose...")
    #     if controller.get_position_status() == PositionStatus.POSE:
    #         controller.set_state(AppState.COLLECTING_IMAGE)

    # elif controller.state == AppState.COLLECTING_IMAGE:
    #     logger.info("Collecting and Saving Image")
    #     controller.save_image()
    #     controller.trigger_after_pose()
    #     controller.set_state(AppState.MOVING_TO_AFTER_POSE)

    # elif controller.state == AppState.MOVING_TO_AFTER_POSE:
    #     logger.info("Moving to after pose...")
    #     if controller.cobot.position_status == PositionStatus.AFTER_POSE:
    #         controller.pose_times.append(datetime.now())
    #         controller.set_waiting_program()
    #         controller.set_state(AppState.MOVING_TO_WAITING)

    # elif controller.state == AppState.PROCESSING_IMAGES:
    #     logger.info('Start Processing the saved images')
    #     controller.process_images()
    #     controller.generate_report()
    #     controller.set_state(AppState.WAITING_INPUT)

    # elif controller.state == AppState.PARAMETER_NOT_FOUND:
    #     controller.set_state(AppState.WAITING_INPUT)

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
