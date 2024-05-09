from settings import FPS


class Timer:
    def __init__(self, max_time, current_time=0):

        self.current_time = current_time
        self.max_time = max_time

        self.active = False

    def activate(self):
        if self.active:
            self.current_time += 1 / FPS
    
    def deactivate(self):
        if self.current_time >= self.max_time:
            self.current_time = 0
            self.active = False
    
    def update(self):
        self.activate()
        self.deactivate()
