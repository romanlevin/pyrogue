class GameObject:
    """docstring for GameObject"""
    def __init__(self, (x, y), name, character, color, blocks=True):
        self.x = x
        self.y = y
        self.name = name
        self.character = character
        self.color = color
        self.blocks = blocks

    def move(self, (dx, dy), state):
        if not state.is_blocked((self.x + dx, self.y + dy)):
            self.x += dx
            self.y += dy
            return True
        else:
            return False

    def set_location(self, (x, y)):
        self.x = x
        self.y = y

    def position(self):
        return (self.x, self.y)
