import libtcodpy as libtcod
from Monster import Monster


class Tile(object):
    def __init__(self, block_move, block_sight=None):
        self.block_move = block_move
        self.block_sight = block_sight if block_sight else block_move
        self.explored = False

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

    def explore(self):
        self.explored = True


class Rectangle(object):
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


class DungeonMaker(object):
    def __init__(self, state):
        self.state = state

    def make_map(self):
        map_height = self.state.map_height
        map_width = self.state.map_width
        self.game_map = [[Tile(True) for y in range(map_height)] for x in range(map_width)]
        self.populate_rooms()
        return self.game_map

    def populate_rooms(self):
        ROOM_MAX_SIZE = 10
        ROOM_MIN_SIZE = 6
        MAX_ROOMS = 30

        map_width = self.state.map_width
        map_height = self.state.map_height
        rooms = []
        for room in range(MAX_ROOMS):
            w = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            h = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            x = libtcod.random_get_int(0, 0, map_width - w - 1)
            y = libtcod.random_get_int(0, 0, map_height - h - 1)
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
                    self.state.player.set_location(room_center)
                else:
                    previous_x, previous_y = rooms[number_of_rooms - 1].center()
                    current_x, current_y = room_center
                    if libtcod.random_get_int(0, 0, 1) == 0:
                        self.create_horizontal_tunnel(previous_x, current_x, previous_y)
                        self.create_vertical_tunnel(previous_y, current_y, current_x)
                    else:
                        self.create_horizontal_tunnel(previous_x, current_x, current_y)
                        self.create_vertical_tunnel(previous_y, current_y, previous_x)
                    self.place_objects(new_room)
                rooms.append(new_room)

    def create_room(self, rectangle):
        game_map = self.game_map
        for x in range(rectangle.x1 + 1, rectangle.x2):
            for y in range(rectangle.y1 + 1, rectangle.y2):
                game_map[x][y].set_floor()

    def create_horizontal_tunnel(self, x1, x2, y):
        game_map = self.game_map
        for x in range(min(x1, x2), max(x1, x2) + 1):
            game_map[x][y].set_floor()

    def create_vertical_tunnel(self, y1, y2, x):
        game_map = self.game_map
        for y in range(min(y1, y2), max(y1, y2) + 1):
            game_map[x][y].set_floor()

    def place_objects(self, room):
        MAX_MONSTERS_IN_ROOM = 3
        state = self.state
        num_monsters = libtcod.random_get_int(0, 0, MAX_MONSTERS_IN_ROOM)
        for i in range(num_monsters):
            x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
            y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)
            die_throw = libtcod.random_get_float(0, 0, 1)
            if die_throw < 0.8:
                monster = Monster(state, (x, y), 'orc', 'o', libtcod.desaturated_green, hp=10, defense=0, power=3)
            else:
                monster = Monster(state, (x, y), 'troll', 'T', libtcod.darker_green, hp=13, defense=1, power=5)
            state.objects.add(monster)

