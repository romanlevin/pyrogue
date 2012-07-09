import libtcodpy as libtcod
from Player import Player
from dungeon_maker import DungeonMaker


class State:
    """docstring for State"""
    def __init__(self, map_width, map_height):
        self.player = Player((0, 0), 'Player', '@', libtcod.white)
        self.objects = set([self.player])
        self.exit = False
        self.game_map = DungeonMaker.make_map(map_width, map_height, self.player, self.objects)

    def step(self):
        return self.objects

    def is_blocked(self, (x, y)):
        if self.game_map[x][y].block_move:
            return True
        for obj in self.objects:
            if obj.blocks and (obj.x, obj.y) == (x, y):
                return True
        return False

