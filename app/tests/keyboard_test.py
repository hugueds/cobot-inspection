import keyboard
import time

def update_program(e):
    print(e)
    print('ok')

keyboard.on_press_key('1', update_program)

while True:
    print('Running')
    time.sleep(1)