

class Fighter(object):
    #combat-related properties and methods (monster, player, NPC).
    def __init__(self, hp=10, defense=1, power=1):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power


class BasicMonster(object):
    def take_turn(self):
        monster = self.owner
        if monster.state.is_in_fov(monster):
            if monster.distance_to_player() >= 2:
                monster.move_towards_player()
