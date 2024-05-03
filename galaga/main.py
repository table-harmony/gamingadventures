import pygame
import os
import random

# pygame.init()
pygame.font.init()
pygame.mixer.get_init()

ScreenWidth, ScreenHeight = 1200, 600
screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))
pygame.display.set_caption("game .5")

FPS = 60
clock = pygame.time.Clock()

# images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# player ship
player_width, player_height = 70, 70
YELLOW_SPACE_SHIP = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png")), (player_width, player_height))

# lasers

RED_LASERS = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASERS = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASERS = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASERS = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

heart_width = 40
heart_height = 40
heart_list = []
HEART_img = pygame.transform.scale(pygame.image.load(os.path.join("assets", "1.png")), (heart_width, heart_height))

# background
BACKGROUND = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "background-black.png")), (ScreenWidth, ScreenHeight))

# colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Ship:
    COOLDOWN = 20

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown(obj)
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(ScreenHeight):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                if self.ship_img == RED_SPACE_SHIP:
                    obj.health -= 10
                if self.ship_img == GREEN_SPACE_SHIP:
                    obj.vel_drop = True
                    obj.health -= 5
                if self.ship_img == BLUE_SPACE_SHIP:
                    obj.switch_controls = True
                    obj.health -= 5
                self.lasers.remove(laser)

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    def cooldown(self, obj):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
            obj.vel = 10

        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - self.get_width() // 4, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not (0 < self.y < height)

    def collision(self, obj):
        return collide(obj, self)


