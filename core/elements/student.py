import display_config as config
import pygame

class Student:
    def __init__(self, name, room_number, floor_number, learned_ratio = 0, energy_ratio = 100):
        self.name = name
        self.room_number = room_number
        self.floor_number = floor_number
        self.learned_ratio = learned_ratio
        self.energy_ratio = energy_ratio
        self.photo = pygame.image.load(config.STUDENT_PHOTO)