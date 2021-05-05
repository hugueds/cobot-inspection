import serial
from threading import Thread
from logger import logger


class BarcodeScanner:

    running = False
    read_value = ''    
    __buffer = set()

    def __init__(self, port='com5', baudrate=9600) -> None:
        self.port = port
        self.baudrate = baudrate

    def start(self):
        self.running = True
        Thread(target=self.update, daemon=True).start()

    def update(self):
        logger.info('Starting Barcode Update Thread...')
        s = serial.Serial(self.port, self.baudrate, timeout=0.5)
        while self.running:            
            if not s.is_open:
                s.open()
            self.read_value = s.readline().decode('utf-8')
            popid = self.read_value  # TODO Condition to add value to buffer
            if self.read_value:
                logger.info(f'[EVENT] Barcode read: {self.read_value}')
            if popid:
                self.__buffer.update([popid])
        else:
            print('Barcode Thread Finished')
            s.close()

    def clear(self):
        self.__buffer.clear()

    def get_buffer(self):        
        if len(self.__buffer):
            logger.info(f'Buffer contents: {self.__buffer}')
            return self.__buffer.pop()

    def stop(self):
        self.running = False
