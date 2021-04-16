import numpy as np
import random as rand


# Задача компоновки

# На вход:
# containers - список возможных размерностей контейнеров
# adj_matrix - матица смежностей элементов
def composition_linker(containers, adj_matrix):
    def transpouse(mat):
        matrix = []
        for i in range(len(mat[0])):
            matrix.append(list())
            for j in range(len(mat)):
                matrix[i].append(mat[j][i])
        return matrix

    def fun(a, b, index_start):
        c = [sum(i) for i in a]
        min_c = min(c)
        k = 0
        n = 0
        for i in c:
            if i == min_c:
                k = n
                break
            n += 1
        print(k)
        print(min_c)
        print(c)
        ind = [k]
        for i in range(len(a[1])):
            if a[k][i] != 0:
                ind.append(i)
        print("indexes   ", ind)
        sum_ind = sum(ind)
        dif_n = []    
        ind.sort(reverse=True)

        while len(ind) > b:
            sum_ind_str = []
            for i in range(len(a)):
                if i in ind:
                    s = 0
                    for j in ind:
                        s += a[i][j]
                    sum_ind_str.append(s)
            for i in range(len(ind)):
                dif_n.append(sum_ind - sum_ind_str[i])
            max_dif = max(dif_n)
            ind_remove = 0
            for i in range(len(dif_n)):
                if dif_n[i] == max_dif:
                    ind_remove = i
                    break
            ind.pop(ind_remove)

        ind.sort(reverse=True)
        index_new = []
        for i in ind:
            index_new.append(index_start[i])
        for i in ind:
            index_start.pop(i)

        while len(ind) < b:
            if len(index_start) != 0:
                ind_my = rand.randint(0, b - len(ind) - 1)
                ind.append(ind_my)
                index_new.append(index_start[ind_my])
                index_start.remove(index_start[ind_my])

        ind.sort(reverse=True)    
        if len(a) != 0:
            for i in ind:
                del a[i]
            print("del str", a)
            if len(a) != 0:
                a_transp = transpouse(a)
                for i in ind:
                    del a_transp[i]
                a = transpouse(a_transp)
        print(a)
        return a, ind, index_new, index_start

    def fun1(a, b):
        index_start = [1,2,3,4,5,6,7]
        ind_new = [[0] for i in range(len(b))]
        ind = [[0] for i in range(len(b))]
        for i in range(len(b)):
            a, ind[i], ind_new[i], index_start = fun(a, b[i], index_start)
        return ind_new

    def fun2(a, v, v_all):
        n = len(v)
        for i in range(n-1):
            for j in range(i+1, n):
                v1 = v_all[i]
                v2 = v_all[j]
                for h in v1:
                    for d in v2:
                        if a[h-1][d-1] != 0:
                            v[i][j] += 1
        q = 0
        for i in range(n-1):
            for j in range(i+1, n):
                if v[i][j] != 0:
                    q += v[i][j]
                    v[j][i] = v[i][j]
        return v, q

    a = adj_matrix[:]

    res_v = fun1(adj_matrix, containers)

    b = [[0,0,0],[0,0,0],[0,0,0]]
    containers_adj, q = fun2(a, b, res_v)

    # На выход - матрица смежностей контейнеров
    return containers_adj
