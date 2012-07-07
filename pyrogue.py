#Following the libtcod tutorial on Rogue Basin.

import libtcodpy as libtcod

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
FPS_LIMIT = 20
START_FULLSCREEN = False
FONT = 'arial10x10.png'


class GameObject(object):
    """docstring for GameObject"""
    def __init__(self, x, y, character, color):
        self.x = x
        self.y = y
        self.character = character
        self.color = color

    def move(self, (x, y)):
        self.x += x
        self.y += y

    def position(self):
        return (self.x, self.y)


class Player(GameObject):
    """docstring for Player"""


class State(object):
    """docstring for State"""
    def __init__(self):
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, '@', libtcod.white)
        npc = GameObject(SCREEN_WIDTH / 2 + 5, SCREEN_HEIGHT / 2, '@', libtcod.yellow)
        self.objects = set([self.player, npc])
        self.exit = False

    def step(self):
        return self.objects


class Screen(object):
    """docstring for Screen"""
    def __init__(self):
        libtcod.console_set_custom_font(FONT, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
        libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'pyrogue', START_FULLSCREEN)
        self.con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.state = State()
        self.exit = False

    def draw_objects(self, objects):
        for obj in objects:
            libtcod.console_set_foreground_color(self.con, obj.color)
            libtcod.console_print_left(self.con, obj.x, obj.y, obj.color, obj.character)

    def clear_objects(self, objects):
        for obj in objects:
            libtcod.console_print_left(self.con, obj.x, obj.y, libtcod.BKGND_NONE, ' ')

    def blit(self):
        libtcod.console_blit(self.con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
        libtcod.console_flush()

    def step(self):
        objects = self.state.step()
        self.draw_objects(objects)
        self.blit()
        self.clear_objects(objects)
        self.handle_keys()

    def handle_keys(self):
        key = libtcod.console_wait_for_keypress(True)
        if key.vk == libtcod.KEY_ESCAPE:
            self.exit = True
            return

        player = self.state.player
        if libtcod.console_is_key_pressed(libtcod.KEY_UP):
            player.move((0, -1))
        elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
            player.move((0, 1))
        elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
            player.move((-1, 0))
        elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
            player.move((1, 0))


state = State()
screen = Screen()

while not libtcod.console_is_window_closed() and not screen.exit:
    screen.step()
