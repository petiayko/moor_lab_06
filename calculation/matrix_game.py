import numpy as np

from calculation.simplex_table import SimplexTable


# функция печати ответа на ЗЛП с заданными буквами
def print_answer(result, letters):
    if type(result) is tuple:
        print('The answer is:')
        for i in range(len(result[0])):
            print(f'{letters[0]}{i + 1} = {round(result[0][i], 3)}')
        print(f'{letters[1]} = {round(result[1], 3)}')
    else:
        print(result)


# класс матричной игры
class MatrixGame:
    # конструктор класса, на вход подается матрица стратегий
    def __init__(self, matrix):
        self.__matrix = matrix

    # метод поиска стратегии для игрока с именем name, на вход подаются буквы, которыми обозначаются переменные и тип
    # ЗЛП, которая будет поставлена в процессе, (максимум или минимум)
    def __find_strategy(self, name, goal, st_letters, ans_letters):
        print(f'To find the strategy of player {name}, compose a linear programming task and solve it:')
        player = SimplexTable(self.__matrix, goal, st_letters).solve()
        if type(player) is not tuple:
            print(f'There is no strategy for player {name}')
            return
        else:
            print_answer(player, st_letters)
            price = 1 / player[1]
            strategy = [i * price for i in player[0]]

            print(f'\nOptimal mixed strategy of player {name} is:\n{ans_letters[1]} = {round(price, 3)}')
            for i in range(len(strategy)):
                print(f'{ans_letters[0]}{i + 1} = {round(strategy[i], 3)}')
            print('\n')
            return price

    # метод решения задачи
    def solve(self):
        price_one = self.__find_strategy(name='A', goal=True, st_letters=('u', 'W'), ans_letters=('x', 'g'))
        self.__matrix = np.transpose(self.__matrix)
        price_two = self.__find_strategy(name='B', goal=False, st_letters=('v', 'Z'), ans_letters=('y', 'h'))
        print(f'h + g = {price_one + price_two}')
