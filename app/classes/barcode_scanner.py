from time import sleep
from threading import Thread
from logger import logger
class BarcodeScanner:

    running = False
    read_value = ''        
    __buffer = set()

    def start(self):        
        self.running = True
        Thread(target=self.update, daemon=True).start()        
        
    def update(self):
        logger.info('Starting Barcode Update Thread...')
        while self.running:
            # read barcode
            # Condition to add value to buffer (check if is not repeated and has 6-7 number digits)
            read_value = ''
            if False:
                self.__buffer.update(read_value)
                pass
            sleep(0.1)
        else:
            print('Barcode Thread Finished')    

    def clear(self):
        self.__buffer.clear()

    def get_buffer(self):
        if len(self.__buffer):
            return self.__buffer.pop()

    def stop(self):
        self.running = False
        