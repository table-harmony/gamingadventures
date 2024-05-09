import pygame
from random import choice
from settings import TILESIZE, APPLE_POS, LAYERS


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, z, groups, image=pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)

        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(0, -10)

        self.z = z


class WaterTile(Tile):
    def __init__(self, pos, groups, animations, z=LAYERS['water']):
        super().__init__(pos, z, groups, animations[0])

        self.animation = animations
        self.frame_index = 0

    def animate(self):
        self.frame_index += 0.1
        if self.frame_index > len(self.animation):
            self.frame_index = 0
        self.image = self.animation[int(self.frame_index)]

    def update(self, player):
        if player.sprite_in_screen(self, offset=10):
            self.animate()


class Tree(Tile):
    def __init__(self, pos, type, groups, image, z=LAYERS['trees']):
        super().__init__(pos, z, groups, image)

        self.health = choice([10, 20, 30, 40, 50])
        self.type = type

        self.alive = True

        self.stump_image = pygame.image.load(
            f'graphics/objects/stumps/{self.type}.png').convert_alpha()

        self.apple_image = pygame.image.load(
            'graphics/objects/crops/apple.png').convert_alpha()
        self.create_apples()

    def create_apples(self):
        self.apples = pygame.sprite.Group()

        for _ in range(self.health // 10 - 1):
            direction = choice(APPLE_POS[self.type])
            Apple(self.rect.topleft + direction,
                  [self.apples, self.groups()[0]], self.apple_image)

    def damage(self):
        self.health -= 10

        if self.apples.sprites():
            choice(self.apples.sprites()).kill()

        if self.health <= 0:
            self.alive = False

            self.image = self.stump_image
            self.rect = self.image.get_rect(center=self.rect.center)
            self.hitbox = self.rect.inflate(0, -10)


class Apple(Tile):
    def __init__(self, pos, groups, image, z=LAYERS['trees']):
        super().__init__(pos, z, groups, image)
