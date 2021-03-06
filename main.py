# Copyright 2021 Peter p.makretskii@gmail.com

from calculation.matrix_game import MatrixGame

# точка входа в программу
if __name__ == '__main__':
    file = open('input/input1.txt', 'r')
    matrix = [[float(val) for val in line.split()] for line in file]

    game = MatrixGame(matrix)
    game.solve()
