import libtcodpy as libtcod
from State import State

#colors
color_dark_wall = libtcod.Color(0, 0, 100)
color_light_wall = libtcod.Color(130, 110, 50)
color_dark_ground = libtcod.Color(50, 50, 150)
color_light_ground = libtcod.Color(200, 180, 50)


class Screen:
    """docstring for Screen"""
    def __init__(self, screen_width, screen_height, map_width, map_height, fps_limit, start_fullscreen, font):
        libtcod.console_set_custom_font(font, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
        libtcod.console_init_root(screen_width, screen_height, 'pyrogue', start_fullscreen)
        self.screen_width = screen_width
        self.screen_height = screen_height
        # self.map_width = map_width
        # self.map_height = map_height
        self.fps_limit = fps_limit
        self.start_fullscreen = start_fullscreen
        self.font = font
        self.console = libtcod.console_new(screen_width, screen_height)
        self.state = State(map_width, map_height)
        self.fov_map = self.build_fov_map()
        self.fov_recompute = True
        self.exit = False
        # self.step()

    def build_fov_map(self):
        game_map = self.state.game_map
        map_width, map_height = len(game_map), len(game_map[0])
        fov_map = libtcod.map_new(map_width, map_height)
        for x in range(map_width):
            for y in range(map_height):
                libtcod.map_set_properties(fov_map, x, y, not game_map[x][y].block_sight, not game_map[x][y].block_move)
        return fov_map

    def compute_fov(self):
        FOV_ALGO = 0  # default FOV algorithm
        FOV_LIGHT_WALLS = True
        TORCH_RADIUS = 10
        self.fov_recompute = True
        player = self.state.player
        libtcod.map_compute_fov(self.fov_map, player.x, player.y, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)

    def draw_objects(self, objects):
        for obj in objects:
            if libtcod.map_is_in_fov(self.fov_map, obj.x, obj.y):
                libtcod.console_set_foreground_color(self.console, obj.color)
                libtcod.console_print_left(self.console, obj.x, obj.y, obj.color, obj.character)

    def draw_map(self, game_map):
        for x in xrange(len(game_map)):
            for y in range(len(game_map[x])):
                visible = libtcod.map_is_in_fov(self.fov_map, x, y)
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

    def clear_objects(self, objects):
        for obj in objects:
            libtcod.console_print_left(self.console, obj.x, obj.y, libtcod.BKGND_NONE, ' ')

    def blit(self):
        libtcod.console_blit(self.console, 0, 0, self.screen_width, self.screen_height, 0, 0, 0)
        libtcod.console_flush()

    def step(self):
        if self.fov_recompute:
            self.compute_fov()
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
        elif key.vk == libtcod.KEY_ENTER and libtcod.KEY_ALT:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
        elif key.vk == libtcod.KEY_CONTROL and ord('s'):
            libtcod.sys_save_screenshot()

        player = self.state.player
        if libtcod.console_is_key_pressed(libtcod.KEY_UP):
            self.move_player(player, (0, -1))
        elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
            self.move_player(player, (0, 1))
        elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
            self.move_player(player, (-1, 0))
        elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
            self.move_player(player, (1, 0))

    def move_player(self, player, direction):
        if player.move(direction, self.state):
            self.fov_recompute = True

