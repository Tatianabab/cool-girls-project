import pygame
import random
from pygame.sprite import Sprite


class Enemy(Sprite):
    def __init__(self, game, step):
        super().__init__()
        self.game = game
        self.step = step
        self.settings = game.settings
        self.image = self.settings.enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, self.settings.screen_width - self.rect.width)
        self.rect.y = -self.rect.height - self.step
        self.enemy_speed = self.game.levels[self.game.current_game_level].enemy_speed
        self.enemy_hp = self.game.levels[self.game.current_game_level].enemy_hp
        self.enemy_damage = self.game.levels[self.game.current_game_level].enemy_damage

    def update(self):
        self.rect.y += self.enemy_speed
        for enemy in self.game.enemy_group.copy():
            if enemy.rect.top >= self.settings.screen_height:
                self.game.enemy_group.remove(enemy)
