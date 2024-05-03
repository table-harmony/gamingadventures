import pygame
import random

pygame.init()

# screen settings

ScreenWidth = 500
ScreenHeight = 600
screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))
pygame.display.set_caption("game .3 ROCK PAPER SCISSOR")

clock = pygame.time.Clock()
FPS = 60

# colors

BLACK = (0, 0, 0)
BACKGROUND = (0, 153, 153)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

colors = [RED, GREEN, BLUE]

choices = [1, 2, 3]
word_choices = ["ROCK", "PAPER", "SCISSOR"]

# block settings
x = ScreenWidth // 15
y = ScreenHeight // 3
width = 100
height = 50
space = 30


def block_pos():
    x_start_list = []
    for i in range(3):
        x_start = x * (i + 1) + width * i + space
        x_start_list.append(x_start)
    return x_start_list


def draw(x_list):
    for i in range(len(x_list)):
        x_start = x_list[i]
        points = [(x_start, y), (x_start + width, y)
            , (x_start + width, y + height), (x_start, y + height)]
        pygame.draw.polygon(screen, colors[i], points)


def computer_choice():
    comp_choise_pos = random.randint(0, 2)
    return comp_choise_pos


def my_choice_computer_choice(my_pos, comp_pos):
    if my_pos == comp_pos:
        return "TIE"
    if choices[my_pos - 1] == choices[comp_pos]:
        return my_pos
    else:
        return comp_pos


# תשנה מיקום + תעשה לכל הטקסטים
font = pygame.font.Font('freesansbold.ttf', 16)

text = font.render('ROCK PAPER SCISSOR GAME', True, BLACK, BACKGROUND)
credit_text = font.render('made by liron kaner', True, BLACK, BACKGROUND)
text1 = font.render('ROCK', True, BLACK, RED)
text2 = font.render('PAPER', True, BLACK, GREEN)
text3 = font.render('SCISSOR', True, BLACK, BLUE)

comp_decision = font.render(': comp decision', True, BLACK, BACKGROUND)
my_decision = font.render('your decision :', True, BLACK, BACKGROUND)

# round_winning_anouncment = font.render('', True, BLACK, BACKGROUND)
# winning_anouncment = font.render(" ", True, BLACK, BACKGROUND)

run = True
mouse_down = False
reset = False
win = False

comp_choice = False
player_choice = False
score_change = False

comp_score = 0
player_score = comp_score

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_down = True
    else:
        mouse_down = False

    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_ESCAPE]:
        run = False

    if keys_pressed[pygame.K_r] and not win:
        reset = False
        comp_choice = False
        player_choice = False
        score_change = False

    if keys_pressed[pygame.K_SPACE]:
        win = False
        player_score = 0
        comp_score = 0

    screen.fill(BACKGROUND)

    x_list = block_pos()

    # draw

    screen.blit(text, (ScreenWidth // 3.8, ScreenHeight // 6))
    screen.blit(credit_text, (ScreenWidth // 2.9, ScreenHeight // 5))
    screen.blit(my_decision, (x_list[0], y + height + 50))
    screen.blit(comp_decision, (x_list[-1], y + height + 50))

    player_score_visual = font.render(str(player_score), True, BLACK, BACKGROUND)
    comp_score_visual = font.render(str(comp_score), True, BLACK, BACKGROUND)

    screen.blit(player_score_visual, (50, y + height + width + 125))
    screen.blit(comp_score_visual, (ScreenWidth - 50, y + height + width + 125))

    draw(x_list)

    screen.blit(text1, (x_list[0] + 0.27 * width, y + 0.4 * height))
    screen.blit(text2, (x_list[1] + 0.23 * width, y + 0.4 * height))
    screen.blit(text3, (x_list[2] + 0.15 * width, y + 0.4 * height))

    x_mouse = pygame.mouse.get_pos()[0]
    y_mouse = pygame.mouse.get_pos()[1]

    while not reset and not comp_choice:
        pos_computer_choice = computer_choice()
        comp_choice = True
        score_change = False

    if player_choice:
        comp_decision1 = font.render(word_choices[pos_computer_choice], True, BLACK, BACKGROUND)
        screen.blit(comp_decision1, (x_list[-1], y + height + 100))

    if mouse_down and not reset and not player_choice:
        for i in range(len(x_list)):
            if x_list[i] <= x_mouse <= x_list[i] + width and y <= y_mouse <= y + height:
                pos_my_choice = i
                player_choice = True

    if player_choice:
        my_decision1 = font.render(word_choices[pos_my_choice], True, BLACK, BACKGROUND)
        screen.blit(my_decision1, (x_list[1] - 50, y + height + 100))
        winner = my_choice_computer_choice(pos_my_choice, pos_computer_choice)

        if not score_change:
            if winner == "TIE":
                round_winning_anouncment = font.render("the round is a TIE", True, BLACK, BACKGROUND)
            else:
                if choices[winner] == choices[pos_my_choice]:
                    round_winning_anouncment = font.render("you won the round", True, BLACK, BACKGROUND)
                    player_score += 1

                elif choices[winner] == choices[pos_computer_choice]:
                    round_winning_anouncment = font.render("comp won the round", True, BLACK, BACKGROUND)
                    comp_score += 1
            score_change = True

    if not player_choice and not win:
        round_winning_anouncment = font.render('', True, BLACK, BACKGROUND)

    if comp_score == 3:
        win = True
        round_winning_anouncment = font.render(" ", True, BLACK, BACKGROUND)
        winning_anouncment = font.render("comp won the game", True, BLACK, BACKGROUND)

    elif player_score == 3:
        win = True
        round_winning_anouncment = font.render(" ", True, BLACK, BACKGROUND)
        winning_anouncment = font.render("you won the game ", True, BLACK, BACKGROUND)

    else:
        winning_anouncment = font.render(" ", True, BLACK, BACKGROUND)

    screen.blit(round_winning_anouncment, (ScreenWidth // 2 - 50, y + height + 150))
    screen.blit(winning_anouncment, (ScreenWidth // 2.9, y + height + 200))

    pygame.display.update()
    clock.tick(FPS)

# main
def main():
    pass


if __name__ == "__main__":
    main()

