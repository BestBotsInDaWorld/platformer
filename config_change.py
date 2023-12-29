from background import *
from settings import KEY_BINDINGS, screen, FPS, clock
from useful_funcs import terminate

menu_active = False
selected_button = None
start = False


def save_settings():
    with open("key_bindings.txt", "w") as f:
        f.write(f'{KEY_BINDINGS["KEY_UP"]}\n{KEY_BINDINGS["KEY_DOWN"]}\n'
                f'{KEY_BINDINGS["KEY_RIGHT"]}\n{KEY_BINDINGS["KEY_LEFT"]}')


def set_settings(*args):
    global selected_button, menu_active, start
    gen_background()
    font = pygame.font.Font(None, 30)

    key_up = pygame.sprite.Sprite()
    key_down = pygame.sprite.Sprite()
    key_left = pygame.sprite.Sprite()
    key_right = pygame.sprite.Sprite()
    to_lobby = pygame.sprite.Sprite()
    buttons = pygame.sprite.Group()

    key_up.image = load_image(rf"menu\buttons\arrow.png")
    key_up.image = pygame.transform.scale(key_up.image, (75, 75))
    key_up.image = pygame.transform.rotate(key_up.image, 270)
    key_up_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 200, 100, 100)
    key_up.rect = key_up_rect
    buttons.add(key_up)

    key_down.image = load_image(rf"menu\buttons\arrow.png")
    key_down.image = pygame.transform.scale(key_down.image, (75, 75))
    key_down.image = pygame.transform.rotate(key_down.image, 90)
    key_down_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 100, 100, 100)
    key_down.rect = key_down_rect
    buttons.add(key_down)

    key_right.image = load_image(rf"menu\buttons\arrow.png")
    key_right.image = pygame.transform.scale(key_right.image, (75, 75))
    key_right.image = pygame.transform.rotate(key_right.image, 180)
    key_right_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 100, 100)
    key_right.rect = key_right_rect
    buttons.add(key_right)

    key_left.image = load_image(rf"menu\buttons\arrow.png")
    key_left.image = pygame.transform.scale(key_left.image, (75, 75))
    key_left_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 100, 100)
    key_left.rect = key_left_rect
    buttons.add(key_left)

    to_lobby.image = load_image(rf"menu\buttons\previous.png")
    to_lobby.image = pygame.transform.scale(to_lobby.image, (75, 75))
    to_lobby_rect = pygame.Rect(WIDTH - 100, HEIGHT - 100, 100, 100)
    to_lobby.rect = to_lobby_rect
    buttons.add(to_lobby)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and menu_active and selected_button:
                key = pygame.key.name(event.key)
                if key == "down" or key == "up" or key == "left" or key == "right":
                    key = key.upper()
                if selected_button == 'KEY_UP':
                    KEY_BINDINGS['KEY_UP'] = f"K_{key}"
                elif selected_button == 'KEY_DOWN':
                    KEY_BINDINGS['KEY_DOWN'] = f"K_{key}"
                elif selected_button == 'KEY_LEFT':
                    KEY_BINDINGS['KEY_LEFT'] = f"K_{key}"
                elif selected_button == 'KEY_RIGHT':
                    KEY_BINDINGS['KEY_RIGHT'] = f"K_{key}"
                menu_active = False
                selected_button = None
                save_settings()

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

        for elem, val in KEY_BINDINGS.items():
            if str(val).isdigit():
                KEY_BINDINGS[elem] = f'K_{pygame.key.name(val)}'
            if (KEY_BINDINGS[elem][2:] == "up" or KEY_BINDINGS[elem][2:] == "down" or
                    KEY_BINDINGS[elem][2:] == "left" or KEY_BINDINGS[elem][2:] == "right"):
                KEY_BINDINGS[elem] = f"K_{KEY_BINDINGS[elem][2:].upper()}"

        string_rendered = font.render(KEY_BINDINGS["KEY_UP"], 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = HEIGHT // 2 - 175
        intro_rect.x = WIDTH // 2
        screen.blit(string_rendered, intro_rect)

        string_rendered = font.render(KEY_BINDINGS["KEY_DOWN"], 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = HEIGHT // 2 - 75
        intro_rect.x = WIDTH // 2
        screen.blit(string_rendered, intro_rect)

        string_rendered = font.render(KEY_BINDINGS["KEY_RIGHT"], 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = HEIGHT // 2 + 25
        intro_rect.x = WIDTH // 2
        screen.blit(string_rendered, intro_rect)

        string_rendered = font.render(KEY_BINDINGS["KEY_LEFT"], 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = HEIGHT // 2 + 125
        intro_rect.x = WIDTH // 2
        screen.blit(string_rendered, intro_rect)

        pygame.display.flip()
        clock.tick(FPS)