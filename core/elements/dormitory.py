from core.elements.student import Student
from core.elements.floor import Floor
import display_config as config

class Dormitory:
    def __init__(self, num_floors, num_rooms_per_floor):
        self.num_floors = num_floors
        self.floors = [Floor(config.ROWS, config.COLS, num_rooms_per_floor) for _ in range(num_floors)]
        self.current_floor = 0
        self.selected_room = None  # Add this to track the selected room


        self.students = \
            [Student(f"Student1_room{room+1}_floor{floor+1}", room, floor) for floor in range(num_floors) for room in range(num_rooms_per_floor)] + \
            [Student(f"Student2_room{room+1}_floor{floor+1}", room, floor) for floor in range(num_floors) for room in range(num_rooms_per_floor)]
        


    def switch_floor(self, floor_number):
        if 0 <= floor_number < self.num_floors:
            self.current_floor = floor_number
            self.selected_room = None  # Reset the selected room when switching floors

    def select_room(self, room_number):
        if 0 <= room_number < len(self.floors[self.current_floor].rooms):
            self.selected_room = room_number