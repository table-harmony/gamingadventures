import pygame

pygame.init()
pygame.mixer.get_init()

FPS = 60
clock = pygame.time.Clock()

# screen settings

ScreenWidth = 500
ScreenHeight = 500
screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))
pygame.display.set_caption("atari game .2 PONG")

# colors

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# players settings

width_player = ScreenWidth // 50
height_player = ScreenWidth // 10

x_player1 = ScreenWidth // 50
y_player1 = ScreenHeight // 2 - height_player // 2

x_player2 = ScreenWidth - x_player1 - width_player
y_player2 = y_player1

# ball settings

x_ball = ScreenWidth // 2
y_ball = ScreenHeight // 2
width_ball = 5
height_ball = width_ball

# velocities

player_velocity = 10

x_origin = 5
x_velocity_ball = -x_origin // 2

y_origin = 6
y_velocity_ball = 0

# scores

score_player1 = 0
score_player2 = score_player1


def draw(x, y, width, height):
    pygame.draw.polygon(screen, WHITE, points=[(x, y), (width + x, y),
                                               (width + x, y + height),
                                               (x, y + height)])


def draw_dotted_line():
    # (width_line) line settings
    width = 5
    space = 10
    height_line = 20

    i = 0
    for _ in range(ScreenWidth // height_line * (i + 1)):
        pygame.draw.polygon(screen, WHITE, points=[(ScreenWidth // 2 - 5,
                                                    height_line * i + space),
                                                   (ScreenWidth // 2 + width,
                                                    height_line * i + space),
                                                   (ScreenWidth // 2 + width,
                                                    height_line * (i + 1)),
                                                   (ScreenWidth // 2 - width,
                                                    height_line * (i + 1))])
        i += 1


def ball_bouncing(x, y, x_velocity, y_velocity, width_ball, height_ball):
    if y - height_ball < 0 or y + height_ball > ScreenHeight:
        y_velocity *= -1

    return x_velocity, y_velocity


def player1_movement(keys, y, velocity):
    if 0 <= y:
        if keys[pygame.K_w]:  # up
            y -= velocity
    if y + height_player <= ScreenHeight:
        if keys[pygame.K_s]:  # down
            y += velocity
    return y


def player2_movement(keys, y, velocity):
    if 0 <= y:
        if keys[pygame.K_UP]:  # up
            y -= velocity
    if y + height_player <= ScreenHeight:
        if keys[pygame.K_DOWN]:  # down
            y += velocity
    return y


def check_for_collisions(x_ball, y_ball, x_player, y_player,
                         width_ball, height_ball, width_player,
                         height_player, x_velocity, y_velocity, x_origin, y_origin):
    if x_ball <= x_player + width_player <= x_ball + width_ball or x_ball <= x_player <= x_ball + width_ball:
        if y_player <= y_ball <= y_player + height_player:
            x_velocity *= -1
            if y_ball <= y_player + 0.5 * height_player:
                y_velocity = -y_origin
            else:
                y_velocity = y_origin

            if abs(x_velocity) != abs(x_origin):
                x_velocity = x_origin
                y_velocity = y_origin

    return x_velocity, y_velocity


# text and sound settings

font = pygame.font.Font('freesansbold.ttf', 32)

text = font.render(str(score_player1), True, WHITE, False)
text1 = font.render(str(score_player2), True, WHITE, False)

textRect = text.get_rect()
text1rect = text1.get_rect()

textRect.center = (100, 50)
text1rect.center = (ScreenWidth - 100, 50)

run = True
stop = True
score_change = False
play_wall_bounce = False

# game loop
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

            if event.key == pygame.K_SPACE:
                stop = not stop

    keys_pressed = pygame.key.get_pressed()
    if not stop:
        y_player1 = player1_movement(keys_pressed, y_player1, player_velocity)
        y_player2 = player2_movement(keys_pressed, y_player2, player_velocity)

    # velocity and position change (ball)

    x_velocity_ball, y_velocity_ball = ball_bouncing(x_ball, y_ball, x_velocity_ball, y_velocity_ball,
                                                                       width_ball, height_ball)

    x_velocity_ball, y_velocity_ball = check_for_collisions(x_ball, y_ball, x_player1, y_player1,
                                                                              width_ball, height_ball, width_player,
                                                                              height_player, x_velocity_ball,
                                                                              y_velocity_ball, x_origin,
                                                                              y_origin)

    x_velocity_ball, y_velocity_ball = check_for_collisions(x_ball, y_ball, x_player2, y_player2,
                                                                              width_ball, height_ball, width_player,
                                                                              height_player, x_velocity_ball,
                                                                              y_velocity_ball, x_origin,
                                                                              y_origin)

    # ball movement
    if not stop:
        x_ball += x_velocity_ball
        y_ball += y_velocity_ball

    # draw

    screen.fill(BLACK)

    # draw ball
    draw(x_ball, y_ball, width_ball, height_ball)

    # draw player1
    draw(x_player1, y_player1, width_player, height_player)

    # draw player2
    draw(x_player2, y_player2, width_player, height_player)

    # draw dotted line
    draw_dotted_line()

    # score change
    if x_ball - width_ball <= 0:
        score_player2 += 1
        score_change = True

    if x_ball + width_ball >= ScreenWidth:
        score_player1 += 1
        score_change = True

    if score_change:
        # velocity reset
        x_origin *= -1
        x_velocity_ball = -x_origin // 2
        y_velocity_ball = 0

        # ball pos reset
        x_ball = ScreenWidth // 2
        y_ball = ScreenHeight // 2

        # players reset pos
        x_player1 = ScreenWidth // 50
        y_player1 = ScreenHeight // 2 - height_player // 2

        x_player2 = ScreenWidth - x_player1 - width_player
        y_player2 = y_player1

        score_change = False

    # displaying score
    text = font.render(str(score_player1), True, WHITE, False)
    text1 = font.render(str(score_player2), True, WHITE, False)

    screen.blit(text, textRect)
    screen.blit(text1, text1rect)

    # win
    if score_player1 == 10 or score_player2 == 10:
        run = False

    pygame.display.update()
    clock.tick(FPS)


# main

def main():
    pass


if __name__ == "__main__":
    main()
