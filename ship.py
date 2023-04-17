from __future__ import annotations

import time

import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING
from bullet import Bullet

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class Ship(Sprite):
    def __init__(self, ai_game: AlienInvasion):
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        self.image = pygame.image.load('images/ship.png').convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.moving_left = False
        self.moving_right = False

        self.bullets = pygame.sprite.Group()

    def update(self):
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed_factor
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed_factor

        self.rect.x = self.x

        self._update_bullets()

    @property
    def speed(self):
        if self.moving_left and not self.moving_right:
            return -1
        elif self.moving_right and not self.moving_left:
            return 1
        return 0

    def update_screen(self):
        self.screen.blit(self.image, self.rect)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

    def reset_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

        self.bullets.empty()

    def fire_bullet(self):
        if self.ai_game.stats.unlimited_ammo or len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self.ai_game, self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self.ai_game.fleet.check_bullet_alien_collisions(self.bullets)

    def check_ship_bullets_collisions(self, bullets: pygame.sprite.Group):
        if self.ai_game.stats.shield:
            return
        collisions = pygame.sprite.spritecollide(self, bullets, True)
        if collisions:
            self.ai_game.ship_hit()
