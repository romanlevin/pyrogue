from GameObject import GameObject
from object_componenets import Fighter
import libtcodpy as libtcod


class Player(GameObject):
    """docstring for Player"""
    def __init__(self, state, (x, y)):
        super(Player, self).__init__(state, (x, y), 'player', '@', libtcod.white, fighter=Fighter())

    def move_or_attack(self, (dx, dy)):
        state = self.state
        x = self.x + dx
        y = self.y + dy
        position = (x, y)
        target = state.find_object(position)
        if target and target.fighter:
            self.fighter.attack(target)
            return False
        else:
            return self.move((dx, dy), state)

    def death(self):
        print 'You died!'
        self.character = '.'
        self.color = libtcod.darker_red
