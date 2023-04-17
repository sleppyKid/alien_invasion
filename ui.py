from __future__ import annotations

import pygame.font
from pygame.sprite import Group
import pygame_textinput

from button import Button
from ship import Ship
from bonuses import BonusSprite

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class UI:
    def __init__(self, ai_game: AlienInvasion):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.text_color = (230, 230, 230)
        self.play_button = Button(ai_game, "Press P to Start")

        self._prep_name_input()
        self._prep_menu_images()

        self.update_score()
        self.update_highscore()
        self.update_level()
        self.update_ships_lives()
        self.update_bonuses()

    def _prep_text(self, text, font_size=48):
        font = pygame.font.SysFont(None, font_size)
        image = font.render(text, True, self.text_color, self.settings.bg_color)
        image_rect = image.get_rect()
        return image, image_rect

    def _prep_menu_images(self):
        self.pause_image = self._prep_text("Pause!", 62)
        self.pause_image[1].center = self.screen_rect.center

        self.title_image = self._prep_text("Alien Invaders", 80)
        self.title_image[1].center = self.screen_rect.centerx, self.screen_rect.centery // 2

        self.game_over_image = self._prep_text(
            "GAME OVER", 82
        )
        self.game_over_image[1].center = self.screen_rect.center[0], self.screen_rect.center[1] // 2

        self.enter_name_image = self._prep_text(
            "Enter your name:"
        )
        self.enter_name_image[1].midbottom = self.screen_rect.centerx, self.screen_rect.centery - 25

        self.name_info_image = self._prep_text(
            "A name must contain 3 to 10 chars", 25
        )
        self.name_info_image[1].midtop = self.screen_rect.centerx, self.screen_rect.centery + 50

        self._prep_highscore_list()

    def _prep_highscore_list(self):
        self.highscore_list = []
        self.titles_names = ("Name", "Score", "Level", "Time (Minutes)")
        self.highscore_field_size = 200
        self.highscore_offset = (len(self.titles_names) - 1) / 2 * self.highscore_field_size

        title = self._prep_text("Best scores:")
        title[1].center = (
            self.title_image[1].centerx,
            self.title_image[1].centery + 70
        )
        self.highscore_list.append(title)

        for n, t in enumerate(self.titles_names):
            title = self._prep_text(t, 35)
            title[1].center = (
                self.title_image[1].centerx - self.highscore_offset + self.highscore_field_size * n,
                self.title_image[1].centery + 120
            )
            self.highscore_list.append(title)

        self.update_highscore_list()

    def _prep_name_input(self):
        pygame.key.set_repeat(200, 25)
        self.name_input = pygame_textinput.TextInputVisualizer(
            font_color=self.text_color,
            cursor_color=self.text_color,
        )
        text = self.settings.default_player_name
        self.name_input.value = text
        self.name_input.manager.cursor_pos = len(text)

    def update_highscore_list(self):
        title_text_size = len(self.titles_names) + 1
        self.highscore_list[title_text_size:] = []

        scores = sorted(self.stats.score_history, key=lambda x: x[0], reverse=True)[:10]
        height = self.highscore_list[-1][1].centery

        for i, score in enumerate(scores):
            items = score[3], f"{round(score[0]):,}", score[1], round(score[2] / 60, 2)

            for n, item in enumerate(items):
                score_image = self._prep_text(str(item), 32)
                score_image[1].center = (
                    self.title_image[1].centerx - self.highscore_offset + self.highscore_field_size * n,
                    height + (35 * i) + 45,
                )
                self.highscore_list.append(score_image)

    def update_score(self):
        score_str = f"{round(self.stats.score):,}"
        self.score_image, self.score_rect = self._prep_text(score_str)
        self.score_rect.centerx = self.screen_rect.centerx
        self.score_rect.top = self.screen_rect.top + 15

    def update_highscore(self):
        high_score = round(self.stats.high_score)
        high_score_str = f"High score: {high_score:,}"
        self.high_score_image, self.high_score_rect = self._prep_text(high_score_str)
        self.high_score_rect.right = self.screen_rect.right - 20
        self.high_score_rect.top = self.screen_rect.top + 15

        self.update_highscore_list()

    def update_level(self):
        high_score_str = f"Level: {self.stats.level}"
        self.level_image, self.level_rect = self._prep_text(high_score_str)
        self.level_rect.left = self.screen_rect.left + 20
        self.level_rect.bottom = self.screen_rect.bottom - 15

    def update_ships_lives(self):
        self.ships = Group()
        for ship_live in range(self.stats.ships_lives):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_live * (ship.rect.width + 10)
            ship.rect.y = 10
            self.ships.add(ship)

    def update_bonuses(self):
        self.bonuses = Group()
        for x, bonus in enumerate(self.stats.bonuses):
            pos = (x + 1) * (self.settings.bonuses_size + 10) - self.settings.bonuses_size // 2 + 10, 100
            bonus = BonusSprite(self.ai_game, pos, bonus)
            self.bonuses.add(bonus)

    def show_menu(self):
        self.screen.blit(*self.title_image)
        self.play_button.draw_button()

        for hs in self.highscore_list:
            self.screen.blit(*hs)

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.bonuses.draw(self.screen)
        self.ships.draw(self.screen)

    def show_pause(self):
        self.screen.blit(*self.pause_image)

    def show_gameover(self):
        self.screen.blit(*self.game_over_image)
        self.screen.blit(*self.enter_name_image)
        self.screen.blit(*self.name_info_image)

        size_x = self.name_input.surface.get_rect().width
        pos = (self.screen_rect.center[0] - size_x / 2,
               self.screen_rect.center[1])
        self.screen.blit(self.name_input.surface, pos)

    def check_name(self):
        name = self.name_input.value
        if 3 <= len(name) <= 10:
            self.stats.add_score(self.name_input.value)
            return True

        elif len(name) > 10:
            self.name_input.value = name[:10]
        else:
            self.name_input.value = self.settings.default_player_name
            self.name_input.manager.cursor_pos = len(self.name_input.value)
        return False

    def check_play_button(self, mouse_pos):
        if self.ai_game.game_state != self.ai_game.game_state.MENU:
            return
        if self.play_button.rect.collidepoint(mouse_pos):
            self.ai_game.start_game()
