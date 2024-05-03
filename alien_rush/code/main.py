from Levels import *
from settings import *


class Game:

    def __init__(self):

        # screen
        self.display = pygame.display.set_mode((ScreenWidth, ScreenHeight))
        pygame.display.set_caption('first AI game')

        self.background = pygame.transform.scale(pygame.image.load('../assets/background.jpg'), (1000, 563))

        self.Level = Level('Game')

    def run(self):

        # game loop
        while True:

            # event loop
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()

            # updating screen
            self.display.blit(self.background, (0, 0))

            self.Level.level_update()

            # updating self.display
            pygame.time.Clock().tick(FPS)
            pygame.display.update()


# running Game
if __name__ == '__main__':
    Game().run()
