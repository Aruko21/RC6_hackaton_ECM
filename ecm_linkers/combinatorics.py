# Функционал, реализующий комбинаторные задачи

# На вход:
# n_elems - количество элементов
# capacities - tuple с возможными емкостями контейнеров (должен быть отсортирован)
def get_containers_by_elems(n_elems, capacities):
    combination = Combination()

    containers = combination.combination_sum(capacities, n_elems)

    print('appropriate containers: ', containers)

    # На выход - list кортежей с перечислением контейнеров, где значение - емкость контейнера
    # Например, [(6, 7, 7), (2, 4, 7 ,7), ...]
    return containers


class Combination:
    def __init__(self):
        self.counter = 0
        self.result = []

    def combination_sum(self, candidates, target):
        self.find_combs([], candidates, target)
        return self.result

    def find_combs(self, temp, candidates, target):  # iteration function to find all solutions
        # if target >= 0:  # break the loop if target is smaller than 0
        for item in candidates:
            if item > target:  # break the loop if smallest item in candidates is greater than target
                break
            temp.append(item)  # append the item
            if item == target:
                if len(self.result) >= 1000000:
                    self.result.clear()

                self.result.append(tuple(temp.copy()))  # append the result
                self.counter += 1

                temp.pop()

                print('{} appropriate combinations'.format(self.counter))
                break
            else:
                index = candidates.index(item)
                self.find_combs(temp, candidates[index:], target - item)
            temp.pop()  # pop item in temp list


# if __name__ == '__main__':
#     candidates = (3, 4, 5, 7, 11, 13, 17, 19, 23)
#     n = 777
#
#     get_containers_by_elems(n, candidates)
