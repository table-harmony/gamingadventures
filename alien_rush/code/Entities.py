import pygame
from settings import *


class Entity(pygame.sprite.Sprite):
    def __init__(self, speed, health, my_group, image):
        super().__init__(my_group)

        # screen
        self.display = pygame.display.get_surface()

        self.my_group = my_group

        # image
        self.image = image
        self.rect = self.image.get_rect()

        self.speed = speed
        self.health = health

        # movement
        self.direction = pygame.math.Vector2()

        # lasers
        self.my_lasers = pygame.sprite.Group()
        self.laser_countdown = 0

    def check_alive(self, group):
        if self.health <= 0:
            self.kill()
        for sprite in group:
            for laser in sprite.my_lasers:
                if laser.rect.colliderect(self.rect):
                    self.health -= 1
                    laser.kill()

    def screen_containment(self):

        if self.rect.bottom >= ScreenHeight:
            self.rect.bottom = ScreenHeight
        elif self.rect.top <= 0:
            self.rect.top = 0

        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= ScreenWidth:
            self.rect.right = ScreenWidth

    def move(self):
        if self.direction:
            self.direction = self.direction.normalize()

        self.rect.center += self.direction * self.speed

    def entity_update(self):
        # movement
        self.move()
        self.screen_containment()

        # lasers
        self.my_lasers.draw(self.display)
        self.my_lasers.update()
