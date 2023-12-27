import pygame
from useful_funcs import *
from menu import animate_background
from settings import *

tile_group = pygame.sprite.Group()
background = pygame.sprite.Group()
tiles = []


def animate_background(pixels):
    for pixel in pixels:
        pixel.move(1, 1)


menu_active = False
selected_button = None
colorsForBack = ["Pink", "Purple", "Blue", "Yellow", "Gray"]
currentColor = 0
start = False


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile, x, y):
        super().__init__(tile_group, background)
        path = rf"Background\{tile}.png"
        self.x = x
        self.y = y
        self.image = load_image(path)
        self.rect = pygame.Rect(0, 0, 50, 50)
        self.rect = self.rect.move(x, y)
        self.image = pygame.transform.scale(self.image, (50, 50))

    def move(self, dx, dy):
        if self.rect.x >= WIDTH or self.rect.y >= HEIGHT:
            self.rect.x = self.rect.x - WIDTH - 50
        else:
            self.rect.x += 1


for i in range(0, 1600, 50):
    for j in range(0, 1600, 50):
        currentColor += 1
        if currentColor > 4:
            currentColor = 0
        tile = Tile(colorsForBack[currentColor], i, j)
        tiles.append(tile)


def save_setting():
    with open("key_binds", "w") as f:
        print(KEY_BINDS)
        f.write(f'{KEY_BINDS["KEY_UP"]}\n{KEY_BINDS["KEY_DOWN"]}\n{KEY_BINDS["KEY_LEFT"]}\n{KEY_BINDS["KEY_RIGHT"]}')


def set_setting(*args):
    global selected_button, menu_active, start

    key_up = pygame.sprite.Sprite()
    key_down = pygame.sprite.Sprite()
    key_left = pygame.sprite.Sprite()
    key_right = pygame.sprite.Sprite()
    to_lobby = pygame.sprite.Sprite()
    buttons = pygame.sprite.Group()

    key_up.image = load_image(rf"menu\buttons\arrow.png")
    key_up.image = pygame.transform.scale(key_up.image, (75, 75))
    key_up.image = pygame.transform.rotate(key_up.image, 90)
    rectKey_up = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 200, 100, 100)
    key_up.rect = rectKey_up
    buttons.add(key_up)

    key_down.image = load_image(rf"menu\buttons\arrow.png")
    key_down.image = pygame.transform.scale(key_down.image, (75, 75))
    key_down.image = pygame.transform.rotate(key_down.image, 270)
    rectKey_down = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 100, 100, 100)
    key_down.rect = rectKey_down
    buttons.add(key_down)

    key_left.image = load_image(rf"menu\buttons\arrow.png")
    key_left.image = pygame.transform.scale(key_left.image, (75, 75))
    key_left.image = pygame.transform.rotate(key_left.image, 180)
    rectKey_left = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 100, 100)
    key_left.rect = rectKey_left
    buttons.add(key_left)

    key_right.image = load_image(rf"menu\buttons\arrow.png")
    key_right.image = pygame.transform.scale(key_right.image, (75, 75))
    rectKey_right = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 100, 100)
    key_right.rect = rectKey_right
    buttons.add(key_right)

    to_lobby.image = load_image(rf"menu\buttons\previous.png")
    to_lobby.image = pygame.transform.scale(to_lobby.image, (75, 75))
    rect_to_lobby = pygame.Rect(WIDTH - 100, HEIGHT - 100, 100, 100)
    to_lobby.rect = rect_to_lobby
    buttons.add(to_lobby)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and menu_active and selected_button:
                key = pygame.key.name(event.key)
                print(key)
                if key == "down" or key == "up" or key == "left" or key == "right":
                    key = key.upper()
                if selected_button == 'KEY_UP':
                    KEY_BINDS['KEY_UP'] = f"K_{key}"
                elif selected_button == 'KEY_DOWN':
                    KEY_BINDS['KEY_DOWN'] = f"K_{key}"
                elif selected_button == 'KEY_LEFT':
                    KEY_BINDS['KEY_LEFT'] = f"K_{key}"
                elif selected_button == 'KEY_RIGHT':
                    KEY_BINDS['KEY_RIGHT'] = f"K_{key}"
                menu_active = False
                selected_button = None
                save_setting()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not menu_active:
                    mouse_pos = pygame.mouse.get_pos()
                    if key_up.rect.collidepoint(mouse_pos):
                        menu_active = True
                        selected_button = 'KEY_UP'
                    elif key_down.rect.collidepoint(mouse_pos):
                        menu_active = True
                        selected_button = 'KEY_DOWN'
                    elif key_left.rect.collidepoint(mouse_pos):
                        menu_active = True
                        selected_button = 'KEY_LEFT'
                    elif key_right.rect.collidepoint(mouse_pos):
                        menu_active = True
                        selected_button = 'KEY_RIGHT'
                    elif to_lobby.rect.collidepoint(mouse_pos):
                        return
            elif event.type == pygame.QUIT:
                terminate()
        background.draw(screen)
        animate_background(tiles)
        buttons.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

