# Copyright 2021 Peter p.makretskii@gmail.com

from copy import deepcopy as dc
import numpy as np


# класс "симплекс таблица"
class SimplexTable:
    def __init__(self, matrix, goal, letter='x'):
        # исходная матрица
        self.__matrix = np.transpose(np.array(matrix))
        # задача на минимум (True) или на максимум (False)
        self.__goal = goal
        # буквы, обозначающие переменные и целевую функцию
        self.__letter = letter

        # симплекс-таблица
        self.__table = (1 - 2 * self.__goal) * self.__matrix
        self.__table = np.concatenate(
            (np.array([(1 - 2 * self.__goal) for _ in range(len(self.__table))])[:, None], self.__table), axis=1)
        self.__table = np.vstack(
            [self.__table, np.array([0] + [(1 - 2 * self.__goal) for _ in range(len(self.__table[0]) - 1)])])

        # число отрицательных значений в столбце свободных членов
        self.__minus_count = len(self.__table[0]) + 1
        # список индексов свободных переменных
        self.__free = [i for i in range(1, len(self.__table[0]))]
        # список индексов базисных переменных
        self.__base = [len(self.__free) + i + 1 for i in range(len(self.__table) - 1)]

    # метод определяет, нужно оптимизировать решение или искать опорное
    def __status(self):
        s_minuses = [i[0] for i in self.__table[:-1] if i[0] < 0]  # минусы столбца свободных членов
        if s_minuses:
            # опорное решение не найдено
            if len(s_minuses) >= self.__minus_count:
                # решений нет
                return 4
            # запоминаем число отрицательных значений в столбце свободных членов
            self.__minus_count = len(s_minuses)
            return 0
        if max(self.__table[-1][1:]) > 0:
            # оптимальное решение не найдено
            return 1
        return 3

    # метод нахождения разрешающего столбца и строки для поиска оптимального решения
    def __find_pivot_optimise(self, flag):
        # flag - значение метода __status
        if flag == 1:
            # случай, когда надо искать оптимальное решение
            max_abs, support_column = -1, -1
            for i in range(1, len(self.__table[-1])):
                if self.__table[-1][i] > 0 and abs(self.__table[-1][i]) > max_abs:
                    max_abs = abs(self.__table[-1][i])
                    support_column = i
            min_div, support_row = 10 ** 8, -1
            for j in range(len(self.__table) - 1):
                if self.__table[j][support_column] > 0:
                    if abs(self.__table[j][0] / self.__table[j][support_column]) < min_div:
                        min_div = abs(self.__table[j][0] / self.__table[j][support_column])
                        support_row = j
        else:
            # случай, когда надо искать опорное решение
            max_abs, support_row = -1, -1
            for i in range(len(self.__table) - 1):
                if self.__table[i][0] < 0 and abs(self.__table[i][0]) >= max_abs:
                    max_abs = abs(self.__table[i][0])
                    support_row = i
            min_div, support_column = 10 ** 8, -1
            for j in range(1, len(self.__table[-1])):
                if self.__table[support_row][j] != 0:
                    if abs(self.__table[-1][j] / self.__table[support_row][j]) <= min_div:
                        min_div = abs(self.__table[-1][j] / self.__table[support_row][j])
                        support_column = j
        # печатаем результат
        print(f'Pivot column: {self.__letter[0]}{self.__free[support_column - 1]}\n'
              f'Pivot row: {self.__letter[0]}{self.__base[support_row]}\n'
              f'Pivot element: {self.__table[support_row][support_column]}\n\n')
        self.__free[support_column - 1], self.__base[support_row] = self.__base[support_row], self.__free[
            support_column - 1]
        return support_row, support_column

    # метод, осуществляющий алгоритм Жорданова исключения
    def __jordan_exception(self, pair_of_coord):
        support_row, support_column = pair_of_coord
        pivot = self.__table[support_row][support_column]
        simplex_table_iter = dc(self.__table)
        for i in range(len(simplex_table_iter)):  # rows
            for j in range(len(simplex_table_iter[0])):  # cols
                if i == support_row and j != support_column:
                    simplex_table_iter[i][j] = self.__table[i][j] / pivot
                elif i != support_row and j == support_column:
                    simplex_table_iter[i][j] = -self.__table[i][j] / pivot
                elif i == support_row and j == support_column:
                    simplex_table_iter[i][j] = 1 / pivot
                else:
                    simplex_table_iter[i][j] = self.__table[i][j] - (
                            self.__table[support_row][j] * self.__table[i][support_column]) / pivot
        return simplex_table_iter

    # метод, осуществляющий решение задачи
    def solve(self):
        iteration = 0
        while True:
            print(f'Iteration number {iteration}')
            iteration += 1
            print(self)
            status = self.__status()  # определяем, нужно оптимизировать или искать опорное решение
            if status != 2 and status != 3 and status != 4:
                self.__table = dc(self.__jordan_exception(self.__find_pivot_optimise(status)))
                continue
            elif status == 3:
                # задача решена
                count_vars = len(self.__free)
                output = []
                for i in range(1, count_vars + 1):  # собираем значения исходных переменных
                    if i in self.__base:
                        ind = self.__base.index(i)
                        output.append(self.__table[ind][0])
                    else:
                        output.append(0)
                return output, self.__table[-1][0]
            else:
                # решений нет
                return 'No solution'

    # метод печати симплекс-таблицы
    def __repr__(self):
        output = '\t\t\tC\t\t\t' + '\t\t\t'.join([f'{self.__letter[0]}{i}' for i in self.__free]) + '\n'
        rows = [f'{self.__letter[0]}{str(i)}' for i in self.__base] + [self.__letter[1]]
        for i in range(len(self.__table)):
            output += f'{rows[i]}\t\t' + \
                      ('%8.3f\t' * len(self.__table[i]) %
                       tuple(self.__table[i])) + '\n'
        return output
