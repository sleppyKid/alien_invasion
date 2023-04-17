from __future__ import annotations

import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class Bullet(Sprite):
    def __init__(self, ai_game: AlienInvasion, ship):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        self.rect = self._create_rect(ship)

        self.y = float(self.rect.y)
        self.direction = -1

    def _create_rect(self, ship):
        rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        rect.midtop = ship.rect.midtop
        return rect

    def update(self):
        self.y += self.settings.bullet_speed_factor * self.direction
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


class AlienBullet(Bullet):
    def __init__(self, ai_game: AlienInvasion, ship):
        super().__init__(ai_game, ship)
        self.color = self.settings.alien_bullet_color
        self.direction = 1

    def _create_rect(self, ship):
        rect = pygame.Rect(0, 0, self.settings.alien_bullet_width,
                                self.settings.alien_bullet_height)
        rect.midbottom = ship.rect.midbottom
        return rect
