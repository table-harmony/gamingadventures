from support import * 
from random import choice, random
from tiles import Tile, Tree
from timer import Timer
from settings import *


class Soil(Tile):
    def __init__(self, pos, groups, image_dict):
        super().__init__(pos, LAYERS['soil'], groups, image_dict['o'])

        self.image_dict = image_dict

    def close_tiles(self, grid):
        close_tiles = []

        x = self.rect.centerx // TILESIZE
        y = self.rect.centery // TILESIZE

        for tile_list in [grid[y - 1][x], grid[y][x + 1], grid[y + 1][x], grid[y][x - 1]]:
            soil_list = list(filter(lambda tile: type(tile) == Soil, tile_list))
            close_tiles.append(soil_list)
        
        return close_tiles

    def update_image(self, grid):
        t, r, b, l = self.close_tiles(grid)

        tile_type = 'o'

        # all sides
        if all((t, r, b, l)):
            tile_type = 'x'

        # horizontal tiles only
        if l and not any((t, r, b)):
            tile_type = 'r'
        if r and not any((t, l, b)):
            tile_type = 'l'
        if r and l and not any((t, b)):
            tile_type = 'lr'

        # vertical tiles only
        if t and not any((l, r, b)):
            tile_type = 'b'
        if b and not any((t, r, l)):
            tile_type = 't'
        if t and b and not any((r, l)):
            tile_type = 'tb'

        # corners
        if l and b and not any((t, r)):
            tile_type = 'tr'
        if r and b and not any((t, l)):
            tile_type = 'tl'
        if l and t and not any((b, r)):
            tile_type = 'br'
        if r and t and not any((b, l)):
            tile_type = 'bl'

        # T shapes
        if all((t, b, r)) and not l:
            tile_type = 'tbr'
        if all((t, b, l)) and not r:
            tile_type = 'tbl'
        if all((r, l, b)) and not t:
            tile_type = 'lrt'
        if all((r, l, t)) and not b:
            tile_type = 'lrb'

        self.image = self.image_dict[tile_type]


class WaterSoil(Tile):
    def __init__(self, pos, groups, images):
        super().__init__(pos, LAYERS['soil'], groups, choice(images))

        self.images = images


class Crop(Tile):
    def __init__(self, pos, type, groups, images):
        super().__init__(pos, LAYERS['soil'], groups, images[0])

        self.images = images

        self.stage = 0
        
        self.timer = Timer(20 * round(random(), 2))
        self.timer.active = True

        self.type = type
        self.grown = False 

    def taken(self, sprite):
        sprite.crops[self.type] += 2
        self.kill()

    def update(self, player):
        if player.sprite_in_screen(self, 50):
            self.timer.update()

            if not self.timer.active and not self.grown:
                self.stage += 1
                
                # if stage is not the final stage
                if self.stage < len(self.images) - 1:
                    self.timer.max_time += round(random(), 2)  # recreate max time
                    self.timer.active = True

                else:  # self is in last stage
                    self.grown = True

                # update image, rect, hitbox according to stage
                self.image = self.images[self.stage]
                self.rect = self.image.get_rect(center=self.rect.center)
                self.hitbox = self.rect.inflate(0, -10)


class Sprinkler(Tile):
    def __init__(self, pos, groups, image):
        super().__init__(pos, LAYERS['items'], groups, image)

        self.overall_timer = Timer(3)
        self.overall_timer.active = True

        self.type = choice(['small', 'large'])
        self.close_tiles = self.close_tiles()

    def close_tiles(self):
        return SPRINKLERS[self.type](self.rect.centerx, self.rect.centery)

    def update(self, soil_layer):
        self.overall_timer.update()

        if not self.overall_timer.active:

            for close_tile in self.close_tiles:
                soil_layer.create_water_soil(close_tile)

            self.overall_timer.active = True


