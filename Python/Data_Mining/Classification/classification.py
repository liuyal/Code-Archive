import os
import sys
import time
import string
import statistics
import sqlite3
import operator
import pandas as pd
import numpy as np
from scipy.stats import entropy


def get_statistics(file_path, data_frame):
    file = open(file_path, "a+")
    file.truncate(0)
    file.write("attribute,max,min,mean,variance\n")
    result = {}
    for item in list(data_frame.columns):
        result[item] = {}
        data_list = data_frame[item]
        data_range = (max(data_list), min(data_list))
        mean = statistics.mean(data_list)
        variance = np.var(np.array(data_list))
        result[item]["range"] = data_range
        result[item]["mean"] = mean
        result[item]["variance"] = variance
        file.write(item + "," + str(data_range[0]) + "," + str(data_range[1]) + "," + str(mean) + "," + str(variance) + "\n")
    file.close()
    return result


def shannon_entropy(data):
    pd_series = pd.Series(data)
    counts = pd_series.value_counts()
    result = entropy(counts, base=2)
    print("Shannon Entropy:", result)
    return counts


def compute_fisher_score(counts, data_frame, stats, file_path):
    result = {}
    count_0 = float(counts[0])
    count_1 = float(counts[1])
    for item in list(data_frame.columns):
        class_0 = data_frame.loc[data_frame[data_frame.columns[-1]] == 0][item]
        mean_0 = statistics.mean(class_0)
        variance_0 = np.var(np.array(class_0))
        class_1 = data_frame.loc[data_frame[data_frame.columns[-1]] == 1][item]
        mean_1 = statistics.mean(class_1)
        variance_1 = np.var(np.array(class_1))
        u = float(stats[item]["mean"])
        s_top = count_0 * (mean_0 - u) * (mean_0 - u) + count_1 * (mean_1 - u) * (mean_1 - u)
        s_bottom = count_0 * variance_0 + count_1 * variance_1
        if item != data_frame.columns[-1]: result[item] = s_top / s_bottom
    sorted_result = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
    file = open(file_path, "a+")
    file.truncate(0)
    file.write("attribute,fisher_score\n")
    for item, value in sorted_result: file.write(str(item) + "," + str(value) + "\n")
    file.flush()
    file.close()
    return sorted_result


def df2db(db_name, table_name, df):
    db_connection = sqlite3.connect(db_name)
    df.to_sql(table_name, db_connection, if_exists='replace', index=False)


if __name__ == "__main__":
    attributes = list(string.ascii_lowercase)

    training_data_frame = pd.read_excel(os.getcwd() + os.sep + "CMPT459DataSetforStudents.xls", sheet_name="Training Data", header=None)
    test_data_frame = pd.read_excel(os.getcwd() + os.sep + "CMPT459DataSetforStudents.xls", sheet_name="Test data", header=None)

    training_data_frame.columns = attributes[0:training_data_frame.shape[1]]
    test_data_frame.columns = attributes[0:test_data_frame.shape[1]]

    training_data_stats = get_statistics(os.getcwd() + os.sep + "training_stats.csv", training_data_frame)
    test_data_stats = get_statistics(os.getcwd() + os.sep + "test_stats.csv", test_data_frame)

    df2db("data.db", "training_dataset", training_data_frame)
    df2db("data.db", "test_dataset", test_data_frame)

    counts = shannon_entropy(list(training_data_frame[attributes[0:training_data_frame.shape[1]][-1]]))

    score = compute_fisher_score(counts, training_data_frame, training_data_stats, os.getcwd() + os.sep + "training_fisher_score.csv")

    print("EOS")
