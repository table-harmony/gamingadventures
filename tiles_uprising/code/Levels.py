from Figures import *
from Settings import *


class Level:
    def __init__(self, name, platforms):

        # screen
        self.display = pygame.display.get_surface()

        self.name = name  # level name

        # platforms in level
        self.platforms = platforms

        # player in level
        self.player_group = pygame.sprite.GroupSingle()
        self.player = Figure(self.player_group, self.platforms, player_image_right)

        self.run_time = 0

    def platforms_update(self):

        # drawing and updating sprites in platforms_group
        self.platforms.draw(self.display)
        self.platforms.update()

    def player_update(self):

        # drawing and updating sprites (player) in player_group
        self.player_group.draw(self.display)
        self.player_group.update()
