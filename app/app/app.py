from classes import Controller

class App:    

    def __init__(self) -> None:
        self.controller = Controller()
        

    def start(self):
        self.controller.connect_to_cobot()
        self.controller.start_camera()
        
    def pause(self):
        pass

    def stop(self):
        pass