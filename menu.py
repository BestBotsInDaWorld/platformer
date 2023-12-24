from useful_funcs import *
import sys
from new import Tile, start


pygame.init()

FPS = 60
WIDTH = 800
HEIGHT = 600
GRAVITY = 0.25
MAX_JUMP_HEIGHT = 80
RESISTANCE = 0.25
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # экран
clock = pygame.time.Clock()


all_sprites = pygame.sprite.Group()
hero_group = pygame.sprite.Group()
tile_group = pygame.sprite.Group()
background = pygame.sprite.Group()
tiles = []


def animate_background(pixels):
    for pixel in pixels:
        pixel.move(1, 1)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    buttons = pygame.sprite.Group()
    font = pygame.font.Font(None, 30)

    play = pygame.sprite.Sprite()
    settings = pygame.sprite.Sprite()
    quitButton = pygame.sprite.Sprite()

    play.image = load_image(rf"menu\buttons\play.png")
    play.image = pygame.transform.scale(play.image, (75, 75))
    rectPlay = pygame.Rect(WIDTH//2 - 200, HEIGHT // 2 - 150, 100, 100)
    play.rect = rectPlay
    buttons.add(play)

    settings.image = load_image(rf"menu\buttons\settings.png")
    settings.image = pygame.transform.scale(settings.image, (75, 75))
    rectSetting = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 50, 100, 100)
    settings.rect = rectSetting
    buttons.add(settings)

    quitButton.image = load_image(rf"menu\buttons\close.png")
    quitButton.image = pygame.transform.scale(quitButton.image, (75, 75))

    rectQuit = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 + 50, 100, 100)
    quitButton.rect = rectQuit
    buttons.add(quitButton)

    colorsForBack = ["Blue", "Pink", "Purple"]
    currentColor = 0

    for i in range(0, 1600, 50):
        for j in range(0, 1600, 50):
            currentColor += 1
            if currentColor > 2:
                currentColor = 0
            tile = Tile(colorsForBack[currentColor], i, j)
            tiles.append(tile)

    while start:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rectPlay.collidepoint(event.pos):
                    print("go")
                    running = True
                    return
                elif rectQuit.collidepoint(event.pos):
                    terminate()
            elif event.type == pygame.QUIT:
                terminate()
        background.draw(screen)
        animate_background(tiles)
        buttons.draw(screen)

        string_rendered = font.render("play", 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = HEIGHT // 2 - 125
        intro_rect.x = WIDTH // 2 - 100
        screen.blit(string_rendered, intro_rect)

        string_rendered = font.render("settings", 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = HEIGHT // 2 - 25
        intro_rect.x = WIDTH // 2 - 100
        screen.blit(string_rendered, intro_rect)

        string_rendered = font.render("exit", 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = HEIGHT // 2 + 75
        intro_rect.x = WIDTH // 2 - 100
        screen.blit(string_rendered, intro_rect)

        pygame.display.flip()
        clock.tick(FPS)
