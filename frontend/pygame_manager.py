import pygame
import random

import display_config as dconfig
import config as config
from frontend.user_panel import UserPanel
from frontend.leaderboard import Leaderboard
from core.elements.student import StudentState

class PygameManager:

    PHOTO_REST = pygame.image.load(dconfig.STUDENT_PHOTO_REST)
    PHOTO_PARTY = pygame.image.load(dconfig.STUDENT_PHOTO_PARTY)
    PHOTO_LEARN = pygame.image.load(dconfig.STUDENT_PHOTO_LEARN)

    def __init__(self, initial_tick):
        pygame.init()

        self.screen = pygame.display.set_mode((dconfig.SCREEN_WIDTH, dconfig.SCREEN_HEIGHT))
        pygame.display.set_caption("Dormitory")

        PygameManager.PHOTO_REST = PygameManager.PHOTO_REST.convert()
        PygameManager.PHOTO_PARTY = PygameManager.PHOTO_PARTY.convert()
        PygameManager.PHOTO_LEARN = PygameManager.PHOTO_LEARN.convert()


        self.user_panel = UserPanel(initial_tick)
        self.leaderboard = Leaderboard()

        self.tick = initial_tick

    def draw_room(self, room):
        for bx, by in room.beds:
            pygame.draw.rect(self.screen, dconfig.WHITE, (bx * dconfig.TILE_SIZE + dconfig.LEADERBOARD, by * dconfig.TILE_SIZE, dconfig.TILE_SIZE * dconfig.BED_WIDTH, dconfig.TILE_SIZE * 3))
            pygame.draw.rect(self.screen, dconfig.RED, (bx * dconfig.TILE_SIZE + dconfig.LEADERBOARD, (by+0.5) * dconfig.TILE_SIZE, dconfig.TILE_SIZE*1.5, dconfig.TILE_SIZE*2))
        for dx, dy in room.desks:
            pygame.draw.rect(self.screen, dconfig.BLACK, (dx * dconfig.TILE_SIZE + dconfig.LEADERBOARD, dy * dconfig.TILE_SIZE, dconfig.TILE_SIZE * 6, dconfig.TILE_SIZE * 2))
    

    def draw_dormitory(self, dormitory):
        floor = dormitory.floors[dormitory.current_floor]
        self.draw_floor(floor)

        for room in floor.rooms:
            self.draw_room(room)
            room.reset_positions()

        for student in floor.get_active_students():
            self.draw_student(student)

    def draw_student(self, student):
        room = student.current_room
        student_img = pygame.transform.scale(self.get_student_photo(student), (dconfig.TILE_SIZE * 1.8, dconfig.TILE_SIZE * 1.5))
        position = self.get_student_position(room, student)
        self.screen.blit(student_img, (position.x * dconfig.TILE_SIZE + dconfig.LEADERBOARD, position.y * dconfig.TILE_SIZE))
    
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

    def draw_floor(self, floor):
        for row in range(dconfig.ROWS):
            for col in range(dconfig.COLS):
                color = dconfig.LIGHT_BROWN if (row, col) not in floor.room_walls() else dconfig.LIGHT_GRAY
                pygame.draw.rect(self.screen, color, (col * dconfig.TILE_SIZE + dconfig.LEADERBOARD, row * dconfig.TILE_SIZE, dconfig.TILE_SIZE, dconfig.TILE_SIZE))
                pygame.draw.rect(self.screen, dconfig.BLACK, (col * dconfig.TILE_SIZE + dconfig.LEADERBOARD, row * dconfig.TILE_SIZE, dconfig.TILE_SIZE, dconfig.TILE_SIZE), 1)

    def draw(self, dormitory, time, difficulty):
        self.screen.fill(dconfig.BLACK)
        self.draw_dormitory(dormitory)
        self.user_panel.draw(self.screen, dormitory, time, difficulty)
        self.leaderboard.draw(self.screen, dormitory)
        pygame.display.flip()


    def handle_keydown(self, event, dormitory):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.user_panel.input_r_arrow_speed.collidepoint(mouse_pos):
                self.tick = self.user_panel.update_tick(1)
            elif self.user_panel.input_l_arrow_speed.collidepoint(mouse_pos):
                self.tick = self.user_panel.update_tick(-1)
            elif self.user_panel.input_r_arrow_floor.collidepoint(mouse_pos):
                dormitory.switch_floor(dormitory.current_floor + 1)
            elif self.user_panel.input_l_arrow_floor.collidepoint(mouse_pos):
                dormitory.switch_floor(dormitory.current_floor - 1)
            elif self.user_panel.input_r_arrow_room.collidepoint(mouse_pos):
                dormitory.select_room(dormitory.selected_room + 1)
            elif self.user_panel.input_l_arrow_room.collidepoint(mouse_pos):
                dormitory.select_room(dormitory.selected_room - 1)
            elif self.leaderboard.r_arrow_leaderboard.collidepoint(mouse_pos):
                self.leaderboard.switch_page(1)
            elif self.leaderboard.l_arrow_leaderboard.collidepoint(mouse_pos):
                self.leaderboard.switch_page(-1)
        return True

