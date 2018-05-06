from classes.cell import Cell
import random


class Playground:
    def __init__(self, h, w, count_of_mines):
        self.size = (h, w)
        self.count_of_mines = count_of_mines
        self.marked_cells = 0
        self.true_marked_cells = 0
        self.field = []
        for i in range(self.size[0]):
            self.field.append([])
            for j in range(self.size[1]):
                self.field[i].append(Cell((i, j)))

    def _add_mine(self, where):
        self.field[where[0]][where[1]].type = 'Mine'

    def first_generation(self, clicked):

        for i in range(self.count_of_mines):
            x = None
            y = None
            while (True):
                x = int(random.random() * 1000 % self.size[1])
                y = int(random.random() * 1000 % self.size[0])
                if ((y, x) != clicked and self.field[y][x].type != 'Mine'):
                    break
            self._add_mine((y, x))
        for i in range(self.size[1]):
            for j in range(self.size[0]):
                if (self.field[i][j].type == 'Mine'):
                    continue
                for ii in range(-1, 2):
                    for jj in range(-1, 2):
                        if (i + ii < 0 or i + ii >= self.size[1] or j + jj < 0 or j + jj >= self.size[0]):
                            continue
                        if (self.field[i + ii][j + jj].type == 'Mine'):
                            # print(i + ii, j + jj)
                            self.field[i][j].num += 1
        print('GENERATED!')

    def open_cell(self, x, y):
        if (self.field[y][x].type == 'Mine'):
            return 1
        # self.field[y][x].open()
        queue = [(y, x), ]
        mark = []
        for i in range(self.size[0]):
            mark.append([])
            for j in range(self.size[1]):
                mark[i].append(0)
        while (queue):
            yy = queue[0][0]
            xx = queue[0][1]
            queue.pop(0)
            mark[yy][xx] = 1
            if (self.field[yy][xx].marked):
                continue
            self.field[yy][xx].open()
            if (self.field[yy][xx].num != 0):
                continue
            try:
                if (self.field[yy + 1][xx].type == 'Free' and yy + 1 < self.size[0] and mark[yy + 1][xx] == 0):
                    queue.append((yy + 1, xx))
            except:
                pass
            try:
                if (self.field[yy - 1][xx].type == 'Free' and yy - 1 >= 0 and mark[yy - 1][xx] == 0):
                    queue.append((yy - 1, xx))
            except:
                pass
            try:
                if (self.field[yy][xx + 1].type == 'Free' and xx + 1 < self.size[1] and mark[yy][xx + 1] == 0):
                    queue.append((yy, xx + 1))
            except:
                pass

            try:
                if (self.field[yy][xx - 1].type == 'Free' and xx - 1 >= 0 and mark[yy][xx - 1] == 0):
                    queue.append((yy, xx - 1))
            except:
                pass

            try:
                if (self.field[yy - 1][xx - 1].type == 'Free' and xx - 1 >= 0 and yy - 1 >= 0 and mark[yy - 1][xx - 1] == 0):
                    queue.append((yy - 1, xx - 1))
            except:
                pass
            try:
                if (self.field[yy + 1][xx - 1].type == 'Free' and xx - 1 >= 0 and yy + 1 < self.size[0] and mark[yy + 1][xx - 1] == 0):
                    queue.append((yy + 1, xx - 1))
            except:
                pass
            try:
                if (self.field[yy - 1][xx + 1].type == 'Free' and xx + 1 < self.size[1] and yy - 1 >= 0 and mark[yy - 1][xx + 1] == 0):
                    queue.append((yy - 1, xx + 1))
            except:
                pass
            try:
                if (self.field[yy + 1][xx + 1].type == 'Free' and xx + 1 < self.size[1] and yy + 1 < self.size[0] and mark[yy + 1][xx + 1] == 0):
                    queue.append((yy + 1, xx + 1))
            except:
                pass


    def mark_cell(self, x, y):
        if (self.field[y][x].opened == False):
            delta = self.field[y][x].mark()
            self.marked_cells += delta
            if(self.field[y][x].type == 'Mine'):
                self.true_marked_cells += delta
