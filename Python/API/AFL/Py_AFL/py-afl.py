#https://barro.github.io/2018/01/taking-a-look-at-python-afl/

import afl
import sys
import string

def step1(user):
    if len(user) > 6: step2(user)
def step2(user):
    if all(c in string.printable for c in user): step3(user)
def step3(user): 123 + user # should trigger an exception

if __name__ == "__main__":
    afl.init()
    step1(sys.stdin.read())
