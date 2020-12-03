from controller import Controller
from time import sleep
from datetime import datetime
from models import Camera, Cobot, Pose
from enumerables import ModbusInterface, PositionStatus, AppState, CobotStatus
from controller import Controller
import keyboard

cobot = Cobot()
controller = Controller()


def test(e: keyboard.KeyboardEvent):
    global cobot
    print(e.name)
    controller.state == AppState.WAITING_PARAMETER
    cobot.set_program(int(e.name))
    print('ok')

def run():    


    keyboard.on_press(test)

    cobot.connect()

    # controller.start_modbus_thread(cobot)

    controller.state = AppState.INITIAL
    controller.state = AppState.WAITING_PARAMETER

    while True:

        # read and write modbus
        cobot.read_interface()
        cobot.update_interface(controller.state)

        # read a break condition / keyboard
        if cobot.status != CobotStatus.RUNNING:        
            print('Cobot is not ready for work... Status:', cobot.status)
            sleep(1)

        if cobot.emergency == CobotStatus.EMERGENCY_STOPPED:
            print('Emergency stop')
            break        
        
        # write information on camera window

        # wait for a new product    
        if controller.state == AppState.WAITING_PARAMETER:
            print('Loading parameters')
            controller.load_parameters()
            sleep(5)
            controller.state = AppState.PARAMETER_LOADED            
            
        elif controller.state == AppState.PARAMETER_LOADED:
            print('Parameters loaded, moving to wait position')
            controller.program = 0
            cobot.set_program(controller.program)  # move to waiting position
            controller.state = AppState.MOVING_TO_WAITING
            
        elif controller.state == AppState.MOVING_TO_WAITING:
            print('Moving to waiting position...')
            print('Position Status', cobot.position_status)
            if cobot.position_status == PositionStatus.WAITING:
                if controller.program_index < controller.total_programs:
                    controller.program = controller.program_list[controller.program_index]
                    cobot.set_program(controller.program)
                    controller.state = AppState.MOVING_TO_POSE        
                else:
                    controller.state = AppState.PROCESSING_IMAGES

        elif controller.state == AppState.MOVING_TO_POSE:
            print('Moving to Pose', controller.program_index + 1)
            if cobot.position_status == PositionStatus.POSE:
                print('Pose reached', controller.program_index + 1)
                controller.state = AppState.COLLECTING_IMAGES
        
        elif controller.state == AppState.COLLECTING_IMAGES:
            print('Collecting Image')
            sleep(5)
            controller.parameter = controller.parameter_list[controller.program_index]
            controller.program_index += 1                    
            cobot.move_to_waiting()
            controller.state = AppState.MOVING_TO_WAITING

        elif controller.state == AppState.PROCESSING_IMAGES:
            print('Processing images')
            sleep(5)
            controller.state = AppState.FINISHED
            print('Job Finished!')

        elif controller.state == AppState.FINISHED:
            print('Waiting for a new Job')
            sleep(1)

        sleep(0.5)
        
            


