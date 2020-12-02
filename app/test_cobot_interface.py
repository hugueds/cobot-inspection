from models import Camera, Cobot, State, CobotStatus, PositionStatus
from time import sleep
from datetime import datetime

state = State.INITIAL

cobot = Cobot()
cobot.connect()

state = State.WAITING_PARAMETER
parameter_list = ['PV110011', 'PV110021', 'PV110031', 'PV110041', 'PV110051', 'PV110061'] # Example
program_list = [x[4:6] for x in parameter_list] # carrega a lista de LTs e separa a lista de parametros
total_programs = len(program_list) 
program_index = 0

while True:

    # read and write modbus
    cobot.read_interface()
    cobot.update_interface(state)

    # read a break condition / keyboard
    if cobot.status != CobotStatus.RUNNING:
        print('Cobot is not ready for work...')
        sleep(1)

    if cobot.emergency == CobotStatus.EMERGENCY_STOPPED:
        print('Emergency stop')
        break        
    
    # write information on camera window

    # wait for a new product    
    if state == State.WAITING_PARAMETER:
        print('Loading parameters')
        sleep(5)
        state = State.PARAMETER_LOADED
        
        
    elif state == State.PARAMETER_LOADED:
        print('Parameters loaded, moving to wait position')
        program = 0
        cobot.set_program(program)  # move to waiting position
        state = State.MOVING_TO_WAITING
        
    elif state == State.MOVING_TO_WAITING:
        if cobot.position_status == PositionStatus.WAITING:
            if program_index < total_programs:
                print('moving to waiting')
                program = program_list[program_index]
                cobot.set_program(program)
                program_index += 1                    
                state = State.MOVING_TO_POSE        
            else:
                state = State.PROCESSING_IMAGES

    elif state == State.MOVING_TO_POSE:
        if cobot.position_status == PositionStatus.POSE:
            print('collecting moving to pose')
            state = State.COLLECTING_IMAGES
    
    elif state == State.COLLECTING_IMAGES:
        print('collecting images')
        sleep(5)
        parameter = parameter_list[program_index]                        
        cobot.move_to_waiting()          
        state = State.MOVING_TO_WAITING

    elif state == State.PROCESSING_IMAGES:
        print('Processing images')
        sleep(5)

