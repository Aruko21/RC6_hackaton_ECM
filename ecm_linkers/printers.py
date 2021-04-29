# Функционал печати промежуточных и/или результирующих данных


def print_each_container_info(containers, adj_matrix):
    for m in range(len(containers)):
        container = containers[m]
        q = 0

        for i in range(len(container)):
            for j in range(len(container) - i):
                value = adj_matrix[container[i], container[j + i]]
                if value > 0:
                    q += value

        # print("q for V{} = {}".format(m, q))
        print("container V{}: '{}', len = {}, q = {}".format(m + 1, containers[m], len(containers[m]), q))
