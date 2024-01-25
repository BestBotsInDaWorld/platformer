import pygame
from settings import clock, screen, FPS, WIDTH, HEIGHT, all_sprites, CONSTUCTOR_CAMERA_X, CONSTUCTOR_CAMERA_Y
from background import animate_background, tiles, load_image, background, gen_background
from tkinter import Tk
import os


blocks = pygame.sprite.Group()
start_point = pygame.Rect(0, HEIGHT, 1, 1)
monitor_info = Tk()
monitor_width_center = monitor_info.winfo_screenwidth() // 2
monitor_height_center = monitor_info.winfo_screenheight() // 2


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

    def apply_mouse(self):
        if not pygame.mouse.get_focused():
            x, y = monitor_info.winfo_pointerxy()
            shift_x = (monitor_width_center - x) % monitor_width_center / monitor_width_center
            shift_y = (monitor_height_center - y) % monitor_height_center / monitor_height_center
            if x > monitor_width_center:
                shift_x -= 1
            if y > monitor_height_center:
                shift_y -= 1
            if abs(x - monitor_width_center) < WIDTH // 2:
                shift_x = 0
            elif abs(y - monitor_height_center) < HEIGHT // 2:
                shift_y = 0
            camera.dx = CONSTUCTOR_CAMERA_X * shift_x
            camera.dy = CONSTUCTOR_CAMERA_Y * shift_y
        else:
            camera.dx = 0
            camera.dy = 0


camera = Camera()


class Button(pygame.sprite.Sprite):
    def __init__(self, sprite_type, pos_x, pos_y, isBlock, withBack, block_rect):
        super().__init__(blocks)

        if isBlock:
            self.image = block_images[sprite_type]  # строка с названием
        else:
            self.image = trap_images[sprite_type]
        if withBack:
            self.image.set_colorkey(self.image.get_at((0, 0)))
        self.rect = self.image.get_rect()
        self.rect.centerx = pos_x + 30
        self.rect.centery = pos_y + 100

    def scroll(self, vector):
        self.rect = self.rect.move(vector, 0)


class Unit(pygame.sprite.Sprite):
    def __init__(self, block_type, pos_x, pos_y, isBlock):
        super().__init__(block_group)
        if isBlock:
            self.image = block_images[block_type]  # строка с названием
        else:
            self.image = trap_images[block_type]
        self.block_type = block_type
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)


hero_group = pygame.sprite.Group()
block_group = pygame.sprite.Group()
block_names = ([f"{name} Big" for name in ["Autumn", "Fantasy", "Grass", "Jade", "Stone", "Wood"]] +
               [f"{name} Small" for name in ["Autumn", "Fantasy", "Grass", "Jade", "Stone", "Wood"]])
block_images = {key: load_image(rf"Terrain\Square Blocks\{key}.png") for key in block_names}


folder_path = 'data\Traps'  # путь к папке Traps
subfolders = os.listdir(folder_path)
folders = [f"{path}\idle.png" for path in subfolders]
trap_images = {path: load_image(rf"Traps\{path}") for path in folders}

# Функция отрисовки уровня


# Создание уровня
level_save = []
selected_block = None

# быстрая установка блока: клик на границы спрайта, три положения по высоте по бокам и одно наверху и внизу
def block_allign(new_block_rect: pygame.rect, colliding_block: pygame.sprite, x: int, y: int) -> None:
    left_right = False
    if x < colliding_block.rect.x + colliding_block.rect.width // 3:
        new_block_rect.x = colliding_block.rect.x - new_block_rect.width
        left_right = True
    elif x > colliding_block.rect.x + colliding_block.rect.width // 3 * 2:
        new_block_rect.x = colliding_block.rect.x + colliding_block.rect.width
        left_right = True
    else:
        new_block_rect.x = colliding_block.rect.x + (colliding_block.rect.width - new_block_rect.width ) // 2

    if left_right:
        if y < colliding_block.rect.y + colliding_block.rect.height // 3:
            new_block_rect.y = colliding_block.rect.y
        elif y < colliding_block.rect.y + colliding_block.rect.height // 3 * 2:  # середина
            new_block_rect.y = colliding_block.rect.y + (colliding_block.rect.height - new_block_rect.height) // 2
        else:
            new_block_rect.y = colliding_block.rect.y + colliding_block.rect.height // 3 * 2
    elif y < colliding_block.rect.y + colliding_block.rect.height // 2:
        new_block_rect.y = colliding_block.rect.y - new_block_rect.height
    else:
        new_block_rect.y = colliding_block.rect.y + colliding_block.rect.height

