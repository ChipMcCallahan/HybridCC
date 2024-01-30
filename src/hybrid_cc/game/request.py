class Request:
    def __str__(self):
        # Filter out attributes that start with an underscore
        user_attrs = {k: v for k, v in self.__dict__.items() if
                      not k.startswith('_')}
        return f"({self.__class__.__name__}: {user_attrs})"


class DestroyRequest(Request):
    def __init__(self, *, target, pos):
        self.target = target
        self.pos = pos


class CreateRequest(Request):
    def __init__(self, *, pos, eid, **kwargs):
        self.pos = pos
        self.id = eid
        self.kwargs = kwargs


class MoveRequest(Request):
    def __init__(self, *, mob_id, directions):
        self.mob_id = mob_id
        self.directions = directions


class WinRequest(Request):
    def __init__(self, *, color):
        self.color = color


class LoseRequest(Request):
    def __init__(self, *, cause):
        self.cause = cause


class ShowHintRequest(Request):
    pass


class HideHintRequest(Request):
    pass
