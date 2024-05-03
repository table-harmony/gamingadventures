from Platforms import *

pygame.init()

ScreenWidth, ScreenHeight = 500, 500
FPS = 60

font = pygame.font.SysFont('georgia', 25)

player_image_right = pygame.image.load('../assets/player.png')
player_image_left = pygame.transform.flip(player_image_right, 180, 0)

Difficulties = {
    'easy': {'space': 50, 'platform_speed': -3, 'platform_amount': 5},
    'normal': {'space': 30, 'platform_speed': -4, 'platform_amount': 7},
    'hard': {'space': 10, 'platform_speed': -5, 'platform_amount': 10}
}

# main menu platforms
main_menu_group = pygame.sprite.Group()

Platform((ScreenWidth / 2, 8 * ScreenHeight / 10), -1, main_menu_group, 'game',
         font.render('  Tiles Uprising  ', True, 'black', 'white'))

Platform((ScreenWidth / 2, ScreenHeight / 5), -1, main_menu_group, 'play',
         font.render('      play      ', True, 'black', 'white'))

Platform((1.7 * ScreenWidth / 10, 8.7 * ScreenHeight / 10), -1, main_menu_group, image=font.render('       ', True, 'black', 'white'))
Platform((8.7 * ScreenWidth / 10, 9.7 * ScreenHeight / 10), -1, main_menu_group, image=font.render('                 ', True, 'black', 'white'))

texts = ['   easy   ', '   normal   ', '   hard   ']
for text_pos, text in enumerate(texts):
    Platform((ScreenWidth / 8, (text_pos + 1) * ScreenHeight / 5), -1, main_menu_group, 'difficulty_' + text,
             font.render(text, True, 'black', 'white'))


# level platforms
def platforms_group(game_difficulty):
    group = pygame.sprite.Group()

    platform_image = pygame.image.load('../assets/plack.png').convert()
    platform_speed = Difficulties[game_difficulty]['platform_speed']

    for _ in range(Difficulties[game_difficulty]['platform_amount']):
        Platform((ScreenWidth / 2, ScreenHeight), platform_speed, group, image=platform_image)

    return group