import pygame

import display_config as dconfig

class UserPanel:
    def __init__(self):
        # Input buffer for typing floor numbers
        self.input_buffer = ""
        self.input_rect = pygame.Rect(dconfig.SCREEN_WIDTH - 120, 150, 100, 30)

        self.room_input_buffer = ""
        self.room_input_rect = pygame.Rect(dconfig.SCREEN_WIDTH - 120, 195, 100, 30)



    def draw(self, screen, dormitory, time, difficulty):
        # Draw the panel for displaying the current floor
        pygame.draw.rect(screen, dconfig.LIGHT_GRAY, (dconfig.SCREEN_WIDTH - dconfig.PANEL_WIDTH, 0, dconfig.PANEL_WIDTH, dconfig.SCREEN_HEIGHT))
        pygame.draw.rect(screen, dconfig.BLACK, (dconfig.SCREEN_WIDTH - dconfig.PANEL_WIDTH, 0, dconfig.PANEL_WIDTH, dconfig.SCREEN_HEIGHT), 2)

        self.draw_inputs(screen, dormitory)
        self.draw_time(screen, time, difficulty)

        if dormitory.selected_room is not None:
            self.draw_selected_room_panel(screen, dormitory)



    def draw_inputs(self, screen, dormitory):
        font = pygame.font.SysFont("Arial", 24)
        text_surface = font.render(f"Floor: {dormitory.current_floor + 1}", True, dconfig.BLACK)
        screen.blit(text_surface, (dconfig.SCREEN_WIDTH - dconfig.PANEL_WIDTH + 20, 110))

        # Draw the input field
        pygame.draw.rect(screen, dconfig.WHITE, self.input_rect)
        pygame.draw.rect(screen, dconfig.BLACK, self.input_rect, 2)

        input_surface = font.render(self.input_buffer, True, dconfig.BLACK)
        input_desc = font.render(f"Go to: ", True, dconfig.BLACK)
        screen.blit(input_surface, (self.input_rect.x + 5, self.input_rect.y))
        screen.blit(input_desc, (dconfig.SCREEN_WIDTH - dconfig.PANEL_WIDTH + 20, 150))

        # Draw the room input field
        pygame.draw.rect(screen, dconfig.WHITE, self.room_input_rect)
        pygame.draw.rect(screen, dconfig.BLACK, self.room_input_rect, 2)

        room_input_surface = font.render(self.room_input_buffer, True, dconfig.BLACK)
        room_input_desc = font.render(f"Room: ", True, dconfig.BLACK)
        screen.blit(room_input_surface, (self.room_input_rect.x + 5, self.room_input_rect.y))
        screen.blit(room_input_desc, (dconfig.SCREEN_WIDTH - dconfig.PANEL_WIDTH + 20, 195))
    


    def draw_time(self, screen, time, difficulty):
        difficulty = 'Easy' if difficulty < 0.8 else 'Hard' if difficulty > 1.2 else 'Moderate'

        font = pygame.font.SysFont("Arial", 24)
        font2 = pygame.font.SysFont("Arial", 20)
        height = 20
        screen.blit(font2.render(f'Day {time // 24} {time%24:02}:00', True, dconfig.BLACK), (dconfig.SCREEN_WIDTH - dconfig.PANEL_WIDTH + 20, height))
        if (time // 24) % 7 == 0:   #Every week
            screen.blit(font.render("EXAM SEASON TIME", True, dconfig.RED), (dconfig.SCREEN_WIDTH - dconfig.PANEL_WIDTH + 20, height + 50))
            screen.blit(font2.render("Difficulty level: " + difficulty, True, dconfig.BLACK), (dconfig.SCREEN_WIDTH - dconfig.PANEL_WIDTH + 20, height + 80))



    def draw_selected_room_panel(self, screen, dormitory):
        # Display stats for the selected room
        font2 = pygame.font.SysFont("Arial", 20)
        floor = dormitory.floors[dormitory.current_floor]
        students_in_room = [s for s in floor.students if s.native_room.number == dormitory.selected_room]
        height = 250
        screen.blit(font2.render("Students in room:", True, dconfig.BLACK), (dconfig.SCREEN_WIDTH - dconfig.PANEL_WIDTH + 20, height))
        height += 30
        for i, student in enumerate(students_in_room): 
            student_info = f"{student.name}"
            screen.blit(font2.render(student_info, True, dconfig.BLACK), (dconfig.SCREEN_WIDTH - dconfig.PANEL_WIDTH + 20, height))
            height+=30
            student_info = f"- Learned: {int(student.knowledge * 100)}%"
            screen.blit(font2.render(student_info, True, dconfig.BLACK), (dconfig.SCREEN_WIDTH - dconfig.PANEL_WIDTH + 20, height))
            height+=30
            student_info = f"- Energy: {int(student.energy * 100)}%"
            screen.blit(font2.render(student_info, True, dconfig.BLACK), (dconfig.SCREEN_WIDTH - dconfig.PANEL_WIDTH + 20, height))
            height+=60
            student_info = f"- Current state: " + student.state.name
            screen.blit(font2.render(student_info, True, dconfig.BLACK), (dconfig.SCREEN_WIDTH - dconfig.PANEL_WIDTH + 20, height))
            height+=60