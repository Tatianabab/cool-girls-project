import pygame
from bullet import Bullet
from pygame.sprite import Sprite
from effects import Effect

class Player(Sprite):
    def __init__(self, game):
        super().__init__()
        self.player_ship = None
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.screen_rect = game.screen.get_rect()
        self.current_ship_index = self.settings.player_ship_index
        self.switch_ship(self.current_ship_index)
        self.move_left = False
        self.move_right = False
        self.bullets = pygame.sprite.Group()

    def switch_ship(self, direction):
        total_ships = len(self.settings.player_ships)
        if total_ships > 0:
            if direction == "forward":
                self.current_ship_index = (self.current_ship_index + 1) % total_ships
            elif direction == "backward":
                self.current_ship_index = (self.current_ship_index - 1) % total_ships
            self.settings.update_bd('players', 'ship_index', self.current_ship_index)
            self.player_ship = self.settings.player_ships[self.current_ship_index]['ship']
            print(self.player_ship)
            self.rect = self.player_ship.get_rect()
            self.rect.midbottom = (self.screen_rect.midbottom[0], self.screen_rect.midbottom[1] - 10)
            self.ship_speed = self.settings.player_ships[self.current_ship_index]['speed']
            self.damage = self.settings.player_ships[self.current_ship_index]['damage']
            self.speed = self.settings.player_ships[self.current_ship_index]['speed']
            self.hp = self.settings.player_ships[self.current_ship_index]['hp']
            self.current_hp = self.hp
            self.ship_description = self.settings.ship_description_font.render(
                f"Урон: {self.damage} "
                f"Скорость: {self.speed} "
                f"Здоровье: {self.hp}", True, (180, 0, 0))
            self.ship_description_rect = self.ship_description.get_rect(center=(self.settings.screen_width // 2,
                                                                                self.settings.screen_height // 2 + 60))
    def fire_bullet(self):
        bullet = Bullet(self.game, self.damage)
        self.bullets.add(bullet)



    def update(self):
        self.player_score_text = self.settings.player_score_font.render(
            f"Очки: {self.settings.player_score}", True, (180, 0, 0))
        self.player_score_text_rect = self.player_score_text.get_rect(
            topright=(self.screen.get_width(), 0))
        self.player_score_text_rect.topright = (
            self.player_score_text_rect.topright[0] - 10,
            self.player_score_text_rect.topright[1] + 10)

        if self.move_left and self.rect.left > 0:
            self.rect.x -= self.ship_speed
        elif self.move_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.ship_speed
        collided_enemies = pygame.sprite.spritecollide(self, self.game.enemy_group, True)

        for enemy in collided_enemies:
            self.current_hp -= enemy.enemy_damage
            if self.current_hp <= 0:
                self.game.game_over = True
                self.settings.update_bd('players', 'score', self.settings.player_record_score)

            self.settings.hit.run_sound_effect()
            effect = Effect(enemy.rect.center[0], enemy.rect.center[1], self.settings)
            self.game.explosion_group.add(effect)
            enemy.kill()
    def blit_player(self):
        ratio = self.current_hp / self.hp
        self.screen.blit(self.player_score_text, self.player_score_text_rect)
        pygame.draw.rect(self.screen, "red", (20, 20, 200, 20))
        pygame.draw.rect(self.screen, "green", (20, 20, 200 * ratio, 20))
        self.screen.blit(self.player_ship, self.rect)
