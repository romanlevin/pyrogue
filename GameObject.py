import math


class GameObject(object):
    """docstring for GameObject"""
    def __init__(self, state, (x, y), name, character, color, blocks=True, fighter=None, ai=None):
        self.state = state
        self.x = x
        self.y = y
        self.name = name
        self.character = character
        self.color = color
        self.blocks = blocks
        self.fighter = fighter
        if self.fighter:
            self.fighter.owner = self
        self.ai = ai
        if self.ai:
            self.ai.owner = self

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

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def move_towards(self, target, state):
        dx = target.x - self.x
        dy = target.y - self.y
        distance = self.distance_to(target)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        self.move((dx, dy), state)
