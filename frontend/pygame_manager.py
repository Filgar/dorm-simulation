import pygame
import random

import display_config as dconfig
import config as config
from frontend.user_panel import UserPanel
from frontend.leaderboard import Leaderboard
from frontend.dormitory_drawer import DormitoryDrawer

class PygameManager:

    def __init__(self, initial_tick):
        pygame.init()

        self.screen = pygame.display.set_mode((dconfig.SCREEN_WIDTH, dconfig.SCREEN_HEIGHT))
        pygame.display.set_caption("Dormitory")

        self.user_panel = UserPanel(initial_tick)
        self.leaderboard = Leaderboard()
        self.dormitory_drawer = DormitoryDrawer()

        self.clock = pygame.time.Clock()
        self.tick = initial_tick

    def draw(self, dormitory, time, difficulty):
        self.screen.fill(dconfig.BLACK)
        self.dormitory_drawer.draw_dormitory(self.screen, dormitory)
        self.user_panel.draw(self.screen, dormitory, time, difficulty)
        self.leaderboard.draw(self.screen, dormitory)
        pygame.display.flip()
        self.clock.tick(self.tick)


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

