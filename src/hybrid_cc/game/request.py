class DestroyRequest:
    def __init__(self, *, target, pos):
        self.target = target
        self.pos = pos


class CreateRequest:
    def __init__(self, *, pos, eid, **kwargs):
        self.pos = pos
        self.id = eid
        self.kwargs = kwargs


class WinRequest:
    def __init__(self, *, color):
        self.color = color


class LoseRequest:
    def __init__(self, *, cause):
        self.cause = cause
