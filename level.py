import pygame
import random
from enemy import Enemy

class Level:
    def __init__(self, level, enemy_speed, enemy_hp, enemy_damage, enemy_spawn_delay, game):
        self.game = game
        self.settings = self.game.settings
        self.level = level
        self.enemy_speed = enemy_speed
        self.enemy_hp = enemy_hp
        self.enemy_damage = enemy_damage
        self.enemy_spawn_delay = enemy_spawn_delay
        self.current_spawn_delay = enemy_spawn_delay
        self.last_enemy_spawn_time = 0


    def level_background_update(self):
        self.settings.scroll += self.settings.scroll_step
        for i in range(0, self.settings.tiles):
            self.game.screen.blit(self.settings.background,
                                  (0, i * -self.settings.background_height + self.settings.scroll))
            self.settings.background_rect.y = i * self.settings.background_height + self.settings.scroll
        if abs(self.settings.scroll) > self.settings.background_height:
            self.settings.scroll = 0

    def level_enemy_spawn(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_enemy_spawn_time >= self.current_spawn_delay:
            max_count = min(3, 5 - self.current_spawn_delay // 1000)
            if self.current_spawn_delay > 1000:
                self.current_spawn_delay -= 50
            count = random.randint(1, max_count)
            for _ in range(count):
                self.step = random.randint(50, 250)
                enemy = Enemy(self.game, self.step)
                self.game.enemy_group.add(enemy)
            self.last_enemy_spawn_time = current_time
        self.game.enemy_group.update()
        self.game.enemy_group.draw(self.game.screen)

    def restart_level(self):
        self.game.player.current_hp = self.game.player.hp
        self.game.settings.player_score = 0
        self.game.enemy_group.empty()
        self.game.explosion_group.empty()
        self.game.level_now.last_enemy_spawn_time = 0
        self.game.level_now.current_spawn_delay = self.game.levels[self.game.current_game_level].enemy_spawn_delay
        self.game.game_over = False

    def switch_level(self, direction):

        total_level = len(self.settings.levels_in_db)
        if total_level > 0:
            if direction == "forward":
                self.game.current_game_level = (self.game.current_game_level + 1) % total_level
            elif direction == "backward":
                self.game.current_game_level = (self.game.current_game_level - 1) % total_level
        print(self.game.current_game_level + 1)
