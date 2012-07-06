#Following the libtcod tutorial on Rogue Basin.

import libtcodpy as libtcod

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
FPS_LIMIT = 20
START_FULLSCREEN = False
FONT = 'arial10x10.png'

libtcod.console_set_custom_font(FONT, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'pyrogue', START_FULLSCREEN)


class Player(object):
    """docstring for player"""
    def __init__(self, x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2, character='@'):
        self.x = x
        self.y = y
        self.character = character

    def move(self, (x, y)):
        self.x += x
        self.y += y

    def position(self):
        return (self.x, self.y)


class State(object):
    """docstring for State"""
    def __init__(self):
        self.player = Player()
        self.exit = False

    def handle_keys(self):
        key = libtcod.console_wait_for_keypress(True)
        if key.vk == libtcod.KEY_ESCAPE:
            self.exit = True
            return

        if libtcod.console_is_key_pressed(libtcod.KEY_UP):
            self.player.move((0, -1))
        elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
            self.player.move((0, 1))
        elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
            self.player.move((-1, 0))
        elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
            self.player.move((1, 0))

    def step(self):
        player = self.player
        libtcod.console_set_foreground_color(0, libtcod.white)
        libtcod.console_print_left(0, player.x, player.y, libtcod.BKGND_NONE, player.character)
        libtcod.console_flush()
        libtcod.console_print_left(0, player.x, player.y, libtcod.BKGND_NONE, ' ')
        self.handle_keys()


state = State()

while not libtcod.console_is_window_closed() and not state.exit:
    state.step()
