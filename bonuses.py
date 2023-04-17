from __future__ import annotations

import random
from typing import TYPE_CHECKING
from enum import Enum
from dataclasses import dataclass

import pygame
from pygame.sprite import Sprite

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class BonusType(Enum):
    GOD = 0
    AMMO = 1
    HEALTH = 2
    SHIELD = 3
    SCORE = 4


@dataclass
class Bonus:
    type: BonusType
    sprite: str
    weight: float
    timer: float = 0
    available: bool = True


class BonusesInfo:
    BONUSES = {
        BonusType.GOD:
            Bonus(BonusType.GOD,
                  'images/tiles/shield.png', weight=0, timer=3, available=False),
        BonusType.AMMO:
            Bonus(BonusType.AMMO,
                  'images/tiles/energy.png', weight=4, timer=5, available=True),
        BonusType.HEALTH:
            Bonus(BonusType.HEALTH,
                  'images/tiles/health.png', weight=1, timer=0, available=True),
        BonusType.SHIELD:
            Bonus(BonusType.SHIELD,
                  'images/tiles/shield.png', weight=2, timer=6, available=True),
        BonusType.SCORE:
            Bonus(BonusType.SCORE,
                  'images/tiles/score.png', weight=2, timer=6, available=True)
    }

    @classmethod
    def get_random_bonus(cls):
        items = filter(lambda x: x[1].available, cls.BONUSES.items())
        bonuses_types, bonus_items = zip(*items)
        weights = tuple(x.weight for x in bonus_items)
        bonus = random.choices(bonuses_types, weights=weights, k=1)[0]
        return bonus


class BonusSprite(Sprite):
    def __init__(self, ai_game: AlienInvasion, position, bonus_type: BonusType):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.bonus_type = bonus_type
        self.bonus_info = BonusesInfo.BONUSES[self.bonus_type]

        self.color = (255, 255, 255)
        self.size = self.settings.bonuses_size

        self.image = pygame.image.load(self.bonus_info.sprite).convert_alpha()
        color_image = pygame.Surface(self.image.get_size()).convert_alpha()
        color_image.fill(self.color)
        self.image.blit(color_image, (0, 0), special_flags=pygame.BLEND_MAX)
        scale = self.image.get_size()[0] / self.image.get_size()[1]
        self.image = pygame.transform.scale(self.image, (self.size * scale, self.size))

        self.rect = self.image.get_rect()
        self.rect.center = position
        self.y = float(self.rect.y)

    def update(self):
        self.y += self.settings.bonuses_speed * 1
        self.rect.y = self.y

    def update_screen(self):
        self.screen.blit(self.image, self.rect)
