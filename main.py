import pygame
from settings import Settings
from player import Player
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.settings.load_bd()
        self.levels = []
        for number, level in enumerate(self.settings.levels_in_db):
            self.levels_s = pygame.image.load(f'images/level_{number+1}.png')
            self.levels_s = pygame.transform.scale(self.levels_s, (80, 80))
            level['image'] = self.levels_s
            self.levels.append(Level(level['level'],
                                     level['enemy_speed'],
                                     level['enemy_hp'],
                                     level['enemy_damage'],
                                     level['enemy_spawn_delay'],
                                     self))
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height), pygame.DOUBLEBUF | pygame.HWSURFACE)
        pygame.display.set_caption("COOL GIRLS")
        pygame.display.set_icon(self.settings.icon)
        self.current_game_level = 0

        self.enemy_group = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()

        self.level_now = self.levels[self.current_game_level]
        self.player = Player(self)
        self.game_begin = False
        self.in_menu = True
        self.in_options = False
        self.game_over = False
        self.in_level = False
    def run_game(self):
        clock = pygame.time.Clock()
        while True:
            if not self.game_begin:
                self._check_menu_events()
                if self.in_menu:
                    self.settings.menu_music.run_music()
                    self._update_menu_screen()
                elif self.in_options:
                    self._update_options_screen()
                elif self.in_level:
                    self._update_level_screen()
            else:
                self.settings.menu_music.stop_music()
                self.settings.game_music.run_music()
                self._check_game_events()
                self.player.update()
                self.player.bullets.update()
                self._update_game_screen()
            clock.tick(self.settings.fps)

    def restart_game(self):
        self.player.current_hp = self.player.hp
        self.settings.player_score = 0
        self.enemy_group.empty()
        self.explosion_group.empty()
        self.level_now.last_enemy_spawn_time = 0
        self.level_now.current_spawn_delay = self.levels[self.current_game_level].enemy_spawn_delay
        self.game_over = False
    def _check_game_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.settings.update_bd('players', 'score', self.settings.player_record_score)
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.settings.shot_sound.run_sound_effect()
                    self.player.fire_bullet()
                if event.key == pygame.K_RETURN and self.game_over:
                    self.level_now.restart_level()
        keys = pygame.key.get_pressed()
        self.player.move_left = keys[pygame.K_a]
        self.player.move_right = keys[pygame.K_d]
    def _check_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
    def _update_game_screen(self):
        if not self.game_over:
            self.level_now.level_background_update()
            self.explosion_group.draw(self.screen)
            self.explosion_group.update()
            self.level_now.level_enemy_spawn()
            self.player.blit_player()
            self.player.bullets.draw(self.screen)
        else:
             self._update_game_over_screen()
        pygame.display.update()

    def _update_game_over_screen(self):
        self.screen.blit(self.settings.menu_background, (0, 0))
        self.player_game_over_text = self.settings.player_game_over_font.render("GAME OVER", True, (180, 0, 0))
        self.player_game_over_text_rect = self.player_game_over_text.get_rect()
        self.player_game_over_text_rect.centerx = self.screen.get_rect().centerx
        self.player_game_over_text_rect.centery = self.screen.get_rect().centery
        self.screen.blit(self.player_game_over_text, self.player_game_over_text_rect)
        if self.settings.button_new_game.draw(self.screen):
            self.game_begin = True
            self.game_over = False
            self.restart_game()
        if self.settings.button_exit.draw(self.screen):
            self.game_over = False
            self.game_begin = False
            self.in_menu = True
        pygame.display.update()

    def _update_level_screen(self):
        self.screen.fill('black')
        if self.settings.button_back.draw(self.screen):
            self.in_menu = True
            self.in_level = False
        if self.settings.backward_button.draw(self.screen):
            self.level_now.switch_level("backward")
        if self.settings.forward_button.draw(self.screen):
            self.level_now.switch_level("forward")

        self.screen.blit(self.settings.levels_in_db[self.current_game_level]['image'],
                         self.settings.levels_in_db[self.current_game_level]['image'].get_rect(center=self.screen.get_rect().center))
        pygame.display.update()

    def _update_menu_screen(self):
        self.screen.blit(self.settings.menu_background, (0, 0))
        self.player_record_score_text = self.settings.player_score_font.render(
            f"Топ очков: {self.settings.player_record_score}", True, (180, 0, 0))
        self.player_record_score_text_rect = self.player_record_score_text.get_rect()
        self.player_record_score_text_rect.centerx = self.screen.get_rect().centerx
        self.player_record_score_text_rect.top = 100
        self.screen.blit(self.player_record_score_text, self.player_record_score_text_rect)
        if self.settings.button_start.draw(self.screen):
            print(self.level_now.enemy_speed)
            self.game_begin = True
            self.in_menu = False
        if self.settings.options_button.draw(self.screen):
            self.in_menu = False
            self.in_options = True
        if self.settings.button_level.draw(self.screen):
            self.in_menu = False
            self.in_level = True
        if self.settings.button_exit.draw(self.screen):
            exit()


        pygame.display.update()

    def _update_options_screen(self):
        self.screen.fill('black')
        if self.settings.button_back.draw(self.screen):
            self.in_menu = True
            self.in_options = False
        if self.settings.music_active:
            self.settings.button_music.set_image(self.settings.music_active_image)
            self.settings.button_music.set_position(self.settings.button_music.width_pos,
                                                    self.settings.button_music.height_pos)
            if self.settings.button_music.draw(self.screen):
                self.settings.music_active = False
                self.settings.menu_music.stop_music()
                self.settings.update_bd('players', 'music_status', 0)
        else:
            self.settings.button_music.set_image(self.settings.music_deactive_image)
            self.settings.button_music.set_position(self.settings.button_music.width_pos,
                                                    self.settings.button_music.height_pos)
            if self.settings.button_music.draw(self.screen):
                self.settings.music_active = True
                self.settings.menu_music.run_music()
                self.settings.update_bd('players', 'music_status', 1)

        if self.settings.sound_active:
            self.settings.button_sound.set_image(self.settings.sound_active_image)
            self.settings.button_sound.set_position(self.settings.button_sound.width_pos,
                                                    self.settings.button_sound.height_pos)
            if self.settings.button_sound.draw(self.screen, sound=False):
                self.settings.sound_active = False
                self.settings.update_bd('players', 'sound_status', 0)
        else:
            self.settings.button_sound.set_image(self.settings.sound_deactive_image)
            self.settings.button_sound.set_position(self.settings.button_sound.width_pos,
                                                    self.settings.button_sound.height_pos)
            if self.settings.button_sound.draw(self.screen, sound=True, force_sound=True):
                self.settings.sound_active = True
                self.settings.update_bd('players', 'sound_status', 1)

        if self.settings.backward_button.draw(self.screen):
            self.player.switch_ship("backward")
        if self.settings.forward_button.draw(self.screen):
            self.player.switch_ship("forward")

        self.screen.blit(self.player.ship_description, self.player.ship_description_rect)
        self.screen.blit(self.player.player_ship,
                         self.player.player_ship.get_rect(center=self.screen.get_rect().center))
        pygame.display.update()


if __name__ == '__main__':
    ai = Game()
    ai.run_game()
