import pygame
from pygame.sprite import Sprite
from effects import Effect


class Bullet(Sprite):
    def __init__(self, game, damage):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.image = self.settings.bullet_image
        self.rect = self.settings.bullet_image.get_rect()
        self.rect.midtop = game.player.rect.midtop
        self.bullet_damage = damage

    def update(self):
        self.rect.y -= self.settings.bullet_speed
        for bullet in self.game.player.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.game.player.bullets.remove(bullet)
        collisions = pygame.sprite.groupcollide(self.game.player.bullets, self.game  .enemy_group, True, False)
        for bullet, enemies in collisions.items():
            for enemy in enemies:
                enemy.enemy_hp -= self.bullet_damage
                self.settings.bullet_hit.run_sound_effect()
                if enemy.enemy_hp <= 0:
                    enemy.kill()
                    self.settings.player_score +=1
                    if self.settings.player_score > self.settings.player_record_score:
                        self.settings.player_record_score = self.settings.player_score

                    effect = Effect(enemy.rect.center[0], enemy.rect.center[1], self.settings)
                    self.game.explosion_group.add(effect)
