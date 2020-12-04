from pymodbus.client.sync import ModbusTcpClient
from enumerables import ModbusInterface


class Modbus:   
    
    def __init__(self, ip, port=502):
        self.ip = ip
        self.port = port
        self.client = ModbusTcpClient(ip, port)

    def read_values(self): # Returns an array of values from a start point
        start_read = 128
        end_read = 140
        return self.__read_register(start_read, start_read - end_read)        

    def write_values(self, values):
        start_write = 200
        end_write = 220
        self.write_values(start_write, values)

    def __read_register(self, address, count=1):
        try:
            reg = self.client.read_holding_registers(address, count=count)
            return reg.registers
        except Exception as e:
            return print('ModBus::__read_register::', str(e))

    def __write_register(self, address, values):
        try:
            self.client.write_registers(address, values)
        except Exception as e:
            print('ModBus::__write_register::', str(e))


        

