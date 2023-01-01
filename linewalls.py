# Лабиринт с тонкими стенами

import pygame as pg
from random import *
from time import time
from collections import deque
from heapq import *
import maze


# класс Клетка
class Cell:
    # конструктор: координаты в лабиринте, стены, посещена или нет
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

    # отрисовка текущей клетки при генерации
    def draw_current_cell(self, sc):
        tile = maze.TILE
        x, y = self.x * tile, self.y * tile
        pg.draw.rect(sc, pg.Color('saddlebrown'), maze.get_rect(x, y, margin=2))

    # отрисовка клетки
    def draw_cell(self, sc):
        tile = maze.TILE
        x, y = self.x * tile, self.y * tile
        if self.visited:
            pg.draw.rect(sc, pg.Color('black'), pg.Rect(x, y, tile, tile))
        if self.walls['top'] or check_cell(grid_cells, self.x, self.y-1)\
                and grid_cells[self.y-1][self.x].walls['bottom']:
            pg.draw.line(sc, pg.Color('darkorange'), [x, y], [x + tile, y], width=2)
        if self.walls['right'] or check_cell(grid_cells, self.x+1, self.y)\
                and grid_cells[self.y][self.x+1].walls['left']:
            pg.draw.line(sc, pg.Color('darkorange'), [x + tile, y], [x + tile, y + tile], width=2)
        if self.walls['bottom'] or check_cell(grid_cells, self.x, self.y+1)\
                and grid_cells[self.y+1][self.x].walls['top']:
            pg.draw.line(sc, pg.Color('darkorange'), [x + tile, y + tile], [x, y + tile], width=2)
        if self.walls['left'] or check_cell(grid_cells, self.x-1, self.y)\
                and grid_cells[self.y][self.x-1].walls['right']:
            pg.draw.line(sc, pg.Color('darkorange'), [x, y + tile], [x, y], width=2)

    # проверка соседних клеток и случайный выбор из них, если есть доступные
    def check_neighbours(self):
        neighbours = []
        top = check_cell(grid_cells, self.x, self.y - 1)
        right = check_cell(grid_cells, self.x + 1, self.y)
        bottom = check_cell(grid_cells, self.x, self.y + 1)
        left = check_cell(grid_cells, self.x - 1, self.y)
        if top and not top.visited:
            neighbours.append(top)
        if right and not right.visited:
            neighbours.append(right)
        if bottom and not bottom.visited:
            neighbours.append(bottom)
        if left and not left.visited:
            neighbours.append(left)
        return choice(neighbours) if neighbours else False


# проверка координат клетки
def check_cell(grid, x, y):
    if x < 0 or x > maze.cols - 1 or y < 0 or y > maze.rows - 1:
        return False
    return grid[y][x]


# удаление стены между клетками
def remove_walls(current_cell, next_cell):
    dx = current_cell.x - next_cell.x
    if dx == 1:
        current_cell.walls['left'] = False
        next_cell.walls['right'] = False
    elif dx == -1:
        current_cell.walls['right'] = False
        next_cell.walls['left'] = False
    dy = current_cell.y - next_cell.y
    if dy == 1:
        current_cell.walls['top'] = False
        next_cell.walls['bottom'] = False
    elif dy == -1:
        current_cell.walls['bottom'] = False
        next_cell.walls['top'] = False


# получение списка доступных соседних клеток
def get_next_nodes(grid, x, y):
    current_cell = grid[y][x]
    neighbours = []
    top = check_cell(grid_cells, current_cell.x, current_cell.y - 1)
    right = check_cell(grid_cells, current_cell.x + 1, current_cell.y)
    bottom = check_cell(grid_cells, current_cell.x, current_cell.y + 1)
    left = check_cell(grid_cells, current_cell.x - 1, current_cell.y)
    # в зависимости от алгоритма нужны разные значения для графов поиска
    if maze.algorithm_path == "dijkstra":
        if top and not current_cell.walls['top'] and not top.walls['bottom']:
            neighbours.append((x, y - 1))
        if right and not current_cell.walls['right'] and not right.walls['left']:
            neighbours.append((x + 1, y))
        if bottom and not current_cell.walls['bottom'] and not bottom.walls['top']:
            neighbours.append((x, y + 1))
        if left and not current_cell.walls['left'] and not left.walls['right']:
            neighbours.append((x - 1, y))
    elif maze.algorithm_path == "a_star":
        if top and not current_cell.walls['top'] and not top.walls['bottom']:
            neighbours.append((1, (x, y - 1)))
        if right and not current_cell.walls['right'] and not right.walls['left']:
            neighbours.append((1, (x + 1, y)))
        if bottom and not current_cell.walls['bottom'] and not bottom.walls['top']:
            neighbours.append((1, (x, y + 1)))
        if left and not current_cell.walls['left'] and not left.walls['right']:
            neighbours.append((1, (x - 1, y)))
    return neighbours


