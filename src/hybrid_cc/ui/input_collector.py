# pylint:disable=no-member


class InputCollector:
    def __init__(self):
        self.pressed = {}
        self.subtick = 0

    def reset(self):
        for d, subtick in self.pressed.copy().items():
            if subtick == 0:
                self.pressed.pop(d)
            else:
                self.pressed[d] = 0
        self.subtick = 0

    def capture(self, dirs):
        if self.subtick == 4:
            self.reset()
        for d in dirs:
            if d not in self.pressed:
                self.pressed[d] = self.subtick
        self.subtick += 1

    def collect(self):
        return list(self.pressed.keys())
