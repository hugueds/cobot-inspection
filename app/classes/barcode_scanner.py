from time import sleep
from threading import Thread
from logger import logger
class BarcodeScanner:

    running = False
    read_value = ''

    def start(self):
        self.running = True
        Thread(target=self.update, daemon=True).start()        
        
    def update(self):
        logger.info('Starting Barcode Update Thread...')
        while self.running:
            # read barcode
            sleep(0.1)
        else:
            print('Barcode Thread Finished')


    def stop(self):
        self.running = False
        