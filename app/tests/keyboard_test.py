import keyboard
import time

def update_program(e):
    print(e.name)
    print('ok')

def update_key(e):
    print(e.name)

keyboard.on_press_key('1', update_program)

keyboard.on_press(update_key)

while True:
    print('Running')
    time.sleep(1)