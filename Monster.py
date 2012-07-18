from GameObject import GameObject
from object_componenets import BasicMonster, Fighter
import libtcodpy as libtcod


class Monster(GameObject):
    """docstring for Player"""
    def __init__(self, state, (x, y), name, character, color, hp, defense, power):
        fighter = Fighter(hp=hp, defense=defense, power=power)
        super(Monster, self).__init__(state, (x, y), name, character,
        color, fighter=fighter, ai=BasicMonster())

    def death(self):
        print '%s is dead!' % self.name.capitalize()
        self.character = '.'
        self.color = libtcod.darker_red
        self.blocks = False
        self.fighter = None
        self.ai = None
        self.name = 'remains of %s' % self.name
