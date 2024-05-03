from Levels import *
from Settings import *


class Game:

    def __init__(self):

        # screen
        self.display = pygame.display.set_mode((ScreenWidth, ScreenHeight))
        pygame.display.set_caption('Game')

        self.background_color = 'grey'

        # level
        self.game_difficulty = 'easy'
        self.Level = Level('main_menu', main_menu_group)

        self.run_time = 0

    def change_level(self):

        level = self.Level  # game level
        player = self.Level.player  # player in level
        platforms = self.Level.platforms  # platforms in level

        if level.name == 'main_menu':  # level is main menu

            player.with_in_screen = True  # screen containment is True

            for sprite in platforms:
                if player.rect.colliderect(sprite.rect):  # if sprite collide with player

                    if 'play' == sprite.name:  # if sprite is play platform
                        self.Level = Level('level', platforms_group(self.game_difficulty))

                    elif 'difficulty_' in sprite.name:  # if sprite is a self.difficulty platform
                        self.game_difficulty = sprite.name.split('_')[1].strip(' ')

                        if sprite.image != font.render('   ' + self.game_difficulty + '   ', True, 'black',
                                                       'white'):  # if sprite.image font not red
                            sprite.image = font.render('   ' + self.game_difficulty + '   ', True, 'red',
                                                       'white')  # make sprite.image font red

                if 'difficulty_' in sprite.name:  # if sprite is a self.difficulty platform
                    if self.game_difficulty != sprite.name.split('_')[1].strip(' '):  # if sprite not red sprite
                        sprite.image = font.render(sprite.name.split('_')[1], True, 'black',
                                                   'white')  # resetting previous chosen self.difficulty back to black

        elif level.name == 'level':  # level is actual game

            player.with_in_screen = False  # screen containment is False

            self.display.blit(font.render('Score : ' + str(int(self.run_time)), True, 'black', self.background_color),
                              (10, 10))  # displaying run time
            self.display.blit(font.render(self.game_difficulty, True, 'black', self.background_color),
                              (10, 40))  # displaying game difficulty

            space = Difficulties[self.game_difficulty]['space']
            if not -space <= player.rect.y <= ScreenHeight + space:  # player not in screen

                player.kill()  # killing player

                text = font.render('You Lost, Good Game', True, 'black', self.background_color)
                self.display.blit(text, (ScreenWidth / 2 - text.get_width() / 2,
                                         ScreenHeight / 2 - text.get_height() / 2))  # displaying losing statement

                return_text = font.render('Main Menu', True, 'black', 'white')
                self.display.blit(return_text, (ScreenWidth / 2 - return_text.get_width() / 2,
                                                ScreenHeight / 2 + text.get_height() / 2 + return_text.get_height() / 2))

                # restarting game
                if pygame.mouse.get_pressed()[0]:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    if ScreenHeight / 2 - text.get_height() / 2 + return_text.get_height() / 2 <= mouse_y <= \
                            ScreenHeight / 2 + text.get_height() / 2 + 1.5 * return_text.get_height():
                        if ScreenWidth / 2 - return_text.get_width() / 2 <= mouse_x <= ScreenWidth / 2 + return_text.get_width() / 2:
                            self.Level = Level('main_menu', main_menu_group)
                            self.run_time = 0

            else:  # player in screen
                self.run_time += 1 / FPS  # updating run time

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
            self.display.fill(self.background_color)

            self.Level.platforms_update()  # updating platforms in level
            self.change_level()  # checking level events
            self.Level.player_update()  # updating player in level

            # updating self.display
            pygame.time.Clock().tick(FPS)
            pygame.display.update()


# running Game
if __name__ == '__main__':
    Game().run()
