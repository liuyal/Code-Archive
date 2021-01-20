import os
import sys
import time
import subprocess
import colorama
import pytest
import model_2048


class TestSuite():

    def __init__(self, size):
        self.game = model_2048.Grid(size)
        self.size = size

    def validate_values(self, row_index, column_index, value_array):
        print()

    def testcase_(self):
        self.game.empty_grid()
        self.game.nodes[0][0].value = 0
        self.game.nodes[1][0].value = 0
        self.game.nodes[2][0].value = 4
        self.game.nodes[3][0].value = 0

        self.game.nodes[0][1].value = 0
        self.game.nodes[1][1].value = 2
        self.game.nodes[2][1].value = 0
        self.game.nodes[3][1].value = 4

        self.game.nodes[0][2].value = 0
        self.game.nodes[1][2].value = 2
        self.game.nodes[2][2].value = 0
        self.game.nodes[3][2].value = 0

        self.game.nodes[0][3].value = 0
        self.game.nodes[1][3].value = 4
        self.game.nodes[2][3].value = 2
        self.game.nodes[3][3].value = 0

        self.game.print_grid()
        self.game.slide_nodes(3)
        self.game.print_grid()
        self.game.slide_nodes(3)
        self.game.print_grid()