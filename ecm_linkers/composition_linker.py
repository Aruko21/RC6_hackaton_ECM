import random as rand
from copy import deepcopy
import numpy as np
import sys
from .analysis import q_composition

# Задача компоновки

# Функция для заполнения контейнера
# На вход:
# adj_matrix - матица смежностей элементов
# b - размерность конейнера
# indices - индексы матрицы смежностей, где отмечены (-1) обработанные элементы
def compose_container(adj_matrix, b, indices):
    indices_new = indices[:]

    # Вычисляются суммы по строкам, минимальная сумма и индекс минимальной суммы матрицы смежности
    sum_by_str = []
    min_sum_by_str = -1
    min_sum_ind = -1
    for i in range(len(adj_matrix)):
        sum_tmp = 0
        for j in range(len(adj_matrix[i])):
            if indices[j] < 0 or indices[i] < 0:
                continue
            sum_tmp += adj_matrix[i][j]
        sum_by_str.append(sum_tmp)

        if indices[i] < 0:
            continue
        if min_sum_by_str > sum_by_str[i] or min_sum_ind < 0:
            min_sum_by_str = sum_by_str[i]
            min_sum_ind = i

    # Контейнер заполняется элементами, смежными с элементом с минимальным количеством связей
    container = [min_sum_ind]
    indices_new[min_sum_ind] = -1
    for i in range(len(indices_new)):
        if indices_new[i] >= 0 and adj_matrix[min_sum_ind][i] > 0:
            container.append(i)
            indices_new[i] = -1

    # Если контейнер получился больше заданной размерности, то лишние элементы удаляются:
    while len(container) > b:
        max_delta = -1
        rem_ind = -1

        for i in container:
            tmp_sum = 0
            for j in container:
                tmp_sum += adj_matrix[i][j]

            delta = sum_by_str[i] - tmp_sum
            if max_delta < delta:
                max_delta = delta
                rem_ind = i

        container.remove(rem_ind)
        indices_new[rem_ind] = rem_ind

    # Если контейнер получился меньше заданной размерности, то он дополняется до требуемого размера
    while len(container) < b:
        for i in range(len(indices_new)):
            if indices_new[i] >= 0:
                container.append(indices_new[i])
                indices_new[i] = -1
                break

    # На выход - заполненный контейнер, индексы обработанных элементов
    return container, indices_new

# Функция для заполнения контейнеров
# На вход:
# adj_matrix - матица смежностей элементов
# b - размерность конейнеров
def compose_containers(adj_matrix, b):
    indices = list(range(0, len(adj_matrix)))
    containers = [[0] for i in range(len(b))]

    for i in range(len(b)):
        containers[i], indices = compose_container(adj_matrix, b[i], indices)

    # На выход - массив контейнеров
    return containers

# Функция для вычисления максимального элемента в матрице R
# На вход:
# s - матица смежностей элементов
# setsV - массив контейнеров
# ignored - индексы обработанных контейнеров
def analyze_delta_r(s, setsV, ignored):
    min_dim = len(s)
    min_ind = -1
    vertic = []
    gorisont = []

    # Нахождение контейнера с минимальной размерностью
    for i in range(len(setsV)):
        if i in ignored:
            continue
        gorisont.append(setsV[i])
        if len(setsV[i]) < min_dim:
            min_dim = len(setsV[i])
            min_ind = i

    # Размерности матрицы R
    vertic = setsV[min_ind]
    gorisont.remove(vertic)
    gorisont = sum(gorisont, [])

    max_el = 0
    max_i = -1
    max_j = -1

    for i in vertic:
        for j in gorisont:
            sum_iqp = 0
            sum_jqp = 0
            sum_ipq = 0
            sum_jpq = 0
            for k in vertic:
                sum_jqp += s[i][k]
                sum_ipq += s[j][k]
            for k in setsV:
                if j in k:
                    for n in k:
                        sum_iqp += s[i][n]
                        sum_jpq += s[j][n]
                    break

            r = sum_iqp - sum_jqp + sum_ipq - sum_jpq - 2 * s[i][j]

            if r > max_el:
                max_el = r
                max_i = i
                max_j = j

    # На выход - максимальный элемент матрицы R и его индексы
    return max_el, max_i, max_j

# Функция для оптимизации опорного решения (итерационный алгоритм)
# На вход:
# s_matr - матица смежностей элементов
# setsV - массив контейнеров
def optimize(s_matr, setsV):
    opt_containers = []

    indices = sum(setsV, [])
    len_setsV = [len(setV) for setV in setsV]
    ignored = []

    # Пока не обработаны все контейнеры
    while len(ignored) < len(len_setsV) - 1:
        q_prev = sys.maxsize
        q_cur = sys.maxsize - 1

        # Пока в матрице R максимальный элемент положительный, элементы тасуются между контейнерами
        while True:
            tmp = []

            if q_prev <= q_cur:
                break
            q_prev = q_cur

            tmp_ind = 0
            for i in range(len(len_setsV)):
                tmp.append(indices[tmp_ind:tmp_ind+len_setsV[i]])
                tmp_ind += len_setsV[i]

            containers_adj = compose_containers_adj(s_matr, tmp)
            q_cur = q_composition(containers_adj)

            max_el, max_i, max_j = analyze_delta_r(s_matr, tmp, ignored)
            if max_el <= 0:
                break

            indices[max_i], indices[max_j] = indices[max_j], indices[max_i]
        
        min_len = len(s_matr)
        min_ind = -1
        for i in range(len(len_setsV)):
            if i in ignored:
                continue
            if len_setsV[i] < min_len:
                min_len = len_setsV[i]
                min_ind = i
        ignored.append(min_ind)

    tmp_ind = 0
    for i in range(len(len_setsV)):
        opt_containers.append(indices[tmp_ind:tmp_ind+len_setsV[i]])
        tmp_ind += len_setsV[i]

    # На выход - массив улучшенных контейнеров
    return opt_containers

# Функция для вычисления матрицы смежности контейнеров
# На вход:
# adj_matrix - матица смежностей элементов
# containers - массив контейнеров
def compose_containers_adj(adj_matrix, containers):
    n = len(containers)
    external_rel_matrix = [[0 for j in range(n)] for i in range(n)]

    for i in range(n - 1):
        for j in range(i + 1, n):
            v1 = containers[i]
            v2 = containers[j]
            for h in v1:
                for d in v2:
                    if adj_matrix[h][d] != 0:
                        external_rel_matrix[i][j] += 1

            external_rel_matrix[j][i] = external_rel_matrix[i][j]

    # На выход - матрица смежностей контейнеров
    return external_rel_matrix


# На вход:
# containers - список возможных размерностей контейнеров
# adj_matrix - матица смежностей элементов
def composition_linker(container_capacities, adj_matrix, optimise=False):
    containers = compose_containers(adj_matrix.tolist(), container_capacities)

    if optimise:
        opt_containers = optimize(adj_matrix, containers)
        return compose_containers_adj(adj_matrix, opt_containers), opt_containers

    # На выход - матрица смежностей контейнеров
    return compose_containers_adj(adj_matrix, containers), containers
