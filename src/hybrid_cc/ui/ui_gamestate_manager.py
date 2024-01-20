from enum import Enum


class UIGamestate(Enum):
    START = 1
    PLAY = 2
    PAUSE = 3
    WIN = 4
    LOSE = 5
    LOAD = 6
    SELECT = 7


class UIGamestateManager:
    def __init__(self):
        start, play, pause, win, lose, load, select = tuple(UIGamestate)
        self.state = start
        self.allowed_transitions = {
            start: [play, select],
            play: [start, pause, win, lose],
            pause: [play, start],
            win: [start],
            lose: [start],
            load: [select],
            select: [load, start]
        }

    def can_transition_to(self, new_state):
        return new_state in self.allowed_transitions[self.state]

    def transition_to(self, new_state):
        if self.can_transition_to(new_state):
            self.state = new_state
            return True
        return False

    @property
    def is_start(self):
        return self.state == UIGamestate.START

    @property
    def is_pause(self):
        return self.state == UIGamestate.PAUSE

    @property
    def is_play(self):
        return self.state == UIGamestate.PLAY

    @property
    def is_win(self):
        return self.state == UIGamestate.WIN

    @property
    def is_lose(self):
        return self.state == UIGamestate.LOSE

    @property
    def is_select(self):
        return self.state == UIGamestate.SELECT

    @property
    def is_load(self):
        return self.state == UIGamestate.LOAD

    def start(self):
        return self.transition_to(UIGamestate.START)

    def pause(self):
        return self.transition_to(UIGamestate.PAUSE)

    def play(self):
        return self.transition_to(UIGamestate.PLAY)

    def win(self):
        return self.transition_to(UIGamestate.WIN)

    def lose(self):
        return self.transition_to(UIGamestate.LOSE)

    def select(self):
        return self.transition_to(UIGamestate.SELECT)

    def load(self):
        return self.transition_to(UIGamestate.LOAD)
