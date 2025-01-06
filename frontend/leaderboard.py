import pygame
from enum import Enum
import display_config as dconfig

class Leaderboard:
    def __init__(self):
        self.font20 = pygame.font.SysFont("Arial", 20)

        self.l_arrow_leaderboard = pygame.Rect(50, 60 - 13, 26, 26)
        self.r_arrow_leaderboard = pygame.Rect(250 - 26, 60 - 13, 26, 26)
        self.page: LeaderboardPage = LeaderboardPage.PARTYING_TIME

    def draw(self, screen, dormitory):
        pygame.draw.rect(screen, dconfig.LIGHT_GRAY, (0, 0, dconfig.PANEL_WIDTH, dconfig.SCREEN_HEIGHT))
        pygame.draw.rect(screen, dconfig.BLACK, (0, 0, dconfig.PANEL_WIDTH, dconfig.SCREEN_HEIGHT), 2)
        self.draw_inputs(screen)
        self.draw_stats(screen, dormitory)

    def draw_inputs(self, screen):
        def arrow(x, y, size, direction):
            return [(x, y), (x + (-1 if direction == 0 else 1) * size, y - size // 2), (x + (-1 if direction == 0 else 1) * size, y + size // 2)]

        pygame.draw.polygon(screen, dconfig.BLACK, arrow(35, 60, 26, 1))
        pygame.draw.polygon(screen, dconfig.BLACK, arrow(265, 60, 26, 0))

        x = 95 if not self.page is LeaderboardPage.PARTIES_ATTENDED else 80         #TODO ugly

        screen.blit(self.font20.render(self.get_activity_name(), True, dconfig.BLACK),(x, 50))

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
                leaderboard = sorted(floor.students, key=lambda student: student.faints, reverse=True)
                values = [student.faints for student in leaderboard]
            case LeaderboardPage.EXAMS_PASSED:
                leaderboard = sorted(floor.students, key=lambda student: student.exam_sessions_survived, reverse=True)
                values = [student.exam_sessions_survived for student in leaderboard]
            case LeaderboardPage.PARTIES_ATTENDED:
                leaderboard = sorted(floor.students, key=lambda student: student.parties_attended, reverse=True)
                values = [student.parties_attended for student in leaderboard]

        top = 130
        screen.blit(self.font20.render(f"Student name", True, dconfig.BLACK),(35, top))
        screen.blit(self.font20.render(f"Value", True, dconfig.BLACK),(225, top))
        top += 35

        for i, student in enumerate(leaderboard):
            record = f"{i+1}.{" " if i + 1 > 9 else "    "}{student.name + (' [*]' if student.dropout else "")}"
            screen.blit(self.font20.render(record, True, dconfig.BLACK), (10, top + i * 35))
            screen.blit(self.font20.render(str(values[i]), True, dconfig.BLACK), (240, top + i * 35))
    
    def switch_page(self, direction):
        self.page = LeaderboardPage((self.page.value + direction) % len(LeaderboardPage))

    def get_activity_name(self):
        match self.page:
            case LeaderboardPage.PARTYING_TIME:
                return "Partying time"
            case LeaderboardPage.LEARNING_TIME:
                return "Learning time"
            case LeaderboardPage.RESTING_TIME:
                return "Resting time"
            case LeaderboardPage.FAINTS:
                return "Faints count"
            case LeaderboardPage.EXAMS_PASSED:
                return "Exams passed"
            case LeaderboardPage.PARTIES_ATTENDED:
                return "Parties attended"


class LeaderboardPage(Enum):
    PARTYING_TIME = 0
    LEARNING_TIME = 1
    RESTING_TIME = 2
    FAINTS = 3
    EXAMS_PASSED = 4
    PARTIES_ATTENDED = 5