class Plow(Tile):
    def __init__(self, pos, groups, image):
        super().__init__(pos, LAYERS['items'], groups, image)

        # speed 
        self.speed = TILESIZE
        type = choice(['horizontal', 'vertical'])
        if type == 'horizontal':
            self.direction = pygame.Vector2(0, 1)
        if type == 'vertical':
            self.direction = pygame.Vector2(1, 0)

        # timer
        self.overall_timer = Timer(5)

        self.action_timer = Timer(2)
        self.action_timer.active = True

        self.crops = {
            'tomato': 1,
            'corn': 1
        }

    def plant_and_collect(self, soil_layer):
        x, y = self.rect.centerx // TILESIZE, self.rect.centery // TILESIZE
        
        water_list = list(filter(lambda sprite: type(sprite) == WaterSoil, soil_layer.GRID[y][x]))
        crop_list = list(filter(lambda sprite: type(sprite) == Crop, soil_layer.GRID[y][x]))

        if water_list:
            crop_type = choice(['tomato', 'corn'])
            if self.crops[crop_type] > 0: 
                soil_layer.create_crop(self.rect.center, crop_type)
            self.crops[crop_type] -= 1

        for crop in crop_list:
            if crop.grown: 
                soil_layer.GRID[y][x].remove(crop)
                crop.taken(self)
                for water in water_list:
                    soil_layer.GRID[y][x].remove(water)
                    water.kill()

    def move(self, grid):
        x, y = self.rect.centerx // TILESIZE, self.rect.centery // TILESIZE
        new_x, new_y = int((self.rect.centerx + self.direction.x * self.speed) // TILESIZE), int((self.rect.centery + self.direction.y * self.speed) // TILESIZE)

        if any(type(sprite) == Soil for sprite in grid[new_y][new_x] + grid[y][x]):
            self.rect.center = new_x * TILESIZE, new_y * TILESIZE
            self.hitbox.center = self.rect.center
            
            grid[y][x].remove(self)
            grid[new_y][new_x].append(self)

        else:
            self.overall_timer.active = True
            self.direction *= -1

    def update(self, soil_layer):
        self.overall_timer.update()

        if not self.overall_timer.active:
            self.action_timer.update()

            if not self.action_timer.active:
                self.move(soil_layer.GRID)
                self.plant_and_collect(soil_layer)

                self.action_timer.active = True


class SoilLayer(pygame.sprite.Group):
    def __init__(self, visible_group):
        super().__init__()

        # groups
        self.visible_group = visible_group
        self.ground_group = pygame.sprite.Group()

        self.tree_group = pygame.sprite.Group()
        self.water_group = pygame.sprite.Group()
        
        self.crop_group = pygame.sprite.Group()
        self.items_group = pygame.sprite.Group()

        self.create_images()

    def create_grid(self):
        groups = [self.ground_group, self.water_group, self.tree_group]   

        self.GRID = []
        for group in groups:
            for tile in group:

                # tile index
                x = tile.rect.centerx // TILESIZE
                y = tile.rect.centery // TILESIZE

                while y > len(self.GRID) - 1:
                    self.GRID.append([])

                while x > len(self.GRID[y]) - 1:
                    self.GRID[y].append([])

                self.GRID[y][x].append(tile)
        
    def create_images(self):

        # soil
        self.soil_dictionary = import_dictionary('graphics/objects/soil')
        self.water_soil_images = import_folder('graphics/objects/water_soil')

        # crops 
        self.crops = {
            'tomato': {'images': import_folder('graphics/objects/crops/tomato')}, 
            'corn': {'images': import_folder('graphics/objects/crops/corn')}
        } 
        
        # items 
        self.items = {
            'sprinkler': {'image': pygame.image.load('graphics/objects/Sprinkler.png').convert_alpha(), 'function': self.create_sprinkler},
            'plow': {'image': pygame.Surface((TILESIZE, TILESIZE)), 'function': self.create_plow}
        }

    def create_soil(self, target_pos):
        x, y = target_pos[0] // TILESIZE, target_pos[1] // TILESIZE

        if all(type(sprite) == Tile for sprite in self.GRID[y][x]):
            soil = Soil(target_pos, [self.visible_group, self.ground_group], self.soil_dictionary)  # create soil
            self.GRID[y][x].append(soil)

            soil.update_image(self.GRID)

            for tile_list in soil.close_tiles(self.GRID):
                for tile in tile_list:
                    tile.update_image(self.GRID)
    
    def create_water_soil(self, target_pos):
        x, y = target_pos[0] // TILESIZE, target_pos[1] // TILESIZE

        if any(type(sprite) == Soil for sprite in self.GRID[y][x]) and all(type(sprite) != WaterSoil for sprite in self.GRID[y][x]):
            water_soil = WaterSoil(target_pos, [self.ground_group, self.visible_group], self.water_soil_images) 
            self.GRID[y][x].append(water_soil)

    def create_crop(self, target_pos, crop_type):
        x, y = target_pos[0] // TILESIZE, target_pos[1] // TILESIZE

        if any(type(sprite) == WaterSoil for sprite in self.GRID[y][x]) and all(type(sprite) != Crop for sprite in self.GRID[y][x]):
            crop_images = self.crops[crop_type]['images']
            crop = Crop(target_pos, crop_type, [self.visible_group, self.crop_group], crop_images)
            self.GRID[y][x].append(crop)

    def create_sprinkler(self, target_pos):
        x, y = target_pos[0] // TILESIZE, target_pos[1] // TILESIZE

        if all(type(sprite) == Tile for sprite in self.GRID[y][x]):
            sprinkler_dict = self.items['sprinkler'] 
            sprinkler = Sprinkler(target_pos, [self.visible_group, self.items_group], sprinkler_dict['image'])

            self.GRID[y][x].append(sprinkler)

    def create_plow(self, target_pos):
        x, y = target_pos[0] // TILESIZE, target_pos[1] // TILESIZE

        if all(type(sprite) in [Tile, Soil] for sprite in self.GRID[y][x]):
            plow_dict = self.items['plow'] 
            plow = Plow(target_pos, [self.visible_group, self.items_group], plow_dict['image'])

            self.GRID[y][x].append(plow)

    def create_item(self, target_pos, item_type):
        self.items[item_type]['function'](target_pos)

    def update(self, player):
        self.items_group.update(self)
        self.tree_group.update()
        self.water_group.update(player)
        self.crop_group.update(player)
