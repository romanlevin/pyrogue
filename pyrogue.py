#Following the libtcod tutorial on Rogue Basin.

import libtcodpy as libtcod
from Screen import Screen

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
MAP_WIDTH = 80
MAP_HEIGHT = 45
FPS_LIMIT = 20
START_FULLSCREEN = False
FONT = 'arial10x10.png'


screen = Screen(SCREEN_WIDTH, SCREEN_HEIGHT, MAP_WIDTH, MAP_HEIGHT, FPS_LIMIT, START_FULLSCREEN, FONT)

while not libtcod.console_is_window_closed() and not screen.exit:
    screen.step()
