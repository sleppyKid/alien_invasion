import time
from enum import Enum
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from bonuses import BonusType
from ui import UI
from game_events import GameEvents

from star import StarsBackground
from ship import Ship
from alien import AlienFleet
from shelter import ShelterBlocks


class GameState(Enum):
    PLAY = 0
    PAUSE = 1
    MENU = 2
    GAMEOVER = 3


class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height),
            pygame.FULLSCREEN if self.settings.fullscreen else 0
        )
        if self.settings.fullscreen:
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")
        self.game_state = GameState.MENU

        self.input = GameEvents(self)
        self.stats = GameStats(self)
        self.ui = UI(self)
        self.ship = Ship(self)
        self.shelters = ShelterBlocks(self)

        self.stars = StarsBackground(self)
        self.fleet = AlienFleet(self)

    def start_game(self):
        if self.game_state.MENU:
            self.settings.initialize_dynamic_settings()
            self.stats.game_active = True
            self.stats.reset_stats()
            self.ui.update_score()
            self.ui.update_level()

            self.reset_game()
            pygame.mouse.set_visible(False)

    def reset_game(self):
        self.ui.update_ships_lives()

        self.fleet.clear_aliens()
        self.ship.reset_ship()
        self.shelters.create_shelters()

        self.fleet.create_fleet()
        self.game_state = GameState.PLAY

    def run_game(self):
        while True:
            self.clock.tick(self.settings.tick_rate)
            self.input.check_events()

            match self.game_state:
                case GameState.PLAY:
                    if self.stats.game_active:
                        self.stars.stars.update()
                        self.ship.update()

                        self.fleet.update_aliens()
                        self.shelters.update()
                        self.stats.update_bonuses()

                case GameState.PAUSE:
                    pass

                case GameState.MENU:
                    self.stars.stars.update()

                case GameState.GAMEOVER:
                    self.stars.stars.update()

            self._update_screen()

    def _update_screen(self):
        match self.game_state:
            case GameState.PLAY:
                self.screen.fill(self.settings.bg_color)
                self.stars.update_screen()
                self.ship.update_screen()
                self.fleet.update_screen()
                self.shelters.update_screen()
                self.ui.show_score()

            case GameState.PAUSE:
                self.ui.show_pause()

            case GameState.MENU:
                self.screen.fill(self.settings.bg_color)
                self.stars.update_screen()
                self.ui.show_menu()

            case GameState.GAMEOVER:
                self.screen.fill(self.settings.bg_color)
                self.stars.update_screen()
                self.ui.show_score()
                self.ui.show_gameover()

        pygame.display.flip()

    def increase_level(self):
        self.fleet.create_fleet()
        self.settings.increase_speed()
        self.shelters.create_shelters()

        self.stats.level += 1
        self.ui.update_level()

    def ship_hit(self):
        if self.stats.ships_lives == 0:
            self.game_over()
        else:
            self.stats.ships_lives -= 1
            self.ui.update_ships_lives()

            self.stats.enable_bonus(BonusType.GOD)

    def pause_game(self):
        if self.game_state == GameState.PLAY:
            self.pause_time = time.time()
            self.game_state = GameState.PAUSE
            self.stats.game_active = False

        elif self.game_state == GameState.PAUSE:
            self.stats.fix_pause_timers(time.time() - self.pause_time)
            self.game_state = GameState.PLAY
            self.stats.game_active = True

    def game_over(self):
        self.game_state = GameState.GAMEOVER
        self.stats.game_active = False
        pygame.mouse.set_visible(True)

    def enter_name(self):
        valid = self.ui.check_name()
        if valid:
            self.game_state = GameState.MENU
