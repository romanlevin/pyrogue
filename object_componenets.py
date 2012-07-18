

class Fighter(object):
    #combat-related properties and methods (monster, player, NPC).
    def __init__(self, hp=10, defense=1, power=1):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power

    def take_damage(self, damage):
        if damage > 0:
            self.hp -= damage
        if self.hp <= 0:
            self.owner.death()

    def attack(self, target):
        damage = self.power - target.fighter.defense

        if damage > 0:
            print '%s attacks %s for %d hit points.' % (self.owner.name.capitalize(), target.name, damage)
            target.fighter.take_damage(damage)
        else:
            print '%s attacks %s, but totally fails.' % (self.owner.name.capitalize(), target.name)


class BasicMonster(object):
    def take_turn(self):
        monster = self.owner
        if monster.state.is_in_fov(monster):
            distance = monster.distance_to_player()
            if distance >= 2:
                monster.move_towards_player()
            if distance == 1:
                monster.fighter.attack(self.owner.state.player)
