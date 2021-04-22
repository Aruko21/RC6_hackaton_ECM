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

    for i in range(n - 1):
        for j in range(i + 1, n):
            if containers_adj[i][j] != 0:
                q += containers_adj[i][j]
                containers_adj[j][i] = containers_adj[i][j]

    return q


# Целевая функция задачи размещения
def q_placement(board_matrix):
    q = 5
    return q
