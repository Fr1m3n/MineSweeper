import pygame
import os
from pygame.locals import *
from classes.playground import Playground

WHITE = (255, 255, 255)
BG = (172, 229, 238)


def load_image(name):
    fullname = os.path.join('res', name)  # Картинки у меня лежат в папке 'res'
    try:
        image = pygame.image.load(fullname)
    except:
        exit(1)
    image = image.convert_alpha()
    pygame.transform.scale(image, (16, 16))
    return image


# def draw_sprite(sprite, y, x):
#     field.field[y][x]
pygame.init()
fontObj = pygame.font.Font(os.path.join('fonts', '11758.ttf'), 20)

# описание параметров игрового поля
field_height = 10  # высота
field_width = 10  # ширина
cell_size = 64  # размер клеток (длина стороны)
count_of_mines = 3  # кол-во мин на поле
field = Playground(field_height, field_width, count_of_mines)  # создание поля
field_surf = pygame.Surface((field_width * cell_size, field_height * cell_size))
field_bgcolor = WHITE
field_surf.fill(field_bgcolor)
# ----

# раздел описания размеров "шапки", где будет отображён интерфейс
header_height = 50
thick = 10  # размер "промежутков" между элементами
header_minwidth = field_width * cell_size
header_surf = pygame.Surface((header_minwidth, header_height))
header_bgcolor = (131, 205, 235)
# ----

# создаём окно с учётом размеров поля, размеров клеток и "промежутков"
window_size = thick * 2 + field_width * cell_size, thick * 3 + header_height + field_height * cell_size
window = pygame.display.set_mode(window_size)
# ----

generated = False
in_process = True
need_render = True
loosed_cell = None

# sprite, sprite_rect = load_image('0.png')
# surf = pygame.Surface((64, 64))
# surf.fill((255,255,255))
# surf.blit(sprite, (0, 0))

# загрузха спрайтов
sprites_num = []  # "номерные спрайты"
for i in range(9):
    sprites_num.append(load_image(str(i) + '.png'))
bomb_sprite = load_image('bomb.png')
free_sprite = load_image('space.png')
flag_sprite = load_image('flag.png')
exploded_sprite = load_image('explosion.png')
brflag_sprite = load_image('broken_flag.png')
# ----

clock = pygame.time.Clock()

# field.first_generation((0, 0))
# field.open_cell(0, 0)

while in_process:
    # print(1)
    for event in pygame.event.get():
        if (event.type == QUIT):
            in_process = False
            pygame.quit()
        elif (event.type == MOUSEBUTTONDOWN):
            need_render = True
            pressed_y = int((event.pos[1] - thick * 2 - header_height) / cell_size)
            pressed_x = int((event.pos[0] - thick) / cell_size)
            print(pressed_y, pressed_x)
            if (event.button == 1):
                if (generated == False):
                    field.first_generation((pressed_y, pressed_x))
                    generated = True
                if (field.open_cell(int(pressed_x), int(pressed_y)) == 1 and field.field[pressed_y][
                    pressed_x].marked == False):
                    print('LOOSE')  # проиграл
                    loosed_cell = (pressed_y, pressed_x)
                    need_render = True
            if (event.button == 3 and generated):
                field.mark_cell(pressed_x, pressed_y)
                if(field.count_of_mines - field.marked_cells < 0):
                    field.mark_cell(pressed_x, pressed_y)
                if(field.true_marked_cells == count_of_mines):
                    print('WIN')
                    score_textOBJ = fontObj.render('WIN WIN WIN WIN WIN WIN', True, (0, 0, 0), header_bgcolor)
                    score_rect = score_textOBJ.get_rect()
                    score_rect.center = (20, 20)
                    header_surf.blit(score_textOBJ, score_rect)
                    need_render = True
                    pygame.time.wait(300)
                    in_process = False
                    window.blit(header_surf, (thick, thick))

    window.fill(BG)
    field_surf.fill(field_bgcolor)
    header_surf.fill(header_bgcolor)
    if (need_render):
        score_textOBJ = fontObj.render(str(count_of_mines - field.marked_cells), True, (0, 0, 0), header_bgcolor)
        score_rect = score_textOBJ.get_rect()
        score_rect.center = (20, 20)
        header_surf.blit(score_textOBJ, score_rect)
        for i in range(field.size[0]):
            for j in range(field.size[1]):
                if (loosed_cell):
                    if (field.field[i][j].type == 'Mine' and field.field[i][j].marked == False):
                        field_surf.blit(bomb_sprite, (j * cell_size, i * cell_size))
                    elif (field.field[i][j].opened):
                        field_surf.blit(sprites_num[field.field[i][j].num], (j * cell_size, i * cell_size))
                    elif (field.field[i][j].marked):
                        if(field.field[i][j].type == 'Mine'):
                            field_surf.blit(flag_sprite, (j * cell_size, i * cell_size))
                        else:
                            field_surf.blit(brflag_sprite, (j * cell_size, i * cell_size))
                    else:
                        field_surf.blit(free_sprite, (j * cell_size, i * cell_size))
                    field_surf.blit(exploded_sprite, (loosed_cell[1] * cell_size, loosed_cell[0] * cell_size))
                else:
                    if (field.field[i][j].marked):
                        field_surf.blit(flag_sprite, (j * cell_size, i * cell_size))
                    elif (field.field[i][j].opened == False):
                        field_surf.blit(free_sprite, (j * cell_size, i * cell_size))
                    else:
                        field_surf.blit(sprites_num[field.field[i][j].num], (j * cell_size, i * cell_size))
        window.blit(header_surf, (thick, thick))
        window.blit(field_surf, (thick, thick * 2 + header_height))
        pygame.display.update()
        need_render = False
    clock.tick(10)
    if (in_process == False):
        pygame.time.wait(3000)

pygame.quit()
