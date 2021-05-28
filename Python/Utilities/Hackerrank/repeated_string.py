import math
import os
import random
import re
import sys


def repeatedString(s, n):
    return int(n / len(s)) * s.count('a') + s[0:n - (int(n / len(s)) * len(s))].count('a')


if __name__ == '__main__':
    s = 'kmretasscityylpdhuwjirnqimlkcgxubxmsxpypgzxtenweirknjtasxtvxemtwxuarabssvqdnktqadhyktagjxoanknhgilnm'
    n = 736778906400
    result = repeatedString(s, n)

    result2 = repeatedString('aba', 10)
