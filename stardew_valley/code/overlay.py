from support import *
from timer import Timer
from settings import Screen_Height, Screen_Width


class Inventory(pygame.sprite.Group):
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.font = pygame.font.Font('LycheeSoda.ttf', 15) 

        self.create_images()
        self.create_slots()

    def create_images(self):

        # inventory background
        self.background = pygame.image.load(
            'graphics/overlay/slots/inventory_background.png').convert_alpha()
        self.background_pos = (
            Screen_Width / 2 - self.background.get_width() / 2, Screen_Height - 125)

        # slots
        self.slot_image = pygame.image.load(
            'graphics/overlay/slots/inventory_slot.png')
        self.selected_slot_image = pygame.image.load(
            'graphics/overlay/slots/selected_inventory_slot.png')

        # items
        self.overlay_item_images = {
            'hoe': pygame.image.load('graphics/overlay/tools/hoe.png').convert_alpha(),
            'axe': pygame.image.load('graphics/overlay/tools/axe.png').convert_alpha(),
            'water': pygame.image.load('graphics/overlay/tools/water.png').convert_alpha(),
            'tomato': pygame.image.load('graphics/overlay/crops/tomato.png').convert_alpha(),
            'corn': pygame.image.load('graphics/overlay/crops/corn.png').convert_alpha(),
            'sprinkler': pygame.image.load('graphics/overlay/machines/Sprinkler.png').convert_alpha(),
            'plow': pygame.Surface((35, 35))
        }

        # emotes
        self.emote_background_image = pygame.image.load('graphics/overlay/emotes/background.png')
        self.emotes = {

        }
        self.emote_types = ['normal', 'cool', 'angry', 'cheery']

        for emote_type in self.emote_types:
            full_path = f'graphics/overlay/emotes/{emote_type}'
            self.emotes[emote_type] = import_folder(full_path)

        self.frame_index = 0
        self.emote_animation = self.emotes['normal']

    def create_slots(self):
        self.slots = pygame.sprite.Group()

        slot_items = [
            ToolItem('hoe', 0.325, self.overlay_item_images['hoe']),
            ToolItem('water', 0.625, self.overlay_item_images['water']),
            ToolItem('axe', 0.325, self.overlay_item_images['axe']),
            CropItem('tomato', 0.25, self.overlay_item_images['tomato']),
            CropItem('corn', 0.25, self.overlay_item_images['corn']),
            MachineItem('sprinkler', 0.2, self.overlay_item_images['sprinkler']),
            MachineItem('plow', 0.2, self.overlay_item_images['plow'])

        ]

        width = self.slot_image.get_width()
        for slot_index, slot_item in enumerate(slot_items):  # create slots
            x = Screen_Width / 2 - 3.5 * width - 15 + slot_index * (width + 5)
            y = Screen_Height - 70

            Slot((x, y), slot_item, slot_index, self.slots, self.slot_image)

    def player_emotes(self):
        keys = pygame.key.get_pressed()

        # emote selection
        emote_keys = [pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v]
        for key in emote_keys:
            if keys[key]: 
                self.emote_animation = self.emotes[self.emote_types[emote_keys.index(key)]]

        # animate emote
        self.frame_index += 0.01  # change frame index
        if self.frame_index > len(self.emote_animation):
            self.frame_index = 0  # set the animation index to 0

        # image = animation in position frame index
        self.image = self.emote_animation[int(self.frame_index)]

        self.display_surface.blit(self.emote_background_image, (0, 0))
        self.display_surface.blit(self.image, (30, 21))

    def update(self, player):
        self.display_surface.blit(self.background, self.background_pos)

        self.player_emotes()
        self.slots.draw(self.display_surface)

        for slot in self.slots:
            if slot == player.selected_slot:
                slot.image = self.selected_slot_image
            else:
                slot.image = self.slot_image

            self.display_surface.blit(slot.item.image, slot.item.rect)


class Slot(pygame.sprite.Sprite):
    def __init__(self, pos, item, index, group, image):
        super().__init__(group)

        self.image = image
        self.rect = self.image.get_rect(center=pos)

        self.item = item
        self.item.rect.center = self.rect.center

        self.index = index

    def update(self):
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                self.rect.center = mouse_pos
                self.item.rect.center = self.rect.center


class SlotItem(pygame.sprite.Sprite):
    def __init__(self, name, image):

        self.image = image
        self.rect = self.image.get_rect()

        self.name = name
        
        self.amount = 1


class MachineItem(SlotItem):
    def __init__(self, name, action_time, image):
        super().__init__(name, image)

        self.timer = Timer(action_time)


class ToolItem(SlotItem):
    def __init__(self, name, action_time, image):
        super().__init__(name, image)

        self.timer = Timer(action_time)


class CropItem(SlotItem):
    def __init__(self, name, action_time, image):
        super().__init__(name, image)

        self.timer = Timer(action_time)
