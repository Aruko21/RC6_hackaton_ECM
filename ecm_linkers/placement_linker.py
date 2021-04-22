import numpy as np


# Задача размещения


def get_base_placement(conts_order, board_matrix):
    n = board_matrix.shape[0]
    m = board_matrix.shape[1]

    minor_dim = 1
    curr_i = 0
    curr_j = 0
    board_matrix[0, 0] = conts_order[0]

    # TODO: прямоугольные матрицы!!!
    for elem in conts_order[1:]:
        if curr_i == curr_j:
            minor_dim += 1
            curr_i = 0
            curr_j = minor_dim - 1
        elif curr_i > curr_j:
            # нижн. левый угол
            tmp_i = curr_i
            curr_i = curr_j + 1
            curr_j = tmp_i
        elif curr_j > curr_i:
            # верхн. правый угол
            tmp_i = curr_i
            curr_i = curr_j
            curr_j = tmp_i

        board_matrix[curr_i, curr_j] = elem


# На вход:
# adj_containers - матрица смжностей контейнеров
def placement_linker(adj_containers):
    n_containers = adj_containers.shape[0]

    board_size = int(np.sqrt(n_containers))

    cells_count = 0
    dimensions = (0, 0)

    if np.power(board_size, 2) >= n_containers:
        cells_count = np.power(board_size, 2)
        dimensions = (board_size, board_size)
    elif board_size * (board_size + 1) >= n_containers:
        cells_count = board_size * (board_size + 1)
        dimensions = (board_size, board_size + 1)
    elif np.power((board_size + 1), 2) >= n_containers:
        cells_count = np.power((board_size + 1), 2)
        board_size = board_size + 1
        dimensions = (board_size, board_size)
    else:
        raise ValueError("Не удалось определить разменость платы")

    board_matrix = np.zeros(dimensions, int)
    ro_vector = np.zeros(n_containers, int)

    for i in range(0, n_containers):
        for j in range(0, n_containers):
            ro_vector[i] += adj_containers[i, j]

    # Первым размещаем первый контейнер
    placed_elems = [1]

    while len(placed_elems) < n_containers:
        k_vector = np.full(n_containers, np.NaN, int)

        for i in range(0, n_containers):
            j_placed = 0

            for j in range(0, n_containers):
                if j + 1 in placed_elems:
                    j_placed += adj_containers[i, j]

            if i + 1 not in placed_elems:
                k_vector[i] = 2 * j_placed - ro_vector[i]

        k_max = np.max(k_vector)

        for i in range(0, n_containers):
            if k_vector[i] == k_max:
                placed_elems.append(i + 1)

    # for elem in placed_elems:

    get_base_placement(placed_elems, board_matrix)
    print("check base matrix: ", board_matrix)

    # q = 0
    #
    # for i in range(board_matrix.shape[0]):
    #     for j in range(board_matrix.shape[1]):
    #         fixed = board_matrix[i, j]
    #
    #         for m in range(board_matrix.shape[0]):
    #             for n in range(board_matrix.shape[1]):
    #                 q += adj_containers[fixed - 1, board_matrix[m, n] - 1] * (abs(i - m) + abs(j - n))
    #
    # return q / 2.0

    # board_matrix = np.array([
    #     [1, 3, 7],
    #     [4, 8, 6],
    #     [2, 5, 9]
    # ])

    l_param = np.zeros(n_containers, float)

    for i in range(board_matrix.shape[0]):
        for j in range(board_matrix.shape[1]):
            fixed = board_matrix[i, j]

            l_tmp = 0
            for m in range(board_matrix.shape[0]):
                for n in range(board_matrix.shape[1]):
                    l_tmp += adj_containers[fixed - 1, board_matrix[m, n] - 1] * (abs(i - m) + abs(j - n))

            l_param[board_matrix[i, j] - 1] = l_tmp / ro_vector[board_matrix[i, j] - 1]


    cont_max = np.argmax(l_param) + 1

    x_max_l = 0
    y_max_l = 0
    for i in range(board_matrix.shape[0]):
        for j in range(board_matrix.shape[1]):
            if board_matrix[i, j] == cont_max:
                x_max_l = j
                y_max_l = i
                break

    x_tmp = 0
    y_tmp = 0
    for i in range(board_matrix.shape[0]):
        for j in range(board_matrix.shape[1]):
            if j != x_max_l:
                x_tmp += adj_containers[cont_max - 1, board_matrix[i, j] - 1] * abs(x_max_l - j)
            if i != y_max_l:
                y_tmp += adj_containers[cont_max - 1, board_matrix[i, j] - 1] * abs(y_max_l - i)

    x_param = x_tmp / ro_vector[board_matrix[y_max_l, x_max_l] - 1]
    y_param = y_tmp / ro_vector[board_matrix[y_max_l, x_max_l] - 1]

    print("check x: ", x_param)
    print("check y: ", y_param)




    # На выход - матрица размешений.
    # Индексы - координаты. Значения - номер контейнера
    return board_matrix
