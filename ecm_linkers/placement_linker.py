import numpy as np
from copy import deepcopy
from .analysis import get_links, q_placement

# Задача размещения

EPS = 1e-5


# Заполнение опорного решения оптимальным образом методом окаймляющих миноров
def get_base_placement(conts_order, board_matrix):
    # i = y; j = x
    y = board_matrix.shape[0]
    x = board_matrix.shape[1]

    minor_dim = 1
    curr_i = 0
    curr_j = 0
    board_matrix[0, 0] = conts_order[0]

    for elem in conts_order[1:]:
        if x > y and curr_j == x - 1:
            # If matrix is a rectangle - than just fill extra col as it is
            curr_i += 1
        elif curr_i == curr_j:
            minor_dim += 1
            curr_i = 0
            curr_j = minor_dim - 1
        elif curr_i > curr_j:
            # bottom left
            tmp_i = curr_i
            curr_i = curr_j + 1
            curr_j = tmp_i
        elif curr_j > curr_i:
            # top right
            tmp_i = curr_i
            curr_i = curr_j
            curr_j = tmp_i

        board_matrix[curr_i, curr_j] = elem


def get_board_dimensions(n_containers):
    board_size = int(np.sqrt(n_containers))

    dimensions = (0, 0)

    if np.power(board_size, 2) >= n_containers:
        dimensions = (board_size, board_size)
    elif board_size * (board_size + 1) >= n_containers:
        dimensions = (board_size, board_size + 1)
    elif np.power((board_size + 1), 2) >= n_containers:
        board_size = board_size + 1
        dimensions = (board_size, board_size)
    else:
        raise ValueError("Не удалось определить размерность платы")

    return dimensions


def get_base_order(adj_containers, ro_vector):
    n_containers = adj_containers.shape[0]

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

    return placed_elems


def get_max_l_criterion(board_matrix, adj_containers, ro_vector):
    n_containers = adj_containers.shape[0]

    l_param = np.zeros(n_containers, float)

    for i in range(board_matrix.shape[0]):
        for j in range(board_matrix.shape[1]):
            l_tmp = get_links(j, i, board_matrix, adj_containers)
            l_param[board_matrix[i, j] - 1] = l_tmp / ro_vector[board_matrix[i, j] - 1]

    # print("check L criterion: ", l_param)

    return np.argmax(l_param) + 1


def get_x_y_options(x, y, board_matrix, adj_containers, ro_vector):
    x_tmp = get_links(x, y, board_matrix, adj_containers, dimension="x")
    y_tmp = get_links(x, y, board_matrix, adj_containers, dimension="y")

    x_param = x_tmp / ro_vector[board_matrix[y, x] - 1]
    y_param = y_tmp / ro_vector[board_matrix[y, x] - 1]

    # print("check x: ", x_param)
    # print("check y: ", y_param)

    # Учет дробных вариантов характеристик + перевод в матричные индексы из координат x и y
    if (x_param - int(x_param)) > EPS:
        x_options = (int(x_param), int(x_param) + 1)
    else:
        x_options = (int(x_param),)

    if (y_param - int(y_param)) > EPS:
        y_reverse = int(y_param)
        y_options = (board_matrix.shape[0] - 1 - y_reverse, board_matrix.shape[0] - 1 - y_reverse - 1)
    else:
        y_reverse = int(y_param)
        y_options = (board_matrix.shape[0] - 1 - y_reverse,)

    return x_options, y_options


# На вход:
# adj_containers - матрица смежностей контейнеров
def placement_linker(adj_containers):
    n_containers = adj_containers.shape[0]

    dimensions = get_board_dimensions(n_containers)

    board_matrix = np.zeros(dimensions, int)
    ro_vector = np.zeros(n_containers, int)

    for i in range(0, n_containers):
        for j in range(0, n_containers):
            ro_vector[i] += adj_containers[i, j]

    placed_elems = get_base_order(adj_containers, ro_vector)

    get_base_placement(placed_elems, board_matrix)
    print("check base matrix:\n", board_matrix)

    best_q_place = q_placement(board_matrix, adj_containers)
    best_board = board_matrix
    previous_q_plase = best_q_place + 1

    while previous_q_plase > best_q_place:
        previous_q_plase = best_q_place
        cont_max = get_max_l_criterion(best_board, adj_containers, ro_vector)

        x_max_l = 0
        y_max_l = 0
        for i in range(best_board.shape[0]):
            for j in range(best_board.shape[1]):
                if best_board[i, j] == cont_max:
                    x_max_l = j
                    y_max_l = i
                    break

        x_options, y_options = get_x_y_options(x_max_l, y_max_l, best_board, adj_containers, ro_vector)

        for x_option in x_options:
            for y_option in y_options:
                new_board_matrix = deepcopy(best_board)

                cont_to_move = new_board_matrix[y_option, x_option]
                new_board_matrix[y_option, x_option] = best_board[y_max_l, x_max_l]
                new_board_matrix[y_max_l, x_max_l] = cont_to_move

                tmp_q_place = q_placement(new_board_matrix, adj_containers)
                print("tmp q: ", tmp_q_place)
                if tmp_q_place < best_q_place:
                    best_q_place = tmp_q_place
                    best_board = new_board_matrix

        print("best matrix:\n", best_board)
        print("Q: ", best_q_place)


    # На выход - матрица размешений.
    # Индексы - координаты. Значения - номер контейнера
    return best_board
