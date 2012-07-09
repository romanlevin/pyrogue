import libtcodpy as libtcod
from Player import Player
from GameObject import GameObject
from dungeon_maker import Tile, Rectangle

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
MAP_WIDTH = 80
MAP_HEIGHT = 45
FPS_LIMIT = 20
START_FULLSCREEN = False
FONT = 'arial10x10.png'


class State:
    """docstring for State"""
    def __init__(self):
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, '@', libtcod.white)
        npc = GameObject(SCREEN_WIDTH / 2 + 5, SCREEN_HEIGHT / 2, '@', libtcod.yellow)
        self.objects = set([self.player, npc])
        self.exit = False
        self.game_map = []
        self.make_map()

    def make_map(self):
        self.game_map = [[Tile(True) for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]
        self.populate_rooms()

    def populate_rooms(self):
        ROOM_MAX_SIZE = 10
        ROOM_MIN_SIZE = 6
        MAX_ROOMS = 30
        rooms = []
        for room in range(MAX_ROOMS):
            w = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            h = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            x = libtcod.random_get_int(0, 0, MAP_WIDTH - w - 1)
            y = libtcod.random_get_int(0, 0, MAP_HEIGHT - h - 1)
            new_room = Rectangle(x, y, w, h)

            failed = False
            for other_room in rooms:
                if new_room.intersect(other_room):
                    failed = True
                    break

            if not failed:
                self.create_room(new_room)
                room_center = new_room.center()
                number_of_rooms = len(rooms)
                if number_of_rooms == 0:
                    self.player.set_location(room_center)
                else:
                    previous_x, previous_y = rooms[number_of_rooms - 1].center()
                    current_x, current_y = room_center
                    if libtcod.random_get_int(0, 0, 1) == 0:
                        self.create_horizontal_tunnel(previous_x, current_x, previous_y)
                        self.create_vertical_tunnel(previous_y, current_y, current_x)
                    else:
                        self.create_horizontal_tunnel(previous_x, current_x, current_y)
                        self.create_vertical_tunnel(previous_y, current_y, previous_x)
                rooms.append(new_room)

    def create_room(self, rectangle):
        for x in range(rectangle.x1 + 1, rectangle.x2):
            for y in range(rectangle.y1 + 1, rectangle.y2):
                self.game_map[x][y].set_floor()

    def create_horizontal_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.game_map[x][y].set_floor()

    def create_vertical_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.game_map[x][y].set_floor()

    def step(self):
        return self.objects
