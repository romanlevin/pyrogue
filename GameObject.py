class GameObject:
    """docstring for GameObject"""
    def __init__(self, x, y, character, color):
        self.x = x
        self.y = y
        self.character = character
        self.color = color

    def move(self, (dx, dy), game_map):
        if not game_map[self.x + dx][self.y + dy].block_move:
            self.x += dx
            self.y += dy

    def set_location(self, (x, y)):
        self.x = x
        self.y = y

    def position(self):
        return (self.x, self.y)