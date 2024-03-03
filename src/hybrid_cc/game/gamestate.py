from enum import Enum


class Gamestate:
    class State(Enum):
        PLAY = 1
        WIN = 2
        LOSE = 3

    state = State.PLAY

    @classmethod
    def win(cls):
        if cls.state == Gamestate.State.PLAY:
            cls.state = Gamestate.State.WIN

    @classmethod
    def is_win(cls):
        return cls.state == Gamestate.State.WIN

    @classmethod
    def lose(cls):
        if cls.state == Gamestate.State.PLAY:
            cls.state = Gamestate.State.LOSE

    @classmethod
    def is_lose(cls):
        return cls.state == Gamestate.State.LOSE

    @classmethod
    def reset(cls):
        cls.state = Gamestate.State.PLAY
