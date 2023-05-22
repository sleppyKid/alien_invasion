from __future__ import annotations

import json
import time
from collections import namedtuple

from typing import TYPE_CHECKING
from bonuses import BonusType, BonusesInfo

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

ScoreInfo = namedtuple('ScoreInfo', [
    'score',
    'level',
    'time',
    'name'
])


class GameStats:
    def __init__(self, ai_game: AlienInvasion):
        self.ai_game = ai_game
        self.settings = ai_game.settings
        self.game_active = False
        self.high_score = 0
        self.level = 1

        self.score_history: list[ScoreInfo] = []
        self.load_score_history()

        self.bonuses = {}
        self.shield = False
        self.unlimited_ammo = False
        self.score_bonus = False

        self.reset_stats()

    def reset_stats(self):
        self.ships_lives = self.settings.ships_lives
        self.score = 0
        self.level = 1
        self.start_time = time.time()
        self.pause_time = 0.0

        self.bonuses.clear()
        self.shield = False
        self.unlimited_ammo = False
        if hasattr(self.ai_game, 'ui'):
            self.ai_game.ui.update_bonuses()

    def fix_pause_timers(self, seconds):
        self.pause_time += seconds
        for bonus in self.bonuses:
            self.bonuses[bonus] += seconds

    def enable_bonus(self, bonus: BonusType):
        if bonus in (BonusType.GOD, BonusType.SHIELD):
            self.ai_game.stats.shield = True
            self.ai_game.ship.image.set_alpha(128)
            self.bonuses[BonusType.SHIELD] = time.time() + BonusesInfo.BONUSES[bonus].timer

        elif bonus == BonusType.HEALTH:
            if self.ai_game.stats.ships_lives < self.settings.ships_lives_bonus_max:
                self.ai_game.stats.ships_lives += 1
                self.ai_game.ui.update_ships_lives()

        elif bonus == BonusType.AMMO:
            self.ai_game.stats.unlimited_ammo = True
            self.bonuses[bonus] = time.time() + BonusesInfo.BONUSES[bonus].timer

        elif bonus == BonusType.SCORE:
            self.score_bonus = True
            self.bonuses[bonus] = time.time() + BonusesInfo.BONUSES[bonus].timer

        self.ai_game.ui.update_bonuses()

    def disable_bonus(self, bonus: BonusType):
        if bonus not in self.bonuses:
            return

        if bonus == BonusType.SHIELD:
            self.shield = False
            self.ai_game.ship.image.set_alpha(255)
        elif bonus == BonusType.AMMO:
            self.unlimited_ammo = False
        elif bonus == BonusType.SCORE:
            self.score_bonus = False

        del self.bonuses[bonus]
        self.ai_game.ui.update_bonuses()

    def update_bonuses(self):
        t = time.time()
        for bonus, end_time in tuple(self.bonuses.items()):
            if t > end_time:
                self.disable_bonus(bonus)

    def load_score_history(self):
        try:
            with open("scores.json", "r") as f:
                self.score_history = [ScoreInfo(*x) for x in json.load(f)]
                if self.score_history:
                    self.high_score = max(self.score_history,
                                          key=lambda x: x.score)[0]
        except FileNotFoundError:
            pass

    def save_score_history(self):
        with open("scores.json", "w") as f:
            json.dump(self.score_history, f, indent=4)

    def add_score(self, name: str):
        total_time = time.time() - (self.start_time + self.pause_time)

        self.score_history.append(ScoreInfo(
            self.score,
            self.level,
            round(total_time, 2),
            name
        ))
        self.save_score_history()

        self.check_high_score()
        self.ai_game.ui.update_highscore()

    def check_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