def create_level():
    global selected_block, level_save, blocks, camera
    gen_background()
    names_blocks_n_traps = block_names + folders
    curr_block = 1
    buttons = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    blocks_small = pygame.sprite.Group()
    block_sur = []
    save_button = pygame.sprite.Sprite()
    eye = pygame.sprite.Sprite()
    next = pygame.sprite.Sprite()
    prev = pygame.sprite.Sprite()
    quit_button = pygame.sprite.Sprite()
    surf = pygame.Surface((800, 200))  # при создании передается размер
    surf.fill((255, 255, 255))
    fon = pygame.Surface((800, 600))
    fon.fill(pygame.Color("orange"))
    block_sur = []
    block_name = []

    next.image = load_image(rf"menu\buttons\play.png")
    next.image = pygame.transform.scale(next.image, (50, 50))
    next_rect = pygame.Rect(575, 525, 100, 100)
    next.rect = next_rect
    buttons.add(next)

    prev.image = load_image(rf"menu\buttons\play.png")
    prev.image = pygame.transform.scale(next.image, (50, 50))
    prev.image = pygame.transform.rotate(next.image, 180)
    prev_rect = pygame.Rect(150, 525, 50, 50)
    prev.rect = prev_rect
    buttons.add(prev)



    current_screen = 0
    block_x = 50
    block_y = 525

    for i in range(12):
        if i >= 6:
            current_screen = 475
        block_rect = pygame.Rect((800 - block_x * 7) // 2 + i * (block_x + 5) + current_screen, block_y - 75, block_x,
                                 block_y)
        block = [Button(block_names[i], block_rect.x, block_rect.y, True, False, block_rect), block_names[i]]
        block_sur.append(block[0])
        block_name.append(block[1])
        blocks.draw(screen)
    current_screen = 1600

    for i in range(len(folders)):
        if i >= 6:
            current_screen = 2000
        if i >= 12:
            current_screen = 2550
        block_rect = pygame.Rect((800 - block_x * 7) // 2 + i * (block_x + 5) + current_screen, block_y - 75, block_x,
                                 block_y)
        block = [Button(folders[i], block_rect.x, block_rect.y, False, True, block_rect), folders[i]]
        block_sur.append(block[0])
        block_name.append(block[1])
        blocks.draw(screen)



    save_button.image = load_image(rf"menu\buttons\save.png")
    save_button.image = pygame.transform.scale(save_button.image, (100, 50))
    save_button.image.set_colorkey(save_button.image.get_at((0, 0)))
    save_rect = pygame.Rect(WIDTH - 125, HEIGHT - 75, 100, 100)
    save_button.rect = save_rect
    buttons.add(save_button)
    block_name = []

    quit_button.image = load_image(rf"menu\buttons\close.png")
    quit_button.image = pygame.transform.scale(quit_button.image, (50, 50))
    quit_rect = pygame.Rect(0, 0, 100, 100)
    quit_button.rect = quit_rect
    buttons.add(quit_button)
    buttons_group = []


    curr_page = 1

    while True:
        camera.apply_mouse()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:  # Левая кнопка мыши
                    x, y = event.pos
                    curr = 0
                    if quit_rect.collidepoint(event.pos):
                        return
                    if save_rect.collidepoint(x, y):
                        save_level()
                        return

                    if next_rect.collidepoint(event.pos):
                        for sprite in block_sur:
                            sprite.scroll(-WIDTH)

                    if prev_rect.collidepoint(event.pos):
                        for sprite in block_sur:
                            sprite.scroll(WIDTH)

                    for block in blocks: # Проверяем, был ли клик на блоке
                        if block.rect.collidepoint(x, y):
                            selected_block = names_blocks_n_traps[curr]
                            break
                        curr += 1

                    else:
                        if selected_block is not None:
                            isBlock = True
                            if r"idle.png" in selected_block:
                                isBlock = False
                            width_block, height_block = 0, 0
                            for block in block_group:
                                if block.rect.collidepoint(event.pos):
                                    width_block, height_block = block.rect.width, block.rect.height

                            new_block_rect = pygame.Rect(x, y, width_block, height_block)

                            for block in block_group:  # добавление выравненного блока по нажатию на границы соседа
                                if block.rect.collidepoint(event.pos):
                                    block_allign(new_block_rect, block, x, y)
                                    break
                            for block in block_group:  # если блок корректно установлен TODO
                                if block.rect.colliderect(new_block_rect):
                                    break
                            else:
                                alligned_x, alligned_y = new_block_rect.x, new_block_rect.y
                                new_unit = Unit(selected_block, alligned_x, alligned_y, isBlock)
                                block_group.add(new_unit)
                                level_save.append(new_unit)
                elif event.button == 3:  # Правая кнопка мыши
                    x, y = event.pos
                    for block in block_group:
                        if block.rect.collidepoint(x, y):
                            level_save.pop(level_save.index(block))
                            block.kill()
                            break
        screen.blit(fon, (0, 0))
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
    for unit in level_save:
        block_type, x, y = unit.block_type, unit.rect.x, unit.rect.y
        level_file.write(f"{block_type} {x} {y}\n")
    level_file.close()


create_level()