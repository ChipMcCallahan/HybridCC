class HashableObject:
    def __init__(self, **attributes):
        self.__dict__.update(attributes)

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.__dict__ == other.__dict__)
