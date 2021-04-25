import ecm_linkers as ecl
import numpy as np
import pandas as pd
import argparse


# Мапа с размерами контейнеров, где ключ - имя файла (строка), значение - кортеж с размерностями
CONT_SIZES = {
    'test20.txt': (3, 4, 5, 7),
    'test50.txt': (10, 13, 15, 17),
    'test250.txt': (30, 45, 55, 70, 80),
    'test1000.txt': (100, 125, 175, 225),
    'test10000.txt': (2000, 2500, 3000),

    'test101.txt': (3, 4, 5, 7),
    'test777.txt': (3, 4, 5, 7, 11, 13, 17, 19, 23)
}


def set_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--in_filename', action='store', type=str,
                            help='Input filename with dataset')

    arguments = arg_parser.parse_args()

    return arguments


def main(arguments):
    elements_adj = pd.read_csv('data/' + arguments.in_filename, sep=',', header=None).values
    cont_sizes = CONT_SIZES[arguments.in_filename]

    # получение возможных компоновок контейнеров
    print("Computing container group combinations...")
    containers_groups = ecl.get_containers_by_elems(len(elements_adj), cont_sizes)

    # print("number of groups: ", len(containers_groups))
    # for group in containers_groups:
    #     print("group: ", group)
    # return
    best_q_comp = -1
    best_containers_adj = []
    best_containers = []
    best_cont_group = []

    print("Computing best composition...")
    # print("check len: ", len(containers_groups))
    for cont_group in containers_groups[:100]:
        tmp_containers_adj, tmp_containers = ecl.composition_linker(cont_group, elements_adj, optimise=False)
        tmp_q_comp = ecl.q_composition(tmp_containers_adj)

        if best_q_comp < 0 or tmp_q_comp < best_q_comp:
            best_q_comp = tmp_q_comp
            best_containers_adj = tmp_containers_adj
            best_containers = tmp_containers
            best_cont_group = cont_group

    print("Optimize best composition...")
    best_containers_adj, best_containers = ecl.composition_linker(best_cont_group, elements_adj, optimise=True)

    print("Containers adjacent matrix:\n", np.array(best_containers_adj))
    for container in best_containers:
        print("container: '{}' len = {}".format(container, len(container)))
    # print("containers structure: ", best_containers)
    print("containers: ", best_cont_group)

    print("Computing placement...")
    board_matrix = ecl.placement_linker(np.array(best_containers_adj))

    print("board matrix:\n", board_matrix)
    print("Q = ", ecl.q_placement(board_matrix, np.array(best_containers_adj)))

    # -----
    # mock часть для тестирования
    # mock_cont_adj = np.array([
    #     [0, 0, 0, 3, 0, 0, 2, 3, 0],
    #     [0, 0, 2, 0, 2, 0, 0, 0, 0],
    #     [0, 2, 0, 1, 0, 0, 0, 0, 0],
    #     [3, 0, 1, 0, 0, 5, 0, 0, 0],
    #     [0, 2, 0, 0, 0, 2, 0, 0, 4],
    #     [0, 0, 0, 5, 2, 0, 5, 0, 0],
    #     [2, 0, 0, 0, 0, 5, 0, 6, 2],
    #     [3, 0, 0, 0, 0, 0, 6, 0, 0],
    #     [0, 0, 0, 0, 4, 0, 2, 0, 0]
    # ])
    #
    # board_matrix = ecl.placement_linker(mock_cont_adj)


if __name__ == "__main__":
    args = set_args()
    main(args)
