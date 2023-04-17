import pygame


class Settings:
    def __init__(self):
        self.fullscreen = False
        self.screen_width = 1280
        self.screen_height = 800
        self.bg_color = (25, 25, 25)
        self.bg_color_game_over = (75, 25, 25)
        self.tick_rate = 100
        self.default_player_name = "Player"

        self.stars_seed = 255  # 0 = always random
        self.stars_scale_min_max = 3, 6
        self.stars_transparency_min_max = 170, 250
        self.stars_num = 100
        self.stars_speed = 1

        self.ship_speed = 3
        self.ships_lives = 2
        self.ships_lives_bonus_max = 3

        self.bonuses_speed = 2
        self.bonuses_size = 50
        self.bonuses_drop_rate = .1
        self.bonus_score_scale = 1.2

        self.bullet_speed = 5
        self.bullet_width = 3  # 300
        self.bullet_height = 15
        self.bullet_color = (220, 220, 220)
        self.bullets_allowed = 3

        self.number_aliens_x = 10
        self.number_aliens_y = 3
        self.start_offset_x = 30
        self.start_offset_y = 50
        self.border_offset_x = 10

        self.fleet_drop_speed = 20
        self.fleet_direction = 1
        self.alien_speed = 1
        self.alien_bullet_width = 5
        self.alien_bullet_height = 15
        self.alien_bullet_color = (220, 0, 0)
        self.alien_color = (
            (200, 0, 0),
            (0, 200, 0),
            (0, 0, 200)
        )
        self.alien_shoot_timer = 5 * 100
        self.alien_shoot_event = pygame.USEREVENT + 1

        self.shelter_count = 3
        self.shelter_pos_y = 130
        self.shelter_height = 4
        self.shelter_width = 15
        self.shelter_brick_size = 8
        self.shelter_brick_distance = 1
        self.shelter_color = (200, 235, 200)

        self.speedup_scale = 1.1
        self.score_scale = 1.25
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = self.ship_speed
        self.bullet_speed_factor = self.bullet_speed
        self.alien_speed_factor = self.alien_speed
        self.alien_shoot_timer_factor = self.alien_shoot_timer

        self.fleet_direction = 1
        self.alien_points = (70, 65, 50)

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_shoot_timer_factor = int(self.alien_shoot_timer_factor * self.speedup_scale)

        self.alien_points = tuple(int(x * self.score_scale) for x in self.alien_points)
