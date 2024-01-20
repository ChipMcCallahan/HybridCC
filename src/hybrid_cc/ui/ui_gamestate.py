from enum import Enum


class UIGamestate:
    class State(Enum):
        START = 1
        PLAY = 2
        PAUSE = 3
        WIN = 4
        LOSE = 5

    def __init__(self):
        start, play, pause, win, lose = tuple(UIGamestate.State)
        self.state = start
        self.allowed_transitions = {
            start: [play],
            play: [start, pause, win, lose],
            pause: [play, start],
            win: [start],
            lose: [start]
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
        return self.state == UIGamestate.State.START

    @property
    def is_pause(self):
        return self.state == UIGamestate.State.PAUSE

    @property
    def is_play(self):
        return self.state == UIGamestate.State.PLAY

    @property
    def is_win(self):
        return self.state == UIGamestate.State.WIN

    @property
    def is_lose(self):
        return self.state == UIGamestate.State.LOSE

    def start(self):
        return self.transition_to(UIGamestate.State.START)

    def pause(self):
        return self.transition_to(UIGamestate.State.PAUSE)

    def play(self):
        return self.transition_to(UIGamestate.State.PLAY)

    def win(self):
        return self.transition_to(UIGamestate.State.WIN)

    def lose(self):
        return self.transition_to(UIGamestate.State.LOSE)
