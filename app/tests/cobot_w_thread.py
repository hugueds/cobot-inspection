from classes import Cobot
from time import sleep



def run():    
    c = Cobot()
    counter = 6
    # c.connect()    
    c.start_read_thread(counter)
    while True:        
        counter += 1
        print(c.a)
        sleep(5)
