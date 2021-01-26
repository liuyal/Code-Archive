import os
import sys
import time
import subprocess
import argparse
import colorama
import model_2048

if __name__ == "__main__":

    game = model_2048.Grid(4)
    game.run()

