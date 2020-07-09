import os
import sys
import time
import csv
import copy
import sqlite3
import itertools


def load_data(file_name):
    data_output = []
    file = open(file_name, "r")
    data = csv.reader(file)
    for row in data: data_output.append(row)
    file.close()

    for i in range(0, len(data_output)):
        for j in range(0, len(data_output[i])):
            data_output[i][j] = data_output[i][j].replace(",", "")

    header = data_output.pop(0)
    return header, data_output


def create_db(file_name, head_row, data_set):
    # Create Table using header
    header = '","'.join(head_row)
    header = '"' + header.replace(",", " VARCHAR(255), ") + '" INT'
    header = "CREATE TABLE IF NOT EXISTS " + file_name + "(" + header + ");"

    # Connect to sqlite db
    sqlite_conn = sqlite3.connect(os.getcwd() + os.sep + file_name + ".db")
    sqlite_cursor = sqlite_conn.cursor()
    sqlite_cursor.execute("DROP TABLE if EXISTS " + file_name + ";")
    sqlite_cursor.execute(header.lower())

    # Insert daata records into db
    for item in data_set:
        items = '"' + '","'.join(item) + '"'
        item_list = items.split(",")
        item_list[-1] = item_list[-1].replace('"', '')
        items = ", ".join(item_list)
        cmd = "INSERT INTO " + file_name + " VALUES(" + items + ");"
        sqlite_cursor.execute(cmd)

    sqlite_conn.commit()
    sqlite_conn.close()


def general_mapper(input_list):
    mapping_list = []

    # Generate Binary code combo for keys
    code_list = []
    for item in itertools.product([0, 1], repeat=len(input_list[0]) - 1):
        code_list.append(item)

    # Append the 0D Apex cuboid
    code_list.pop(0)
    apex_sum = 0.0
    for item in input_list: apex_sum = float(item[-1]) + apex_sum
    mapping_list.append(("*,*,*,*,*,*", apex_sum))

    # Generate all cuboids from 1 to n Dimension using binary code
    for keys in input_list:
        for code in code_list:
            key_value = []
            for i in range(0, len(code)):
                if code[i] == 1:
                    key_value.append(keys[i])
                else:
                    key_value.append('*')
            mapping_list.append((",".join(key_value), float(keys[-1])))

    return mapping_list


def reducer(input_pair):
    output = {}
    for key, value in input_pair:
        # Check if key exists in output dictionary
        if key not in output.keys():
            output[key] = value
        else:
            output[key] += value
    return output


def cube_sort(dimensions, output):
    # Sort cube base on the level of lattice
    result = {}
    for item in output:
        level = dimensions - item.count("*")
        if level + 1 not in result.keys():
            result[level + 1] = []
            result[level + 1].append(item)
        else:
            result[level + 1].append(item)

        print(item, output[item])

    return result


if __name__ == "__main__":
    file_name = "data"
    header, data = load_data(file_name + ".csv")
    create_db(file_name, header, data)

    mapping = general_mapper(data)
    output = reducer(mapping)
    cuboid = cube_sort(len(header) - 1, output)

    print("\n\nEOS\n\n")
