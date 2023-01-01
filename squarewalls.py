# Лабиринт с объёмными стенами

import pygame as pg
from random import *
from heapq import *
from time import time
from collections import deque
import maze


# случайная генерация
def random_grid(sc, clock):
    # получение карты
    grid = [[1 if random() < maze.frequency and (col, row) != maze.start else 0 for col in range(maze.cols)]
            for row in range(maze.rows)]
    animated = []
    # анимация
    while maze.animation:
        sc.fill(pg.Color('black'))
        a = randint(0, maze.cols * maze.rows - 1)
        # постепенно отрисовываем по одной новой случайно выбранной клетке
        if a not in animated:
            animated.append(a)
            [[pg.draw.rect(sc, pg.Color('darkorange'), maze.get_rect(x, y), border_radius=maze.TILE // 5)
              for x, col in enumerate(row) if col and y * maze.cols + x in animated] for y, row in enumerate(grid)]
            pg.display.flip()
            clock.tick(maze.ticks)
        [pg.quit() for event in pg.event.get() if event.type == pg.QUIT]
        # когда отрисовано всё, выход из цикла
        if len(animated) == maze.cols * maze.rows:
            break
    return grid


# рекурсивный бэктрекер
def recursive_grid(sc, clock):
    # изначально все клетки - стены
    grid = [[1 for _ in range(maze.cols)] for _ in range(maze.rows)]
    tile = maze.TILE
    stack = []  # стек для хранения предыдущих
    colors = [] # цветовая схема

    # проверка клетки
    def check_node(x, y):
        return grid[y][x] if 0 <= x < maze.cols and 0 <= y < maze.rows else False

    # алгоритм
    def create(x, y):
        # помечаем текущую клетку как свободную
        grid[y][x] = 0
        # случайным образом выбираем направление
        ways = [[-1, 0], [0, -1], [1, 0], [0, 1]]
        shuffle(ways)
        # пока есть куда идти
        while len(ways):
            # анимация
            if maze.animation:
                sc.fill(pg.Color('black'))
                [[pg.draw.rect(sc, pg.Color('darkorange'), maze.get_rect(x, y), border_radius=tile // 5)
                  for x, col in enumerate(row) if col] for y, row in enumerate(grid)]
                [pg.draw.rect(sc, colors[i], maze.get_rect(x, y, margin=tile // 6), border_radius=12)
                 for i, (x, y) in enumerate(stack)]
                pg.display.flip()
                clock.tick(maze.ticks)
            [pg.quit() for event in pg.event.get() if event.type == pg.QUIT]

            # удаляем путь из доступных
            way = ways.pop()
            # проходим на 2 клетки в выбранном направлении
            new_x, new_y = x + way[0] * 2, y + way[1] * 2
            # если там стена, то добавляем 2 клетки в стек
            # и рекурсивно вызываем алгоритм для последней
            if check_node(new_x, new_y):
                stack.append((x, y))
                colors.append(maze.get_color(len(stack)))
                inter_x, inter_y = x + way[0], y + way[1]
                stack.append((inter_x, inter_y))
                colors.append(maze.get_color(len(stack)))
                grid[inter_y][inter_x] = 0
                create(new_x, new_y)
        return

    create(maze.start[0], maze.start[1])
    return grid


# генерация алгоритмом Прима
def prim_grid(sc, clock):
    # все стены есть, посещённых нет
    grid = [[None for _ in range(maze.cols)] for _ in range(maze.rows)]
    tile = maze.TILE
    ways = [[-1, 0], [0, -1], [1, 0], [0, 1]] # доступные пути

    # проверка координат
    def check_node(x, y):
        return True if 0 <= x < maze.cols and 0 <= y < maze.rows else False

    # получение количества соседних клеток,
    # являющихся границами сгенерированной области
    def cells_around(x, y):
        s_cells = 0
        for move_x, move_y in [[-1, 0], [0, -1], [1, 0], [0, 1]]:
            if check_node(x + move_x, y + move_y) and grid[y + move_y][x + move_x] == 0:
                s_cells += 1
        return s_cells

    # удаление заданной клетки из списка границ
    def remove_walls(x, y):
        for wall in walls:
            if wall[0] == x and wall[1] == y:
                walls.remove(wall)

    # обновление списка граничных клеток
    def add_walls(x, y):
        # карты условий и индексов
        conditions = [bool(x), bool(y), x != maze.cols - 1, y != maze.rows - 1]
        map_ = [[0, 1, 3, 2], [0, 1, 2, 3], [0, 2, 3, 1], [1, 2, 3, 0]]
        short_map = [[0, 2], [1, 3], [2, 0], [3, 1]]

        # проход по каждому из 4 направлений
        for i in range(4):
            # выбираем 2 клетки с противоположных сторон от данной
            unvisited_x, unvisited_y = x + ways[short_map[i][0]][0], y + ways[short_map[i][0]][1]
            cell_x, cell_y = x + ways[short_map[i][1]][0], y + ways[short_map[i][1]][1]
            # если одна непосещённая, а другая - граница (проход),
            # помечаем текущую как новую границу и проверяем её соседей с других направлений
            # если мы не дошли до края, то помечаем непосещённые как стены и добавляем в список
            if (conditions[i] and check_node(unvisited_x, unvisited_y) and grid[unvisited_y][unvisited_x] is None and
                check_node(cell_x, cell_y) and grid[cell_y][cell_x] == 0):
                s_cells = cells_around(x, y)
                if s_cells < 2:
                    grid[y][x] = 0
                    for j in range(3):
                        if conditions[map_[i][j]] and check_node(x + ways[map_[i][j]][0], y + ways[map_[i][j]][1]):
                            if grid[y + ways[map_[i][j]][1]][x + ways[map_[i][j]][0]] != 0:
                                grid[y + ways[map_[i][j]][1]][x + ways[map_[i][j]][0]] = 1
                            if ways[map_[i][j]] not in walls:
                                walls.append((x + ways[map_[i][j]][0], y + ways[map_[i][j]][1]))

    # начинаем со заданной клетки
    x, y = maze.start
    grid[y][x] = 0
    walls = [(x + move_x, y + move_y) for move_x, move_y in ways
             if 0 <= x + move_x < maze.cols and 0 <= y + move_y < maze.rows]
    # изначально она окружена стенами
    for move_x, move_y in ways:
        if 0 <= x + move_x < maze.cols and 0 <= y + move_y < maze.rows:
            grid[y + move_y][x + move_x] = 1

    while walls:
        # анимация
        if maze.animation:
            sc.fill(pg.Color('black'))
            [[pg.draw.rect(sc, pg.Color('darkorange'), maze.get_rect(x, y), border_radius=tile // 5)
              for x, col in enumerate(row) if col] for y, row in enumerate(grid)]
            pg.display.flip()
            clock.tick(maze.ticks)
        [pg.quit() for event in pg.event.get() if event.type == pg.QUIT]

        # случайно выбираем клетку из списка стен и работаем с ней
        x, y = choice(walls)
        add_walls(x, y)
        remove_walls(x, y)

    # отмечаем все оставшиеся клетки как стены
    for i in range(maze.rows):
        for j in range(maze.cols):
            if grid[i][j] is None:
                grid[i][j] = 1

    # создаём вход и выход
    for i in range(maze.cols):
        if not grid[1][i]:
            grid[0][i] = 0
            break

    for i in range(maze.cols - 1, 0, -1):
        if grid[maze.rows - 2][i] == 0:
            grid[maze.rows - 1][i] = 0
            break
    return grid


# список доступных путей из данной клетки
def get_next_nodes(grid, x, y):
    def check_next_node(grid, x, y):
        return True if 0 <= x < maze.cols and 0 <= y < maze.rows and not grid[y][x] else False

    ways = [-1, 0], [0, -1], [1, 0], [0, 1]
    if maze.algorithm_path == "dijkstra":
        return [(x + dx, y + dy) for dx, dy in ways if check_next_node(grid, x + dx, y + dy)]
    elif maze.algorithm_path == "a_star":
        return [(1, (x + dx, y + dy)) for dx, dy in ways if check_next_node(grid, x + dx, y + dy)]


# получение графа путей
def generate_graph(grid):
    graph = {}
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if not col:
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


# запуск модуля
def run():
    pg.init()
    pg.display.set_caption("Лабиринт")
    sc = pg.display.set_mode(maze.RES, pg.RESIZABLE)
    clock = pg.time.Clock()
    tile = maze.TILE
    grid = []
    gen_start, gen_time = 0.0, 0.0

    # генерация
    if maze.algorithm_generation == "random":
        gen_start = time()
        grid = random_grid(sc, clock)
        gen_time = time() - gen_start
    elif maze.algorithm_generation == "recursive":
        gen_start = time()
        grid = recursive_grid(sc, clock)
        gen_time = time() - gen_start
    elif maze.algorithm_generation == "prim":
        gen_start = time()
        grid = prim_grid(sc, clock)
        gen_time = time() - gen_start

    # подготовка к поиску пути
    graph = generate_graph(grid)
    goal = maze.start
    queue = []
    visited = {maze.start: None}
    old_goal = goal
    begin, end = 0.0, 0.0

    # поиск пути
    while True:
        # анимация
        sc.fill(pg.Color('black'))
        [[pg.draw.rect(sc, pg.Color('darkorange'), maze.get_rect(x, y), border_radius=tile // 5)
          for x, col in enumerate(row) if col] for y, row in enumerate(grid)]
        [pg.draw.rect(sc, pg.Color('forestgreen'), maze.get_rect(x, y)) for x, y in visited]
        if maze.algorithm_path == "dijkstra":
            [pg.draw.rect(sc, pg.Color('darkslategray'), maze.get_rect(x, y)) for x, y in queue]
        elif maze.algorithm_path == "a_star":
            [pg.draw.rect(sc, pg.Color('darkslategray'), maze.get_rect(*xy)) for _, xy in queue]

        # получение конечной клетки
        mouse_pos = maze.get_click_mouse_pos(sc)
        begin = time()
        if (mouse_pos and mouse_pos[0] < maze.cols and mouse_pos[1] < maze.rows and
                not grid[mouse_pos[1]][mouse_pos[0]]):
            # получение списка посещённых клеток и графа маршрутов
            if maze.algorithm_path == "dijkstra":
                queue, visited = dijkstra(maze.start, mouse_pos, graph)
            elif maze.algorithm_path == "a_star":
                queue, visited = a_star(maze.start, mouse_pos, graph)
            # установка цели
            goal = mouse_pos
        path_head, path_segment = goal, goal
        length_way = 0
        # отрисовка начала и конца пути
        pg.draw.rect(sc, pg.Color('blue'), maze.get_rect(*maze.start), tile, border_radius=tile // 3)
        pg.draw.rect(sc, pg.Color('magenta'), maze.get_rect(*path_head), tile, border_radius=tile // 3)
        # отрисовка кратчайшего маршрута при проходе по графу
        while path_segment and path_segment in visited:
            pg.draw.rect(sc, pg.Color('white'), maze.get_rect(*path_segment), tile, border_radius=tile // 3)
            path_segment = visited[path_segment]
            length_way += 1
        # обновление картинки только при изменении конечной точки
        if old_goal != goal:
            end = time() - begin
            old_goal = goal
            # with open("maze.txt", "at") as file:
            #     file.write(f"square {maze.algorithm_generation} {maze.algorithm_path} {maze.cols} {maze.rows} " +
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
