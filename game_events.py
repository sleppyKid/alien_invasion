from __future__ import annotations

import sys
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class GameEvents:
    def __init__(self, ai_game: AlienInvasion):
        self.ai = ai_game

    def check_events(self):
        events = pygame.event.get()

        for event in events:
            match event.type:
                case pygame.QUIT:
                    sys.exit()
                case pygame.KEYDOWN:
                    self._check_keydown_events(event)
                case pygame.KEYUP:
                    self._check_keyup_events(event)
                case pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self.ai.ui.check_play_button(mouse_pos)
                case self.ai.settings.alien_shoot_event:
                    self.ai.fleet.fire_random_bullet()

        if self.ai.game_state == self.ai.game_state.GAMEOVER:
            self.ai.ui.name_input.update(events)

    def _check_keydown_events(self, event):
        match self.ai.game_state:
            case self.ai.game_state.PLAY:
                match event.key:
                    case pygame.K_RIGHT:
                        self.ai.ship.moving_right = True
                    case pygame.K_LEFT:
                        self.ai.ship.moving_left = True
                    case pygame.K_SPACE:
                        self.ai.ship.fire_bullet()
                    case pygame.K_ESCAPE:
                        self.ai.pause_game()

            case self.ai.game_state.MENU:
                match event.key:
                    case pygame.K_p:
                        self.ai.start_game()

            case self.ai.game_state.GAMEOVER:
                match event.key:
                    case pygame.K_RETURN:
                        self.ai.enter_name()

        # Global
        match event.key:
            case pygame.K_q:
                if self.ai.game_state != self.ai.game_state.GAMEOVER:
                    sys.exit(0)

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ai.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ai.ship.moving_left = False
