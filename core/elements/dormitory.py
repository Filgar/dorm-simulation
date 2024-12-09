from typing import List

from core.elements.floor import Floor
from core.elements.room import Room
import display_config as dconfig
import config as config

class Dormitory:
    def __init__(self):
        self.num_floors: int = config.NUM_FLOORS
        self.floors: List[Floor] = [Floor(level) for level in range(self.num_floors)]
        self.current_floor: int = 0
        self.selected_room: Room = None  # Add this to track the selected room


    def switch_floor(self, floor_number: int) -> None:
        if 0 <= floor_number < self.num_floors:
            self.current_floor = floor_number
            self.selected_room = None  # Reset the selected room when switching floors

    def select_room(self, room_number: int) -> None:
        if 0 <= room_number < len(self.floors[self.current_floor].rooms):
            self.selected_room = room_number

    def clear_students_knowledge(self) -> None:
        for floor in self.floors:
            for student in floor.students:
                student.knowledge = 0