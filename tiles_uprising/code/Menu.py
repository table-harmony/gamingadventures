import pygame
from Platforms import *
from Settings import *
from Figures import *

pygame.init()

Screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))

main_menu_group = pygame.sprite.Group()

font = pygame.font.SysFont('georgia', 25)

Platform((ScreenWidth / 2, 8 * ScreenHeight / 10), -1, main_menu_group, font.render('Liron"s Game', True, 'black', 'white'), 'game')

texts = ['   easy   ', '   normal   ', '   hard   ']

for i in range(3):
    Platform((ScreenWidth / 8, (i + 1) * ScreenHeight / 5), -1, main_menu_group, font.render(texts[i], True, 'black', 'white'), 'difficulty_' + texts[i])

Platform((ScreenWidth / 2, ScreenHeight / 5), -1, main_menu_group, font.render('      play      ', True, 'black', 'white'), 'play')

Platform((8.7 * ScreenWidth / 10, 9.7 * ScreenHeight / 10), -1, main_menu_group, font.render(' settings ', True, 'black', 'white'), 'settings')

player_group = pygame.sprite.GroupSingle()
player = Figure(player_group, main_menu_group)

difficulty = 'normal'

while True:

    # event loop
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()

    Screen.fill('green')

    # platform update
    main_menu_group.draw(Screen)
    main_menu_group.update()

    for sprite in main_menu_group:
        if player.rect.colliderect(sprite.rect):   # if sprite collide with player

            if 'play' == sprite.name:  # if sprite is play platform
                pass
            elif 'game' == sprite.name:  # if sprite is game info platform
                pass
            elif 'settings' == sprite.name:  # if sprite is settings platform
                pass
            elif '_' in sprite.name:  # if sprite is a difficulty platform

                difficulty = sprite.name.split('_')[1].strip(' ')

                if sprite.image != font.render('    ' + difficulty + '    ', True, 'black', 'white'):  # if sprite.image font not red
                    sprite.image = font.render('    ' + difficulty + '    ', True, 'red', 'white')  # make sprite.image font red

        if '_' in sprite.name:  # if sprite is a difficulty platform
            if difficulty != sprite.name.split('_')[1].strip(' '):  # if sprite not red sprite
                sprite.image = font.render(sprite.name.split('_')[1], True, 'black', 'white')  # resetting previous chosen difficulty back to black

    # player update
    player_group.draw(Screen)
    player_group.update()

    # updating self.display
    pygame.time.Clock().tick(FPS)
    pygame.display.update()
