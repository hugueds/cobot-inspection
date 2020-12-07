from classes import Cobot
from time import sleep


c = Cobot()

def run():    
    counter = 6
    # c.connect()    
    c.start_read_thread(counter)
    while True:        
        counter += 1
        print(c.a)
        sleep(5)
