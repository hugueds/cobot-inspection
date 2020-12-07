from time import sleep
from datetime import datetime
from classes import Cobot
from enumerables import PositionStatus, AppState, CobotStatus
from classes import Controller
import keyboard
from logger import logger

def test(e: keyboard.KeyboardEvent):
    global cobot, controller, start        
    if e.name == 'enter':
        start = True
    if e.name == 'm':
       controller.manual_mode = not controller.manual_mode 
       status = 'manual' if controller.manual_mode else 'auto'
       print('Controller set to ', status)
    if e.name.isdigit() and controller.manual_mode:
        controller.set_program(int(e.name))

def run():

    global cobot, controller, start

    cobot = Cobot()
    controller = Controller(cobot)
    start = False

    keyboard.on_press(test)
    
    # controller.start_modbus_thread(cobot)

    controller.manual_mode = True

    controller.set_state(AppState.INITIAL)
    controller.set_state(AppState.WAITING_INPUT)

    while True:
        
        # cobot.read_interface()
        # cobot.update_interface(controller.state)

        # read a break condition / keyboard
        if cobot.status != CobotStatus.RUNNING:
            start = False
            print('Cobot is not ready for work... Status:', cobot.status)
            sleep(1)
            continue

        if cobot.emergency == CobotStatus.EMERGENCY_STOPPED:
            print('Emergency stop')
            sleep(1)
            continue

        if controller.manual_mode and controller.state == AppState.WAITING_INPUT:
            print('Cobot in Manual mode')
            sleep(1)
            continue        

        if controller.state == AppState.WAITING_INPUT and not controller.manual_mode:
            # wait for mona/scanner trigger
            print('Waiting new product')
            sleep(1)
            if start:
                start = False
                print('New Product')                
                controller.set_state(AppState.WAITING_PARAMETER)        

        # wait for a new product    
        elif controller.state == AppState.WAITING_PARAMETER:
            print('Loading parameters...')
            controller.load_parameters()
            sleep(5)
            controller.set_state(AppState.PARAMETER_LOADED)
            
        elif controller.state == AppState.PARAMETER_LOADED:
            print('Parameters loaded, moving to wait position')
            controller.program = 0
            controller.set_program(controller.program)  # move to waiting position
            controller.set_state(AppState.MOVING_TO_WAITING)
            
        elif controller.state == AppState.MOVING_TO_WAITING:
            print('Moving to waiting position...')
            print('Position Status:', cobot.position_status)
            if cobot.position_status == PositionStatus.WAITING:
                if controller.program_index < controller.total_programs:
                    controller.program = controller.program_list[controller.program_index]
                    controller.set_program(controller.program)
                    controller.set_state(AppState.MOVING_TO_POSE)
                else:
                    controller.set_state(AppState.PROCESSING_IMAGES)

        elif controller.state == AppState.MOVING_TO_POSE:
            print('Moving to Pose', controller.program_index + 1)
            if cobot.position_status == PositionStatus.POSE:
                print('Pose reached', controller.program_index + 1)
                controller.set_state(AppState.COLLECTING_IMAGES)
        
        elif controller.state == AppState.COLLECTING_IMAGES:
            print('Collecting Image...')
            sleep(1)
            controller.parameter = controller.parameter_list[controller.program_index] # do a new function
            controller.program_index += 1 # do a new function
            controller.set_program(0) # do a new function
            controller.set_state(AppState.MOVING_TO_WAITING)

        elif controller.state == AppState.PROCESSING_IMAGES:
            print('Processing collected images...')
            sleep(5)
            print('Job Finished!')
            controller.set_state(AppState.FINISHED)

        elif controller.state == AppState.FINISHED:
            print('Waiting for a new Job')
            sleep(3)
            controller.set_state(AppState.WAITING_INPUT)

        sleep(0.5)
        
            


