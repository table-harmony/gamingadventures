import pygame
from settings import *


class Laser(pygame.sprite.Sprite):
    def __init__(self, speed, direction, center, my_group, image=pygame.Surface((20, 20))):
        super().__init__(my_group)

        # image
        self.image = image

        self.rect = self.image.get_rect()
        self.rect.center = center

        self.direction = direction
        self.speed = speed

    def destroy_laser(self):
        if not 0 <= self.rect.x <= ScreenWidth and 0 <= self.rect.y <= ScreenHeight:  # if laser out of screen
            self.kill()  # kill laser

    def collision(self, group):
        for sprite in group:
            if self.rect.colliderect(sprite.rect):
                self.kill()
                sprite.health -= 1

    def move(self):
        self.rect.center += self.direction * self.speed

    def update(self):
        self.move()

        self.destroy_laser()  # destroying lasers which are out of the screen
