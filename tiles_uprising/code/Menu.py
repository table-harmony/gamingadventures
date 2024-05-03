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