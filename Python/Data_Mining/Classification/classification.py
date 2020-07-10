import os
import sys
import time
import string
import statistics
import sqlite3
import operator
import copy
import pandas as pd
import numpy as np
from scipy.stats import entropy
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import AdaBoostClassifier


def df2db(db_name, table_name, df):
    db_connection = sqlite3.connect(db_name)
    df.to_sql(table_name, db_connection, if_exists='replace', index=False)


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
    print("Shannon Entropy:", entropy(counts, base=2))
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


def decision_tree_k_fold(data_frame, k=10):
    copy_frame = copy.deepcopy(data_frame)
    x_data = copy_frame.drop(data_frame.columns[-1], axis=1)
    y_data = copy_frame[data_frame.columns[-1]]

    # x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.10)

    result_list = []
    for i in range(0, k):
        lower_bound = int(i * data_frame.shape[0] / k)
        upper_bound = int(i * data_frame.shape[0] / k + data_frame.shape[0] / k)
        x_data_test_subset = x_data[lower_bound:upper_bound]
        y_data_test_subset = y_data[lower_bound:upper_bound]
        x_data_train_subset = pd.concat([x_data[0:lower_bound], x_data[upper_bound:]])
        y_data_train_subset = pd.concat([y_data[0:lower_bound], y_data[upper_bound:]])

        classifier = DecisionTreeClassifier()
        classifier.fit(x_data_train_subset, y_data_train_subset)
        y_predicted = classifier.predict(x_data_test_subset)

        cm = confusion_matrix(y_data_test_subset, y_predicted)
        report = classification_report(y_data_test_subset, y_predicted, digits=4, output_dict=True)
        result_list.append(report)

        print("Round: " + str(i))
        print(cm)
        print(classification_report(y_data_test_subset, y_predicted, digits=4))

    return result_list


def adaptive_boost(data_frame, k=10):
    copy_frame = copy.deepcopy(data_frame)
    x_data = copy_frame.drop(data_frame.columns[-1], axis=1)
    y_data = copy_frame[data_frame.columns[-1]]

    result_list = []
    for i in range(0, k):
        lower_bound = int(i * data_frame.shape[0] / k)
        upper_bound = int(i * data_frame.shape[0] / k + data_frame.shape[0] / k)

        x_data_test_subset = x_data[lower_bound:upper_bound]
        y_data_test_subset = y_data[lower_bound:upper_bound]

        x_data_train_subset = pd.concat([x_data[0:lower_bound], x_data[upper_bound:]])
        y_data_train_subset = pd.concat([y_data[0:lower_bound], y_data[upper_bound:]])

        adaboost_classifier = AdaBoostClassifier(DecisionTreeClassifier(), n_estimators=50, learning_rate=1)
        adaboost_classifier.fit(x_data_train_subset, y_data_train_subset)
        y_predicted = adaboost_classifier.predict(x_data_test_subset)
        report = classification_report(y_data_test_subset, y_predicted, digits=4, output_dict=True)
        result_list.append(report)

        cm = confusion_matrix(y_data_test_subset, y_predicted)

        print("AdaBoost Round: " + str(i))
        print(cm)
        print(classification_report(y_data_test_subset, y_predicted, digits=4))

    return result_list


if __name__ == "__main__":
    attributes = list(string.ascii_lowercase)

    training_data_frame = pd.read_excel(os.getcwd() + os.sep + "CMPT459DataSetforStudents.xls", sheet_name="Training Data", header=None)
    # test_data_frame = pd.read_excel(os.getcwd() + os.sep + "CMPT459DataSetforStudents.xls", sheet_name="Test data", header=None)

    training_data_frame.columns = attributes[0:training_data_frame.shape[1]]
    # test_data_frame.columns = attributes[0:test_data_frame.shape[1]]

    # training_data_stats = get_statistics(os.getcwd() + os.sep + "training_stats.csv", training_data_frame)
    # test_data_stats = get_statistics(os.getcwd() + os.sep + "test_stats.csv", test_data_frame)
    #
    # df2db("data.db", "training_dataset", training_data_frame)
    # df2db("data.db", "test_dataset", test_data_frame)
    #
    # counts = shannon_entropy(list(training_data_frame[attributes[0:training_data_frame.shape[1]][-1]]))
    # score = compute_fisher_score(counts, training_data_frame, training_data_stats, os.getcwd() + os.sep + "training_fisher_score.csv")

    #TODO: add run time
    decision_tree_k_fold(training_data_frame, k=10)
    adaptive_boost(training_data_frame, k=10)

    print("EOS")
