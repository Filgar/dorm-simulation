from enum import Enum
import pygame

import display_config as dconfig

class Student:
    def __init__(self, name: str, room: 'Room', learned_ratio = 0, energy_ratio = 100): # See PEP 484/forward references
        self.name: str = name
        self.native_room: 'Room' = room
        self.current_room: 'Room' = room
        self.learned_ratio = learned_ratio
        self.energy_ratio = energy_ratio
        self.photo = None
        self.state: StudentState = StudentState.RESTING

        room.set_bed_owner(self)
        room.set_desk_owner(self)
        self.update_photo()


    def update_photo(self) -> None:
        if self.state == StudentState.RESTING:
            self.photo = pygame.image.load(dconfig.STUDENT_PHOTO_REST)
        elif self.state == StudentState.PARTYING:
            self.photo = pygame.image.load(dconfig.STUDENT_PHOTO_PARTY)
        elif self.state == StudentState.SLEEPING:
            self.photo = pygame.image.load(dconfig.STUDENT_PHOTO_LEARN)
        else:
            raise Exception("State of the student is unknown")

class StudentState(Enum):
    PARTYING = 0
    RESTING = 1
    SLEEPING = 2