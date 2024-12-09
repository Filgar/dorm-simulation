from typing import List

import display_config as dconfig
import config as config
from core.elements.student import Student


class StudentPosition:
    def __init__(self, x, y, occupant, owner):
        self.x = x
        self.y = y
        self.occupant = occupant
        self.owner = owner



class Room:
    def __init__(self, x, y, number: int, side="LEFT"):
        self.x = x
        self.y = y
        self.number: int = number
        self.party_ongoing = False

        if side=="LEFT":
            list_beds = [(x + 1, y + dconfig.ROOM_HEIGHT - 4), (x + dconfig.BED_WIDTH + 3, y + dconfig.ROOM_HEIGHT - 4)]
            list_desks = [(x + 1, y + 1), (x + dconfig.BED_WIDTH + 3, y + 1)]
        else:
            list_beds = [(x + 4, y + dconfig.ROOM_HEIGHT - 4), (x + dconfig.ROOM_WIDTH - dconfig.BED_WIDTH - 1, y + dconfig.ROOM_HEIGHT - 4)]
            list_desks = [(x + 4, y + 1), (x + dconfig.ROOM_WIDTH - dconfig.BED_WIDTH - 1, y + 1)]

        self.beds: list = list_beds  # Bed positions
        self.desks: list = list_desks  # Desk positions
        self.party_pos = self.prepare_party_positions()
        self.rest_pos = self.prepare_resting_positions()
        self.learn_pos = self.prepare_learning_positions()

    def prepare_party_positions(self) -> List[StudentPosition]:
        positions = []
        for i in range(config.ROOM_PARTY_CAPACITY):
            positions.append(StudentPosition(self.x + 1 + (i * 2), self.y + dconfig.ROOM_HEIGHT / 2 - 1, False, None))
        return positions
    
    def prepare_resting_positions(self) -> List[StudentPosition]:
        return [
            StudentPosition(self.beds[0][0] + 2, self.beds[0][1] + 0.5, False, None),
            StudentPosition(self.beds[1][0] + 2, self.beds[1][1] + 0.5, False, None)
        ]
    
    def prepare_learning_positions(self) -> List[StudentPosition]:
        return [
            StudentPosition(self.desks[0][0] + 1, self.desks[0][1] + 1, False, None),
            StudentPosition(self.desks[0][0] + 4, self.desks[0][1] + 1, False, None),
            StudentPosition(self.desks[1][0] + 1, self.desks[1][1] + 1, False, None),
            StudentPosition(self.desks[1][0] + 4, self.desks[1][1] + 1, False, None)
        ]
    
    def set_bed_owner(self, student: Student) -> None:
        for pos in self.rest_pos:
            if pos.owner is None:
                pos.owner = student
                return
        raise Exception("No free bed is left in the room")
    
    def set_desk_owner(self, student: Student) -> None:
        owned_indexes = [0, 2]      # Quite dirty hack to give separate desk for each student

        for i in owned_indexes:
            if self.learn_pos[i].owner is None:
                self.learn_pos[i].owner = student
                return
        raise Exception("No free desk is left in the room")

    def get_resting_position(self, student: Student) -> StudentPosition:
        if student.native_room.number != self.number:
            return False # No resting position available, student must go back or sleep on the floor
        
        for pos in self.rest_pos:
            if pos.owner.name == student.name:
                pos.occupied = True
                return pos
        raise Exception("No resting position available")

    def get_learning_position(self, student: Student) -> StudentPosition:
        if student.native_room.number == self.number:
            for pos in self.learn_pos:
                if pos.owner is not None and pos.owner.name == student.name:
                    pos.occupied = True
                    return pos
        else:
            for pos in self.learn_pos:
                if not pos.occupied and pos.owner.name is None:
                    pos.occupied = True
                    return pos
        raise Exception("No learning position available")

    def get_partying_position(self) -> StudentPosition:
        for pos in self.party_pos:
            if not pos.occupied:    # Party position is never owned
                pos.occupied = True
                return pos
        raise Exception("No party position available")
    
    def reset_positions(self) -> None:
        for pos in self.party_pos:
            pos.occupied = False
        for pos in self.rest_pos:
            pos.occupied = False
        for pos in self.learn_pos:
            pos.occupied = False
    
