# ----------------------------------------------------------------------
# DATE: 2020/06/10
# AUTHOR: Jerry Liu
# EMAIL: Liuyal@sfu.ca
#
# DESCRIPTION:
# Script for generating data cube base on csv data set
# And finding parent t and child t`pairs (t, t`) where t.sum >= 3xt`.sum
# ----------------------------------------------------------------------
import os
import sys
import time
import csv
import copy
import sqlite3
import itertools
import threading
import datetime
import shutil
import pandas as pd


def load_data(file_name):
    # open csv file and Read each row and append each column into list
    data_output = []
    file = open(file_name, "r")
    data = csv.reader(file)
    for row in data: data_output.append([s.replace(',', '') for s in row])
    file.close()

    return data_output


def create_db(file_name, data_set):
    # create sql query or adding table with correct type
    header = data_set.pop(0)
    header = [item.replace(' ', '_') for item in header]
    header = '"' + '","'.join(header) + '"'
    header = header.replace('",', '" VARCHAR(255), ') + " VARCHAR(255)"
    header = header.replace('"Gift_Amount" VARCHAR(255)', '"Gift_Amount" INT')
    header = "CREATE TABLE IF NOT EXISTS " + file_name + "(" + header + ");"

    # Create and connect to sqlite db file and crete table for data set
    sqlite_conn = sqlite3.connect(os.getcwd() + os.sep + file_name + ".db")
    sqlite_cursor = sqlite_conn.cursor()
    sqlite_cursor.execute("DROP TABLE if EXISTS " + file_name + ";")
    sqlite_cursor.execute(header.lower())

    # append data set into db table
    for item in data_set:
        item[5] = item[5].replace(",", " ")
        items = '"' + '","'.join(item) + '"'
        item_list = items.split(",")
        item_list[-1] = item_list[-1].replace('"', '')
        items = ", ".join(item_list)
        cmd = "INSERT INTO " + file_name + " VALUES(" + items + ");"
        sqlite_cursor.execute(cmd)

    sqlite_conn.commit()
    sqlite_conn.close()


def generate_key_structure(header, data_set):
    # Find all distinct values for each attribute and create data structure to store
    data = {}
    for item in header[0:-1]: data[item] = []
    for packet in data_set:
        for i in range(0, len(header) - 1):
            data[header[i]].append(packet[i])
    for item in header[0:-1]: data[item] = set(data[item])
    return data


def generate_cuboid_lattice(keys):
    # Load header/attributes into a list
    header = list(keys.keys())
    binary_code_mapping = {}
    mapping = {}

    # Initialize structure for binary code and lattice of cuboids
    for item in keys.keys():
        binary_code_mapping[list(keys.keys()).index(item)] = []
        mapping[list(keys.keys()).index(item)] = []
    binary_code_mapping[len(keys)] = []
    mapping[len(keys)] = []

    # Generate binary code base on length of header (dimension)
    binary_code_list = []
    for item in itertools.product([0, 1], repeat=len(keys)):
        binary_code_list.append(item)

    # Append binary code into mapping structure
    for item in binary_code_list:
        binary_code_mapping[sum(item)].append(item)

    # Match binary code with attributes to create lattice of cuboid
    attribute_list = []
    for level in binary_code_mapping:
        for code in binary_code_mapping[level]:
            new_code = []
            for i in range(0, len(code)):
                if code[i] == 0:
                    new_code.append('*')
                else:
                    new_code.append(header[i])
            attribute_list.append(",".join(new_code))

    # Append Levels for cuboids
    for item in attribute_list:
        index = len(keys) - item.count('*')
        mapping[index] = {}

    # Append attributes to each level
    for item in attribute_list:
        index = len(keys) - item.count('*')
        mapping[index][item] = []

    return mapping


def generate_records_sql(file_name, mapping):
    # Connect to db
    sqlite_conn = sqlite3.connect(os.getcwd() + os.sep + file_name + ".db")
    sqlite_cursor = sqlite_conn.cursor()
    queries = []
    cube = copy.deepcopy(mapping)

    for level in cube:
        for item in cube[level]:
            keyword_list = list(filter(len, item.replace("*", "").split(",")))
            # Generate query using attributes and run on db
            if len(keyword_list) == 0:
                sql_cmd = "SELECT sum(gift_amount) as total FROM " + file_name + ";"
            else:
                sql_cmd = "SELECT " + ",".join(keyword_list) + ", sum(gift_amount) as total FROM " + file_name + " GROUP by " + ",".join(keyword_list) + ";"
            # Save query and result to lattice of cuboid
            queries.append(sql_cmd)
            sqlite_cursor.execute(sql_cmd)
            cube[level][item] = sqlite_cursor.fetchall()

    sqlite_conn.close()
    return cube, queries


