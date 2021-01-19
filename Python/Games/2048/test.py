import os
import sys
import time
import subprocess
import argparse
import colorama
import pytest
import model_2048

if __name__ == "__main__":
    size = 4
    game = model_2048.Grid(size)

    # game.nodes[0][0].value = 4
    # game.nodes[1][0].value = 2
    # game.nodes[2][0].value = 2

    game.print_grid()
    game.slide_nodes(1)
    game.print_grid()
