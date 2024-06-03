import pygame


class Button:
    def __init__(self, image, scale, settings):
        self.image = image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.settings = settings
        self.scale = scale
        self.set_size()
        self.clicked = False

    def set_position(self, x, y):
        self.rect.topleft = (x, y)

    def set_image(self, image):
        self.image = image
        self.set_size()

    def set_size(self):
        self.image = pygame.transform.scale(self.image, (int(self.width * self.scale), int(self.height * self.scale)))
        self.rect = self.image.get_rect()

    def draw(self, surface, sound=True, force_sound=False):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
                if sound:
                    self.settings.button_click_sound.run_sound_effect(force_sound=force_sound)
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action