def generate_records(mapping, records, dimension):
    # Copy Cube structure and create data frame for queries
    cube = copy.deepcopy(mapping)
    df = pd.DataFrame(records, columns=dimension)
    df["Gift_Amount"] = df["Gift_Amount"].astype(float)

    for level in cube:
        for keys in cube[level]:
            attributes = list(filter(("*").__ne__, keys.split(",")))

            # Run query on data frame and extract tuple, value
            if len(attributes) != 0:
                query = df.groupby(attributes).sum()
                record = list(query.index)
                values = list(query.values)
                for i in range(0, len(query)):
                    
                    # Check if tuple of 1 or more
                    if not isinstance(record[i], tuple):
                        record_tuple = list((record[i],))
                    else:
                        record_tuple = list((record[i]))
                    record_tuple.append(values[i][0])
                    cube[level][keys].append(tuple(record_tuple))
            else:
                # For apex cube
                query = df["Gift_Amount"].sum()
                cube[level][keys].append((float(query),))

    return cube


def generate_data_cube(mapping):
    # Create copy of data cube for mapping attribute fields
    cube = copy.deepcopy(mapping)
    for level in cube:
        for node in cube[level]:
            cube[level][node] = []

    # Add * padding to generalized attribute fields
    for level in mapping:
        for node in mapping[level]:
            mask = node.split(",")
            for fields in mapping[level][node]:
                item = list(fields[0:-1])
                if len(item) > 0:
                    for mask_item in list(mask):
                        if "*" not in mask_item:
                            mask[mask.index(mask_item)] = item.pop(0)
                cube[level][node].append(",".join(mask) + "," + str(fields[-1]))

    return cube


def save_data_cube(file_name, folder_name, cube):
    # Create output folders if not exist
    if not os.path.exists(os.getcwd() + os.sep + "output_lattice"):
        os.makedirs(os.getcwd() + os.sep + "output_lattice")

    # Save each level of the lattice into a csv file
    for level in cube:
        file = open(os.getcwd() + os.sep + folder_name + os.sep + file_name + "_" + str(level) + ".csv", "a+")
        file.truncate(0)
        for aggro in cube[level]:
            file.write("\n".join(cube[level][aggro]) + "\n")
            file.flush()
        file.close()


def find_pc_pairs_threader(level, folder_name, min_sum, cube, pair):
    pairs = []
    start_time = time.time()
    # Check parent child pairs
    for parent_node in cube[pair[0]][pair[1]]:
        for child_node in cube[pair[2]][pair[3]]:

            # Check Apex cube
            if parent_node.count('*') == len(cube) - 1:
                parent_amount = float(parent_node.split(',')[-1])
                child_amount = float(child_node.split(',')[-1])
                if parent_amount >= level * child_amount:
                    pairs.append((parent_node, child_node))
            else:
                # Check non Apex cube
                is_parent_child = True
                p_set = parent_node.split(',')[0:-1]
                c_set = child_node.split(',')[0:-1]

                # Create dimension index tuple for matching
                check_list = []
                for p_set_item in p_set:
                    if p_set_item != "*":
                        check_list.append((p_set_item, p_set.index(p_set_item)))

                # Check child dimension index match parent
                for check_list_item, index in check_list:
                    c_set_item = c_set[index]
                    if check_list_item.lower() != c_set_item.lower():
                        is_parent_child = False

                # Pair is parent-child and t.sum >= 3 x t'.sum
                if is_parent_child:
                    parent_amount = float(parent_node.split(',')[-1])
                    child_amount = float(child_node.split(',')[-1])
                    if parent_amount >= min_sum * child_amount:
                        pairs.append((parent_node, child_node))

    # Save all pairings to csv file
    file = open(os.getcwd() + os.sep + folder_name + os.sep + "pair_" + str(level) + ".csv", "a+")
    file.truncate(0)
    for p, c in pairs:
        file.write(str(p) + ",," + str(c) + "\n")
    file.flush()
    file.close()

    # Show Thread run time
    delta_time = time.time() - start_time
    format_time = time.strftime("%H:%M:%S", time.gmtime(delta_time))
    sys.stdout.write("Thread " + str(level) + ": Complete in " + str(format_time) + "\n")


