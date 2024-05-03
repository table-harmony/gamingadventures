import random
from Entities import *
from Lasers import *
from settings import *


class Enemy(Entity):
    def __init__(self, speed, health, name, my_group, image=pygame.Surface((20, 20))):
        super().__init__(speed, health, my_group, image)

        self.status = 'idle'
        self.name = name

        self.rect = self.rect.inflate(25, 25)  # enlarging rect

        self.rect.center = random.randrange(0, ScreenWidth), random.randrange(0, ScreenHeight)

        self.laser_cool_down = enemies[self.name]['laser_cool_down']
        self.attack_range = enemies[self.name]['attack_range']
        self.notice_range = enemies[self.name]['notice_range']

    def player_enemy_distance(self, player):
        player_x, player_y = player.rect.center
        self_x, self_y = self.rect.center

        self.direction = pygame.Vector2(player_x - self.rect.centerx, player_y - self.rect.centery)
        return ((self_x - player_x)**2 + (self_y - player_y)**2) ** 0.5

    def get_status(self, player):
        distance = self.player_enemy_distance(player)

        if self.attack_range >= distance:
            self.status = 'attack'
        elif self.notice_range >= distance:
            self.status = 'move'
        else:
            self.status = 'idle'

    def change_pos(self):
        if self.status == 'move':
            self.move()

    def attack(self, player):
        if self.name == 'long_shooter' or self.name == 'shooter':
            if self.status == 'attack' and self.laser_countdown >= self.laser_cool_down:
                self.laser_countdown = 0
                Laser(6, self.direction, self.rect.center, self.my_lasers, pygame.image.load('../assets/enemy_laser.png'))
        elif self.name == 'suicidal':
            if self.status == 'attack':
                self.kill()
                player.health -= 1

    def update(self, player_group):
        self.get_status(player_group.sprite)

        self.change_pos()
        self.entity_update()

        self.laser_countdown += 1
        self.attack(player_group.sprite)

        self.check_alive(player_group)
