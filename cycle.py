class Cycle:

    def __init__(self, vertices):
        self.i = 0
        self.n = len(vertices)
        self.now = vertices[self.i]
        self.vertices = vertices
        self.round = 0

    def next(self):
        self.i = (self.i + 1) % self.n
        if self.i == 0:
            self.round += 1
        self.now = self.vertices[self.i]
        return self.now
