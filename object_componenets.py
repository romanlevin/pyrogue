

class Fighter(object):
    #combat-related properties and methods (monster, player, NPC).
    def __init__(self, hp=10, defense=1, power=1):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power


class BasicMonster(object):
    def take_turn(self, state):
        monster = self.owner
        if libtcod.map_is_in_fov():
            pass
