import pygame
import os
from csv import reader
from settings import TILESIZE

def get_layer(path):
    layer = []

    with open(path) as layer_layout:
        for row in reader(layer_layout, delimiter=','):
            layer.append(row)

    return layer

def import_folder(path):
    images = []
    animations = os.listdir(path)

    for animation in animations:
        full_path = path + '/' + animation
        image = pygame.image.load(full_path).convert_alpha()
        images.append(image)

    return images


def import_dictionary(path):
    dictionary = {}
    animations = os.listdir(path)

    for animation in animations:
        full_path = path + '/' + animation
        image = pygame.image.load(full_path).convert_alpha()

        dictionary[animation.split('.')[0]] = image

    return dictionary


def import_graphics(path):
    surf = pygame.image.load(path).convert_alpha()
    images = []

    x_num_tiles = surf.get_width() // TILESIZE
    y_num_tiles = surf.get_height() // TILESIZE

    for col in range(y_num_tiles):
        for row in range(x_num_tiles):
            image = surf.subsurface((row * TILESIZE, col * TILESIZE, TILESIZE, TILESIZE))
            images.append(image)

    return images
