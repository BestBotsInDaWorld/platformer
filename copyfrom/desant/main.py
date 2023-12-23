import pygame
import os
import sys
import random

size = width, height = 800, 600
pygame.init()
pygame.display.set_caption(f'Balls, fps:{60}')
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)  # по директории дата
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Mountain(pygame.sprite.Sprite):
    image = load_image("mountains.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Mountain.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем горы внизу
        self.rect.bottom = height


class Landing(pygame.sprite.Sprite):
    image = load_image("pt.png")

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Landing.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        # если ещё в небе
        if not pygame.sprite.collide_mask(self, mountain):  # mountain в игровом цикле
            self.rect = self.rect.move(0, 1)


if __name__ == '__main__':
    play = False
    running = True
    fps = 60
    clock = pygame.time.Clock()
    image = pygame.Surface([100, 100])
    image.fill(pygame.Color("black"))

    while running:
        mountain = Mountain()
        screen.fill('white')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                Landing(event.pos)
            if event.type == pygame.MOUSEWHEEL:
                fps = min(120, max(1, fps + int(event.precise_y)))
                pygame.display.set_caption(f'Balls, fps:{fps}')
        all_sprites.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
        all_sprites.update()

    pygame.quit()
