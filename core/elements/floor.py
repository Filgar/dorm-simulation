from typing import List
import json
import numpy as np

import display_config as dconfig
import config as config
from core.elements.room import Room
from core.elements.student import Student, StudentState

class Floor:
    def __init__(self, level: int):
        self.level: int = level
        self.rooms: List[Room] = self.generate_rooms()
        self.students: List[Student] = self.generate_students()

    def __iter__(self):
        return iter(self.students)

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
        students_json = self.parse_population_json()
        already_generated_students = self.level * config.ROOMS_PER_FLOOR * 2

        for i, room in enumerate(self.rooms):
            if len(students_json) > already_generated_students:
                students.append(Student(students_json[already_generated_students]['student_name'], room,
                                        learning_rate=students_json[already_generated_students]['learning_rate'],
                                        resting_rate=students_json[already_generated_students]['resting_rate'],
                                        stamina_rate=students_json[already_generated_students]['stamina_rate'],
                                        eagerness_to_party=students_json[already_generated_students]['eagerness_to_party'],
                                        image_dir=students_json[already_generated_students]['image_dir']))
                already_generated_students += 1

                students.append(Student(students_json[already_generated_students]['student_name'], room,
                                        learning_rate=students_json[already_generated_students]['learning_rate'],
                                        resting_rate=students_json[already_generated_students]['resting_rate'],
                                        stamina_rate=students_json[already_generated_students]['stamina_rate'],
                                        eagerness_to_party=students_json[already_generated_students]['eagerness_to_party'],
                                        image_dir=students_json[already_generated_students]['image_dir'])
                                if len(students_json) > already_generated_students
                                else Student(f"Student2_room{i+1}_floor{self.level+1}", room))
                already_generated_students += 1
            else:
                students.append(Student(f"Student1_room{i+1}_floor{self.level+1}", room))
                students.append(Student(f"Student2_room{i+1}_floor{self.level+1}", room))
        return students
    

    def room_walls(self) -> set:
        walls = set()
        for room in self.rooms:
            x, y = room.x, room.y
            for i in range(dconfig.ROOM_WIDTH):
                walls.add((y, x + i))  # Top wall
                walls.add((y + dconfig.ROOM_HEIGHT - 1, x + i))  # Bottom wall
            for j in range(dconfig.ROOM_HEIGHT):
                walls.add((y + j, x))  # Left wall
                walls.add((y + j, x + dconfig.ROOM_WIDTH - 1))  # Right wall
        return walls
    
    
    def get_students_in_room(self, room: Room) -> List[Student]:
        return [s for s in self.students if s.current_room == room]
    
    def get_room_owners(self, room: Room) -> List[Student]:
        return [s for s in self.students if s.native_room == room]
    
    def get_active_students(self) -> List[Student]:
        return [s for s in self.students if not s.dropout]
    
    
    def partying_neighbours_count(self, room: Room) -> bool:
        count = 0
        for neighbour in self.get_neighbouring_rooms(room):
            count += self.room_partying_count(neighbour)
        return count
    
    def get_neighbouring_rooms(self, room: Room) -> List[Room]:
        if room.number > config.ROOMS_PER_FLOOR // 2:
            if room.number == config.ROOMS_PER_FLOOR // 2:
                return [next(r for r in self.rooms if r.number == room.number + 1)]
            elif room.number == config.ROOMS_PER_FLOOR - 1:
                return [next(r for r in self.rooms if r.number == room.number - 1)]
            else:
                return [
                    next(r for r in self.rooms if r.number == room.number - 1),
                    next(r for r in self.rooms if r.number == room.number + 1)
                ]
        else:
            if room.number == 0:
                return [next(r for r in self.rooms if r.number == room.number + 1)]
            elif room.number == config.ROOMS_PER_FLOOR // 2 - 1:
                return [next(r for r in self.rooms if r.number == room.number - 1)]
            else:
                return [
                    next(r for r in self.rooms if r.number == room.number - 1),
                    next(r for r in self.rooms if r.number == room.number + 1)
                ]
            
    def find_partying_place(self) -> Room:
        partying_rooms = [r for r in self.rooms if self.room_is_partying(r) and not self.room_partying_count(r) >= config.ROOM_PARTY_CAPACITY]
        if len(partying_rooms) == 0:
            return None
        
        weights = [self.room_partying_count(r)*24 for r in partying_rooms] #squared so hardly prefer bigger parties
        return np.random.choice(partying_rooms, p=weights/np.sum(weights))

    def room_partying_count(self, room: Room) -> int:
        return len([s for s in self.get_students_in_room(room) if s.state == StudentState.PARTYING])
    
    def room_is_partying(self, room: Room) -> int: # Returns number of students partying in the room
        return self.room_partying_count(room) > 0
    
    def parse_population_json(self):
        file_path = config.POPULATION_FILE

        with open(file_path, 'r') as file:
            students = json.load(file)

        return students
