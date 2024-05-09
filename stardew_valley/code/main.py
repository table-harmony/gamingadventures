from level import *


pygame.init()


class Game:
    def __init__(self):

        # screen setup
        self.screen = pygame.display.set_mode((Screen_Width, Screen_Height))
        pygame.display.set_caption('Stardew Valley')

        # clock
        self.clock = pygame.time.Clock()

        # level
        self.level = Level()

    def run(self):

        # game loop
        while True:

            # events
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()

            self.level.run()

            self.clock.tick(FPS)
            pygame.display.update()


if __name__ == '__main__':
    Game().run()
