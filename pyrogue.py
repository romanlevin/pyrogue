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

class Player(GameObject):
    """docstring for Player"""


class State:
    """docstring for State"""
    def __init__(self):
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, '@', libtcod.white)
        npc = GameObject(SCREEN_WIDTH / 2 + 5, SCREEN_HEIGHT / 2, '@', libtcod.yellow)
        self.objects = set([self.player, npc])
        self.exit = False
        self.game_map = self.make_map()

    def make_map(self):
        game_map = [[Tile(False) for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]
        game_map[30][30].set_wall()
        game_map[31][30].set_wall()
        game_map[32][30].set_wall()
        game_map[33][30].set_wall()
        return game_map

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


state = State()
screen = Screen()

while not libtcod.console_is_window_closed() and not screen.exit:
    screen.step()
