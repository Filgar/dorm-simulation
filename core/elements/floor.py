import display_config as config
from core.elements.room import Room
from core.elements.student import Student

class Floor:
    def __init__(self, rows, cols, num_rooms, level):
        self.rows = rows
        self.cols = cols
        self.num_rooms = num_rooms
        self.level = level
        self.rooms = self.generate_rooms()
        self.students = self.generate_students()

    def generate_rooms(self):
        x, y = 0, 0  # Start room placement
        rooms_left = 0
        rooms = []

        for i in range(self.num_rooms):
            if y + config.ROOM_HEIGHT <= self.rows:
                rooms.append(Room(x, y, i))
                y += config.ROOM_HEIGHT-1
            else:
                rooms_left = self.num_rooms - i
                break
                
        x, y = self.cols - config.ROOM_WIDTH, 0
        for j in range(rooms_left):
            if y + config.ROOM_HEIGHT <= self.rows:
                rooms.append(Room(x, y, i+j, "RIGHT"))
                y += config.ROOM_HEIGHT-1
        return rooms
    
    def generate_students(self):
        students = []
        for i, room in enumerate(self.rooms):
            students.append(Student(f"Student1_room{i+1}_floor{self.level+1}", room))
            students.append(Student(f"Student2_room{i+1}_floor{self.level+1}", room))
        return students
    

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