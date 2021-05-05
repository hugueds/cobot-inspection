from classes.barcode_scanner import BarcodeScanner
from time import sleep
# from serial import Serial

b = BarcodeScanner()
b.start()

while True:        
    sleep(1)
    