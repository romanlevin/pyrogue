#Following the libtcod tutorial on Rogue Basin.

import libtcodpy as libtcod

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
MAP_WIDTH = 80
MAP_HEIGHT = 45
FPS_LIMIT = 20
START_FULLSCREEN = False
FONT = 'arial10x10.png'

color_dark_wall = libtcod.Color(0, 0, 100)
color_dark_ground = libtcod.Color(50, 50, 100)


class GameObject:
    """docstring for GameObject"""
    def __init__(self, x, y, character, color):
        self.x = x
        self.y = y
        self.character = character
        self.color = color

    def move(self, (dx, dy), game_map):
        if not game_map[self.x + dx][self.y + dy].block_move:
            self.x += dx
            self.y += dy

    def set_location(self, (x, y)):
        self.x = x
        self.y = y

    def position(self):
        return (self.x, self.y)


class Tile:
    def __init__(self, block_move, block_sight=None):
        self.block_move = block_move
        self.block_sight = block_sight if block_sight else block_move

    def set_block_move(self, block_move=True):
        self.block_move = block_move

    def set_block_sight(self, block_sight=True):
        self.block_sight = block_sight

    def set_wall(self):
        self.set_block_move()
        self.set_block_sight()

    def set_floor(self):
        self.set_block_move(False)
        self.set_block_sight(False)


class Rectangle:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return (center_x, center_y)

    def intersect(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

    def __str__(self):
        return "(%d, %d), (%d, %d)" % (self.x1, self.y1, self.x2, self.y2)


class Player(GameObject):
    """docstring for Player"""


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


class Screen:
    """docstring for Screen"""
    def __init__(self):
        libtcod.console_set_custom_font(FONT, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
        libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'pyrogue', START_FULLSCREEN)
        self.console = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.state = State()
        self.exit = False

    def draw_objects(self, objects):
        for obj in objects:
            libtcod.console_set_foreground_color(self.console, obj.color)
            libtcod.console_print_left(self.console, obj.x, obj.y, obj.color, obj.character)

    def draw_map(self, game_map):
        for x in xrange(len(game_map)):
            for y in range(len(game_map[x])):
                wall = game_map[x][y].block_sight
                if wall:
                    libtcod.console_set_back(self.console, x, y, color_dark_wall, libtcod.BKGND_SET)
                else:
                    libtcod.console_set_back(self.console, x, y, color_dark_ground, libtcod.BKGND_SET)

    def clear_objects(self, objects):
        for obj in objects:
            libtcod.console_print_left(self.console, obj.x, obj.y, libtcod.BKGND_NONE, ' ')

    def blit(self):
        libtcod.console_blit(self.console, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
        libtcod.console_flush()

    def step(self):
        objects = self.state.step()
        self.draw_objects(objects)
        self.draw_map(self.state.game_map)
        self.blit()
        self.clear_objects(objects)
        self.handle_keys()

    def handle_keys(self):
        key = libtcod.console_wait_for_keypress(True)
        if key.vk == libtcod.KEY_ESCAPE:
            self.exit = True
            return
        if key.vk == libtcod.KEY_ENTER and libtcod.KEY_ALT:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        player = self.state.player
        game_map = self.state.game_map
        if libtcod.console_is_key_pressed(libtcod.KEY_UP):
            player.move((0, -1), game_map)
        elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
            player.move((0, 1), game_map)
        elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
            player.move((-1, 0), game_map)
        elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
            player.move((1, 0), game_map)


screen = Screen()

while not libtcod.console_is_window_closed() and not screen.exit:
    screen.step()
