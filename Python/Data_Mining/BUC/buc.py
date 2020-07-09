'''
Algorithm Description:

According to the given data set, the number of occurrences of tuples from 0 to the maximum dimension is recursively calculated.
If it is greater than or equal to min_sup, the result is added. If it is smaller than min_sup, the result is pruned.

For example, the data set is as follows:
a1,b1
a1,b2
a2,b1
a1,b2

Min_sup takes 2.

0 dimension to 1 dimension:
There are four tuples from the 0-1 dimension, a1, a2, b1, b2. The number of occurrences is a1:3, a2:1, b1:2, and b2:2.
Since a2 does not satisfy min_sup, pruning is performed and other tuples are added to the result.

1D to 2D:
The result from the 0-dimensional to 1-dimensional is: a1:3, b1:2, b2:2. So we expand on the basis of these three tuples,
making it from 1D to 2D, there will be: (a1, b1), (a1, b2), where (a1, b1) :1, (a1, b2): 2, so we have to pruning (a1, b1), (a1, b2) into the result.

So the end result is: a1, b1, b2, (a1, b2)
'''

import csv
import copy


# Read the data in csv
def load_data(file_name):
    data_output = []
    with open(file_name, "r", newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            data_output.append(row)

    return data_output


# : Determine if a contains b
def contain(a, b):
    flag = True
    for item in b:
        if item not in a:
            flag = False
            break

    return flag


# : Get the number of occurrences in data_set according to the input item
def get_times(input_item, data_set):
    times = 0
    for data in data_set:
        if contain(data, input_item):
            times = times + 1

    return times


# : Determine if a tuple is in a list
def item_in_list(item, input_list):
    for input in input_list:
        if set(item) == set(input):
            return True

    return False


# : Remove duplicate elements from each layer
def check_data(level_output):
    set_output = []
    for item in level_output:
        if not item_in_list(item, set_output):
            set_output.append(item)

    return set_output


# According to input_data, get a tuple containing a, dimension (a dimension +1 of a)
def get_data_by_input(data_set_item, a):
    # copy parameters
    data_set_item = copy.deepcopy(data_set_item)
    a = copy.deepcopy(a)
    output_data = []

    if contain(data_set_item, a):
        # Delete the data of a from input_data
        for item in a:
            data_set_item.remove(item)

        # Delete to add a dimension to a
        for data in data_set_item:
            output_item = copy.deepcopy(a)
            output_item.append(data)
            output_data.append(output_item)

    return output_data


# Get all tuples whose dimensions are dim and whose support is greater than min_sup, that is, a layer of elements whose dimensions are dim
def get_next_data_layer_by_min_sup(data_set, input_data, dim, min_sup):
    final_level_output = copy.deepcopy(input_data)

    if len(input_data) == 0 and dim == 1:
        # Process from 0 dimension to 1 dimension, that is, first obtain the tuple of dimension +1 according to the value corresponding to data_set, and then calculate the number of occurrences of it, greater than min_sup to join the output
        for b in range(len(data_set)):
            layer_data = get_data_by_input(data_set[b], [])
            for c in range(len(layer_data)):
                if get_times(layer_data[c], data_set) >= min_sup:
                    final_level_output.append(layer_data[c])
    else:
        # Process from n dimension to (n+1) dimension, that is, first obtain the tuple of dimension +1 according to the value corresponding to data_set, and then calculate the number of occurrences of it, greater than min_sup to join the output
        for a in range(len(input_data)):
            for b in range(len(data_set)):
                if len(input_data[a]) == dim - 1:
                    layer_data = get_data_by_input(data_set[b], input_data[a])
                    for c in range(len(layer_data)):
                        if get_times(layer_data[c], data_set) >= min_sup:
                            final_level_output.append(layer_data[c])

    final_level_output = check_data(final_level_output)
    return final_level_output


def buc(data_set, input_list, dim, min_sup):
    if dim < len(dimension):
        dim = dim + 1
        level_output = get_next_data_layer_by_min_sup(data_set, input_list, dim, min_sup)
        return buc(data_set, level_output, dim, min_sup)
    else:
        return input_list


if __name__ == "__main__":

    dimension = {"a", "b", "c", "d"}
    output = {}

    buc_data_set = load_data("data.csv")
    buc_output = buc(buc_data_set, [], 0, 1)

    for item in buc_output:
        print(str(",".join(item)) + ": " + str(get_times(item, buc_data_set)))
