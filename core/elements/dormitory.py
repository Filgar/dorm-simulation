from typing import List

from core.elements.floor import Floor
from core.elements.room import Room
import config as config

class Dormitory:
    def __init__(self):
        self.num_floors: int = config.NUM_FLOORS
        self.floors: List[Floor] = [Floor(level) for level in range(self.num_floors)]
        self.current_floor: int = 0
        self.selected_room: int = 0


    def switch_floor(self, floor_number: int) -> None:
        if 0 <= floor_number < self.num_floors:
            self.current_floor = floor_number
            self.select_room(0)

    def select_room(self, room_number: int) -> None:
        if 0 < room_number < len(self.floors[self.current_floor].rooms):
            self.selected_room = room_number

    def finish_exam_session(self) -> None:
        self.clear_students_knowledge()
        self.pass_exams()

    def clear_students_knowledge(self) -> None:
        for floor in self.floors:
            for student in floor.get_active_students():
                student.knowledge = 0

    def pass_exams(self) -> None:
        for floor in self.floors:
            for student in floor.get_active_students():
                student.exam_sessions_survived += 1
                student.get_older()