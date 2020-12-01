import cv2 as cv
from models import Camera, Cobot, State
import logging
import yaml
from datetime import datetime
from time import sleep

FORMAT = ('%(asctime)-15s %(threadName)-15s %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')

logging.basicConfig(format=FORMAT)
log = logging.getLogger()

def read_config(path='config.yml'):
    with open(path, 'r') as file:
        return yaml.safe_load(file)

# TODO: Create a thread for Modbus writing and communication

def main():

    state = State.INITIAL
    operation_result = 0 # 0 -> None, 1 -> OK, 2 -> NOT_OK
    total_programs = 0
    program_list = []
    program = '00'
    program_index = 0
    start_datetime = datetime.now()
    final_datetime = start_datetime
    pose_times = []

    config = read_config()
    # load CU image Model
    camera = Camera()
    camera.start()    
    cobot = Cobot(config['cobot']['ip'], config['cobot']['modbus_port'])
    # cobot.connect()


    # check if robot is on running State

        # check if robot is in Home Position if not move there
    if not cobot.home_position:
        state = State.MOVING
        cobot.set_program(program)

    while not cobot.home_position:
        print('Waiting Cobot in Home position')
        sleep(5)

    state = State.WAITING_PARAMETER

    while True: # Put another condition

        # read and write modbus       

        # wait for a new product    
        if state == State.WAITING_PARAMETER:
            # identify CU model 
            # load popid + CU information   
            # move to position 0000XX00 - C.U + Position for Variant or just position 
            program_list = ['01', '02', '03', '04'] # carrega a lista de LTs e separa a lista de parametros
            total_programs = len(program_list)
            # clear the pictures folder
            state = State.PARAMETER_LOADED
            if False:
                state = State.PARAMETER_NOT_FOUND
            
        elif state == State.PARAMETER_LOADED:
            program_index = 0
            pose_times = []
            start_datetime = datetime.now()
            # move to identify CU model (optional)
            # load keras model for the CU     
            cobot.set_program(program)  # move to waiting position
            state = State.MOVING_TO_WAITING
            
        elif state == State.MOVING_TO_WAITING:
            if cobot.wait_position:
                if program_index < total_programs:
                    program = program_list[program_index]
                    cobot.set_program(program)
                    program_index += 1                    
                    state = State.MOVING_TO_POSE        
                else:
                    state = State.PROCESSING_IMAGES

        elif state == State.MOVING_TO_POSE:
            if cobot.pose_position:                
                state = State.COLLECTING_IMAGES
        
        elif state == State.COLLECTING_IMAGES:
            camera.read()
            camera.save_image()
            cobot.move_to_waiting()            
            pose_times.append(time = datetime.now())
            state = State.MOVING_TO_WAITING

        elif state == State.PROCESSING_IMAGES:
            # Load all pictures inside a folder
            # Classify every picture and store into array
            # compare each picture prediction to 0000XXXX - CU, Position, Port, Variant
            # if all pictures are correct, send an OK report
            # write a footer on picture describing the results
            # save all picures to a folder containing POPID and CU
            # save log to database
            operation_result = 1 if True else False

            state = State.WAITING_PARAMETER          
                      
        

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)    
