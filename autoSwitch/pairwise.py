class Pairwise:
    def __init__(self):
        self.first = b''
        self.second = b''

    def add_next(self, data):
        if not self.first:
            self.first = data
        elif not self.second:
            self.second = data
        else:
            self.first = self.second
            self.second = data

    def contains(self, data):
        return data in self.first + self.second
