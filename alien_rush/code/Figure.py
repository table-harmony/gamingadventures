from Lasers import *
from Entities import *
from math import atan


class Player(Entity):
    def __init__(self, speed, health, my_group, image=pygame.Surface((20, 20))):
        super().__init__(speed, health, my_group, image)

        self.rect.center = ScreenWidth / 2, ScreenHeight / 2

    def get_input(self):
        keys = pygame.key.get_pressed()

        # movement
        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        # shoot
        if pygame.mouse.get_pressed()[0]:
            self.shoot()

    def shoot(self):
        if self.laser_countdown >= FPS / 2:

            mouse_x, mouse_y = pygame.mouse.get_pos()  # mouse position

            # laser direction
            laser_direction = pygame.Vector2(mouse_x - self.rect.centerx, mouse_y - self.rect.centery)

            Laser(6, laser_direction.normalize(), self.rect.center, self.my_lasers, pygame.image.load('../assets/player_laser.png'))

            # reset countdown
            self.laser_countdown = 0

    def update(self, enemy_group):
        self.get_input()

        self.laser_countdown += 1

        self.entity_update()
        self.check_alive(enemy_group)
