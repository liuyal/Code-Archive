import os
import sys
import time
import cv2
import numpy as np
import image_processes
import solve
import predict


def print_board(sudoku):
    for i in range(len(sudoku)):
        if i % 3 == 0:
            if i == 0:
                print(" ┎─────────┰─────────┰─────────┒")
            else:
                print(" ┠─────────╂─────────╂─────────┨")
        for j in range(len(sudoku[0])):
            if j % 3 == 0:
                print(" ┃ ", end=" ")
            if j == 8:
                print(sudoku[i][j] if sudoku[i][j] != 0 else ".", " ┃")
            else:
                print(sudoku[i][j] if sudoku[i][j] != 0 else ".", end=" ")
    print(" ┖─────────┸─────────┸─────────┚")


def display_image(img):
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    empty = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    td_2 = [[3, 6, 0, 0, 0, 5, 4, 0, 0],
            [2, 0, 0, 0, 4, 6, 0, 5, 0],
            [9, 4, 0, 0, 0, 0, 8, 0, 2],
            [0, 2, 0, 6, 1, 0, 0, 4, 0],
            [0, 0, 3, 0, 5, 0, 7, 0, 0],
            [0, 9, 0, 0, 7, 2, 0, 8, 0],
            [7, 0, 6, 0, 0, 0, 0, 1, 8],
            [0, 1, 0, 2, 8, 0, 0, 0, 6],
            [0, 0, 2, 1, 0, 0, 0, 7, 4]]

    board = [[7, 8, 0, 4, 0, 0, 1, 2, 0],
             [6, 0, 0, 0, 7, 5, 0, 0, 9],
             [0, 0, 0, 6, 0, 1, 0, 7, 8],
             [0, 0, 7, 0, 4, 0, 2, 6, 0],
             [0, 0, 1, 0, 5, 0, 9, 3, 0],
             [9, 0, 4, 0, 6, 0, 0, 0, 5],
             [0, 7, 0, 3, 0, 0, 0, 1, 2],
             [1, 2, 0, 0, 0, 7, 4, 0, 0],
             [0, 4, 9, 2, 0, 6, 0, 0, 7]]

    # solve.solve_board(board)
    # print_board(board)

    img = cv2.imread('1.png')
    image_grid = image_processes.extract(img)

    sudoku = predict.extract_number_image(image_grid)

    display_image(sudoku)

    # print_board(sudoku)
