import os
import sys
import time
import subprocess
import argparse
import colorama
import random
import math
import numpy
import pynput
import threading


class node():

    def __init__(self, id):
        self.id = id
        self.value = 0
        self.ptr_up = None
        self.ptr_down = None
        self.ptr_left = None
        self.ptr_right = None


class grid():

    def __init__(self, n=4):
        self.size = n
        self.score = 0
        self.nodes = []

        # Create rows of nodes
        id_counter = 0
        for i in range(0, n):
            node_list = []
            for j in range(0, n):
                new_node = node(id_counter)
                node_list.append(new_node)
                id_counter += 1
            self.nodes.append(node_list)

        # Generate random Index for starting values
        start_indexes = random.sample(range(0, size * size - 1), math.ceil(size / 2))

        # Node linkage and value assignment
        for i in range(0, len(self.nodes)):
            current_row = self.nodes[i]
            if i == 0:
                previous_row = None
                next_row = self.nodes[i + 1]
            elif i == n - 1:
                previous_row = self.nodes[i - 1]
                next_row = None
            else:
                previous_row = self.nodes[i - 1]
                next_row = self.nodes[i + 1]

            for j in range(0, len(current_row)):
                current_node = current_row[j]

                # Assign random values
                for index in start_indexes:
                    if index == current_node.id:
                        current_node.value = numpy.random.choice([2, 4], p=[0.85, 0.15])

                if j == 0:
                    previous_node = None
                    next_node = current_row[j + 1]
                elif j == n - 1:
                    previous_node = current_row[j - 1]
                    next_node = None
                else:
                    previous_node = current_row[j - 1]
                    next_node = current_row[j + 1]

                current_node.ptr_right = next_node
                current_node.ptr_left = previous_node

                if previous_row == None:
                    current_node.ptr_up = None
                else:
                    current_node.ptr_up = previous_row[j]
                if next_row == None:
                    current_node.ptr_down = None
                else:
                    current_node.ptr_down = next_row[j]

    def new_value(self):
        done = False
        while not done:
            index = random.randrange(0, self.size * self.size - 1)
            for row in self.nodes:
                for item in row:
                    if item.id == index and item.value == 0:
                        item.value = numpy.random.choice([2, 4], p=[0.95, 0.05])
                        done = True

    def print_grid(self):
        for row in self.nodes:
            for item in row:
                print(item.value, end=" ")
            print()

    def slide_values(self, direction):

        if direction == 1:

            for n in range(self.size-1, 0, -1):

                for k in range(0, self.size, 1):

                    current_row = self.nodes[n]


                    current_node = current_row[k]




    def on_press(self, key):
        try:
            if key == pynput.keyboard.Key.up:
                self.slide_values(0)
            if key == pynput.keyboard.Key.down:
                self.slide_values(1)
            if key == pynput.keyboard.Key.left:
                self.slide_values(2)
            if key == pynput.keyboard.Key.right:
                self.slide_values(3)
            if key == pynput.keyboard.Key.esc:
                return False
        except Exception as e:
            print(e)

    def on_release(self, key):
        print(end="")

    def run(self):
        with pynput.keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()


if __name__ == "__main__":
    size = 4
    game = grid(size)
    game.print_grid()

    game.slide_values(1)
    print()
    game.print_grid()

    # game.run()
