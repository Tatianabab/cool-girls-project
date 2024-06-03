import pygame.image
import math
from datetime import datetime
import my_sql
from button import Button
from sounds import Sounds

players = '[index] INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, ' \
          'time_create TIME NOT NULL, ' \
          'player_id STRING DEFAULT NULL, ' \
          'ship_index INTEGER NOT NULL DEFAULT 0, ' \
          'score INTEGER NOT NULL DEFAULT 0, ' \
          'music_status BOOL DEFAULT 1, ' \
          'sound_status BOOL DEFAULT 1'

levels = '[index] INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, ' \
          'level INTEGER NOT NULL, ' \
          'enemy_speed INTEGER NOT NULL, ' \
          'enemy_hp INTEGER NOT NULL, ' \
          'enemy_damage INTEGER NOT NULL, ' \
          'enemy_spawn_delay INTEGER NOT NULL'


my_sql_util = my_sql.my_sql
my_sql_util.create_table('players', players)
my_sql_util.create_table('levels', levels)



comp_id = '55'


class Settings:
    def __init__(self):
        self.levels_in_db = None
        self.screen_width = 480
        self.screen_height = 720
        self.fps = 60
        self.background = pygame.image.load('images/game_back.png')
        self.background = pygame.transform.scale(self.background,
                                                 (self.screen_width, self.screen_height))

        self.menu_background = pygame.image.load('images/menu_back.png')
        self.menu_background = pygame.transform.scale(self.menu_background,
                                                      (self.screen_width, self.screen_height))

        self.scroll = 0
        self.scroll_step = 2
        self.background_height = self.background.get_height()
        self.background_rect = self.background.get_rect()
        self.tiles = math.ceil(self.screen_width / self.background_height) + 1

        self.icon = pygame.image.load('images/icon.png')

        # self.levels_count = {}
        # for i in range(1, 6):
        #     self.levels_s = pygame.image.load(f'images/level_{i}.png')
        #     self.levels_s = pygame.transform.scale(self.levels_s, (80, 80))
        #     self.levels_count[i - 1] = {}
        #     self.levels_count[i - 1]['level'] = self.levels_s
        # self.level_index = 0

        self.player_ships = {}
        for i in range(1, 7):
            self.player_ship = pygame.image.load(f'images/ship_{i}.png')
            self.player_ship = pygame.transform.scale(self.player_ship, (80, 80))
            self.player_ships[i - 1] = {}
            self.player_ships[i - 1]['ship'] = self.player_ship

        self.player_ships[0]['hp'] = 200
        self.player_ships[0]['speed'] = 6
        self.player_ships[0]['damage'] = 9

        self.player_ships[1]['hp'] = 100
        self.player_ships[1]['speed'] = 10
        self.player_ships[1]['damage'] =5

        self.player_ships[2]['hp'] = 150
        self.player_ships[2]['speed'] = 12
        self.player_ships[2]['damage'] = 3

        self.player_ships[3]['hp'] = 90
        self.player_ships[3]['speed'] = 11
        self.player_ships[3]['damage'] = 10

        self.player_ships[4]['hp'] = 400
        self.player_ships[4]['speed'] = 7
        self.player_ships[4]['damage'] = 2

        self.player_ships[5]['hp'] = 300
        self.player_ships[5]['speed'] = 9
        self.player_ships[5]['damage'] = 6

        self.player_ship_index = 0

        self.bullet_image = pygame.image.load('images/bullet.png')
        self.bullet_image = pygame.transform.scale(self.bullet_image, (10, 20))
        self.bullet_speed = 5

        self.button_start = pygame.image.load("images/button_start.png")
        self.button_start = Button(self.button_start, 0.4, self)
        self.button_start.set_position((self.screen_width - self.button_start.rect.width) // 2,
                                       ( self.screen_height - self.button_start.rect.height) // 2 - self.button_start.rect.height * 2)

        self.button_exit = pygame.image.load("images/back_button.png")
        self.button_exit = Button(self.button_exit, 0.4, self)
        self.button_exit.set_position((self.screen_width - self.button_exit.rect.width) // 2,
                                      (self.screen_height - self.button_exit.rect.height) // 2 + self.button_exit.rect.height * 2)

        self.button_level = pygame.image.load("images/button_resume.png")
        self.button_level = Button(self.button_level, 0.3, self)
        self.button_level.set_position((self.screen_width - self.button_level.rect.width) // 2,
                                      (self.screen_height - self.button_level.rect.height) // 2 + self.button_level.rect.height * 4.5)

        self.options_img = pygame.image.load("images/button_options.png")
        self.options_button = Button(self.options_img, 0.4, self)
        self.options_button.set_position((self.screen_width - self.options_button.rect.width) // 2,
                                         (self.screen_height - self.options_button.rect.height) // 2)

        self.button_back = pygame.image.load("images/button_back.png")
        self.button_back = Button(self.button_back, 0.3, self)
        self.button_back.set_position((self.screen_width - self.button_back.rect.width * 2),
                                      (self.screen_height - self.button_back.rect.height * 2))

        self.button_new_game = pygame.image.load("images/new_game.png")
        self.button_new_game = Button(self.button_new_game, 0.4, self)
        self.button_new_game.set_position((self.screen_width - self.button_start.rect.width) // 2,
                                       (self.screen_height - self.button_start.rect.height) // 2 - self.button_new_game.rect.height * 2)

        self.music_active_image = pygame.image.load("images/button_music_active.png")
        self.music_deactive_image = pygame.image.load("images/button_music_deactive.png")
        self.button_music = Button(self.music_active_image, 0.3, self)
        self.button_music.width_pos = 63
        self.button_music.height_pos = 63

        self.sound_active_image = pygame.image.load("images/button_sound_active.png")
        self.sound_deactive_image = pygame.image.load("images/button_sound_deactive.png")
        self.button_sound = Button(self.sound_active_image, 0.3, self)
        self.button_sound.width_pos = 158
        self.button_sound.height_pos = 63

        self.music_active = True
        self.sound_active = True
        self.menu_music = Sounds("sounds/menu_theme.mp3", 0.5, self)
        self.game_music = Sounds("sounds/game_theme.mp3", 0.2, self)
        self.shot_sound = Sounds("sounds/shot.wav", 0.2, self)
        self.hit = Sounds("sounds/hit.wav", 0.2, self)
        self.bullet_hit = Sounds("sounds/bUllet_hit.wav", 0.2, self)
        self.button_click_sound = Sounds("sounds/button_click.mp3", 0.2, self)

        self.backward = pygame.image.load("images/backward.png")
        self.backward_button = Button(self.backward, 0.3, self)
        self.backward_button.set_position(63, (self.screen_height - self.backward_button.rect.height) // 2)

        self.forward = pygame.image.load("images/forward.png")
        self.forward_button = Button(self.forward, 0.3, self)
        self.forward_button.set_position(self.screen_width - 126,
                                         (self.screen_height - self.forward_button.rect.height) // 2)

        self.ship_description_font = pygame.font.Font(None, 24)
        self.player_score_font = pygame.font.Font(None, 28)

        self.player_game_over_font = pygame.font.Font(None, 50)

        self.player_score = 0
        self.player_record_score = 0

        self.enemy_image = pygame.image.load('images/enemy.png')
        self.enemy_image = pygame.transform.scale(self.enemy_image, (80, 80))

        self.expl_images = []
        for num in range(1, 6):
            image = pygame.image.load(f"images/explosion/exp{num}.png")
            image = pygame.transform.scale(image, (50, 50))
            self.expl_images.append(image)

    def load_bd(self):
        self.levels_in_db = my_sql_util.table_get_all('levels')
        print("-")
        print(self.levels_in_db)
        user_in_db = my_sql_util.table_get('players', 'player_id', comp_id)
        if not user_in_db:
            my_sql_util.table_insert('players', (datetime.now(), comp_id, 0, 0, 1, 1))
        else:
            user_data = user_in_db[0]
            self.player_ship_index = user_data['ship_index']
            self.player_record_score = user_data['score']
            self.music_active = user_data['music_status']
            self.sound_active = user_data['sound_status']

    def update_bd(self, name, data, params):
        my_sql_util.table_update(name, comp_id, data, params)


