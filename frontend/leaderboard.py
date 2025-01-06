import pygame
from enum import Enum
import display_config as dconfig

class Leaderboard:
    def __init__(self):
        self.font20 = pygame.font.SysFont("Arial", 20)

        self.l_arrow_leaderboard = pygame.Rect(50, 60 - 13, 26, 26)
        self.r_arrow_leaderboard = pygame.Rect(250 - 26, 60 - 13, 26, 26)
        self.page: LeaderboardPage = LeaderboardPage.PARTYING_TIME
        self.activities: list[str] = ["Partying time", "Learning time", "Resting time", "Faints count", "Exams passed"]

    def draw(self, screen, dormitory):
        pygame.draw.rect(screen, dconfig.LIGHT_GRAY, (0, 0, dconfig.PANEL_WIDTH, dconfig.SCREEN_HEIGHT))
        pygame.draw.rect(screen, dconfig.BLACK, (0, 0, dconfig.PANEL_WIDTH, dconfig.SCREEN_HEIGHT), 2)
        self.draw_inputs(screen)
        self.draw_stats(screen, dormitory)

    def draw_inputs(self, screen):
        def arrow(x, y, size, direction):
            return [(x, y), (x + (-1 if direction == 0 else 1) * size, y - size // 2), (x + (-1 if direction == 0 else 1) * size, y + size // 2)]

        pygame.draw.polygon(screen, dconfig.BLACK, arrow(50, 60, 26, 1))
        pygame.draw.polygon(screen, dconfig.BLACK, arrow(250, 60, 26, 0))
        screen.blit(self.font20.render(self.activities[self.page.value], True, dconfig.BLACK),(100, 60 - 13))

    def draw_stats(self, screen, dormitory):
        floor = dormitory.floors[dormitory.current_floor]
        values = None
        match self.page:
            case LeaderboardPage.PARTYING_TIME:
                leaderboard = sorted(floor.students, key=lambda student: student.time_partying, reverse=True)
                values = [student.time_partying for student in leaderboard]
            case LeaderboardPage.LEARNING_TIME:
                leaderboard = sorted(floor.students, key=lambda student: student.time_learning, reverse=True)
                values = [student.time_learning for student in leaderboard]
            case LeaderboardPage.RESTING_TIME:
                leaderboard = sorted(floor.students, key=lambda student: student.time_resting, reverse=True)
                values = [student.time_resting for student in leaderboard]
            case LeaderboardPage.FAINTS:
                leaderboard = sorted(floor.students, key=lambda student: student.party_overdose, reverse=True)
                values = [student.party_overdose for student in leaderboard]
            case LeaderboardPage.EXAMS_PASSED:
                leaderboard = sorted(floor.students, key=lambda student: student.exam_sessions_survived, reverse=True)
                values = [student.exam_sessions_survived for student in leaderboard]

        top = 130
        screen.blit(self.font20.render(f"Student name", True, dconfig.BLACK),(35, top))
        screen.blit(self.font20.render(f"Value", True, dconfig.BLACK),(225, top))
        top += 35

        for i, student in enumerate(leaderboard):
            screen.blit(self.font20.render(f"{i+1}. {student.name + (' [*]' if student.dropout else "")}", True, dconfig.BLACK), (10, top + i * 35))
            screen.blit(self.font20.render(str(values[i]), True, dconfig.BLACK), (240, top + i * 35))
    
    def switch_page(self, direction):
        self.page = LeaderboardPage((self.page.value + direction) % len(LeaderboardPage))


class LeaderboardPage(Enum):
    PARTYING_TIME = 0
    RESTING_TIME = 1
    LEARNING_TIME = 2
    FAINTS = 3
    EXAMS_PASSED = 4