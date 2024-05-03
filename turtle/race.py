import turtle
import random
import pygame

pygame.font.init()

ScreenWidth, ScreenHeight = 650, 650
screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))
pygame.display.set_caption("scores")

FPS = 5
clock = pygame.time.Clock()

wn = turtle.Screen()

jan = turtle.Turtle()
fev = turtle.Turtle()
may = turtle.Turtle()
april = turtle.Turtle()
mar = turtle.Turtle()
june = turtle.Turtle()
jul = turtle.Turtle()
aug = turtle.Turtle()

turtle_list = [jan, fev, may, april, mar, june, jul, aug]
colors = ["RED", "pink", "green", "orange", "blue", "black", "yellow", "purple"]
colors_to_print = [(255, 0, 0), (255, 182, 193), (0, 255, 0), (255, 165, 0), (0, 0, 255), (255, 255, 255), (255, 255, 0), (255, 0, 255)]

scores = [0, 0, 0, 0, 0, 0, 0, 0]


def get_to_pos():
    for turtle_pos in range(len(turtle_list)):
        turtle = turtle_list[turtle_pos]
        turtle.shape("turtle")
        turtle.color(colors[turtle_pos])
        turtle.pd()

        turtle.clear()
        turtle.setheading(90)
        turtle.pu()
        x = -175 + turtle_pos * 50
        y = -200
        turtle.goto(x, y)


def draw_scores():
    for turtle_pos in range(len(turtle_list)):
        turtle_score_label = main_font.render(str(scores[turtle_pos]), 1, colors_to_print[turtle_pos])

        screen.blit(turtle_score_label, (50 + turtle_pos * 75, ScreenHeight - 200))
        pygame.draw.rect(screen, colors_to_print[turtle_pos], (50 + turtle_pos * 75, ScreenHeight - 100, 10, 10))

        pygame.display.update()


main_font = pygame.font.SysFont("comicsans", 30)

round_count = 1
count_destination = -1

main_font_2 = pygame.font.SysFont("comicsans", 40)

game_label = main_font_2.render("Turtle game by Liron", 1, (255, 255, 255))
round_destination_label = main_font_2.render(("round destination : " + str(count_destination)), 1, (255, 255, 255))

run = True
while run:
    clock.tick(FPS)

    if round_count == count_destination:
        run = False

    screen.fill((0, 0, 0))
    draw_scores()

    screen.blit(game_label, (ScreenWidth // 2 - game_label.get_width() // 2, 100))

    round_label = main_font_2.render("round number : " + str(round_count), 1, (255, 255, 255))
    screen.blit(round_label, (ScreenWidth // 2 - round_label.get_width(), 225))

    screen.blit(round_destination_label, (ScreenWidth // 2 - round_label.get_width(), 300))

    pygame.display.update()

    get_to_pos()

    win = False
    while not win:
        for turtle_pos in range(len(turtle_list)):
            turtle = turtle_list[turtle_pos]
            turtle.pd()
            speed = random.randint(1, 15)
            turtle.color(colors[turtle_pos])
            turtle.fd(speed)

            if turtle.pos()[1] >= 200:
                win = True
                draw_scores()
                for turtle in turtle_list:
                    turtle.clear()
                    turtle.speed(10)
                    turtle.pu()
                    turtle.setpos(0, 0)
                    turtle.setheading(0)
                    turtle.speed(2)

                get_to_pos()
                round_count += 1
                scores[turtle_pos] += 1

turtle.mainloop()
