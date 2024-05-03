import pygame
from Settings import *


class Figure(pygame.sprite.Sprite):
    def __init__(self, my_group, collision_objects=None, image=pygame.Surface((20, 20), 10)):
        super().__init__(my_group)

        # screen
        self.display = pygame.display.get_surface()
        self.with_in_screen = True  # player cant go over screen (for now)

        # platforms
        self.collision_objects = collision_objects

        # image
        self.image = image

        self.rect = self.image.get_rect()
        self.rect.center = ScreenWidth / 2, ScreenHeight / 2

        # movement
        self.direction = pygame.math.Vector2()

        self.speed = 1
        self.gravity = 0.8

        # jumping
        self.jumps_in_air = 0
        self.jump_speed = -16
        self.jumping = False
        self.jumping_timer = 0

    def get_input(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction.x = 5

            self.image = player_image_left

        elif keys[pygame.K_a]:
            self.direction.x = -5

            self.image = player_image_right

        else:
            self.direction.x = 0

        if (keys[pygame.K_SPACE] or keys[pygame.K_j]) and not self.jumping and self.jumps_in_air <= 1:
            self.jump()
            self.jumping = True
            self.jumps_in_air += 1

    def jump(self):
        self.direction.y = self.jump_speed

    def apply_gravity(self):
        self.direction.y += self.gravity

    def cool_down(self):

        if self.jumping:
            self.jumping_timer += 1

            if self.jumping_timer >= FPS / 2:
                self.jumping = False
                self.jumping_timer = 0

    def horizontal_movement_collision(self, group):
        self.apply_gravity()  # applying player gravity
        self.rect.y += self.direction.y * self.speed  # moving player

        for sprite in group:
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    self.jumps_in_air = 0

                elif self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom

    def vertical_movement_collision(self, group):
        self.rect.x += self.direction.x * self.speed  # moving player

        for sprite in group:
            if sprite.rect.colliderect(self.rect):

                if self.direction.x > 0:
                    self.rect.right = sprite.rect.left
                elif self.direction.x < 0:
                    self.rect.left = sprite.rect.right

                self.jumps_in_air = 0

    def screen_containment(self):
        if self.with_in_screen:  # if player is not allowed beyond screen

            if self.rect.bottom > ScreenHeight:
                self.rect.bottom = ScreenHeight
                self.jumps_in_air = 0
            elif self.rect.top < 0:
                self.rect.top = 0
                self.jumps_in_air = 0

            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right > ScreenWidth:
                self.rect.right = ScreenWidth

    def update(self):
        self.get_input()

        self.cool_down()

        # movement
        self.horizontal_movement_collision(self.collision_objects)
        self.vertical_movement_collision(self.collision_objects)

        self.screen_containment()
