import pygame
import os
import sys
import random



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


size = width, height = 300, 300
pygame.init()
screen = pygame.display.set_mode(size)


class Hero(pygame.sprite.Sprite):
    image = load_image("creature.png", -1)

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Hero.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0

    def update(self, *args):
        scancode: pygame.key.ScancodeWrapper = args[0]
        if scancode[pygame.K_DOWN]:
            self.rect = self.rect.move(0, 10)
        if scancode[pygame.K_UP]:
            self.rect = self.rect.move(0, -10)
        if scancode[pygame.K_LEFT]:
            self.rect = self.rect.move(-10, 0)
        if scancode[pygame.K_RIGHT]:
            self.rect = self.rect.move(10, 0)


if __name__ == '__main__':
    play = False
    running = True
    fps = 60
    clock = pygame.time.Clock()
    image = pygame.Surface([100, 100])
    image.fill(pygame.Color("red"))
    image = load_image("error.png")
    all_sprites = pygame.sprite.Group()
    all_sprites.add(Hero(all_sprites))
    pygame.mouse.set_visible(False)
    while running:
        screen.fill('white')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEWHEEL:
                fps = min(120, max(1, fps + int(event.precise_y)))
                pygame.display.set_caption(f'Image, fps:{fps}')
        all_sprites.update(pygame.key.get_pressed())
        all_sprites.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()