import os
import pygame
import sys


def load_image(name, color_key=None, parent_dir=""):
    if parent_dir:
        fullname = rf"{parent_dir}\data\{name}"
    else:
        fullname = os.path.abspath(rf"data\{name}")
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)

    return image


def load_ost(name):
    fullname = os.path.join(r'data\Osts', name)
    pygame.mixer.music.load(fullname)
    pygame.mixer.music.play()


def cut_sheet(sheet, columns, rows):
    rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
    cycle = []
    for j in range(rows):
        for i in range(columns):
            frame_location = (rect.w * i, rect.h * j)
            frame = sheet.subsurface(pygame.Rect(frame_location, rect.size))
            frame.set_colorkey(frame.get_at((0, 0)))
            cycle.append(frame)
    return cycle


def terminate():
    pygame.quit()
    sys.exit()