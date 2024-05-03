import pygame
import random

pygame.init()
pygame.mixer.get_init()

# screen settings

ScreenWidth = 500
ScreenHeight = 600
screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))
pygame.display.set_caption("atari game .1 BREAKOUT")

# colors

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

FPS = 60
clock = pygame.time.Clock()

# block + plack settings

width_block = ScreenWidth // 10
height_block = ScreenWidth // 25
x_plack = ScreenWidth // 2 - width_block // 2
y_plack = 12 * ScreenHeight // 16

# ball settings

x_ball = x_plack + width_block / 2
y_ball = y_plack - 20
width_ball = 5
height_ball = width_ball

# velocities

x_velocity_ball = random.uniform(2, 6)
y_velocity_ball = random.uniform(x_velocity_ball, x_velocity_ball + 1)


# the board of blocks summoning = line 66
def blocks(columns_num, colors_num, num_of_one_color):
    board = []
    rows_num = colors_num * num_of_one_color
    for _ in range(rows_num):
        board.append([])
    for col in range(columns_num):
        for color in range(colors_num):
            for i in range(num_of_one_color):
                board[color * num_of_one_color + i].append(color + 1)
    board = board[::-1]
    return board


# values for blocks, draw_blocks
colors = [WHITE, YELLOW, BLUE, GREEN, RED, BLACK]
num = 15
colors_num = len(colors) - 1
num_of_one_color = num // colors_num
space = 4.8
board = blocks(num, colors_num, num_of_one_color)


# drawing the blocks summoning = line 159
def draw_blocks(num, board, colors, space):
    width_blocks = ScreenWidth // 10
    height_blocks = 20
    for col in range(len(board)):
        for row in range(num):
            color = colors[board[col][row]]
            x_blocks = row * width_blocks
            y_blocks = col * height_blocks
            pygame.draw.polygon(screen, color, points=[(x_blocks + space,
                                                        y_blocks + space),
                                                       (x_blocks + width_blocks,
                                                        y_blocks + space),
                                                       (x_blocks + width_blocks,
                                                        y_blocks + height_blocks),
                                                       (x_blocks + space,
                                                        y_blocks + height_blocks)])


# checking for collisions function summoning = line 177
def check_for_collisions(top_block, left_block, width_block, height_block,
                         top_ball, left_ball, width_ball, height_ball,
                         x_velocity_ball, y_velocity_ball, stop):
    if top_block <= top_ball <= top_block + width_block:
        if left_ball <= left_block <= left_ball + height_ball:
            # collisions = True
            if y_velocity_ball > 0:
                y_velocity_ball *= -1

        if left_ball <= left_block + height_block <= left_ball + height_ball:
            # collisions = True
            if y_velocity_ball < 0:
                y_velocity_ball *= -1

    if left_block <= left_ball <= left_block + height_block:
        if top_ball <= top_block <= top_ball + width_ball:
            # collisions = True
            if x_velocity_ball > 0:
                x_velocity_ball *= -1

        if top_ball <= top_block + width_block <= top_ball + width_ball:
            # collisions = True
            if x_velocity_ball < 0:
                x_velocity_ball *= -1
    return x_velocity_ball, y_velocity_ball


# images sounds
heart = pygame.image.load("assets/heart.png").convert()
theme_music = pygame.mixer.Sound("assets/theme.wav")


original_life = 5
life = original_life
play_main = False
run = True
stop = True

while run:
    # game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:

            # escaping game

            if event.key == pygame.K_ESCAPE:
                run = False

            # stopping game

            if event.key == pygame.K_SPACE:
                play_main = not play_main
                stop = not stop

        # main block changing position
        if event.type == pygame.MOUSEMOTION and not stop:
            x_plack = pygame.mouse.get_pos()[0] - width_block / 2
    # draw

    screen.fill(WHITE)

    # draw blocks

    draw_blocks(num, board, colors, space)
    # draw hearts

    for i in range(life):
        heart.set_colorkey((0, 0, 0))
        screen.blit(heart, (50 + i * 50, 14 * ScreenHeight // 16))

    # draw ball

    pygame.draw.polygon(screen, BLACK, points=[(x_ball, y_ball), (width_ball + x_ball, y_ball),
                                               (width_ball + x_ball, y_ball + height_ball),
                                               (x_ball, y_ball + height_ball)])
    # draw main block

    pygame.draw.polygon(screen, BLACK, points=[(x_plack, y_plack), (width_block + x_plack, y_plack),
                                               (width_block + x_plack, y_plack + height_block),
                                               (x_plack, y_plack + height_block)])

    # checking collisions between ball and plack by function "check for collisions"
    # main block
    x_velocity_ball, y_velocity_ball = check_for_collisions(x_plack, y_plack,
                                                            width_block, height_block,
                                                            x_ball, y_ball, width_ball, height_ball,
                                                            x_velocity_ball, y_velocity_ball, stop)
    # all blocks

    for row_num in range(len(board)):
        row = board[row_num]
        for col_num in range(len(row)):
            col = row[col_num]
            x_block = row_num * width_block + space
            y_block = col_num * height_block + space
            x_old_velocity_ball = x_velocity_ball
            y_old_velocity_ball = y_velocity_ball
            if board[col_num][row_num] > 0:
                x_velocity_ball, y_velocity_ball = check_for_collisions(x_block, y_block,
                                                                        width_block, height_block,
                                                                        x_ball, y_ball, width_ball, height_ball,
                                                                        x_velocity_ball, y_velocity_ball, stop)
            if x_old_velocity_ball != x_velocity_ball or y_old_velocity_ball != y_velocity_ball:
                board[col_num][row_num] -= 1

    # changing ball location

    if not stop:
        x_ball += x_velocity_ball
        y_ball += y_velocity_ball

    # wall bouncing

    if x_ball - width_ball < 0 or x_ball + width_ball > ScreenWidth:
        x_velocity_ball *= -1

    if y_ball - height_ball < 0:
        y_velocity_ball *= -1

    # resetting positions

    if y_ball - height_ball > ScreenHeight:
        play_main = False
        play_losing = True
        life -= 1
        stop = not stop
        x_plack = ScreenWidth // 2 - width_block // 2
        x_ball = x_plack + width_block // 2
        y_ball = y_plack - 20
        x_velocity_ball = random.uniform(2, 4)
        y_velocity_ball = random.uniform(x_velocity_ball, x_velocity_ball + 1)

    # resetting life

    if life == 0 and not stop:
        life = original_life
        board = blocks(num, colors_num, num_of_one_color)

    # sound control if you want that it will play lines 234, 235 needs to be notes

    if play_main:
        pygame.mixer.unpause()
        pygame.mixer.Sound.play(theme_music)
    else:
        pygame.mixer.pause()

    pygame.display.update()
    clock.tick(FPS)


# main
def main():
    pass


if __name__ == "__main__":
    main()
