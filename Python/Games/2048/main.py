import os
import sys
import time
import subprocess
import argparse
import colorama
import pytest
import model_2048

class model_tester():

    def __init__(self, size):
        self.game = model_2048.Grid(size)
        self.size = size

    def validate_values(self, row_index, column_index, value_array):
        print()

    def empty_grid(self):
        print()


if __name__ == "__main__":

    test = model_tester(4)
