import math
import os
import random
import re
import sys


# Complete the jumpingOnClouds function below.
def jumpingOnClouds(c, n):
    stack = []
    jump = 0
    for i in range(0, n):
        stack.append(c[i])
        if c[i] == 1:
            jump += 1
            stack = []
        if c[i] == 0:
            if len(stack) == 2:
                jump += 1
            elif len(stack) == 3:
                stack = [0]
                pass
            elif len(stack) >= 3:
                jump += 1
                stack = []
    return jump


if __name__ == '__main__':
    c = [0, 0, 1, 0, 0, 1, 0]
    c2 = [0, 0, 0, 1, 0, 0]
    c3 = [0, 0, 1, 0, 0, 0, 0, 1, 0, 0]

    result = jumpingOnClouds(c3, len(c3))

    print(result)
