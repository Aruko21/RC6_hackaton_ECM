import numpy as np

# Вычисление целевых функций каждой задачи


# Целевая функция задачи компоновки
# Возвращает матрицу внешних связей контейнеров и их количество
# 
# На вход:
# adj_matrix - матица смежностей элементов
# containers_adj - массив контейнеров
def q_composition(adj_matrix, containers_adj):
    n = len(containers_adj)
    external_rel_matrix = [[0 for j in range(n)] for i in range(n)]
    
    for i in range(n-1):
        for j in range(i+1, n):
            v1 = containers_adj[i]
            v2 = containers_adj[j]
            for h in v1:
                for d in v2:
                    if adj_matrix[h][d] != 0:
                        external_rel_matrix[i][j] += 1
    q = 0
    for i in range(n-1):
        for j in range(i+1, n):
            if external_rel_matrix[i][j] != 0:
                q += external_rel_matrix[i][j]
                external_rel_matrix[j][i] = external_rel_matrix[i][j]
    return external_rel_matrix, q

# Целевая функция задачи размещения
def q_placement(board_matrix):
    q = 5
    return q
