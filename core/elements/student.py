from enum import Enum
import pygame
import random

import display_config as dconfig

class Student:
    def __init__(self, name: str, room: 'Room', learning_rate: float = random.random(), resting_rate: float = random.random(),
                stamina_rate: float = random.random(), eagerness_to_party: float = random.random()):
        self.name: str = name
        self.native_room: 'Room' = room             # See PEP 484/forward references
        self.current_room: 'Room' = room

        self.knowledge = 0
        self.energy = 0.5

        self.base_learning_rate = learning_rate     # Base values - dependant on the student, never changes
        self.base_resting_rate = resting_rate
        self.base_stamina_rate = stamina_rate

        self.learning_rate = learning_rate          # Dynamically affected by other agents
        self.stamina_rate = stamina_rate
        self.resting_rate = resting_rate

        self.eagerness_to_party = eagerness_to_party

        self.time_partying = 0
        self.time_learning = 0
        self.time_resting = 0



        self.photo = None
        self.state: StudentState = StudentState.RESTING

        room.set_bed_owner(self)
        room.set_desk_owner(self)

    def validate_values(self) -> None:
        self.learning_rate = max(0, min(self.base_learning_rate, self.learning_rate))
        self.stamina_rate = max(0, min(self.base_stamina_rate, self.stamina_rate))
        self.resting_rate = max(0, min(self.base_resting_rate, self.resting_rate))
        self.energy = max(0, min(1, self.energy))
        self.knowledge = max(0, min(1, self.knowledge))

        

class StudentState(Enum):
    PARTYING = 0
    RESTING = 1
    LEARNING = 2