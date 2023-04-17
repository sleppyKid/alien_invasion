from __future__ import annotations
import pygame
from pygame.sprite import Sprite

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class ShelterBlocks:
    def __init__(self, ai_game: AlienInvasion):
        self.ai_game = ai_game
        self.settings = ai_game.settings
        self.shelters = []
        self.screen = ai_game.screen

    def create_shelters(self):
        self.shelters.clear()
        num = self.settings.shelter_count + 1
        spacing = self.settings.screen_width / num
        y = self.settings.screen_height - self.settings.shelter_pos_y
        for x in range(1, num):
            shelter = Shelter(self.ai_game, (spacing * x, y))
            self.shelters.append(shelter)

    def update_screen(self):
        for shelter in self.shelters:
            for brick in shelter.bricks.sprites():
                brick.draw(self.screen)

    def update(self):
        for s in self.shelters:
            s.update()


class Shelter:
    def __init__(self, ai_game: AlienInvasion, pos):
        self.pos = pos
        # print(pos)
        self.ai_game = ai_game
        self.settings = ai_game.settings

        self.bricks = self._create_bricks()

    def _create_bricks(self):
        bricks = pygame.sprite.Group()
        num_x = self.settings.shelter_width
        num_y = self.settings.shelter_height
        num_x = num_x if num_x % 2 else num_x - 1
        offset_x = num_x // 2
        offset_y = num_y // 2
        brick_distance = self.settings.shelter_brick_size + self.settings.shelter_brick_distance
        for x_pos in range(num_x):
            for y_pos in range(num_y):
                x = self.pos[0] + (x_pos - offset_x) * brick_distance
                y = self.pos[1] + (y_pos - offset_y) * brick_distance

                brick = ShelterBrick(self, (x, y))
                bricks.add(brick)
            continue
        return bricks

    def update(self):
        pygame.sprite.groupcollide(self.ai_game.ship.bullets, self.bricks, True, True)
        pygame.sprite.groupcollide(self.ai_game.fleet.bullets, self.bricks, True, True)
        pygame.sprite.groupcollide(self.ai_game.fleet.aliens, self.bricks, False, True)


class ShelterBrick(Sprite):
    def __init__(self, shelter: Shelter, pos):
        super().__init__()
        self.shelter = shelter
        self.color = self.shelter.settings.shelter_color

        self.rect = pygame.Rect(0, 0, self.shelter.settings.shelter_brick_size,
                                self.shelter.settings.shelter_brick_size)
        self.rect.center = pos

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
