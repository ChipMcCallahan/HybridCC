class UIHints:
    pending = []

    @classmethod
    def add(cls, hint):
        cls.pending.append(hint)

    @classmethod
    def clear(cls):
        cls.pending.clear()