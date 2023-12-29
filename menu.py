from useful_funcs import terminate
from settings import clock, screen, FPS
from background import *


def start_screen():
    gen_background()
    buttons = pygame.sprite.Group()
    font = pygame.font.Font(None, 30)

    play_button = pygame.sprite.Sprite()
    settings_button = pygame.sprite.Sprite()
    quit_button = pygame.sprite.Sprite()

    play_button.image = load_image(rf"menu\buttons\play.png")
    play_button.image = pygame.transform.scale(play_button.image, (75, 75))
    play_rect = pygame.Rect(WIDTH//2 - 200, HEIGHT // 2 - 150, 100, 100)
    play_button.rect = play_rect
    buttons.add(play_button)

    settings_button.image = load_image(rf"menu\buttons\settings.png")
    settings_button.image = pygame.transform.scale(settings_button.image, (75, 75))
    settings_rect = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 50, 100, 100)
    settings_button.rect = settings_rect
    buttons.add(settings_button)

    quit_button.image = load_image(rf"menu\buttons\close.png")
    quit_button.image = pygame.transform.scale(quit_button.image, (75, 75))

    quit_rect = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 + 50, 100, 100)
    quit_button.rect = quit_rect
    buttons.add(quit_button)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    return
                elif quit_rect.collidepoint(event.pos):
                    terminate()
            elif event.type == pygame.QUIT:
                terminate()
        background.draw(screen)
        animate_background(tiles)
        buttons.draw(screen)

        string_rendered = font.render("Начать", 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = HEIGHT // 2 - 125
        intro_rect.x = WIDTH // 2 - 100
        screen.blit(string_rendered, intro_rect)

        string_rendered = font.render("Настройки", 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = HEIGHT // 2 - 25
        intro_rect.x = WIDTH // 2 - 100
        screen.blit(string_rendered, intro_rect)

        string_rendered = font.render("Выход", 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = HEIGHT // 2 + 75
        intro_rect.x = WIDTH // 2 - 100
        screen.blit(string_rendered, intro_rect)

        pygame.display.flip()
        clock.tick(FPS)
