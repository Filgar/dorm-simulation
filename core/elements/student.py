import display_config as config
from core.elements.room import Room
import pygame

class Student:
    def __init__(self, name, room, learned_ratio = 0, energy_ratio = 100):
        self.name = name
        self.native_room = room
        self.current_room = room
        self.learned_ratio = learned_ratio
        self.energy_ratio = energy_ratio
        self.photo = pygame.image.load(config.STUDENT_PHOTO)