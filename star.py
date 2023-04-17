from __future__ import annotations
import pygame
from pygame.sprite import Sprite
import random

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class StarsBackground:
    def __init__(self, ai_game: AlienInvasion):
        self.ai_game = ai_game
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.stars = pygame.sprite.Group()

        self._create_stars()

    def _create_stars(self):
        if self.settings.stars_seed != 0:
            random.seed(self.settings.stars_seed)
        for x in range(self.settings.stars_num):
            star = Star(self)
            self.stars.add(star)
        random.seed(None)

    def update_screen(self):
        self.stars.draw(self.screen)


class Star(Sprite):
    def __init__(self, stars: StarsBackground):
        super().__init__()
        self.stars = stars
        self.settings = stars.settings

        self.image = pygame.image.load("images/star3.png").convert_alpha()
        self.scale = random.randint(*self.settings.stars_scale_min_max)
        self.transparency = random.randint(*self.settings.stars_transparency_min_max)

        self.image = pygame.transform.scale(self.image, (self.scale, self.scale))
        self.image = pygame.transform.rotate(self.image, random.randint(0, 360))
        self.image.fill((255, 255, 255, random.randint(3, self.transparency)),
                        special_flags=pygame.BLEND_RGBA_MULT)

        self.rect = self.image.get_rect()
        self.rect.y = random.randint(0, self.settings.screen_height)
        self.x = random.randint(0, self.settings.screen_width)
        self.y = random.randint(0, self.settings.screen_height)

    def update(self) -> None:
        self.x += self.settings.stars_speed * self.stars.ai_game.ship.speed * -1 * 0.25
        self.y += self.settings.stars_speed
        self.rect.x = self.x % self.settings.screen_width
        self.rect.y = self.y % self.settings.screen_height
