import pygame

import display_config as dconfig

class UserPanel:

    MEMORIAL_PHOTO = pygame.image.load(dconfig.MEMORIAL_PHOTO)

    def __init__(self):
        UserPanel.MEMORIAL_PHOTO = UserPanel.MEMORIAL_PHOTO.convert()

        # Input buffer for typing floor numbers
        self.input_buffer = ""
        self.input_rect = pygame.Rect(dconfig.SCREEN_WIDTH - 120, 150, 100, 30)

        self.room_input_buffer = ""
        self.room_input_rect = pygame.Rect(dconfig.SCREEN_WIDTH - 120, 195, 100, 30)

        self.font16 = pygame.font.SysFont("Arial", 16)
        self.font20 = pygame.font.SysFont("Arial", 20)
        self.font24 = pygame.font.SysFont("Arial", 24)



    def draw(self, screen, dormitory, time, difficulty):
        # Draw the panel for displaying the current floor
        pygame.draw.rect(screen, dconfig.LIGHT_GRAY, (dconfig.SCREEN_WIDTH - dconfig.PANEL_WIDTH, 0, dconfig.PANEL_WIDTH, dconfig.SCREEN_HEIGHT))
        pygame.draw.rect(screen, dconfig.BLACK, (dconfig.SCREEN_WIDTH - dconfig.PANEL_WIDTH, 0, dconfig.PANEL_WIDTH, dconfig.SCREEN_HEIGHT), 2)

        self.draw_inputs(screen, dormitory)
        self.draw_time(screen, time, difficulty)

        if dormitory.selected_room is not None:
            self.draw_selected_room_panel(screen, dormitory)



    def draw_inputs(self, screen, dormitory):
        text_surface = self.font24.render(f"Floor: {dormitory.current_floor + 1}", True, dconfig.BLACK)
        screen.blit(text_surface, (dconfig.SCREEN_WIDTH - dconfig.PANEL_WIDTH + 20, 110))

        # Draw the input field
        pygame.draw.rect(screen, dconfig.WHITE, self.input_rect)
        pygame.draw.rect(screen, dconfig.BLACK, self.input_rect, 2)

        input_surface = self.font24.render(self.input_buffer, True, dconfig.BLACK)
        input_desc = self.font24.render(f"Go to: ", True, dconfig.BLACK)
        screen.blit(input_surface, (self.input_rect.x + 5, self.input_rect.y))
        screen.blit(input_desc, (dconfig.SCREEN_WIDTH - dconfig.PANEL_WIDTH + 20, 150))

        # Draw the room input field
        pygame.draw.rect(screen, dconfig.WHITE, self.room_input_rect)
        pygame.draw.rect(screen, dconfig.BLACK, self.room_input_rect, 2)

        room_input_surface = self.font24.render(self.room_input_buffer, True, dconfig.BLACK)
        room_input_desc = self.font24.render(f"Room: ", True, dconfig.BLACK)
        screen.blit(room_input_surface, (self.room_input_rect.x + 5, self.room_input_rect.y))
        screen.blit(room_input_desc, (dconfig.SCREEN_WIDTH - dconfig.PANEL_WIDTH + 20, 195))
    


    def draw_time(self, screen, time, difficulty):
        if difficulty < 0.75:
            difficulty_level = 'Very Easy'
        elif difficulty < 0.9:
            difficulty_level = 'Easy'
        elif difficulty < 1.1:
            difficulty_level = 'Moderate'
        elif difficulty < 1.25:
            difficulty_level = 'Hard'
        else:
            difficulty_level = 'Very Hard'

        height = 20
        screen.blit(self.font20.render(f'Day {time // 24} {time%24:02}:00', True, dconfig.BLACK), (dconfig.SCREEN_WIDTH - dconfig.PANEL_WIDTH + 20, height))
        if (time // 24) % 7 == 0:   #Every week
            screen.blit(self.font24.render("EXAM SEASON TIME", True, dconfig.RED), (dconfig.SCREEN_WIDTH - dconfig.PANEL_WIDTH + 20, height + 20))
            screen.blit(self.font20.render('Difficulty level: ' + difficulty_level, True, dconfig.BLACK), (dconfig.SCREEN_WIDTH - dconfig.PANEL_WIDTH + 20, height + 50))



    def draw_selected_room_panel(self, screen, dormitory):
        # Display stats for the selected room
        floor = dormitory.floors[dormitory.current_floor]
        students_in_room = floor.get_students_in_room(floor.rooms[dormitory.selected_room])

        top = 250
        screen.blit(self.font20.render(f"Students in room {dormitory.selected_room + 1}:", True, dconfig.BLACK), (dconfig.SCREEN_WIDTH - dconfig.PANEL_WIDTH + 20, top))
        top += 30
        for student in students_in_room: 
            if student.dropout:
                top = self.draw_student_memorial(screen, student, top)
            else:
                top = self.draw_student_details(screen, student, top)


    def draw_student_details(self, screen, student, top) -> int:
        text_width = 50
        left = dconfig.SCREEN_WIDTH - dconfig.PANEL_WIDTH + 20
        x_size = dconfig.PANEL_WIDTH - 40 - text_width

        student_info = f"{student.name}"
        screen.blit(self.font20.render(student_info, True, dconfig.BLACK), (left, top))
        top += 30
        
        self.draw_student_progress_bar(screen, student.knowledge, dconfig.BLUE, (left, top), (x_size, 20), "Knowledge")
        top += 50
        self.draw_student_progress_bar(screen, student.fun, dconfig.ORANGE, (left, top), (x_size, 20), "Fun")
        top += 50
        self.draw_student_progress_bar(screen, student.energy, dconfig.GREEN, (left, top), (x_size, 20), "Energy")
        top += 50

        student_info = f"Current state: " + student.state.name
        screen.blit(self.font20.render(student_info, True, dconfig.BLACK), (left, top))
        
        return top + 60

    def draw_student_progress_bar(self, screen, value, color, position, size, text):
        screen.blit(self.font16.render(text, True, dconfig.BLACK), (position[0], position[1]))
        pygame.draw.rect(screen, dconfig.DARK_GRAY, (position[0], position[1] + 20, *size))
        pygame.draw.rect(screen, color, (position[0], position[1] + 20, size[0] * value, size[1]))

    def draw_student_memorial(self, screen, student, top) -> int:
        left = dconfig.SCREEN_WIDTH - dconfig.PANEL_WIDTH + 60

        student_info = f"{student.name}"
        screen.blit(self.font20.render(student_info, True, dconfig.BLACK), (left - 15, top))
        top += 25

        memorial_img = pygame.transform.scale(self.MEMORIAL_PHOTO, (dconfig.PANEL_WIDTH - 120, dconfig.PANEL_WIDTH - 160))
        screen.blit(memorial_img, (left, top))
        top += dconfig.PANEL_WIDTH - 160 + 10

        student_info = "Forever in our hearts"
        screen.blit(self.font16.render(student_info, True, dconfig.BLACK), (left + 15, top))
        top += 20

        student_info = "(And Messenger conversation)"
        screen.blit(self.font16.render(student_info, True, dconfig.BLACK), (left - 15, top))
        return top + 30

    