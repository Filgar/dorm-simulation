import pygame

import display_config as dconfig
import config

from core.elements.student import StudentState

class DormitoryDrawer:

    PHOTO_REST = pygame.image.load(dconfig.STUDENT_PHOTO_REST)
    PHOTO_PARTY = pygame.image.load(dconfig.STUDENT_PHOTO_PARTY)
    PHOTO_LEARN = pygame.image.load(dconfig.STUDENT_PHOTO_LEARN)


    def __init__(self):
        DormitoryDrawer.PHOTO_REST = DormitoryDrawer.PHOTO_REST.convert()
        DormitoryDrawer.PHOTO_PARTY = DormitoryDrawer.PHOTO_PARTY.convert()
        DormitoryDrawer.PHOTO_LEARN = DormitoryDrawer.PHOTO_LEARN.convert()

    def draw_dormitory(self, screen, dormitory):
        floor = dormitory.floors[dormitory.current_floor]
        self.draw_floor(screen, floor)

        for room in floor.rooms:
            self.draw_room(screen, room)
            room.reset_positions()

        for student in floor.get_active_students():
            self.draw_student(screen, student)

    def draw_room(self, screen, room):
        for bx, by in room.beds:
            pygame.draw.rect(screen, dconfig.WHITE, (bx * dconfig.TILE_SIZE + dconfig.LEADERBOARD, by * dconfig.TILE_SIZE, dconfig.TILE_SIZE * dconfig.BED_WIDTH, dconfig.TILE_SIZE * 3))
            pygame.draw.rect(screen, dconfig.RED, (bx * dconfig.TILE_SIZE + dconfig.LEADERBOARD, (by+0.5) * dconfig.TILE_SIZE, dconfig.TILE_SIZE*1.5, dconfig.TILE_SIZE*2))
        for dx, dy in room.desks:
            pygame.draw.rect(screen, dconfig.BLACK, (dx * dconfig.TILE_SIZE + dconfig.LEADERBOARD, dy * dconfig.TILE_SIZE, dconfig.TILE_SIZE * 6, dconfig.TILE_SIZE * 2))
    

    def draw_dormitory(self, screen, dormitory):
        floor = dormitory.floors[dormitory.current_floor]
        self.draw_floor(screen, floor)

        for room in floor.rooms:
            self.draw_room(screen, room)
            room.reset_positions()

        for student in floor.get_active_students():
            self.draw_student(screen, student)

    def draw_student(self, screen, student):
        room = student.current_room
        student_img = pygame.transform.scale(self.get_student_photo(student), (dconfig.TILE_SIZE * 1.8, dconfig.TILE_SIZE * 1.5))
        position = self.get_student_position(room, student)
        screen.blit(student_img, (position.x * dconfig.TILE_SIZE + dconfig.LEADERBOARD, position.y * dconfig.TILE_SIZE))
    
    def get_student_photo(self, student):
        if student.photo is not None:
            return pygame.image.load(config.POPULATION_ASSETS_DIRECTORY + student.photo)
        else:
            if student.state == StudentState.RESTING:
                return self.PHOTO_REST
            elif student.state == StudentState.PARTYING:
                return self.PHOTO_PARTY
            elif student.state == StudentState.LEARNING:
                return self.PHOTO_LEARN
            else:
                raise Exception("Student state not recognized")

    def get_student_position(self, room, student):
        match student.state:
            case StudentState.RESTING:
                return room.get_resting_position(student)
            case StudentState.PARTYING:
                return room.get_partying_position()
            case StudentState.LEARNING:
                return room.get_learning_position(student)
            case _:
                raise Exception("Student is in a state that is impossible for us to understand with our mortal minds")

    def draw_floor(self, screen, floor):
        for row in range(dconfig.ROWS):
            for col in range(dconfig.COLS):
                color = dconfig.LIGHT_BROWN if (row, col) not in floor.room_walls() else dconfig.LIGHT_GRAY
                pygame.draw.rect(screen, color, (col * dconfig.TILE_SIZE + dconfig.LEADERBOARD, row * dconfig.TILE_SIZE, dconfig.TILE_SIZE, dconfig.TILE_SIZE))
                pygame.draw.rect(screen, dconfig.BLACK, (col * dconfig.TILE_SIZE + dconfig.LEADERBOARD, row * dconfig.TILE_SIZE, dconfig.TILE_SIZE, dconfig.TILE_SIZE), 1)
