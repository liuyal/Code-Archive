import os, sys, time
import itertools


def frequency_counter(item_set, data_set, max_length):
    result = {}
    for tuple in item_set:
        if len(tuple) <= max_length:
            result[tuple] = 0
            for row in data_set:
                check_counter = 0
                for item in tuple:
                    if item in row: check_counter += 1
                if check_counter == len(tuple): result[tuple] += 1
            if result[tuple] == 0: result.pop(tuple, None)

    return result


def generate_item_set(T_set):
    item_set = []
    for i in range(1, len(T_set) + 1):
        R = list(itertools.combinations(list(T_set), i))
        item_set.append(R)
    item_set = list(itertools.chain.from_iterable(item_set))
    return item_set


if __name__ == "__main__":
    T = [["f", "a", "c", "d", "g", "l", "m", "p"],
         ["a", "b", "c", "f", "l", "m", "o"],
         ["b", "f", "h", "j", "o"],
         ["b", "c", "k", "s", "p"],
         ["a", "f", "c", "e", "l", "p", "m", "n"]]

    T_set = set(T[0] + T[1] + T[2] + T[3] + T[4])

    item_set = generate_item_set(T_set)
    max_length = max(len(x) for x in T)

    pattern_frequency = frequency_counter(item_set, T,  max_length)
    sorted_patterns = sorted(pattern_frequency.items(), key=lambda kv: kv[1], reverse=True)
    for tuple, value in sorted_patterns: print(", ".join(tuple), "\t", value)
