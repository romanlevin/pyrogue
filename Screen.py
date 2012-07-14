import libtcodpy as libtcod
from State import State

#colors
color_dark_wall = libtcod.Color(0, 0, 100)
color_light_wall = libtcod.Color(130, 110, 50)
color_dark_ground = libtcod.Color(50, 50, 150)
color_light_ground = libtcod.Color(200, 180, 50)


class Screen(object):
    """docstring for Screen"""
    def __init__(self, screen_width, screen_height, map_width, map_height, fps_limit, start_fullscreen, font):
        libtcod.console_set_custom_font(font, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
        libtcod.console_init_root(screen_width, screen_height, 'pyrogue', start_fullscreen)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fps_limit = fps_limit
        self.console = libtcod.console_new(screen_width, screen_height)
        self.state = State(map_width, map_height)
        self.fov_recompute = True
        self.exit = False
        self.mode = 'playing'

    def step(self):
        if self.fov_recompute:
            self.state.compute_fov()
            self.fov_recompute = False
        self.draw_objects()
        self.draw_map()
        self.blit()
        self.clear_objects()
        player_action = self.handle_keys()
        if player_action == 'exit':
            self.exit = True
        elif player_action == "didnt-take-turn":
            pass

    def draw_objects(self):
        fov_map = self.state.fov_map
        for obj in self.state.objects:
            if libtcod.map_is_in_fov(fov_map, obj.x, obj.y):
                libtcod.console_set_foreground_color(self.console, obj.color)
                libtcod.console_print_left(self.console, obj.x, obj.y, obj.color, obj.character)

    def draw_map(self):
        game_map = self.state.game_map
        fov_map = self.state.fov_map
        for x in xrange(len(game_map)):
            for y in range(len(game_map[x])):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map[x][y].block_sight
                if not visible and game_map[x][y].explored:
                    if wall:
                        libtcod.console_set_back(self.console, x, y, color_dark_wall, libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_back(self.console, x, y, color_dark_ground, libtcod.BKGND_SET)
                elif visible:
                    if wall:
                        libtcod.console_set_back(self.console, x, y, color_light_wall, libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_back(self.console, x, y, color_light_ground, libtcod.BKGND_SET)
                    game_map[x][y].explore()

    def clear_objects(self):
        for obj in self.state.objects:
            libtcod.console_print_left(self.console, obj.x, obj.y, libtcod.BKGND_NONE, ' ')

    def blit(self):
        libtcod.console_blit(self.console, 0, 0, self.screen_width, self.screen_height, 0, 0, 0)
        libtcod.console_flush()

    def handle_keys(self):
        key = libtcod.console_wait_for_keypress(True)
        if key.vk == libtcod.KEY_ESCAPE:
            return 'exit'
        elif key.vk == libtcod.KEY_ENTER and libtcod.KEY_ALT:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
        elif key.vk == libtcod.KEY_CONTROL and ord('s'):
            libtcod.sys_save_screenshot()

        if self.mode == 'playing':
            if libtcod.console_is_key_pressed(libtcod.KEY_UP):
                self.move_player((0, -1))
                move = True
                return 'move'
            elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
                self.move_player((0, 1))
                move = True
                return 'move'
            elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
                self.move_player((-1, 0))
                move = True
                return 'move'
            elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
                self.move_player((1, 0))
                move = True
                return 'move'
        if move:
            return 'move'
        else:
            return "didnt-take-turn"

    def move_player(self, direction):
        if self.state.move_player(direction):
            self.fov_recompute = True
