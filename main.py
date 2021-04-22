import ecm_linkers as ecl
# import pandas as pd
import numpy as np

CONT_SIZES = (2, 3, 4, 5)


def main():
    # TODO: обработка csv файла и получение матрицы смежности (формирование рандомно?)
    # elements_adj = np.array([
    #     [1, 2, 3],
    #     [4, 5, 6],
    #     [7, 8, 9]
    # ])
    #
    # # получение воможных компоновок контейнеров
    # containers_groups = []
    #
    # best_q_comp = -1
    # best_containers_adj = []
    #
    # for cont_group in containers_groups:
    #     tmp_containers_adj = ecl.composition_linker(cont_group, elements_adj)
    #     tmp_q_comp = ecl.q_composition(tmp_containers_adj)
    #
    #     if best_q_comp < 0 or tmp_q_comp < best_q_comp:
    #         best_q_comp = tmp_q_comp
    #         best_containers_adj = tmp_containers_adj
    #
    # board_matrix = ecl.placement_linker(best_containers_adj)

    mock_cont_adj = np.array([
        [0, 0, 0, 3, 0, 0, 2, 3, 0],
        [0, 0, 2, 0, 2, 0, 0, 0, 0],
        [0, 2, 0, 1, 0, 0, 0, 0, 0],
        [3, 0, 1, 0, 0, 5, 0, 0, 0],
        [0, 2, 0, 0, 0, 2, 0, 0, 4],
        [0, 0, 0, 5, 2, 0, 5, 0, 0],
        [2, 0, 0, 0, 0, 5, 0, 6, 2],
        [3, 0, 0, 0, 0, 0, 6, 0, 0],
        [0, 0, 0, 0, 4, 0, 2, 0, 0]
    ])

    # получение воможных компоновок контейнеров
    containers_groups = []

    best_q_comp = -1
    best_containers_adj = []

    for cont_group in containers_groups:
        tmp_containers_adj, tmp_q_comp = ecl.composition_linker(cont_group, elements_adj)

        if best_q_comp < 0 or tmp_q_comp < best_q_comp:
            best_q_comp = tmp_q_comp
            best_containers_adj = tmp_containers_adj
    board_matrix = ecl.placement_linker(mock_cont_adj)
    # Печать результатов ?


if __name__ == "__main__":
    main()
