from enumerables import modbus_interface
from classes.cobot import Cobot
from time import sleep

c = Cobot()

c.connect()

c.set_trigger(2)
