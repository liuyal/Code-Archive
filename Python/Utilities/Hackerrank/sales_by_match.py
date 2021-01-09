import math
import os
import random
import re
import sys
import collections

# Complete the sockMerchant function below.
def sockMerchant(n, ar):
    sock_pairs = 0
    counter = collections.Counter(ar).items()
    for pair, count in counter:

        if count % 2 == 0:
            sock_pairs += count / 2
        elif (count - 1) % 2 == 0 and count != 1:
            sock_pairs += (count - 1) / 2

    return int(sock_pairs)


if __name__ == '__main__':
    n = 9
    ar = [10, 20, 20, 10, 10, 30, 50, 10, 20]

    result = sockMerchant(n, ar)

    print(result)
