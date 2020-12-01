from models import Cobot
from time import sleep

ip = '10.8.66.212'

cobot = Cobot(ip)
cobot.connect()

counter = 0

while True:
    sleep(1)
    reg = cobot.read_register(129)
    cobot._write_register(129, counter)
    print(reg.registers)
    counter += 1    
