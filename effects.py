import pygame
from pygame.sprite import Sprite


class Effect(Sprite):
    def __init__(self, x, y, settings):
        super().__init__()
        self.index = 0
        self.settings = settings
        self.images = self.settings.expl_images
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 4
        self.counter += 1
        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
