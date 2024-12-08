import display_config as config
from core.elements.room import Room

class Floor:
    def __init__(self, rows, cols, num_rooms):
        self.rows = rows
        self.cols = cols
        self.num_rooms = num_rooms
        self.rooms = []
        self.generate_rooms()

    def generate_rooms(self):
        x, y = 0, 0  # Start room placement
        rooms_left = 0
        
        for i in range(self.num_rooms):
            if y + config.ROOM_HEIGHT <= self.rows:
                self.rooms.append(Room(x, y))
                y += config.ROOM_HEIGHT-1
            else:
                rooms_left = self.num_rooms - i
                break
                
        x, y = self.cols - config.ROOM_WIDTH, 0
        for i in range(rooms_left):
            if y + config.ROOM_HEIGHT <= self.rows:
                self.rooms.append(Room(x, y, "RIGHT"))
                y += config.ROOM_HEIGHT-1

        # DRAW IN MANAGER

        # Draw rooms
        # for room in self.rooms:
        #     room.draw(screen)

    def room_walls(self):
        walls = set()
        for room in self.rooms:
            x, y = room.x, room.y
            # Add the walls of the room
            for i in range(config.ROOM_WIDTH):
                walls.add((y, x + i))  # Top wall
                walls.add((y + config.ROOM_HEIGHT - 1, x + i))  # Bottom wall
            for j in range(config.ROOM_HEIGHT):
                walls.add((y + j, x))  # Left wall
                walls.add((y + j, x + config.ROOM_WIDTH - 1))  # Right wall
        return walls