import  sys
from useful_funcs import *

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
            new_x = self.rect.x - WIDTH
            new_y = self.rect.y - HEIGHT
            self.rect.x = new_x
            self.rect.y = new_y
        else:
            self.rect.x += 1
            self.rect.y += 1


class Hero(pygame.sprite.Sprite):
    def __init__(self, character, x, y):
        super().__init__(hero_group, all_sprites)

        path = rf"Main Characters\{character}\\"

        self.frames_forward = {"Run": self.cut_sheet(load_image(path + "Run.png"), 12, 1),
                               "Fall": self.cut_sheet(load_image(path + "Fall.png"), 1, 1),
                               "Hit": self.cut_sheet(load_image(path + "Hit.png"), 7, 1),
                               "Idle": self.cut_sheet(load_image(path + "Idle.png"), 11, 1),
                               "Jump": self.cut_sheet(load_image(path + "Jump.png"), 1, 1),
                               "Double Jump": self.cut_sheet(load_image(path + "Double Jump.png"), 6, 1)}
        self.frames_backwards = {key: [pygame.transform.flip(self.frames_forward[key][i], True, False)
                                       for i in range(len(self.frames_forward[key]))]
                                 for key in self.frames_forward.keys()}

        self.action = "Idle"

        self.direction = 'right'
        self.dx = 0

        self.dy = 0
        self.jump_number = 0
        self.jump_increase = 0
        self.cur_jump_height = 0

        self.cur_frame = 0
        self.image = self.frames_forward["Run"][self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        cycle = []
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                frame = sheet.subsurface(pygame.Rect(frame_location, self.rect.size))
                frame.set_colorkey(frame.get_at((0, 0)))
                cycle.append(frame)
        return cycle

    def set_image(self, direction, action):
        if self.direction == 'right':
            self.image = self.frames_forward[action][self.cur_frame]
        else:
            self.image = self.frames_backwards[action][self.cur_frame]

    def update(self, *args):
        scancode: pygame.key.ScancodeWrapper = args[0]

        has_resistance = 1
        has_gravity = 1

        if scancode[pygame.K_DOWN]:
            self.dy += 0.1

        if scancode[pygame.K_UP]:
            self.jump_number = max(1, self.jump_number)
            if self.cur_jump_height != MAX_JUMP_HEIGHT and not (not self.jump_increase and self.cur_jump_height > 0):
                self.jump_increase = True
                self.dy = -5
                self.cur_jump_height = min(float(MAX_JUMP_HEIGHT), self.cur_jump_height - self.dy)
                has_gravity = False
            elif not self.jump_increase:
                if self.jump_number == 1:
                    self.jump_number += 1
                    self.cur_jump_height = 0
        else:
            self.jump_increase = False
        if scancode[pygame.K_RIGHT]:
            self.direction = 'right'
            if not self.jump_number:
                self.dx = min(5.0, self.dx + 0.1)
            else:
                self.dx = min(5.0, max(1.0, self.dx + 0.1))
            if self.dx >= 0:
                has_resistance = 0

        if scancode[pygame.K_LEFT]:
            self.direction = 'left'
            if not self.jump_number:
                self.dx = max(-5.0, self.dx - 0.1)
            else:
                self.dx = max(-5.0, min(-1.0, self.dx - 0.1))
            if self.dx <= 0:
                has_resistance = 0

        if has_resistance and self.dy == 0:
            if self.dx < 0:
                self.dx = min(0.0, self.dx + RESISTANCE)
            else:
                self.dx = max(0.0, self.dx - RESISTANCE)

        if has_gravity:
            self.dy = min(5.0, self.dy + GRAVITY)

        if self.rect.top == HEIGHT - self.rect.height:  # заменить на коллизию снизу
            self.dy = min(self.dy, 0)
            self.cur_jump_height = 0
            self.jump_number = 0

        if self.dy < 0:
            if self.jump_number == 1:
                self.action = "Jump"
            else:
                self.action = "Double Jump"
        elif self.dy > 0:
            self.action = "Fall"
        elif self.dx != 0:
            self.action = "Run"
        else:
            self.action = "Idle"

        self.cur_frame = (self.cur_frame + 1) % len(self.frames_forward[self.action])
        self.set_image(self.direction, self.action)
        self.rect = self.rect.move(self.dx, self.dy)
        self.rect.top = min(HEIGHT - self.rect.height, self.rect.top)


dragon = Hero("Mask Dude", 50, 50)


running = False
start = True


def animate_background(pixels):
    for pixel in pixels:
        pixel.move(1, 1)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    global running, start

    buttons = pygame.sprite.Group()
    tile_group = pygame.sprite.Group()
    string_group = pygame.sprite.Group()
    intro_text = ["Play", "",
                  "Settings",
                  "Exit"]
    font = pygame.font.Font(None, 30)
    text_coord = 50

    play = pygame.sprite.Sprite()
    settings = pygame.sprite.Sprite()
    quitButton = pygame.sprite.Sprite()

    play.image = load_image(rf"menu\buttons\play.png")
    play.image = pygame.transform.scale(play.image, (75, 75))
    rectPlay = pygame.Rect(WIDTH//2 - 200, HEIGHT // 2 - 150, 100, 100)
    coordPlay = (WIDTH//2 - 50, HEIGHT // 2 - 150, 100, 100)
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


if start:
    start_screen()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(pygame.Color("orange"))
    hero_group.update(pygame.key.get_pressed())
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
