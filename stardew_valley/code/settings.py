from pygame import Vector2

Screen_Width, Screen_Height = 1200, 600

FPS = 60
TILESIZE = 64

LAYERS = {
    'ground': 0,
    'soil': 1,
    'items': 2,
    'water': 3,
    'player': 4,
    'trees': 5

}


APPLE_POS = {
    'large': [Vector2(10, 20), Vector2(30, 40), Vector2(50, 30), Vector2(45, 50), Vector2(15, 60)],
    'small': [Vector2(10, 20), Vector2(30, 40), Vector2(50, 30), Vector2(45, 50), Vector2(15, 60)]

}

SPRINKLERS = {
    'small': lambda x, y: [(x, y - TILESIZE), (x + TILESIZE, y), (x, y + TILESIZE), (x - TILESIZE, y)],
    'large': lambda x, y: [(x - TILESIZE, y - TILESIZE), (x, y - TILESIZE), (x + TILESIZE, y - TILESIZE), (x - TILESIZE, y),
                           (x + TILESIZE, y), (x - TILESIZE, y + TILESIZE), (x, y + TILESIZE), (x + TILESIZE, y + TILESIZE)]
}

