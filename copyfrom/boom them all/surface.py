import pygame
import os
import sys
import random

size = width, height = 800, 600
pygame.init()
pygame.display.set_caption(f'Balls, fps:{60}')
screen = pygame.display.set_mode(size)
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


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


class Bomb(pygame.sprite.Sprite):
    image = load_image("bomb.png")
    image_boom = load_image("boom.png")

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__(*group)
        self.image = Bomb.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - self.rect.width)
        self.rect.y = random.randrange(height - self.rect.height)
        self.mask = pygame.mask.from_surface(self.image)
        while pygame.sprite.spritecollideany(self, all_sprites):
            self.rect.x = random.randrange(width - self.rect.width)
            self.rect.y = random.randrange(height - self.rect.height)

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image = self.image_boom


if __name__ == '__main__':
    play = False
    running = True
    fps = 60
    clock = pygame.time.Clock()
    image = pygame.Surface([100, 100])
    image.fill(pygame.Color("red"))
    all_sprites = pygame.sprite.Group()

    for _ in range(20):
        bomb = Bomb()
        all_sprites.add(bomb)

    while running:
        screen.fill('white')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEWHEEL:
                fps = min(120, max(1, fps + int(event.precise_y)))
                pygame.display.set_caption(f'Balls, fps:{fps}')
        all_sprites.update(event)
        all_sprites.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
        all_sprites.update()
        horizontal_borders.draw(screen)
        vertical_borders.draw(screen)

    pygame.quit()