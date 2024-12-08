import pygame
import display_config as config

from frontend.user_panel import UserPanel

class PygameManager:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("Dormitory")

        self.user_panel = UserPanel()


    def draw_room(self, room):
        # Draw beds
        for bx, by in room.beds:
            pygame.draw.rect(self.screen, config.WHITE, (bx * config.TILE_SIZE, by * config.TILE_SIZE, config.TILE_SIZE * config.BED_WIDTH, config.TILE_SIZE * 3))
            pygame.draw.rect(self.screen, config.RED, (bx * config.TILE_SIZE, (by+0.5) * config.TILE_SIZE, config.TILE_SIZE*1.5, config.TILE_SIZE*2))
        # Draw desks
        for dx, dy in room.desks:
            pygame.draw.rect(self.screen, config.BLACK, (dx * config.TILE_SIZE, dy * config.TILE_SIZE, config.TILE_SIZE * 6, config.TILE_SIZE * 2))
    

    def draw_dormitory(self, dormitory):
        # Draw the current floor
        self.draw_floor(dormitory.floors[dormitory.current_floor])

        for room in dormitory.floors[dormitory.current_floor].rooms:
            self.draw_room(room)
        # Draw students
        students_on_floor = [s for s in dormitory.students if s.floor_number == dormitory.current_floor]
        for student in students_on_floor:
            room = dormitory.floors[dormitory.current_floor].rooms[student.room_number]
            student_num = student.name.split('_')[0]
            bed_pos = room.beds[0] if student_num == 'Student1' else room.beds[1]
            student_img = pygame.transform.scale(student.photo, (config.TILE_SIZE * 1.5, config.TILE_SIZE * 1.5))
            self.screen.blit(student_img, (bed_pos[0] * config.TILE_SIZE, (room.y + config.ROOM_HEIGHT / 2 - 1.5) * config.TILE_SIZE))

    def draw_floor(self, floor):
        for row in range(floor.rows):
            for col in range(floor.cols):
                color = config.LIGHT_BROWN if (row, col) not in floor.room_walls() else config.LIGHT_GRAY
                pygame.draw.rect(self.screen, color, (col * config.TILE_SIZE, row * config.TILE_SIZE, config.TILE_SIZE, config.TILE_SIZE))
                pygame.draw.rect(self.screen, config.BLACK, (col * config.TILE_SIZE, row * config.TILE_SIZE, config.TILE_SIZE, config.TILE_SIZE), 1)

    def draw(self, dormitory):
        self.screen.fill(config.BLACK)
        self.draw_dormitory(dormitory)
        self.user_panel.draw(self.screen, dormitory)
        pygame.display.flip()


    def handle_keydown(self, event, dormitory):
        if event.key == pygame.K_ESCAPE:
            running = False
        elif event.key == pygame.K_RETURN:  # Confirm floor or room change
            if input_buffer.isdigit():
                floor_number = int(input_buffer) - 1  # Floors are 1-indexed for user
                dormitory.switch_floor(floor_number)
                input_buffer = ""  # Clear the buffer
            elif room_input_buffer.isdigit():
                room_number = int(room_input_buffer) - 1  # Rooms are 1-indexed for user
                dormitory.select_room(room_number)
                room_input_buffer = ""  # Clear the buffer
        elif event.key == pygame.K_BACKSPACE:
            if self.user_panel.input_rect.collidepoint(pygame.mouse.get_pos()):
                input_buffer = input_buffer[:-1]
            elif self.user_panel.room_input_rect.collidepoint(pygame.mouse.get_pos()):
                room_input_buffer = room_input_buffer[:-1]
        else:
            if event.unicode.isdigit():
                if self.user_panel.input_rect.collidepoint(pygame.mouse.get_pos()):
                    input_buffer += event.unicode
                elif self.user_panel.room_input_rect.collidepoint(pygame.mouse.get_pos()):
                    room_input_buffer += event.unicode

