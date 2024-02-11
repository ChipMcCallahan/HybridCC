class Clock:
    tick = 0

    @classmethod
    def increment(cls):
        cls.tick += 1

    @classmethod
    def reset(cls):
        cls.tick = 0
