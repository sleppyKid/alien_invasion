from __future__ import annotations
import pygame.font
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class Button:
    def __init__(self, aigame: AlienInvasion, msg: str):
        self.screen = aigame.screen
        self.screen_rect = self.screen.get_rect()

        self.width, self.height = 350, 50
        self.button_color = aigame.settings.bg_color
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midbottom = (self.screen_rect.midbottom[0],
                               self.screen_rect.midbottom[1] - 35)

        self._prep_msg(msg)

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
