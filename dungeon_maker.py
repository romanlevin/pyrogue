class Tile:
    def __init__(self, block_move, block_sight=None):
        self.block_move = block_move
        self.block_sight = block_sight if block_sight else block_move

    def set_block_move(self, block_move=True):
        self.block_move = block_move

    def set_block_sight(self, block_sight=True):
        self.block_sight = block_sight

    def set_wall(self):
        self.set_block_move()
        self.set_block_sight()

    def set_floor(self):
        self.set_block_move(False)
        self.set_block_sight(False)


class Rectangle:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return (center_x, center_y)

    def intersect(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

    def __str__(self):
        return "(%d, %d), (%d, %d)" % (self.x1, self.y1, self.x2, self.y2)
