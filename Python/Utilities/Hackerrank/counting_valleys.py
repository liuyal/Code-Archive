import math
import os
import random
import re
import sys
import collections
from itertools import groupby

# Complete the sockMerchant function below.
def countingValleys(steps, path):
    count = 0
    arr = []
    arr.append(0)

    for item in path:
        if item == "U":
            count+= 1
        elif item == "D":
            count += -1
        arr.append(count)

    f = lambda x: x == 0
    result = [i for k, g in groupby(arr, f) for i in (g if k else (sum(g),))]
    r_count = 0

    for item in result:
        if item < 0:
            r_count+=1

    return r_count

if __name__ == '__main__':
    n = 8
    ar = ["U","D","D","D","U","D","U","U"]

    result = countingValleys(n, ar)

    print(result)
