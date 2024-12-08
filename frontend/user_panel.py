import pygame

import display_config as config

class UserPanel:
    def __init__(self):
        # Input buffer for typing floor numbers
        self.input_buffer = ""
        self.input_rect = pygame.Rect(config.SCREEN_WIDTH - 120, 60, 100, 30)

        self.room_input_buffer = ""
        self.room_input_rect = pygame.Rect(config.SCREEN_WIDTH - 120, 105, 100, 30)

    def draw(self, screen, dormitory):
        # Draw the panel for displaying the current floor
        pygame.draw.rect(screen, config.LIGHT_GRAY, (config.SCREEN_WIDTH - config.PANEL_WIDTH, 0, config.PANEL_WIDTH, config.SCREEN_HEIGHT))
        pygame.draw.rect(screen, config.BLACK, (config.SCREEN_WIDTH - config.PANEL_WIDTH, 0, config.PANEL_WIDTH, config.SCREEN_HEIGHT), 2)

        font = pygame.font.SysFont("Arial", 24)
        text_surface = font.render(f"Floor: {dormitory.current_floor + 1}", True, config.BLACK)
        screen.blit(text_surface, (config.SCREEN_WIDTH - config.PANEL_WIDTH + 20, 20))

        # Draw the input field
        pygame.draw.rect(screen, config.WHITE, self.input_rect)
        pygame.draw.rect(screen, config.BLACK, self.input_rect, 2)

        input_surface = font.render(self.input_buffer, True, config.BLACK)
        input_desc = font.render(f"Go to: ", True, config.BLACK)
        screen.blit(input_surface, (self.input_rect.x + 5, self.input_rect.y))
        screen.blit(input_desc, (config.SCREEN_WIDTH - config.PANEL_WIDTH + 20, 60))

        # Draw the room input field
        pygame.draw.rect(screen, config.WHITE, self.room_input_rect)
        pygame.draw.rect(screen, config.BLACK, self.room_input_rect, 2)

        room_input_surface = font.render(self.room_input_buffer, True, config.BLACK)
        room_input_desc = font.render(f"Room: ", True, config.BLACK)
        screen.blit(room_input_surface, (self.room_input_rect.x + 5, self.room_input_rect.y))
        screen.blit(room_input_desc, (config.SCREEN_WIDTH - config.PANEL_WIDTH + 20, 105))

        if dormitory.selected_room is not None:
            self.draw_selected_room_panel(screen, dormitory)


    def draw_selected_room_panel(self, screen, dormitory):
        # Display stats for the selected room
        font2 = pygame.font.SysFont("Arial", 20)
        floor = dormitory.floors[dormitory.current_floor]
        students_in_room = [s for s in floor.students if s.native_room.number == dormitory.selected_room]
        screen.blit(font2.render("Students in room:", True, config.BLACK), (config.SCREEN_WIDTH - config.PANEL_WIDTH + 20, 150))
        height = 180
        for i, student in enumerate(students_in_room): 
            student_info = f"{student.name}"
            screen.blit(font2.render(student_info, True, config.BLACK), (config.SCREEN_WIDTH - config.PANEL_WIDTH + 20, height))
            height+=30
            student_info = f"- Learned: {student.learned_ratio}%"
            screen.blit(font2.render(student_info, True, config.BLACK), (config.SCREEN_WIDTH - config.PANEL_WIDTH + 20, height))
            height+=30
            student_info = f"- Energy: {student.energy_ratio}%"
            screen.blit(font2.render(student_info, True, config.BLACK), (config.SCREEN_WIDTH - config.PANEL_WIDTH + 20, height))
            height+=60