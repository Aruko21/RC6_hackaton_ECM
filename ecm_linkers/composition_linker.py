import random as rand
import sys

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
        ind = [k]
        for i in range(len(a[0])):
            if a[k][i] != 0:
                ind.append(i)
                
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
                
            if len(a) != 0:
                a_transp = transpouse(a)
                for i in ind:
                    del a_transp[i]
                a = transpouse(a_transp)
        return a, ind, index_new, index_start

    def fun1(a, b):
        index_start = list(range(0, len(a)))
        
        ind_new = [[0] for i in range(len(b))]
        ind = [[0] for i in range(len(b))]
        for i in range(len(b)):
            a, ind[i], ind_new[i], index_start = fun(a, b[i], index_start)
        return ind_new
    
    def analyze_delta_r(s, setsV):
        min_dim = len(setsV[0])
        vertic = []
        gorisont = setsV[:]

        for i in range(len(setsV)):
            if len(setsV[i]) <= min_dim:
                min_dim = len(setsV[i])
                vertic = setsV[i]
        if vertic in gorisont:
            gorisont.remove(vertic)
            gorisont = sum(gorisont, [])

        r = [[0 for j in range(len(gorisont))] for i in range(min_dim)]

        max_el = 0
        max_i = -1
        max_j = -1

        for i in range(min_dim):
            for j in range(len(gorisont)):
                sum_iqp = 0
                sum_jqp = 0
                sum_ipq = 0
                sum_jpq = 0
                for k in vertic:
                    sum_jqp += s[i][k]
                    sum_ipq += s[j][k]
                for k in setsV:
                    if gorisont[j] in k:
                        for n in k:
                            sum_iqp += s[i][n]
                            sum_jpq += s[j][n]
                        break

                r[i][j] = sum_iqp - sum_jqp + sum_ipq - sum_jpq - 2 * s[i][j]

                if r[i][j] > max_el:
                    max_el = r[i][j]
                    max_i = i
                    max_j = j
        return max_el, max_i, max_j
    
    def optimize(s_matr, setsV):
        opt_containers = []
        res = setsV[:]
        s = s_matr[:]

        while len(res) > 1:
            q_prev = sys.maxsize
            q_cur = sys.maxsize - 1
            while True:
                if q_prev <= q_cur:
                    break
                q_prev = q_cur
                _, q = q_composition(s, res)
                q_cur = q

                max_el, max_i, max_j = analyze_delta_r(s, res)
                if max_el <= 0:
                    break

                s[max_i], s[max_j] = s[max_j], s[max_i]
                for i in range(len(s)):
                    s[i][max_i], s[i][max_j] = s[i][max_j], s[i][max_i]
                ind = 0
                swap_i1 = -1
                swap_j1 = -1
                swap_i2 = -1
                swap_j2 = -1
                for i in range(len(res)):
                    for j in range(len(res[i])):
                        if ind == max_i:
                            swap_i1 = i
                            swap_j1 = j
                        if ind == max_j:
                            swap_i2 = i
                            swap_j2 = j
                        ind += 1
                res[swap_i1][swap_j1], res[swap_i2][swap_j2] = res[swap_i2][swap_j2], res[swap_i1][swap_j1]

            min_dim = len(res[0])
            rem_ind = -1
            for i in range(len(res)):
                if len(res[i]) <= min_dim:
                    min_dim = len(res[i])
                    rem_ind = i
            if res[rem_ind] in res:
                opt_containers.append(res[rem_ind])
                res.remove(res[rem_ind])
        opt_containers.append(res[0])

        return s, opt_containers
    
    a = adj_matrix[:]
    res_v = fun1(a, containers)
    opt_s, opt_containers = optimize(adj_matrix, res_v)
    containers_adj, q = q_composition(opt_s, opt_containers)

    # На выход - матрица смежностей контейнеров
    return containers_adj, q