# случайная генерация лабиринта
def random_grid(grid, sc, clock):
    for row in grid:
        for cell in row:
            cell.visited = False
            cell.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
    current_cell = grid[0][0]
    while True:
        # анимация
        if maze.animation:
            sc.fill(pg.Color('darkslategray'))
            [[cell.draw_cell(sc) for cell in row] for row in grid]
            current_cell.draw_current_cell(sc)
            pg.display.flip()
            clock.tick(maze.ticks)

        # алгоритм
        current_cell.visited = True
        r = [random(), random(), random(), random()]
        s = ["top", "right", "bottom", "left"]
        for i in range(4):
            current_cell.walls[s[i]] = r[i] < maze.frequency
        # переход на новый ряд
        if current_cell.x + current_cell.y * maze.cols + 1 < maze.cols * maze.rows:
            if current_cell.x + 1 < maze.cols:
                current_cell = grid[current_cell.y][current_cell.x + 1]
            else:
                current_cell = grid[current_cell.y + 1][0]
        else:
            break
        [pg.quit() for event in pg.event.get() if event.type == pg.QUIT]
    return grid


# рекурсивный бэктрекер
def recursive_grid(grid, sc, clock):
    # сначала все стены есть
    for row in grid:
        for cell in row:
            cell.visited = False
            cell.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
    start_x, start_y = maze.start         # начальная клетка
    current_cell = grid[start_y][start_x] # текущая клетка
    stack = []                            # стек для хранения посещённых
    colors, color = [], 0                 # цветовая схема
    while True:
        # анимация
        if maze.animation:
            sc.fill(pg.Color('darkslategray'))
            [[cell.draw_cell(sc) for cell in row] for row in grid]
            current_cell.draw_current_cell(sc)
            [pg.draw.rect(sc, colors[i], maze.get_rect(cell.x, cell.y, margin=maze.TILE // 6),
             border_radius=maze.TILE // 3) for i, cell in enumerate(stack)]
            pg.display.flip()
            clock.tick(maze.ticks)

        # алгоритм
        current_cell.visited = True
        next_cell = current_cell.check_neighbours()
        if next_cell:
            next_cell.visited = True
            stack.append(current_cell)
            colors.append(maze.get_color(len(stack)))
            color += 1
            remove_walls(current_cell, next_cell)
            current_cell = next_cell
        elif stack:
            current_cell = stack.pop()
        else:
            break

        [pg.quit() for event in pg.event.get() if event.type == pg.QUIT]
    return grid


# генерация алгоритмом Прима
def prim_grid(grid, sc, clock):
    # все стены есть
    for row in grid:
        for cell in row:
            cell.visited = None
            cell.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
    ways = [-1, 0], [0, -1], [1, 0], [0, 1] # доступные направления
    x, y = maze.start                       # стартовая клетка
    grid[y][x].visited = True               # отмечаем как посещённую
    # соседние отмечаем как непосещённые
    for way in ways:
        if check_cell(grid, x+way[0], y+way[1]):
            grid[y+way[1]][x+way[0]].visited = False
    while True:
        # определяем границы сгенерированной области
        borders = []
        for row in grid:
            for cell in row:
                if cell.visited == False:
                    borders.append(cell)
        visited = []
        # выбираем случайную из них
        current_cell = choice(borders) if borders else False
        x, y = False, False
        # если есть, отмечаем как посещённую
        if current_cell:
            current_cell.visited = True
            x, y = current_cell.x, current_cell.y
        # если соседние посещённые, добавляем их в список
        # если нет, помечаем как границы
        for way in ways:
            if check_cell(grid, x + way[0], y + way[1]):
                if grid[y+way[1]][x+way[0]].visited:
                    visited.append(grid[y+way[1]][x+way[0]])
                elif grid[y+way[1]][x+way[0]].visited is None:
                    grid[y + way[1]][x + way[0]].visited = False
        # разрушаем стену между текущей клеткой и
        # случайной из посещённых соседних
        if visited:
            previous_cell = choice(visited)
            remove_walls(previous_cell, current_cell)
        # подсчитываем клетки-границы
        # если есть, продолжаем алгоритм
        counter = 0
        for row in grid:
            for cell in row:
                if cell.visited == False:
                    counter += 1

        # анимация
        [pg.quit() for event in pg.event.get() if event.type == pg.QUIT]
        if maze.animation:
            sc.fill(pg.Color('darkslategray'))
            [[cell.draw_cell(sc) for cell in row] for row in grid]
            current_cell.draw_current_cell(sc)
            pg.display.flip()
            clock.tick(maze.ticks)
        # переход на новую итерацию или выход из цикла
        if counter:
            continue
        else:
            break
    return grid


# получение графа путей
def generate_graph(grid):
    graph = {}
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(grid, x, y)
    return graph


# логика алгоритма Дейкстры
def dijkstra(start, goal, graph):
    queue = deque([start])
    visited = {start: None}
    while queue:
        cur_node = queue.popleft()
        if cur_node == goal:
            break
        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            if next_node not in visited:
                queue.append(next_node)
                visited[next_node] = cur_node
    return queue, visited


# логика алгоритма А*
def a_star(start, goal, graph):
    queue = []
    heappush(queue, (0, start))
    cost_visited = {start: 0}
    visited = {start: None}
    while queue:
        cur_cost, cur_node = heappop(queue)
        if cur_node == goal:
            break
        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            neigh_cost, neigh_node = next_node
            new_cost = cost_visited[cur_node] + neigh_cost
            if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                priority = new_cost + maze.heuristic(neigh_node, goal)
                heappush(queue, (priority, neigh_node))
                cost_visited[neigh_node] = new_cost
                visited[neigh_node] = cur_node
    return queue, visited


# глобально заданный лабиринт
grid_cells = [[Cell(col, row) for col in range(maze.cols)] for row in range(maze.rows)]


# обновление размеров
def configure():
    global grid_cells
    grid_cells = [[Cell(col, row) for col in range(maze.cols)] for row in range(maze.rows)]


# запуск модуля
def run():
    global grid_cells
    pg.init()
    pg.display.set_caption("Лабиринт")
    tile = maze.TILE
    sc = pg.display.set_mode(maze.RES, pg.RESIZABLE)
    clock = pg.time.Clock()
    gen_start, gen_time = 0.0, 0.0

    # генерация
    if maze.algorithm_generation == "random":
        gen_start = time()
        grid_cells = random_grid(grid_cells, sc, clock)
        gen_time = time() - gen_start
    elif maze.algorithm_generation == "recursive":
        gen_start = time()
        grid_cells = recursive_grid(grid_cells, sc, clock)
        gen_time = time() - gen_start
    elif maze.algorithm_generation == "prim":
        gen_start = time()
        grid_cells = prim_grid(grid_cells, sc, clock)
        gen_time = time() - gen_start

    # подготовка к поиску пути
    graph = generate_graph(grid_cells)
    goal = maze.start
    queue = []
    if maze.algorithm_path == "a_star":
        heappush(queue, (0, maze.start))
    visited = {maze.start: None}
    old_goal = goal
    begin, end = 0.0, 0.0

    # поиск пути
    while True:
        # анимация
        sc.fill(pg.Color('black'))
        [[cell.draw_cell(sc) for cell in row] for row in grid_cells]
        [pg.draw.rect(sc, pg.Color('forestgreen'), maze.get_rect(x, y)) for x, y in visited]
        if maze.algorithm_path == "dijkstra":
            [pg.draw.rect(sc, pg.Color('darkslategray'), maze.get_rect(x, y)) for x, y in queue]
        elif maze.algorithm_path == "a_star":
            [pg.draw.rect(sc, pg.Color('darkslategray'), maze.get_rect(*xy)) for _, xy in queue]

        # получение конечной точки
        mouse_pos = maze.get_click_mouse_pos(sc)
        begin = time()
        # получение списка посещённых клеток и графа маршрутов
        if mouse_pos:
            if maze.algorithm_path == "dijkstra":
                queue, visited = dijkstra(maze.start, mouse_pos, graph)
            elif maze.algorithm_path == "a_star":
                queue, visited = a_star(maze.start, mouse_pos, graph)
            # установка цели
            goal = mouse_pos
        length_way = 0
        path_head, path_segment = goal, goal
        # отрисовка начала и конца пути
        pg.draw.rect(sc, pg.Color('blue'), maze.get_rect(*maze.start), tile, border_radius=tile // 5)
        pg.draw.rect(sc, pg.Color('magenta'), maze.get_rect(*path_head), tile, border_radius=tile // 5)
        # отрисовка кратчайшего маршрута при обратном проходе по графу
        while path_segment and path_segment in visited:
            pg.draw.rect(sc, pg.Color('white'), maze.get_rect(*path_segment), tile, border_radius=tile // 3)
            path_segment = visited[path_segment]
            length_way += 1
        # обновление картинки только при изменении конечной точки
        if old_goal != goal:
            end = time() - begin
            old_goal = goal
            # with open("maze.txt", "at") as file:
            #     file.write(f"lines {maze.algorithm_generation} {maze.algorithm_path} {maze.cols} {maze.rows} " +
            #                f"{gen_time:.4} {length_way - 1} {end:.4}\n")
        # вывод данных в заголовок окна
        if maze.animation:
            pg.display.set_caption(f"Лабиринт (длина пути: {length_way - 1}; время прохода: {end:.4} сек.)")
        else:
            pg.display.set_caption(f"Лабиринт (время генерации: {gen_time:.4} сек.; длина пути: " +
                                   f"{length_way - 1}; время прохода: {end:.4} сек.)")

        [pg.quit() for event in pg.event.get() if event.type == pg.QUIT]
        pg.display.flip()
        clock.tick(maze.ticks)