class Player(Ship):
    def __init__(self, x, y, vel, switch_controls, vel_drop, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASERS
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.vel = vel
        self.switch_controls = switch_controls
        self.vel_drop = vel_drop

    def move_lasers(self, vel, objs):
        self.cooldown(self)
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(ScreenHeight) and laser in self.lasers:
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def ship_controls(self, controls):
        if controls[0] and player.y - player_velocity > 0:
            player.y -= player.vel

        if controls[1] and player.x - player_velocity > 0:
            player.x -= player.vel

        if controls[2] and player.y + player_velocity + player.get_height() + 20 < ScreenHeight:
            player.y += player.vel

        if controls[3] and player.x + player.get_width() + player_velocity < ScreenWidth:
            player.x += player.vel

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, RED,
                         (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, GREEN, (
            self.x, self.y + self.ship_img.get_height() + 10,
            self.ship_img.get_width() * (self.health / self.max_health),
            10))


class Enemy(Ship):
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.color = color
        self.ship_img, self.laser_img = COLOR_MAP[self.color]
        self.vel_x, self.vel_y, (self.x, self.y) = pos_speed[self.color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel_x, vel_y):
        self.x += vel_x
        self.y += vel_y

    # def shoot(self):
    #     if self.cool_down_counter == 0:
    #         laser = Laser(self.x - self.get_width() // 4, self.y, self.laser_img)
    #         self.lasers.append(laser)
    #         self.cool_down_counter = 1


# fonts
main_menu_font_1 = pygame.font.SysFont("comicsans", 70)
main_menu_font_2 = pygame.font.SysFont("comicsans", 50)

main_font = pygame.font.SysFont("comicsans", 30)
lost_font = pygame.font.SysFont("comicsans", 50)


def draw_window():
    screen.blit(BACKGROUND, (0, 0))
    lives_label = main_font.render(("Lives: " + str(lives)), 1, WHITE)
    level_label = main_font.render(("Level: " + str(level)), 1, WHITE)
    remaining_enemies_label = main_font.render(("Enemies: " + str(len(enemies))), 1, WHITE)

    screen.blit(lives_label, (10, 10))
    screen.blit(level_label, (ScreenWidth - level_label.get_width() - 10, 10))
    screen.blit(remaining_enemies_label, (10, lives_label.get_height() + 10))
    # screen.blit(HEART_img, (100, 100))

    for enemy in enemies:
        enemy.draw(screen)

    player.draw(screen)

    if lost:
        lost_label = lost_font.render("YOU LOST :)", 1, WHITE)
        screen.blit(lost_label, (ScreenWidth // 2 - lost_label.get_width() // 2
                                 , ScreenHeight // 2))
    pygame.display.update()


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (int(offset_x), int(offset_y))) is not None


level = 0
lives = 5

time_control = 0
player_velocity = 8
switch_controls = False
vel_drop = False
player = Player(ScreenWidth // 2, ScreenHeight // 2, player_velocity, switch_controls, vel_drop)

enemies = []
wave_length = 0

red_vel_y = 2

blue_vel_y = 1


laser_vel = 4

COLOR_MAP = {
    "red": (RED_SPACE_SHIP, RED_LASERS),
    "green": (GREEN_SPACE_SHIP, GREEN_LASERS),
    "blue": (BLUE_SPACE_SHIP, BLUE_LASERS)
}
colors = ["red", "blue", "green"]


lost_count = 0
lost = False


def main_menu():
    title_font_1 = pygame.font.SysFont("comicsans", 50)
    title_label_1 = title_font_1.render("Press the mouse to begin...", 1, WHITE)

    title_font_2 = pygame.font.SysFont("comicsans", 20)
    title_label_2 = title_font_2.render("space invaders inspired game, made by liron kaner", 1, WHITE)

    run = False
    while not run:
        screen.blit(BACKGROUND, (0, 0))
        screen.blit(title_label_1, (ScreenWidth // 2 - title_label_1.get_width() / 2, ScreenHeight // 3))
        screen.blit(title_label_2, (ScreenWidth // 2 - title_label_2.get_width() / 2, ScreenHeight // 2))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = True
    return run


run = main_menu()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()

    clock.tick(FPS)

    draw_window()

    if lives <= 0 or player.health <= 0:
        lost = True
        lost_count += 1

    if lost:
        if lost_count >= FPS * 5:
            run = False
        else:
            continue

    if len(enemies) == 0:
        level += 1
        wave_length += 5
        for i in range(wave_length):
            color = random.choice(colors)
            if random.randint(0, 1) == 1:
                random_green = (random.randrange(-1500, -100), random.randrange(50, ScreenHeight // 2))
                green_vel_x = 5
            else:
                random_green = (
                    random.randrange(ScreenWidth + 100, ScreenWidth + 1500), random.randrange(50, ScreenHeight // 2))
                green_vel_x = -5

            pos_speed = {
                "red": (0, red_vel_y, (random.randrange(75, ScreenWidth - 75), random.randrange(-1500, -100))),
                "green": (green_vel_x, 0.25, random_green),
                "blue": (0, blue_vel_y, (random.randrange(75, ScreenWidth - 75), random.randrange(-1500, -100)))
            }

            enemy = Enemy(pos_speed[color][2][0], pos_speed[color][2][1], color)

            enemies.append(enemy)

    keys = pygame.key.get_pressed()

    if player.switch_controls and time_switch_controls <= FPS * 3:
        controls = [keys[pygame.K_w], keys[pygame.K_d], keys[pygame.K_s], keys[pygame.K_a]]
        time_switch_controls += 1

    else:
        controls = [keys[pygame.K_w], keys[pygame.K_a], keys[pygame.K_s], keys[pygame.K_d]]
        time_switch_controls = 0
        player.switch_controls = False

    if player.vel_drop and time_control <= FPS * 3:
        player.vel = 3
        time_control += 1

    else:
        time_control = 0
        player.vel_drop = False
        player.vel = 10

    player.ship_controls(controls)

    if keys[pygame.K_p]:
        player.shoot()

    for enemy in enemies:
        if enemy.color == "green":
            if enemy.vel_x > 0:
                if enemy.x + enemy.get_width() >= ScreenWidth + 300:
                    enemy.vel_x = -5
                    enemy.y += 10
            else:
                if enemy.x <= -300:
                    enemy.vel_x = 5

        enemy.move(enemy.vel_x, enemy.vel_y)
        enemy.move_lasers(laser_vel, player)

        if random.randrange(0, 4 * FPS) == 1:
            enemy.shoot()

        if collide(enemy, player):
            player.health -= 10
            enemies.remove(enemy)

        elif enemy.y + enemy.get_height() > ScreenHeight:
            enemies.remove(enemy)
            lives -= 1

    player.move_lasers(-laser_vel, enemies)

