class Cell:
    def __init__(self, where):
        self.coordinates = where
        self.type = 'Free'
        self.opened = False
        self.marked = False
        self.num = 0

    def open(self):
        if (self.marked == False):
            self.opened = True

    def mark(self):
        self.marked = not self.marked
        if (self.marked):
            return 1
        else:
            return -1
