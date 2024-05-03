from Figure import *
from Enemies import *

pygame.init()


class Level:
    def __init__(self, name):

        # screen
        self.display = pygame.display.get_surface()

        self.name = name  # level name

        self.waves = 0
        self.font = pygame.font.SysFont('georgia', 20)

        self.player_group = pygame.sprite.GroupSingle()
        self.player = Player(5, 5, self.player_group, pygame.image.load('../assets/player_image.png'))

        # enemy group
        self.enemy_group = pygame.sprite.Group()

    def display_stuff(self):

        font = self.font

        # wave number
        self.display.blit(font.render('Level: ' + str(self.waves), True, 'black', 'white'), (10, 10))

        # player hearts
        for i in range(self.player.health):
            self.display.blit(pygame.image.load('../assets/player_hearts.png'), (20 * (i + 0.5), 40))

        # enemies
        for i in range(len(self.enemy_group)):
            self.display.blit(pygame.image.load('../assets/enemy_symbol.png'), (20 * (i + 0.5), 80))

    def respawn_enemies(self):
        if not self.enemy_group:
            self.waves += 1  # next wave

            for _ in range(random.randrange(0, 8)):
                enemy_name = random.choice(['long_shooter', 'shooter', 'suicidal'])
                enemy_image = pygame.image.load(enemies[enemy_name]['image'] + '.png')
                Enemy(enemies[enemy_name]['enemy_speed'], enemies[enemy_name]['enemy_health'], enemy_name, self.enemy_group, enemy_image)

    def level_update(self):

        self.display_stuff()

        # updating player
        self.player_group.draw(self.display)
        self.player_group.update(self.enemy_group)

        # updating enemies
        self.enemy_group.draw(self.display)
        self.enemy_group.update(self.player_group)

        self.respawn_enemies()
