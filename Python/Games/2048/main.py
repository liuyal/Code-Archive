import os
import sys
import time
import subprocess
import argparse
import colorama
import pytest
import TestSuite
import model_2048

if __name__ == "__main__":
    # testsuites = TestSuite.TestSuite(4)

    game = model_2048.Grid(4)
    game.run()

