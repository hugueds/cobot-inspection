from .cobot import Cobot

class ModBusUpdater:

    started = False

    def __init__(self, app, cobot: Cobot):
        self.app = app
        self.cobot = cobot

    def start(self):
        if not self.started:
            self.started = True
            self.loop()

    def stop(self):
        pass

    def loop(self):
        

