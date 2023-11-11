import os
import sys
import time

n = 500

text = "ed vd_<N>\nnext"

for i in range(1, n):
    print(text.replace("<N>", str(i)))
