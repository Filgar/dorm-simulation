from typing import List

import display_config as dconfig
import config as config
from core.elements.room import Room
from core.elements.student import Student

class Floor:
    def __init__(self, level: int):
        self.level: int = level
        self.rooms: List[Room] = self.generate_rooms()
        self.students: List[Student] = self.generate_students()

    def generate_rooms(self) -> List[Student]:
        x, y = 0, 0  # Start room placement
        rooms_left = 0
        rooms = []

        for i in range(config.ROOMS_PER_FLOOR):
            if y + dconfig.ROOM_HEIGHT <= dconfig.ROWS:
                rooms.append(Room(x, y, i))
                y += dconfig.ROOM_HEIGHT-1
            else:
                rooms_left = config.ROOMS_PER_FLOOR - i
                break
                
        x, y = dconfig.COLS - dconfig.ROOM_WIDTH, 0
        for j in range(rooms_left):
            if y + dconfig.ROOM_HEIGHT <= dconfig.ROWS:
                rooms.append(Room(x, y, i+j, "RIGHT"))
                y += dconfig.ROOM_HEIGHT-1
        return rooms
    
    def generate_students(self) -> List[Student]:
        students = []
        for i, room in enumerate(self.rooms):
            students.append(Student(f"Student1_room{i+1}_floor{self.level+1}", room))
            students.append(Student(f"Student2_room{i+1}_floor{self.level+1}", room))
        return students
    

    def room_walls(self) -> set:
        walls = set()
        for room in self.rooms:
            x, y = room.x, room.y
            # Add the walls of the room
            for i in range(dconfig.ROOM_WIDTH):
                walls.add((y, x + i))  # Top wall
                walls.add((y + dconfig.ROOM_HEIGHT - 1, x + i))  # Bottom wall
            for j in range(dconfig.ROOM_HEIGHT):
                walls.add((y + j, x))  # Left wall
                walls.add((y + j, x + dconfig.ROOM_WIDTH - 1))  # Right wall
        return walls