from models import Cobot
from time import sleep


def run():

    cobot = Cobot()
    cobot.connect()

    counter = 0

    while True:
        sleep(1)
        reg = cobot.modbus_client.read_holding_registers(258, count=1)
        # reg = cobot.__read_register(129)        
        # cobot._write_register(129, counter)
        print(reg.registers[0])
        counter += 1    


        