import pygame
from settings import clock, screen, FPS, WIDTH, HEIGHT, all_sprites
from background import animate_background, tiles, load_image, background, gen_background
import os

start_point = pygame.Rect(0, HEIGHT, 1, 1)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 6 -
                    min(WIDTH // 6, abs(start_point.left - target.rect.left)))
        start_point.x += self.dx
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 1.2)
        start_point.y += self.dy


class Block(pygame.sprite.Sprite):
    def __init__(self, block_type, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = block_images[block_type]  # строка с названием
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)


hero_group = pygame.sprite.Group()
block_group = pygame.sprite.Group()
block_names = ([f"{name} Big" for name in ["Autumn", "Fantasy", "Grass", "Jade", "Stone", "Wood"]] +
               [f"{name} Big" for name in ["Autumn", "Fantasy", "Grass", "Jade", "Stone", "Wood"]])
block_images = {key: load_image(rf"Terrain\Square Blocks\{key}.png") for key in block_names}

# Функция отрисовки уровня



# Создание уровня
level_save = []
selected_block = None


# Главный цикл игры
def create_level():
    global selected_block, level_save
    gen_background()
    camera = Camera()
    buttons = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    block_sur = []
    save_button = pygame.sprite.Sprite()
    eye = pygame.sprite.Sprite()
    quit_button = pygame.sprite.Sprite()
    surf = pygame.Surface((800, 200))  # при создании передается размер
    surf.fill((255, 255, 255))

    save_button.image = load_image(rf"menu\buttons\save_button.png")
    save_button.image = pygame.transform.scale(save_button.image, (60, 60))
    save_rect = pygame.Rect(WIDTH - 100, HEIGHT - 100, 100, 100)
    save_button.rect = save_rect
    buttons.add(save_button)
    block_name = []

    quit_button.image = load_image(rf"menu\buttons\close.png")
    quit_button.image = pygame.transform.scale(quit_button.image, (50, 50))
    quit_rect = pygame.Rect(0, 0, 100, 100)
    quit_button.rect = quit_rect
    buttons.add(quit_button)

    eye.image = load_image(rf"menu\buttons\play.png")
    eye.image = pygame.transform.scale(save_button.image, (60, 60))
    eye_rect = pygame.Rect(WIDTH - 100, HEIGHT - 105, 100, 100)
    eye.rect = eye_rect
    all_sprites.add(eye)

    for i in range(6):
        block = [Block(block_names[i], (800 - 50 * 7) // 2 + i * 55, 525), block_names[i]]
        block_sur.append(block[0])
        block_name.append(block[1])
        blocks.add(block_sur)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    # Передвижение вправо
                    camera.dx -= 1
                elif event.key == pygame.K_LEFT:
                    # Передвижение влево
                    camera.dx += 1
                elif event.key == pygame.K_UP:
                    # Передвижение вверх
                    camera.dy += 1
                elif event.key == pygame.K_DOWN:
                    # Передвижение вниз
                    camera.dy -= 1

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:  # Левая кнопка мыши
                    x, y = event.pos
                    curr = 0
                    if quit_rect.collidepoint(event.pos):
                        return
                    if save_rect.collidepoint(x, y):
                        save_level()
                        return

                    for block in blocks: # Проверяем, был ли клик на блоке
                        if block.rect.collidepoint(x, y):
                            selected_block = block_names[curr]
                            break
                        curr += 1

                    else:    # Проверяем, что выбранный блок не ниже верхней точки оставшихся блоков
                        if selected_block is not None and y < 550:
                            # Проверяем пересечение с уже существующими блоками
                            is_intersecting = False
                            new_block_rect = pygame.Rect(x, y, 40, 40)
                            for block in block_group:
                                if block.rect.colliderect(new_block_rect):
                                    is_intersecting = True
                                    break

                            if not is_intersecting:
                                block_group.add(Block(selected_block, x, y))
                                level_save.append((selected_block, x, y))

                elif event.button == 3:  # Правая кнопка мыши
                    x, y = event.pos
                    for block in block_group:
                        if block.rect.collidepoint(x, y):
                            block_group.remove(block)
                            all_sprites.remove(block)
                            break

        screen.fill(pygame.Color("orange"))

        block_group.draw(screen)
        for sprite in block_group:
            camera.apply(sprite)
        screen.blit(surf, (0, 500))
        blocks.draw(screen)
        buttons.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)


def save_level():
    # Сохранение уровня в файл
    folder_path = "levels"
    file_count = sum([len(files) for _, _, files in os.walk(folder_path)])
    level_path = f'levels/lvl{file_count + 1}.txt'
    level_file = open(level_path, "w")
    for block in level_save:
        block_type, x, y = block
        level_file.write(f"{block_type} {x} {y}\n")
    level_file.close()


create_level()