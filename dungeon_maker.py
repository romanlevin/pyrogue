import libtcodpy as libtcod


class Tile:
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


class DungeonMaker:
    @staticmethod
    def make_map(MAP_WIDTH, MAP_HEIGHT, player):
        game_map = [[Tile(True) for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]
        DungeonMaker.populate_rooms(game_map, MAP_WIDTH, MAP_HEIGHT, player)
        return game_map

    @staticmethod
    def populate_rooms(game_map, MAP_WIDTH, MAP_HEIGHT, player):
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
                DungeonMaker.create_room(game_map, new_room)
                room_center = new_room.center()
                number_of_rooms = len(rooms)
                if number_of_rooms == 0:
                    player.set_location(room_center)
                else:
                    previous_x, previous_y = rooms[number_of_rooms - 1].center()
                    current_x, current_y = room_center
                    if libtcod.random_get_int(0, 0, 1) == 0:
                        DungeonMaker.create_horizontal_tunnel(game_map, previous_x, current_x, previous_y)
                        DungeonMaker.create_vertical_tunnel(game_map, previous_y, current_y, current_x)
                    else:
                        DungeonMaker.create_horizontal_tunnel(game_map, previous_x, current_x, current_y)
                        DungeonMaker.create_vertical_tunnel(game_map, previous_y, current_y, previous_x)
                rooms.append(new_room)

    @staticmethod
    def create_room(game_map, rectangle):
        for x in range(rectangle.x1 + 1, rectangle.x2):
            for y in range(rectangle.y1 + 1, rectangle.y2):
                game_map[x][y].set_floor()

    @staticmethod
    def create_horizontal_tunnel(game_map, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            game_map[x][y].set_floor()

    @staticmethod
    def create_vertical_tunnel(game_map, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            game_map[x][y].set_floor()
