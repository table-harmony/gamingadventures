import pygame
import random


class Platform(pygame.sprite.Sprite):
    def __init__(self, center, speed: int or float, my_group, name='platform', image=pygame.Surface((100, 20))):
        super().__init__(my_group)

        # name / identification
        self.name = name

        # group self belongs to
        self.my_group = my_group

        # looks
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = center

        # movement
        self.speed = speed

    def respawn(self):
        ScreenWidth, ScreenHeight = pygame.display.get_window_size()  # screen size

        if self.rect.bottom <= 0:
            self.rect.centerx = random.randrange(10 + self.rect.width, ScreenWidth - self.rect.width - 10)
            self.rect.centery = random.randrange(ScreenHeight, ScreenHeight + 300)

    def move(self):
        self.rect.centery += self.speed

    def update(self):
        self.respawn()
        self.move()
