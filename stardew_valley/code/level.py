from player import *
from tiles import Tile, WaterTile, Tree


class Level:
    def __init__(self):

        # screen
        self.display_surface = pygame.display.get_surface()

        # all visible sprites
        self.visible_sprites = Camera()

        # creating level
        self.level_setup()

    def level_setup(self):
        self.layouts = {
            'water': {'layer': get_layer('map/world_water.csv'), 'graphics': import_folder('graphics/objects/water')},
            'ground': {'layer': get_layer('map/world_ground.csv'), 'graphics': import_graphics('graphics/tilesets/Grass.png')},
            'barrier': {'layer': get_layer('map/world_barrier.csv')},
            'trees': {'layer': get_layer('map/world_trees.csv'), 'graphics': import_folder('graphics/objects/trees')},
        }

        self.barrier_group = pygame.sprite.Group()
        self.soil_layer = SoilLayer(self.visible_sprites)

        for style, layout in self.layouts.items():
            for row_pos, row in enumerate(layout['layer']):
                for col_pos, col in enumerate(row):
                    if col != '-1':
                        x = TILESIZE * col_pos
                        y = TILESIZE * row_pos

                        if style == 'barrier':
                            Tile((x, y), LAYERS['ground'], [self.visible_sprites, self.barrier_group])
                        if style == 'water':
                            WaterTile((x, y), [self.visible_sprites, self.soil_layer.water_group], layout['graphics'])
                        if style == 'ground':
                            Tile((x, y), LAYERS['ground'], [self.visible_sprites, self.soil_layer.ground_group], layout['graphics'][int(col)])
                        if style == 'trees':
                            if col == '0':
                                tree_type = 'small'
                                images = layout['graphics'][1]
                            if col == '1':
                                tree_type = 'large'
                                images = layout['graphics'][0]

                            Tree((x, y), tree_type, [self.visible_sprites, self.soil_layer.tree_group], images)

        self.soil_layer.create_grid()

        self.player_group = pygame.sprite.GroupSingle()
        self.player = Player((1000, 1000), self.soil_layer,
                    [self.barrier_group, self.soil_layer.tree_group], [self.visible_sprites, self.player_group])

    def run(self):
        
        # draw visible sprites
        self.visible_sprites.custom_draw(self.player)

        # update 
        self.player_group.update(self.soil_layer.GRID)
        self.soil_layer.update(self.player)


class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.display = pygame.display.get_surface()

        self.offset = pygame.Vector2()

    def custom_draw(self, player):
        self.offset.x = Screen_Width / 2 - player.rect.centerx
        self.offset.y = Screen_Height / 2 - player.rect.centery

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.y):
                if sprite.z == layer:

                    # if sprite in screen
                    if player.sprite_in_screen(sprite, offset=50):
                        offset_pos = sprite.rect.topleft + self.offset
                        self.display.blit(sprite.image, offset_pos)
