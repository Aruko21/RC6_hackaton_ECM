import numpy as np
import itertools


# Функционал, реализующий комбинаторные задачи

# На вход:
# n_elems - количество элементов
# capacities - tuple с возможными емкостями контейнеров
def get_containers_by_elems(n_elems, capacities):
    containers = []

    for m in range(1, n_elems):
        current_min_sum = capacities[0] * m
        current_max_sum = capacities[-1] * m
        if current_min_sum > n_elems or current_max_sum < n_elems:
            continue

        tmp_arr = [p for p in itertools.combinations_with_replacement(capacities, r=m) if sum(p) == n_elems]
        if tmp_arr:
            containers.append(tmp_arr)

    # На выход - list кортежей с перечислением контейнеров, где значение - емкость контейнера
    # Например, [(6, 7, 7), (2, 4, 7 ,7), ...]
    return containers


# def multiset_digit_combo(m, t):
#     """Returns a generator of digit lists.  The digit lists
#     returned are lexicographically sorted combinations of the
#     multiset specified by m[].  m[0] through m[9] indicate how
#     many of each digit is permitted in the output.  The argument
#     t indicates the total length of the output list.  The caller
#     must ensure that t <= m[0] + m[1] + ... + m[9]"""
#
#     # Track how many of each digit we're using.
#     count = [0] * 10
#
#     # Preallocate our output.
#     output = [0] * t
#
#     # Now increment our way through valid combinations.
#     backfill_to = t
#     reached_last_combo = False
#     while not reached_last_combo:
#         # Fill lower digits with the lexicographically lowest legal
#         # combination given our upper digits.  On the first iteration,
#         # this fills all digits.
#         d = 0
#         for i in range(0, backfill_to):
#             while count[d] >= m[d] and d < 9:
#                 d += 1
#             output[i] = d
#             count[d] += 1
#
#             # Output current solution in natural digit order.
#         revout = output[::-1]
#         yield revout
#
#         # Assume we'll run out.
#         reached_last_combo = True
#
#         # Try to increment our combination to the next lexical combo.
#         for i in range(0, t):
#             # Back the current digit out of the count.
#             count[output[i]] -= 1
#
#             # Try to increment the digit.
#             while output[i] + 1 <= 9:
#                 output[i] += 1
#                 if count[output[i]] < m[output[i]]:
#                     # Yes:  Keep the incremented digit, and remember where
#                     # we need to backfill to.
#                     count[output[i]] += 1
#                     backfill_to = i
#
#                     # Keep going...
#                     reached_last_combo = False
#                     break
#
#                     # Did we find one?  If so, break out of for loop also.
#             if not reached_last_combo:
#                 break
#
#
# if __name__ == '__main__':
#     containers_list_outer = [0, 1, 0, 1, 0, 1, 1, 0, 0, 0]
#     n = 20
#
#     for x in multiset_digit_combo(containers_list_outer, 10):
#         print(x)
#
#     print(get_containers_by_elems(n, containers_list_outer))
    # print(1)
