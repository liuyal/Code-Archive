import os
import sys
import time
import subprocess
import threading
import copy
import random
import math
import numpy
import pynput


class Node():

    def __init__(self, id):
        self.id = id
        self.value = 0
        self.ptr_up = None
        self.ptr_down = None
        self.ptr_left = None
        self.ptr_right = None


class Grid():

    def __init__(self, n=4):
        self.size = n
        self.score = 0
        self.nodes = []
        self.index_up = 0
        self.index_down = 1
        self.index_left = 2
        self.index_right = 3
        self.setup_grid()

    def setup_grid(self, verbose=False):
        # Create rows of nodes
        id_counter = 0
        for i in range(0, self.size):
            node_list = []
            for j in range(0, self.size):
                new_node = Node(id_counter)
                node_list.append(new_node)
                id_counter += 1
            self.nodes.append(node_list)

        # Generate random Index for starting values
        start_indexes = random.sample(range(0, self.size * self.size - 1), math.ceil(self.size / 2))

        # Node linkage and value assignment
        for i in range(0, len(self.nodes)):
            current_row = self.nodes[i]
            if i == 0:
                previous_row = None
                next_row = self.nodes[i + 1]
            elif i == self.size - 1:
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
                elif j == self.size - 1:
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
        if verbose:
            self.print_grid()

    def new_node(self):
        done = False
        while not done:
            index = random.randrange(0, self.size * self.size - 1)
            for row in self.nodes:
                for item in row:
                    if item.id == index and item.value == 0:
                        item.value = numpy.random.choice([2, 4], p=[0.95, 0.05])
                        done = True

    def sum_nodes(self, node_values):
        value_list = list(filter((0).__ne__, node_values))
        for _ in range(0, self.size):
            value_list.append(0)
            for n in range(0, len(value_list) - 1):
                if value_list[n] == value_list[n + 1]:
                    value_list[n] += value_list[n + 1]
                    value_list[n + 1] = 0
                    self.score += value_list[n]
            value_list = list(filter((0).__ne__, value_list))
        value_list += [0] * (self.size - len(value_list))
        return value_list

    def slide_nodes(self, direction):
        if direction == self.index_up:
            for k in range(0, self.size, 1):
                stack = []
                for n in range(0, self.size, 1):
                    node = self.nodes[n][k]
                    stack.append(node.value)
                result = self.sum_nodes(stack)
                for n in range(0, self.size, 1):
                    self.nodes[n][k].value = result[n]
        elif direction == self.index_down:
            for k in range(0, self.size, 1):
                stack = []
                for n in range(self.size - 1, -1, -1):
                    node = self.nodes[n][k]
                    stack.append(node.value)
                result = self.sum_nodes(stack)
                result.reverse()
                for n in range(self.size - 1, -1, -1):
                    self.nodes[n][k].value = result[n]
        elif direction == self.index_left:
            for k in range(0, self.size, 1):
                stack = []
                node_list = self.nodes[k]
                for node in node_list:
                    stack.append(node.value)
                result = self.sum_nodes(stack)
                for n in range(0, self.size, 1):
                    self.nodes[k][n].value = result[n]
        elif direction == self.index_right:
            for k in range(0, self.size, 1):
                stack = []
                node_list = self.nodes[k]
                for node in node_list:
                    stack.insert(0, node.value)
                result = self.sum_nodes(stack)
                for n in range(0, self.size, 1):
                    self.nodes[k][n].value = result[-1 * n - 1]

    def empty_grid(self):
        for i in range(0, self.size):
            for j in range(0, self.size):
                self.nodes[i][j].value = 0

    def print_grid(self):
        for row in self.nodes:
            for item in row:
                print(item.value, end=" ")
            print()
        print("Score:", self.score, "\n")

    def on_press(self, key):
        try:
            old_grid = copy.deepcopy(self.nodes)
            if key == pynput.keyboard.Key.up:
                self.slide_nodes(self.index_up)
            if key == pynput.keyboard.Key.down:
                self.slide_nodes(self.index_down)
            if key == pynput.keyboard.Key.left:
                self.slide_nodes(self.index_left)
            if key == pynput.keyboard.Key.right:
                self.slide_nodes(self.index_right)
            if key == pynput.keyboard.Key.esc:
                return False

            for i in range(0, self.size):
                for j in range(0, self.size):
                    if old_grid[i][j].value != self.nodes[i][j].value:
                        self.new_node()
                        self.print_grid()
                        return True
            self.print_grid()

        except Exception as e:
            print(e)

    def on_release(self, key):
        print(end="")

    def run(self):
        with pynput.keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()
