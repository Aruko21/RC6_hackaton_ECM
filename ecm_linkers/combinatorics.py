import numpy as np
import itertools


# Функционал, реализующий комбинаторные задачи

# На вход:
# n_elems - количество элементов
# capacities - list с возможными емкостями контейнеров
def get_containers_by_elems(n_elems, capacities):
    capacities.sort()
    res_array = []

    for m in range(1, n_elems):
        current_min_sum = capacities[0] * m
        current_max_sum = capacities[-1] * m
        if current_min_sum > n_elems or current_max_sum < n_elems:
            continue

        res_array.append([p for p in itertools.combinations_with_replacement(capacities, r=m)])

    containers = []
    for res_series in res_array:
        for res in res_series:
            if sum(res) == n_elems:
                containers.append(res)

    # На выход - list с перечислением контейнеров, где значение - емкость контейнера
    return containers


# if __name__ == '__main__':
#     containers_list_outer = [2, 4, 6, 7]
#     n = 20
#
#     print(get_containers_by_elems(n, containers_list_outer))
