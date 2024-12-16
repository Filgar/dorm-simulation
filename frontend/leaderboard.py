import pygame
import display_config as dconfig

class Leaderboard:
    def __init__(self):
        self.font16 = pygame.font.SysFont("Arial", 16)
        self.font20 = pygame.font.SysFont("Arial", 20)
        self.font24 = pygame.font.SysFont("Arial", 24)
        self.width = 0



        self.l_arrow_leaderboard = pygame.Rect(self.width + 50, 60 - 13, 26, 26)
        self.r_arrow_leaderboard = pygame.Rect(self.width + 250 - 26, 60 - 13, 26, 26)
        self.type = 0
        self.list_of_activity = ["Parting time", "Learning time", "Resting time", "Overdose value", "Sessions passed"]

    def draw(self, screen, dormitory):
        # Draw the panel for displaying the current floor
        pygame.draw.rect(screen, dconfig.LIGHT_GRAY, (self.width, 0, dconfig.PANEL_WIDTH, dconfig.SCREEN_HEIGHT))
        pygame.draw.rect(screen, dconfig.BLACK, (self.width, 0, dconfig.PANEL_WIDTH, dconfig.SCREEN_HEIGHT), 2)
        self.draw_inputs(screen, dormitory)
        self.draw_stats(screen, dormitory)

    def draw_inputs(self, screen, dormitory):
        def arrow(x, y, size, direction):
            return [(x, y), (x + (-1 if direction == 0 else 1) * size, y - size // 2), (x + (-1 if direction == 0 else 1) * size, y + size // 2)]

        pygame.draw.polygon(screen, dconfig.BLACK, arrow(self.width + 50, 60, 26, 1))
        pygame.draw.polygon(screen, dconfig.BLACK, arrow(self.width + 250, 60, 26, 0))
        screen.blit(self.font20.render(self.list_of_activity[self.type], True, dconfig.BLACK),(self.width + 100, 60 - 13))

    def draw_stats(self, screen, dormitory):
        floor = dormitory.floors[dormitory.current_floor]
        values = None
        if self.type == 0:
            leaderboard = sorted(floor.students, key=lambda student: student.time_partying, reverse=True)
            values = [student.time_partying for student in leaderboard]
        elif self.type == 1:
            leaderboard = sorted(floor.students, key=lambda student: student.time_learning, reverse=True)
            values = [student.time_learning for student in leaderboard]
        elif self.type == 2:
            leaderboard = sorted(floor.students, key=lambda student: student.time_resting, reverse=True)
            values = [student.time_resting for student in leaderboard]
        elif self.type == 3:
            leaderboard = sorted(floor.students, key=lambda student: student.party_overdose, reverse=True)
            values = [student.party_overdose for student in leaderboard]
        elif self.type == 4:
            leaderboard = sorted(floor.students, key=lambda student: student.exam_sessions_survived, reverse=True)
            values = [student.exam_sessions_survived for student in leaderboard]

        top = 130
        screen.blit(self.font20.render(f"Student name", True, dconfig.BLACK),(self.width + 35, top))
        screen.blit(self.font20.render(f"Value", True, dconfig.BLACK),(self.width + 225, top))

        i = 0
        for student in leaderboard:
            top += 35
            screen.blit(self.font20.render(f"{i+1}.", True, dconfig.BLACK), (self.width + 10, top))
            screen.blit(self.font20.render(student.name, True, dconfig.BLACK), (self.width + 35, top))
            screen.blit(self.font20.render(str(values[i]), True, dconfig.BLACK), (self.width + 240, top))
            i += 1

