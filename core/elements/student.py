from enum import Enum
import pygame
import random

import display_config as dconfig

class Student:
    def __init__(self, name: str, room: 'Room', learning_rate: float = None, resting_rate: float = None,
                stamina_rate: float = None, eagerness_to_party: float = None, image_dir: str = None):
        self.name: str = name
        self.native_room: 'Room' = room             # See PEP 484/forward references
        self.current_room: 'Room' = room
        self.dropout = False

        self.knowledge = 0
        self.energy = 0.5
        self.fun = 0.5

        get_rate = lambda rate: max(0.05, min(random.gauss(rate, 0.25), 1)) if rate is not None else max(0.05, min(random.gauss(0.5, 0.25), 1))

        self.base_learning_rate = get_rate(learning_rate)     # Base values - dependant on the student, never changes
        self.base_resting_rate = get_rate(resting_rate)
        self.stamina_rate = get_rate(stamina_rate)
        self.eagerness_to_party_base = get_rate(eagerness_to_party)
                                        
        self.learning_rate = self.base_learning_rate          # Dynamically affected by other agents
        self.resting_rate = self.base_resting_rate
        self.eagerness_to_party = get_rate(eagerness_to_party)

        self.time_partying = 0
        self.time_learning = 0
        self.time_resting = 0
        self.party_overdose = 0
        self.exam_sessions_survived = 0



        self.photo = image_dir
        self.state: StudentState = StudentState.RESTING

        room.set_bed_owner(self)
        room.set_desk_owner(self)

    def validate_rates(self) -> None:
        self.learning_rate = max(0.05, min(1, self.learning_rate))
        self.resting_rate = max(0.05, min(1, self.resting_rate))
        self.eagerness_to_party = max(0.05, min(1, self.eagerness_to_party))

    def validate_values(self) -> None:
        self.energy = max(0, min(1, self.energy))
        self.knowledge = max(0, min(1, self.knowledge))
        self.fun = max(0, min(1, self.fun))


    def get_older(self) -> None:
        self.eagerness_to_party *= 0.9      # As the time goes, students are less eager to party, get tired faster, but posess more knowledge
        self.stamina_rate *= 0.9
        self.knowledge = self.exam_sessions_survived * 0.05




class StudentState(Enum):
    PARTYING = 0
    RESTING = 1
    LEARNING = 2


class StudentDataModel:
    name: str
    learning_rate_bias: float
    resting_rate_bias: float
    stamina_rate_bias: float
    eager_to_party_bias: float
    photo: str
