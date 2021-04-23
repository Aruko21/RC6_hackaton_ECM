import numpy as np


# Вычисление целевых функций каждой задачи


# Целевая функция задачи компоновки
# Возвращает матрицу внешних связей контейнеров и их количество
# 
# На вход:
# adj_matrix - матица смежностей элементов
# containers_adj - массив контейнеров
def q_composition(containers_adj):
    q = 0
    n = len(containers_adj)

    # Вычисления производятся по верхне-треугольной матрице
    for i in range(n - 1):
        for j in range(i + 1, n):
            if containers_adj[i][j] != 0:
                q += containers_adj[i][j]

    return q


# Целевая функция задачи размещения
def q_placement(board_matrix, containers_adj):
    q = 0

    for y in range(board_matrix.shape[0]):
        for x in range(board_matrix.shape[1]):
            q += get_links(x, y, board_matrix, containers_adj)

    return q / 2.0


def get_links(x, y, board_matrix, containers_adj, dimension=None):
    container = board_matrix[y, x]
    links = 0

    for i in range(board_matrix.shape[0]):
        for j in range(board_matrix.shape[1]):
            if dimension == "x":
                placement_links = abs(j - x)
            elif dimension == "y":
                placement_links = abs(i - y)
            else:
                placement_links = abs(i - y) + abs(j - x)

            links += containers_adj[container - 1, board_matrix[i, j] - 1] * placement_links

    return links

