import os
from datetime import datetime
from time import sleep
import logging
import cv2 as cv
from models import Camera, Cobot, State, CobotStatus, PositionStatus

FORMAT = ('%(asctime)-15s %(threadName)-15s %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')

logging.basicConfig(format=FORMAT)
log = logging.getLogger()

# TODO: Create a thread for Modbus writing and communication

def main():

    state = State.INITIAL
    operation_result = 0 # 0 -> None, 1 -> OK, 2 -> NOT_OK
    total_programs = 0
    program_list = []
    parameter_list = []
    program = '00'
    program_index = 0
    start_datetime = datetime.now()
    final_datetime = start_datetime
    pose_times = []
    component_unit = ''    
    
    # load CU image Model
    camera = Camera()
    camera.start()

    cobot = Cobot()
    cobot.connect()

    cobot.read_interface()
    cobot.update_interface(state)

    # check if robot is on running State
    while cobot.status != CobotStatus.RUNNING:
        print('Cobot is not ready for work... Status: %d', cobot.status)
        sleep(5)

    # check if robot is in Home Position if not move there
    if not cobot.position_status == PositionStatus.HOME:
        state = State.MOVING
        home_program = 99
        cobot.set_program(home_program)

    while not cobot.position_status == PositionStatus.HOME:
        cobot.read_interface()
        print('Waiting Cobot in Home position')
        sleep(5)

    state = State.WAITING_PARAMETER

    while True: # Put another condition

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
            # identify CU number/model 
            # load popid + CU information            
            component_unit = ''
            parameter_list = ['PV110011', 'PV110021', 'PV110031', 'PV110041', 'PV110051', 'PV110061'] # Example
            program_list = [int(x[5:7]) for x in parameter_list] # carrega a lista de LTs e separa a lista de parametros
            total_programs = len(program_list)            
            parameter_found = True # Check if all parameters are correct
            # Print total programs
            if parameter_found:
                state = State.PARAMETER_LOADED
            else:
                state = State.PARAMETER_NOT_FOUND
            
        elif state == State.PARAMETER_LOADED:
            operation_result = 0
            program_index = 0
            pose_times = []
            start_datetime = datetime.now()
            # move to identify CU model (optional)
            # load keras model for the CU     
            # clear the pictures folder
            program = 0
            cobot.set_program(program)  # move to waiting position
            state = State.MOVING_TO_WAITING
            
        elif state == State.MOVING_TO_WAITING:
            if cobot.position_status == PositionStatus.WAITING:
                if program_index < total_programs:
                    program = program_list[program_index]
                    cobot.set_program(program)
                    state = State.MOVING_TO_POSE        
                else:
                    state = State.PROCESSING_IMAGES

        elif state == State.MOVING_TO_POSE:
            if cobot.position_status == PositionStatus.POSE:
                state = State.COLLECTING_IMAGES
        
        elif state == State.COLLECTING_IMAGES:
            parameter = parameter_list[program_index]
            camera.read()
            camera.save_image(parameter)
            cobot.move_to_waiting()            
            pose_times.append(datetime.now())
            state = State.MOVING_TO_WAITING

        elif state == State.PROCESSING_IMAGES:
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
            operation_result = 1 if True else False
            final_datetime = datetime.now()
            total_time = (start_datetime - final_datetime).seconds
            print('Total operation time: %d', total_time)
            program_index += 1                    
            state = State.WAITING_PARAMETER          

    print('Finishing Program')                 
        

if __name__ == '__main__':
    try:
        main()        
    except Exception as e:
        print('Finishing program due error')
        print(e)
