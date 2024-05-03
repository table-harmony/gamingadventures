import pygame

pygame.init()
pygame.mixer.get_init()

# screen settings

ScreenWidth = 900
ScreenHeight = 600
screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))
pygame.display.set_caption("game .4 SPACE_SHIP")

# colors

SPACE_BACKGROUND = pygame.transform.scale(pygame.image.load("assets/bg.jpg"), (ScreenWidth, ScreenHeight))
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

FPS = 60
clock = pygame.time.Clock()

# space ship settings
space_ship_velocity = 10

x_left = 100
y_left = ScreenHeight // 3

x_right = ScreenWidth - 100
y_right = y_left

ship_width = 60
ship_height = 40

space_ship = pygame.transform.scale(pygame.image.load("assets/space_ship.png"), (ship_width, ship_height))

left_space_ship = pygame.transform.rotate(space_ship, 90)
right_space_ship = pygame.transform.rotate(space_ship, 270)

# bullet settings

width_bullet = 10
height_bullet = 5

left_bullet_velocity = 5
right_bullet_velocity = -left_bullet_velocity

left_bullets = []
right_bullets = []

maximum_bullets = 10


def draw(bullets, color):
    pygame.draw.line(screen, BLACK, (ScreenWidth // 2, 0), (ScreenWidth // 2, ScreenHeight), 5)
    for bullet in bullets:
        x = bullet[0]
        y = bullet[1]
        bullet_points = [(x, y), (x + width_bullet, y),
                         (x + width_bullet, y + height_bullet),
                         (x, y + height_bullet)]

        pygame.draw.polygon(screen, color, bullet_points)


def ship_control(key_list, x, y):
    if key_list[0] and y >= 0:
        y -= space_ship_velocity

    if key_list[1] and (0 <= x < ScreenWidth // 2 or ScreenWidth // 2 < x):
        x -= space_ship_velocity

    if key_list[2] and y + ship_height <= ScreenHeight:
        y += space_ship_velocity

    if key_list[3] and (x + ship_width < ScreenWidth // 2 or ScreenWidth // 2 < x + ship_width <= ScreenWidth):
        x += space_ship_velocity

    return x, y


def change_bullet_pos(bullets, velocity):
    for bullet in bullets:
        bullet[0] += velocity
    return bullets


def remove_bullets(left_bullets, right_bullets, width, height):
    left_to_remove = []
    right_to_remove = []
    for left_bullet in left_bullets:
        if left_bullet[0] >= ScreenWidth:
            left_to_remove.append(left_bullet)

        for right_bullet in right_bullets:
            if left_bullet[0] <= right_bullet[0] <= left_bullet[0] + width and left_bullet[1] <= right_bullet[1] <= \
                    left_bullet[1] + height:
                left_to_remove.append(left_bullet)
                right_to_remove.append(right_bullet)

    return left_to_remove, right_to_remove


def changing_bullet_list(bullets, to_remove, x, y, score_player):
    for bullet in bullets:
        if bullet in to_remove or bullet[0] < 0:
            bullets.remove(bullet)

        if x <= bullet[0] <= x + ship_width and y <= bullet[1] <= y + ship_height + 20:
            bullets.remove(bullet)
            score_player -= 1

    return bullets, score_player


score_left = 10
score_right = 10

# texts and sounds
font = pygame.font.SysFont("comicsansms", 25)

health_text = font.render("HEALTH", True, WHITE, False)

shot_sound = pygame.mixer.Sound("assets/gun_shot.wav")

stop = False
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

            if event.key == pygame.K_r and stop:
                stop = False
                score_left = 10
                score_right = score_left

                x_left = 100
                x_right = ScreenWidth - 100

                y_left = ScreenHeight // 2
                y_right = y_left

                left_bullets = []
                right_bullets = []

            if event.key == pygame.K_f and len(left_bullets) < maximum_bullets and not stop:
                left_bullets.append([x_left + 15, y_left + ship_height * 0.65])

                pygame.mixer.Sound.play(shot_sound)

            if event.key == pygame.K_RCTRL and len(right_bullets) < maximum_bullets and not stop:
                right_bullets.append([x_right - 15, y_right + ship_height * 0.65])

                pygame.mixer.Sound.play(shot_sound)

    screen.blit(SPACE_BACKGROUND, (0, 0))

    screen.blit(left_space_ship, (x_left, y_left))

    screen.blit(right_space_ship, (x_right, y_right))

    screen.blit(health_text, (0, 0))
    screen.blit(health_text, (ScreenWidth - 100, 0))

    left_score_text = font.render(str(score_left), True, WHITE, False)
    right_score_text = font.render(str(score_right), True, WHITE, False)

    screen.blit(left_score_text, (150, 0))
    screen.blit(right_score_text, (ScreenWidth - 150, 0))

    draw(left_bullets, RED)

    draw(right_bullets, GREEN)

    if not stop:
        keys_pressed = pygame.key.get_pressed()

        left_key_list = [keys_pressed[pygame.K_w], keys_pressed[pygame.K_a],
                         keys_pressed[pygame.K_s], keys_pressed[pygame.K_d]]

        right_key_list = [keys_pressed[pygame.K_UP], keys_pressed[pygame.K_LEFT],
                          keys_pressed[pygame.K_DOWN], keys_pressed[pygame.K_RIGHT]]

        x_left, y_left = ship_control(left_key_list, x_left, y_left)
        x_right, y_right = ship_control(right_key_list, x_right, y_right)

        left_bullets = change_bullet_pos(left_bullets, left_bullet_velocity)
        right_bullets = change_bullet_pos(right_bullets, right_bullet_velocity)

        left_remove, right_remove = remove_bullets(left_bullets, right_bullets, width_bullet, height_bullet)

        left_bullets, score_right = changing_bullet_list(left_bullets, left_remove, x_right, y_right, score_right)

        right_bullets, score_left = changing_bullet_list(right_bullets, right_remove, x_left, y_left, score_left)

    if score_left == 0 or score_right == 0:
        stop = True

    pygame.display.update()
    clock.tick(FPS)

# hi Liron
# amongos
