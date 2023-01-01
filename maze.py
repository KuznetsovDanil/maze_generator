import sys
import pygame as pg
from operator import add

# расширение встроенного лимита рекурсии
# для избежания сбоев в программе
sys.setrecursionlimit(2000)

# предустановленные значения характеристик лабиринта
TILE = 30
cols, rows = 30, 25
RES = cols * TILE + 2, rows * TILE + 2
start = 0, 0
ticks = 60
animation = False
algorithm_generation = "random"
algorithm_path = "dijkstra"
frequency = 0.2


# обновление установленных пользователем параметров лабиринта
# с проверкой на соответствие типов и диапазонов
def set_maze(_cols, _rows, _tile, _anim, _ticks, _start, _gen, _path, _freq):
    global cols, rows, TILE, RES, animation, ticks, start, \
           algorithm_generation, algorithm_path, frequency
    if isinstance(_cols, int) and 5 <= _cols <= 150:
        cols = _cols
    if isinstance(_rows, int) and 5 <= _rows <= 100:
        rows = _rows
    if isinstance(_tile, int) and 5 <= _tile <= 100:
        TILE = _tile
    RES = cols * TILE + 2, rows * TILE + 2
    if isinstance(_anim, bool):
        animation = _anim
    if isinstance(_ticks, int) and 10 <= _ticks <= 100:
        ticks = _ticks
    if (isinstance(_start, tuple) and
        isinstance(_start[0], int) and isinstance(_start[1], int) and
        1 <= _start[0] <= cols and 1 <= _start[1] <= rows):
        start = _start
    algorithm_generation = _gen
    algorithm_path = _path
    if isinstance(_freq, float) and 0.05 <= _freq <= 0.45:
        frequency = _freq


# получение данных для отрисовки клетки:
# координаты верхней левой точки и стороны
def get_rect(x, y, margin=1):
    return (x * TILE + margin, y * TILE + margin,
           TILE - margin * 2, TILE - margin * 2)


# получение координат клетки, на которую указывает курсор
def get_click_mouse_pos(sc):
    x, y = pg.mouse.get_pos()
    grid_x, grid_y = x // TILE, y // TILE
    pg.draw.rect(sc, pg.Color('red'), get_rect(grid_x, grid_y))
    click = pg.mouse.get_pressed()
    return (grid_x, grid_y) if click[0] else False


# циклическая цветовая схема для анимации бэктрекера
def get_color(i):
    i %= 480
    if 0 <= i < 55:
        return tuple(list(map(add, [100, 50, 210], [i*2, 0, 0])))
    elif 55 <= i < 135:
        return tuple(list(map(add, [210, 50, 210], [0, 0, 110-i*2])))
    elif 135 <= i < 215:
        return tuple(list(map(add, [210, 50, 50], [0, i*2-270, 0])))
    elif 215 <= i < 295:
        return tuple(list(map(add, [210, 210, 50], [430-i*2, 0, 0])))
    elif 295 <= i < 375:
        return tuple(list(map(add, [50, 210, 50], [0, 0, i*2-590])))
    elif 375 <= i < 455:
        return tuple(list(map(add, [50, 210, 210], [0, 750-i*2, 0])))
    else:
        return tuple(list(map(add, [50, 50, 210], [i*2-910, 0, 0])))


# эвристика "манхэттенского расстояния" для алгоритма А*
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
