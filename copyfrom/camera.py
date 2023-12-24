import pygame
import os
import sys

SIZE = WIDTH, HEIGHT = 400, 400
FPS = 60
clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption(f'Balls, fps:{60}')
screen = pygame.display.set_mode(SIZE)
tiles_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player = None


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)  # по директории дата
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        terminate()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))  # фон с размерами окна
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))  # текст, ..., цвет текста
        intro_rect = string_rendered.get_rect()  # прямоугольник для строки
        text_coord += 10
        intro_rect.y = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    if not os.path.exists(filename) or filename[len(filename) - 3:] != "txt":
        print(f"Файл '{filename}' не найден")
        terminate()
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


tile_images = {
    'wall': load_image('box.png'),  # сразу пригрузить холст чтобы не загружать потом
    'empty': load_image('grass.png')
}

player_image = load_image('mario.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]  # строка с названием
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)  # получаем левый топ коорд холста и получаем передвинутый


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def update(self, key, *args):
        if key == pygame.K_DOWN:
            if self.pos_y + 1 < len(level) and level[self.pos_y + 1][self.pos_x] != '#':
                self.pos_y += 1
                self.rect = self.rect.move(0, tile_width)
        if key == pygame.K_UP:
            if self.pos_y - 1 >= 0 and level[self.pos_y - 1][self.pos_x] != '#':
                self.pos_y -= 1
                self.rect = self.rect.move(0, -tile_width)
        if key == pygame.K_LEFT:
            if self.pos_x - 1 >= 0 and level[self.pos_y][self.pos_x - 1] != '#':
                self.pos_x -= 1
                self.rect = self.rect.move(-tile_width, 0)
        if key == pygame.K_RIGHT:
            if self.pos_x + 1 < max(map(len, level)) and level[self.pos_y][self.pos_x + 1] != '#':
                self.pos_x += 1
                self.rect = self.rect.move(tile_width, 0)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        print(self.dx, self.dy)
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


if __name__ == '__main__':
    level = load_level('map.txt')
    start_screen()
    camera = Camera()
    player, level_x, level_y = generate_level(level)
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    while True:
        screen.fill('white')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEWHEEL:
                FPS = min(120, max(1, FPS + int(event.precise_y)))
                pygame.display.set_caption(f'Balls, fps:{FPS}')
            if event.type == pygame.KEYDOWN:
                all_sprites.update(event.key)
                camera.update(player)
                for sprite in all_sprites:
                    camera.apply(sprite)
        all_sprites.draw(screen)
        player_group.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()