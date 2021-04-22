import ecm_linkers as ecl
import numpy as np
import pandas as pd
import argparse


# Мапа с размерами контейнеров, где ключ - размерность (строка), значение - кортеж с размерностями
CONT_SIZES = {
    '20': (3, 4, 5, 7),
    '50': (10, 13, 15, 17),
    '250': (30, 45, 55, 70, 80),
    '1000': (100, 125, 175, 225),
    '10000': (2000, 2500, 3000),

    '101': (3, 4, 5, 7),
    '777': (3, 4, 5, 7, 11, 13, 17, 19, 23)
}


def set_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--in_filename', action='store', type=str,
                            help='Input filename with dataset')
    arg_parser.add_argument('--cont_number', action='store', type=str,
                            help='Containers number')

    arguments = arg_parser.parse_args()

    return arguments


def main(arguments):
    elements_adj = pd.read_csv('data/' + arguments.in_filename, sep=',', header=None).values
    cont_sizes = CONT_SIZES[arguments.cont_number]

    # получение возможных компоновок контейнеров
    containers_groups = ecl.get_containers_by_elems(len(elements_adj), cont_sizes)

    best_q_comp = -1
    best_containers_adj = []

    for cont_group in containers_groups:
        tmp_containers_adj = ecl.composition_linker(cont_group, elements_adj)
        tmp_q_comp = ecl.q_composition(tmp_containers_adj)

        if best_q_comp < 0 or tmp_q_comp < best_q_comp:
            best_q_comp = tmp_q_comp
            best_containers_adj = tmp_containers_adj

    board_matrix = ecl.placement_linker(best_containers_adj)

    # -----
    # mock часть для тестирования
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

    board_matrix = ecl.placement_linker(mock_cont_adj)
    # Печать результатов ?


if __name__ == "__main__":
    args = set_args()
    main(args)
