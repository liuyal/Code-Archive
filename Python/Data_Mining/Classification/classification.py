import os
import sys
import time
import string
import statistics
import scipy
import pandas as pd
import numpy as np
from scipy.stats import entropy


def get_statistics(file_path, data_frame):
    result = {}

    file = open(file_path, "a+")
    file.truncate(0)
    file.write("item,max,min,mean,variance\n")

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

def compute_fisher_score(counts, data_frame, stats):

    result = {}
    for item in list(data_frame.columns):



        attribute_mean = stats[item]["mean"]






        result[item] = 0

    return result


if __name__ == "__main__":
    attributes = list(string.ascii_lowercase)
    training_data_frame = pd.read_excel(os.getcwd() + os.sep + "CMPT459DataSetforStudents.xls", sheet_name="Training Data", header=None)
    test_data_frame = pd.read_excel(os.getcwd() + os.sep + "CMPT459DataSetforStudents.xls", sheet_name="Test data", header=None)
    training_data_frame.columns = attributes[0:training_data_frame.shape[1]]
    test_data_frame.columns = attributes[0:test_data_frame.shape[1]]

    training_data_stats = get_statistics(os.getcwd() + os.sep + "training_stats.csv", training_data_frame)
    test_data_stats = get_statistics(os.getcwd() + os.sep + "test_stats.csv", test_data_frame)

    counts = shannon_entropy(list(training_data_frame[attributes[0:training_data_frame.shape[1]][-1]]))

    score = compute_fisher_score(counts, training_data_frame, training_data_stats)


    print("EOS")
