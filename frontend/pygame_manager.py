import pygame
import display_config as dconfig

from frontend.user_panel import UserPanel
from core.elements.student import StudentState

class PygameManager:

    PHOTO_REST = pygame.image.load(dconfig.STUDENT_PHOTO_REST)
    PHOTO_PARTY = pygame.image.load(dconfig.STUDENT_PHOTO_PARTY)
    PHOTO_LEARN = pygame.image.load(dconfig.STUDENT_PHOTO_LEARN)

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((dconfig.SCREEN_WIDTH, dconfig.SCREEN_HEIGHT))
        pygame.display.set_caption("Dormitory")

        PygameManager.PHOTO_REST = PygameManager.PHOTO_REST.convert()
        PygameManager.PHOTO_PARTY = PygameManager.PHOTO_PARTY.convert()
        PygameManager.PHOTO_LEARN = PygameManager.PHOTO_LEARN.convert()


        self.user_panel = UserPanel()


    def draw_room(self, room):
        for bx, by in room.beds:
            pygame.draw.rect(self.screen, dconfig.WHITE, (bx * dconfig.TILE_SIZE, by * dconfig.TILE_SIZE, dconfig.TILE_SIZE * dconfig.BED_WIDTH, dconfig.TILE_SIZE * 3))
            pygame.draw.rect(self.screen, dconfig.RED, (bx * dconfig.TILE_SIZE, (by+0.5) * dconfig.TILE_SIZE, dconfig.TILE_SIZE*1.5, dconfig.TILE_SIZE*2))
        for dx, dy in room.desks:
            pygame.draw.rect(self.screen, dconfig.BLACK, (dx * dconfig.TILE_SIZE, dy * dconfig.TILE_SIZE, dconfig.TILE_SIZE * 6, dconfig.TILE_SIZE * 2))
    

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
        student_img = pygame.transform.scale(self.get_student_photo(student), (dconfig.TILE_SIZE * 1.5, dconfig.TILE_SIZE * 1.5))
        position = self.get_student_position(room, student)
        self.screen.blit(student_img, (position.x * dconfig.TILE_SIZE, position.y * dconfig.TILE_SIZE))
    
    def get_student_photo(self, student):
        if student.photo is not None:
            return pygame.image.load(dconfig.ASSETS_PATH + student.photo)
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
                pygame.draw.rect(self.screen, color, (col * dconfig.TILE_SIZE, row * dconfig.TILE_SIZE, dconfig.TILE_SIZE, dconfig.TILE_SIZE))
                pygame.draw.rect(self.screen, dconfig.BLACK, (col * dconfig.TILE_SIZE, row * dconfig.TILE_SIZE, dconfig.TILE_SIZE, dconfig.TILE_SIZE), 1)

    def draw(self, dormitory, time, difficulty):
        self.screen.fill(dconfig.BLACK)
        self.draw_dormitory(dormitory)
        self.user_panel.draw(self.screen, dormitory, time, difficulty)
        pygame.display.flip()


    def handle_keydown(self, event, dormitory):

        # TODO prettify this blasphemous code below
        if event.key == pygame.K_ESCAPE:
            return False
        elif event.key == pygame.K_SPACE:
            dormitory.next_turn()
        elif event.key == pygame.K_RETURN:  # Confirm floor or room change
            if self.user_panel.input_buffer.isdigit():
                floor_number = int(self.user_panel.input_buffer) - 1  # Floors are 1-indexed for user
                dormitory.switch_floor(floor_number)
                self.user_panel.input_buffer = ""  # Clear the buffer
            elif self.user_panel.room_input_buffer.isdigit():
                room_number = int(self.user_panel.room_input_buffer) - 1  # Rooms are 1-indexed for user
                dormitory.select_room(room_number)
                self.user_panel.room_input_buffer = ""  # Clear the buffer
        elif event.key == pygame.K_BACKSPACE:
            if self.user_panel.input_rect.collidepoint(pygame.mouse.get_pos()):
                self.user_panel.input_buffer = self.user_panel.input_buffer[:-1]
            elif self.user_panel.room_input_rect.collidepoint(pygame.mouse.get_pos()):
                self.user_panel.room_input_buffer = self.user_panel.room_input_buffer[:-1]
        else:
            if event.unicode.isdigit():
                if self.user_panel.input_rect.collidepoint(pygame.mouse.get_pos()):
                    self.user_panel.input_buffer += event.unicode
                elif self.user_panel.room_input_rect.collidepoint(pygame.mouse.get_pos()):
                    self.user_panel.room_input_buffer += event.unicode
        return True