def find_pc_pairs(folder_name, cube, min_sum):
    # Create Threads for each pairing each level of the lattice cuboid
    thread_list = []
    pair_checks = {}
    pair_checks_list = []

    for level in range(0, len(cube) - 1):
        parent = cube[level]
        child = cube[level + 1]
        # Is Apex cuboid create all parent child pairs
        if len(parent) == 1 and list(parent.keys())[0].count('*') == 6:
            pair_checks[list(parent.keys())[0]] = []
            for children in child:
                pair_checks[list(parent.keys())[0]].append((level, list(parent.keys())[0], level + 1, children))
        else:
            for parent_node in parent:
                pair_checks[parent_node] = []
                for child_node in child:

                    # Check if parent and child have same dimension
                    parent_key_set = set(parent_node.replace('*,', '').split(','))
                    child_key_set = set(child_node.replace('*,', '').split(','))
                    pc_key_intersection = parent_key_set.intersection(child_key_set)

                    if len(pc_key_intersection) != 0:

                        # Check if parent and child have same dimension at same index
                        is_parent_child = True
                        p_set = parent_node.split(',')
                        c_set = child_node.split(',')
                        check_list = []

                        # Create dimension index tuple for matching
                        for p_set_item in p_set:
                            if p_set_item != "*":
                                check_list.append((p_set_item, p_set.index(p_set_item)))

                        # Check child dimension index match parent
                        for check_list_item, index in check_list:
                            c_set_item = c_set[index]
                            if check_list_item.lower() != c_set_item.lower():
                                is_parent_child = False

                        # Is child append pair to pair list
                        if is_parent_child:
                            pair_checks[parent_node].append((level, parent_node, level + 1, child_node))

    # Add records to each parent child dimension pairs
    for item in pair_checks.keys():
        for pair in pair_checks[item]:
            pair_checks_list.append(pair)

    # Create output folder
    if not os.path.exists(os.getcwd() + os.sep + folder_name):
        os.makedirs(os.getcwd() + os.sep + folder_name)
    else:
        shutil.rmtree(os.getcwd() + os.sep + folder_name)
        os.makedirs(os.getcwd() + os.sep + folder_name)

    # Threading to handle parent child pairing
    for i in range(0, len(pair_checks_list)):
        # find_pc_pairs_threader(i, folder_name, min_sum, cube, pair_checks_list[i])
        thread_list.append(threading.Thread(target=find_pc_pairs_threader, args=(i, folder_name, min_sum, cube, pair_checks_list[i])))
    [item.start() for item in thread_list]
    [item.join() for item in thread_list]


def find_pc_pairs_v2(folder_name, cube, dimension, min_sum):
    records = []
    pairs = []

    for level in cube:
        for keys in cube[level]:
            for item in cube[level][keys]:
                records.append(item.split(','))

    for item in records:
        if len(item) > 7: print(item)

    df = pd.DataFrame(records, columns=dimension)

    print(df)


def merge_pairs_csv(folder_name):
    # Read all inputs
    data = ""
    for csv_name in os.listdir(os.getcwd() + os.sep + folder_name):
        file = open(os.getcwd() + os.sep + folder_name + os.sep + csv_name, "r+")
        text = file.read()
        data = data + text
        file.close()

    # Write to final output csv
    data_list = data.split('\n')
    file = open(os.getcwd() + os.sep + folder_name + ".csv", "a+")
    file.truncate(0)
    file.write("\n".join(data_list))
    file.flush()
    file.close()

    return data_list


if __name__ == "__main__":
    # Load Data from csv file and extract the dimensions
    file_name = "cube"
    # create_db(file_name, load_data(file_name + ".csv"))
    data = load_data(file_name + ".csv")
    dimension = data.pop(0)

    print("START Time: " + datetime.datetime.now().strftime("%Y%m%d %H:%M:%S") + "\n")

    keys = generate_key_structure(dimension, data)
    cuboid_lattice = generate_cuboid_lattice(keys)
    # cuboid_lattice_complete, queries = generate_records_sql(file_name, cuboid_lattice)
    cuboid_lattice_complete = generate_records(cuboid_lattice, data, dimension)
    cube = generate_data_cube(cuboid_lattice_complete)
    save_data_cube(file_name, "output_lattice", cube)
    find_pc_pairs("output_pairs", cube, min_sum=3)
    # find_pc_pairs_v2("output_pairs_v2", cube, dimension, min_sum=3)
    pair_list = merge_pairs_csv("output_pairs")

    print("\nEND Time: " + datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"))
