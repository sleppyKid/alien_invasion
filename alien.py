from __future__ import annotations

import random

import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING, Optional

from bullet import AlienBullet
from bonuses import BonusType, BonusSprite, BonusesInfo

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class AlienFleet:
    def __init__(self, ai_game: AlienInvasion):
        self.ai_game = ai_game

        self.aliens = pygame.sprite.Group()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.scoreboard = ai_game.ui
        self.stats = ai_game.stats

        self.bullets = pygame.sprite.Group()
        self.bonuses = pygame.sprite.Group()

        pygame.time.set_timer(self.settings.alien_shoot_event, self.settings.alien_shoot_timer_factor, loops=1)

        self.create_fleet()

    def create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        number_aliens_x = self.settings.number_aliens_x + 1
        number_aliens_y = self.settings.number_aliens_y

        start_offset_x = self.settings.start_offset_x
        # start_offset_y = self.settings.start_offset_y

        available_width = self.settings.screen_width - start_offset_x * 2
        available_height = (self.settings.screen_height - start_offset_x) / 2

        spacing_x = available_width / number_aliens_x
        spacing_y = available_height / number_aliens_y

        if spacing_x < alien_width * 1.2:
            print(f'Not enough space for {number_aliens_x} aliens!')
            number_aliens_x = round(available_width / (alien_width * 1.33))
            spacing_x = available_width / number_aliens_x
            print(f'Aliens number changed to {number_aliens_x}!')

        for row in range(0, number_aliens_y):
            for alien_num in range(1, number_aliens_x):
                self._create_alien(alien_num, row, spacing_x, spacing_y)

    def _create_alien(self, alien_num, row, spacing_x, spacing_y):
        alien = Alien(self, row, alien_num)
        alien_width, alien_height = alien.rect.size
        alien.x = self.settings.start_offset_x + (spacing_x * alien_num) - alien_width / 2
        alien.rect.x = alien.x
        alien.rect.y = alien.y = self.settings.start_offset_y + (spacing_y * row)
        self.aliens.add(alien)

    def clear_aliens(self):
        self.aliens.empty()
        self.bullets.empty()
        self.bonuses.empty()

    def update_screen(self):
        self.aliens.draw(self.screen)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.bonuses.draw(self.screen)

    def update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        self._update_bullets()
        self._update_bonuses()

        if pygame.sprite.spritecollideany(self.ai_game.ship, self.aliens):
            self.ai_game.game_over()

        self._check_aliens_bottom()
        self._check_bullets_collision()

    def fire_random_bullet(self):
        pygame.time.set_timer(self.settings.alien_shoot_event,
                              self.settings.alien_shoot_timer_factor, loops=1)

        if not self.stats.game_active:
            return

        alien = random.choice(self._find_shooting_aliens())
        bullet = AlienBullet(self.ai_game, alien)
        self.bullets.add(bullet)

    def check_bullet_alien_collisions(self, bullets: pygame.sprite.Group):
        collisions = pygame.sprite.groupcollide(bullets, self.aliens, True, True)
        if collisions:
            for _, aliens in collisions.items():
                for alien in aliens:
                    score = self.settings.alien_points[alien.type]
                    if self.stats.score_bonus:
                        score *= self.settings.bonus_score_scale

                    self.stats.score += score

                    if random.randint(1, 100) < self.settings.bonuses_drop_rate * 100:
                        self.create_bonus(alien.rect.center)

            self.scoreboard.update_score()

        if not self.aliens:
            self.bullets.empty()
            bullets.empty()
            self.ai_game.increase_level()

    def _check_bullets_collision(self):
        pygame.sprite.groupcollide(self.bullets, self.ai_game.ship.bullets, True, True)

    def create_bonus(self, position, bonus_type: Optional[BonusType] = None):
        if bonus_type is None:
            bonus_type = BonusesInfo.get_random_bonus()

        bonus = BonusSprite(self.ai_game, position, bonus_type)
        self.bonuses.add(bonus)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self.ai_game.game_over()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _find_shooting_aliens(self):
        ships = {}
        for ship in self.aliens:
            check = ships.get(ship.num)
            if check and ship.row > check.row:
                ships[ship.num] = ship
            else:
                ships[ship.num] = ship
        return tuple(ships.values())

    def _update_bullets(self):
        self.bullets.update()
        self._check_screen_borders(self.bullets)

        self.ai_game.ship.check_ship_bullets_collisions(self.bullets)

    def _update_bonuses(self):
        self.bonuses.update()
        self._check_screen_borders(self.bonuses)

        collisions = pygame.sprite.spritecollide(self.ai_game.ship, self.bonuses, True)
        for bonus in collisions:
            self.stats.enable_bonus(bonus.bonus_type)

    def _check_screen_borders(self, sprite_group: pygame.sprite.Group):
        for sprite in sprite_group.copy():
            if sprite.rect.top >= self.settings.screen_height:
                sprite_group.remove(sprite)


class Alien(Sprite):
    def __init__(self, alien_fleet: AlienFleet, row=0, num=0):
        super().__init__()
        self.fleet = alien_fleet
        self.screen = alien_fleet.screen
        self.settings = alien_fleet.settings

        self.row = row
        self.num = num
        self.type = min(len(self.settings.alien_color) - 1, max(self.row, 0))

        self.image = pygame.image.load("images/alien_bw.png").convert_alpha()
        color_image = pygame.Surface(self.image.get_size()).convert_alpha()
        self.color = self.settings.alien_color[self.type]
        color_image.fill(self.color)
        self.image.blit(color_image, (0, 0), special_flags=pygame.BLEND_MAX)

        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.x + self.rect.width >= \
                screen_rect.right - self.settings.border_offset_x or self.x <= self.settings.border_offset_x:
            return True
        return False

    def update(self) -> None:
        self.x += self.settings.alien_speed_factor * self.settings.fleet_direction
        self.rect.x = self.lerp(self.rect.x, self.x, 0.05)
        self.rect.y = self.lerp(self.rect.y, self.y, 0.05)

    def lerp(self, a, b, t):
        return (1 - t) * a + t * b
