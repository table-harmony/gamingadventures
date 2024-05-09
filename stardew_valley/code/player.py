from overlay import *
from soil import * 
from tiles import Tree


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, soil_layer, collision_groups, groups):
        super().__init__(groups)

        # screen
        self.display_surface = pygame.display.get_surface()

        # status
        self.status_direction = 'down'
        self.status_type = 'idle'

        # animations
        self.create_animations()
        self.animation = self.get_animation()
        self.frame_index = 0

        # setup
        self.image = self.animation[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = pygame.Rect(
            self.rect.centerx, self.rect.centery, TILESIZE, TILESIZE - 10)

        self.z = LAYERS['player']
        self.collision_groups = collision_groups

        # movement
        self.direction = pygame.Vector2()
        self.speed = 4

        # soil_layer
        self.soil_layer = soil_layer

        # inventory
        self.inventory = Inventory()
        self.selected_slot = self.get_selected_slot(0)

        self.crops = {
            'tomato': 100,
            'corn': 100
        }

    def create_animations(self):
        self.animations_dict = {
            'up': {},
            'right': {},
            'down': {},
            'left': {}
        }

        # all animation types
        animation_types = ['idle', 'run', 'hoe', 'water', 'axe', 'placement']

        # create animations
        for direction in self.animations_dict:
            for type in animation_types:
                self.animations_dict[direction][type] = import_folder(
                    f'graphics/player/{direction}/{type}')

    def animate(self):
        self.frame_index += 0.1  # change frame index
        if self.frame_index > len(self.animation):
            self.frame_index = 0  # set the animation index to 0

        # image = animation in position frame index
        self.image = self.animation[int(self.frame_index)]

    def get_animation(self):
        # get animation according to status
        return self.animations_dict[self.status_direction][self.status_type]

    def get_selected_slot(self, index):
        # get selected slot according to index
        return list(filter(lambda slot: slot.index == index, self.inventory.slots))[0]

    def sprite_in_screen(self, sprite, offset=0):
        # if sprite in player's sight
        if self.rect.x - Screen_Width / 2 - offset < sprite.rect.centerx < self.rect.x + self.rect.width + Screen_Width / 2 + offset:
            if self.rect.y - Screen_Height / 2 - offset < sprite.rect.centery < self.rect.y + self.rect.height + Screen_Height / 2 + offset:
                return True
        return False

    def direction_management(self, keys):
        # direction
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        # changing slot
        inventory_keys = [pygame.K_1, pygame.K_2,
                          pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7]
        for key in inventory_keys:
            if keys[key]:
                self.selected_slot = self.get_selected_slot(
                    inventory_keys.index(key))

        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            for slot in self.inventory.slots:
                if slot.rect.collidepoint(mouse_pos):
                    self.selected_slot = slot

    def get_input(self):
        keys = pygame.key.get_pressed()  # keys pressed

        # if slot's item is a crop or an item
        if type(self.selected_slot.item) in [ToolItem, CropItem, MachineItem]:
            if keys[pygame.K_p] and not self.selected_slot.item.timer.active:
                self.selected_slot.item.timer.active = True

            if not self.selected_slot.item.timer.active:
                self.direction_management(keys)  # change direction
            else:
                self.direction = pygame.Vector2()  # set direction to 0, 0
        else:
            self.direction_management(keys)  # change direction

    def slot_management(self):
        slot = self.selected_slot

        # if slot's item is a crop or a tool
        if type(slot.item) in [CropItem, ToolItem, MachineItem]:
            slot.item.timer.activate()
            if slot.item.timer.current_time >= slot.item.timer.max_time:  # timer ended
                self.slot_item_use()  # use slot's item

            slot.item.timer.deactivate()

    def status_management(self):
        # direction status
        if self.direction != pygame.Vector2():  # player moving

            if self.direction.y > 0:
                self.status_direction = 'down'
            elif self.direction.y < 0:
                self.status_direction = 'up'

            if self.direction.x > 0:
                self.status_direction = 'right'
            elif self.direction.x < 0:
                self.status_direction = 'left'

            self.status_type = 'run'

        else:  # player not moving
            self.status_type = 'idle'

        # slot status
        if type(self.selected_slot.item) == ToolItem:
            if self.selected_slot.item.timer.active:
                self.status_type = self.selected_slot.item.name

        if type(self.selected_slot.item) in [MachineItem, CropItem]:
            if self.selected_slot.item.timer.active:
                self.status_type = 'placement'

        self.slot_management()

        # change animation according to status
        if self.animation != self.get_animation():
            self.animation = self.get_animation()
            self.frame_index = 0

    def slot_item_use(self):
        x, y = round(self.rect.centerx / TILESIZE) * TILESIZE, round(self.rect.centery / TILESIZE) * TILESIZE

        directions = ['up', 'right', 'down', 'left']
        close_tiles = [(x, y - TILESIZE), (x + TILESIZE, y),
                       (x, y + TILESIZE), (x - TILESIZE, y)]

        target_pos = close_tiles[directions.index(self.status_direction)]

        if type(self.selected_slot.item) == ToolItem:
            if self.selected_slot.item.name == 'hoe':
                self.soil_layer.create_soil(target_pos)
            if self.selected_slot.item.name == 'water':
                self.soil_layer.create_water_soil(target_pos)
            if self.selected_slot.item.name == 'axe':
                trees = list(filter(lambda sprite: type(sprite) == Tree, self.soil_layer.GRID[target_pos[1] // TILESIZE][target_pos[0] // TILESIZE]))

                for tree in trees: 
                    tree.damage()
        if type(self.selected_slot.item) == MachineItem:
            self.soil_layer.create_item(target_pos, self.selected_slot.item.name)
        if type(self.selected_slot.item) == CropItem:
            if self.crops[self.selected_slot.item.name] > 0:
                self.soil_layer.create_crop(target_pos, self.selected_slot.item.name)
            self.crops[self.selected_slot.item.name] -= 1

    def collisions(self, collision_type):
        for collision_group in self.collision_groups:
            for sprite in collision_group.sprites():
                if self.hitbox.colliderect(sprite.hitbox):

                    if collision_type == 'vertical':
                        if self.direction.x > 0:
                            self.hitbox.right = sprite.hitbox.left
                        else:
                            self.hitbox.left = sprite.hitbox.right

                    if collision_type == 'horizontal':
                        if self.direction.y > 0:
                            self.hitbox.bottom = sprite.hitbox.top
                        else:
                            self.hitbox.top = sprite.hitbox.bottom

    def seed_collision(self, grid):
        x, y = self.rect.centerx // TILESIZE, self.rect.centery // TILESIZE

        crop_tile = list(filter(lambda tile: type(tile) == Crop, grid[y][x]))

        if list(filter(lambda crop: crop.grown, crop_tile)) :
            for tile in grid[y][x]:
                if type(tile) == Crop:
                    grid[y][x].remove(tile)
                    tile.taken(self)
                if type(tile) == WaterSoil:
                    grid[y][x].remove(tile) 

    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.centerx += round(self.direction.x * self.speed)
        self.collisions('vertical')
        self.rect.centerx = self.hitbox.centerx

        self.hitbox.centery += round(self.direction.y * self.speed)
        self.collisions('horizontal')
        self.rect.centery = self.hitbox.centery

    def update(self, grid):
        self.get_input()

        self.status_management()

        self.animate()

        self.seed_collision(grid)
        self.move()

        self.inventory.update(self)
