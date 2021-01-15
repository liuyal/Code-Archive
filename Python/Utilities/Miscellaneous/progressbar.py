import time, sys, os
from tqdm import tqdm


def type_1():
    toolbar_width = 40
    # setup toolbar
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width + 1))  # return to start of line, after '['
    for _ in range(0, toolbar_width):
        time.sleep(0.1)  # do real work here
        # update the bar
        sys.stdout.write("-")
        sys.stdout.flush()
    sys.stdout.write("]\n")  # this ends the progress bar


def type_3():
    text = ""
    for char in tqdm(["a", "b", "c", "d"]):
        time.sleep(0.25)
        text = text + char


def type_4():
    pbar = tqdm(total=100)
    for _ in range(10):
        time.sleep(0.1)
        pbar.update(10)
    pbar.close()


if __name__ == "__main__":
    type_1()
    type_3()
    type_4()
