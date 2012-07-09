import libtcodpy as libtcod
from Player import Player
from GameObject import GameObject
from dungeon_maker import DungeonMaker


class State:
    """docstring for State"""
    def __init__(self, screen_width, screen_height, map_width, map_height):
        self.player = Player(screen_width / 2, screen_height / 2, '@', libtcod.white)
        npc = GameObject(screen_width / 2 + 5, screen_height / 2, '@', libtcod.yellow)
        self.objects = set([self.player, npc])
        self.exit = False
        self.game_map = DungeonMaker.make_map(map_width, map_height, self.player)

    def step(self):
        return self.objects
