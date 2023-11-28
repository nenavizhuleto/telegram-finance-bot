class Iota:
    def __init__(self):
        self.counter = 0

    def next(self) -> int:
        self.counter = self.counter + 1

        return self.counter


iota = Iota()

