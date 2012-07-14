from Player import Player
from dungeon_maker import DungeonMaker
import libtcodpy as libtcod


class State(object):
    """docstring for State"""
    def __init__(self, map_width, map_height):
        self.player = Player(self, (0, 0))
        self.objects = set([self.player])
        self.exit = False
        self.map_width = map_width
        self.map_height = map_height
        self.DungeonMaker = DungeonMaker(self)
        self.game_map = self.DungeonMaker.make_map()
        self.fov_map = self.build_fov_map()

    def step(self):
        pass

    def is_blocked(self, (x, y)):
        if self.game_map[x][y].block_move:
            return True
        for obj in self.objects:
            if obj.blocks and (obj.x, obj.y) == (x, y):
                return True
        return False

    def find_object(self, (x, y)):
        for obj in self.objects:
            if (obj.x, obj.y) == (x, y):
                return obj
        return None

    def build_fov_map(self):
        game_map = self.game_map
        map_width, map_height = self.map_width, self.map_height
        fov_map = libtcod.map_new(map_width, map_height)
        for x in range(map_width):
            for y in range(map_height):
                libtcod.map_set_properties(fov_map, x, y, not game_map[x][y].block_sight, not game_map[x][y].block_move)
        return fov_map

    def compute_fov(self):
        FOV_ALGO = 0  # default FOV algorithm
        FOV_LIGHT_WALLS = True
        TORCH_RADIUS = 10
        player = self.player
        libtcod.map_compute_fov(self.fov_map, player.x, player.y, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)

    def move_player(self, direction):
        player = self.player
        if player.move_or_attack(direction):
            return True
        else:
            return False
