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
            # TODO Change home to waiting
            controller.set_home_pose() # TODO Move only the Z axis to the maximum
            controller.new_product()
            controller.set_state(AppState.LOADING_PARAMETERS)

    elif controller.state == AppState.LOADING_PARAMETERS:
        controller.load_parameters()
        if controller.parameters_found:
            logger.info(f'Parameters loaded for this Popid')
            controller.set_state(AppState.PARAMETER_LOADED)
        else:
            logger.error(f'Parameters not found')
            controller.set_state(AppState.PARAMETER_NOT_FOUND)

    elif controller.state == AppState.PARAMETER_LOADED:
        first_component = controller.component_list[0]
        controller.start_job(first_component.number)
        controller.set_state(AppState.MOVING_TO_WAITING)

    elif controller.state == AppState.MOVING_TO_HOME:
        if controller.get_position_status() == PositionStatus.HOME:
            pass
        pass

    elif controller.state == AppState.MOVING_TO_WAITING:
        logger.info("Moving to Waiting...")
        if controller.get_position_status() == PositionStatus.POSE:
            if controller.component_index >= controller.total_components:
                controller.set_state(AppState.FINISHED)
            elif controller.total_poses <= 0:
                controller.job_done()
            else:
                # controller.first_pose()
                # controller.next_pose()
                pose = controller.get_pose(0)
                controller.cobot.set_pose(pose)
                controller.set_state(AppState.MOVING_TO_POSE)

    elif controller.state == AppState.MOVING_TO_POSE:
        logger.info("Moving to Pose...")
        if controller.get_position_status() == PositionStatus.POSE:
            if controller.pose_index >= controller.total_poses:
                controller.job_done()
                controller.set_home_pose()
                controller.set_state(AppState.MOVING_TO_WAITING)
            else:
                if controller.check_inspection():
                    controller.set_state(AppState.PROCESSING_IMAGE)
                else:
                    controller.next_pose()
                    sleep(0.2)
                    controller.set_state(AppState.MOVING_TO_POSE)

    elif controller.state == AppState.PROCESSING_IMAGE:
        logger.info("Collecting Image")
        controller.process_image()
        sleep(1)
        if controller.param_result:  # Only move if the result match or someone request for it
            controller.next_pose()
            controller.set_state(AppState.MOVING_TO_POSE)
        else:
            logger.warn('Parameter not matched, redoing operation')
           

    elif controller.state == AppState.FINISHED:
        logger.info('All Component Jobs finished, Returning to Home Position')
        # TODO: Generate Report
        # TODO: Log all next popids in the queue
        controller.set_home_pose()
        # controller.set_state(AppState.MOVING_TO_HOME)
        controller.set_state(AppState.WAITING_INPUT)


    elif controller.state == AppState.MOVING_TO_HOME:
        if controller.get_position_status() == PositionStatus.POSE:
            controller.set_state(AppState.WAITING_INPUT)

    elif controller.state == AppState.PARAMETER_NOT_FOUND:
        controller.set_state(AppState.WAITING_INPUT)

    sleep(0.2)
