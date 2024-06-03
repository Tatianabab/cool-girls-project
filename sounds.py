import pygame


class Sounds:
    def __init__(self, bg_music, level, settings):
        self.settings = settings
        self.bg_music = bg_music
        self.level = level
        self.play = False

    def run_music(self):
        if not self.play and self.settings.music_active:
            self.play = True
            pygame.mixer.music.load(self.bg_music)
            pygame.mixer.music.set_volume(self.level)
            pygame.mixer.music.play(-1)

    def stop_music(self):
        if self.play:
            self.play = False
            pygame.mixer.music.stop()

    def set_volume(self, level):
        self.level = level
        pygame.mixer.music.set_volume(self.level)

    def run_sound_effect(self, force_sound=False):
        if self.settings.sound_active or force_sound:
            sound = pygame.mixer.Sound(self.bg_music)
            sound.play()