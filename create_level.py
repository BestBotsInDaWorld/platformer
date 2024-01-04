import pygame
from settings import clock, screen, FPS, WIDTH, HEIGHT, all_sprites
from background import animate_background, tiles, load_image, background, gen_background


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
        super().__init__(block_group, all_sprites)
        self.image = block_images[block_type]  # строка с названием
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)


hero_group = pygame.sprite.Group()
block_group = pygame.sprite.Group()
block_names = ([f"{name} Big" for name in ["Autumn", "Fantasy", "Grass", "Jade", "Stone", "Wood"]] +
               [f"{name} Big" for name in ["Autumn", "Fantasy", "Grass", "Jade", "Stone", "Wood"]])
block_images = {key: load_image(rf"Terrain\Square Blocks\{key}.png") for key in block_names}

print(block_names)

# Функция отрисовки уровня



# Создание уровня
level = pygame.sprite.Group()
level_save = []
selected_block = None





# Главный цикл игры
def create_level():
    global selected_block, level, level_save
    gen_background()
    camera = Camera()
    blocks = pygame.sprite.Group()
    observer = pygame.sprite.Group()
    block_sur = []
    save_button = pygame.sprite.Sprite()
    eye = pygame.sprite.Sprite()

    save_button.image = load_image(rf"menu\buttons\play.png")
    save_button.image = pygame.transform.scale(save_button.image, (60, 60))
    save_rect = pygame.Rect(WIDTH - 100, HEIGHT - 105, 100, 100)
    save_button.rect = save_rect
    all_sprites.add(save_button)
    block_name = []

    eye.image = load_image(rf"menu\buttons\play.png")
    eye.image = pygame.transform.scale(save_button.image, (60, 60))
    eye_rect = pygame.Rect(WIDTH - 100, HEIGHT - 105, 100, 100)
    eye.rect = eye_rect
    all_sprites.add(eye)

    for i in range(6):
        block = [Block(block_names[i], (800 - 50 * 7) // 2 + i * 55, 500), block_names[i]]
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

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    x, y = event.pos
                    curr = 0
                    if save_rect.collidepoint(x, y):
                        save_level()
                        return

                    for block in blocks: # Проверяем, был ли клик на блоке
                        if block.rect.collidepoint(x, y):
                            selected_block = block_names[curr]
                            break
                        curr += 1
                    else:
                        # Проверяем, что выбранный блок не ниже верхней точки оставшихся блоков
                        if selected_block is not None and round(y / 50) * 48 < 550:
                            x = round(x / 50) * 48
                            y = round(y / 50) * 48
                            level.add(Block(selected_block, x, y))
                            level_save.append((selected_block, x, y))
                            selected_block = None
                elif event.button == 3:  # Правая кнопка мыши
                    x, y = event.pos
                    for block in level:
                        if block.rect.collidepoint(x, y):
                            level.remove(block)
                            all_sprites.remove(block)
                            break

        screen.fill(pygame.Color("orange"))
        all_sprites.draw(screen)
        level.draw(screen)
        blocks.draw(screen)
        for sprite in all_sprites:
            camera.apply(sprite)
        pygame.display.flip()
        clock.tick(FPS)


def save_level():
    # Сохранение уровня в файл
    level_file = open("lvl1.txt", "w")
    for block in level_save:
        block_type, x, y = block
        level_file.write(f"{block_type} {x} {y}\n")
    level_file.close()

create_level()