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
from sklearn.ensemble import GradientBoostingClassifier


def df2db(db_name, table_name, df):
    db_connection = sqlite3.connect(db_name)
    df.to_sql(table_name, db_connection, if_exists='replace', index=False)


def get_statistics(data_frame, file_path):
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
    print(counts)
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


def average_report(report):

    total_precision_0 = 0.0
    total_recall_0 = 0.0
    total_precision_1 = 0.0
    total_recall_1 = 0.0

    for item in report:
        precision_0 = item[2]['0']['precision']
        recall_0 = item[2]['0']['recall']
        precision_1 = item[2]['1']['precision']
        recall_1 = item[2]['1']['recall']
        total_precision_0 = total_precision_0 + precision_0
        total_recall_0 = total_recall_0 + recall_0
        total_precision_1 = total_precision_1 + precision_1
        total_recall_1 = total_recall_1 + recall_1

    average_precision_0 = total_precision_0 / len(report)
    average_recall_0 = total_recall_0 / len(report)
    average_precision_1 = total_precision_1 / len(report)
    average_recall_1 = total_recall_1 / len(report)

    print("Class 0 Average Precision:", average_precision_0)
    print("Class 0 Average Recall:", average_recall_0)
    print("Class 1 Average Precision:", average_precision_1)
    print("Class 1 Average Recall:", average_recall_1)


def save_report(result_list, file_path):
    file = open(file_path, "a+")
    file.truncate(0)
    for i, cm, report in result_list:
        file.write("Round: " + str(i) + "\n")
        file.write(",".join([str(k) for k in cm.tolist()[0]]) + "\n")
        file.write(",".join([str(k) for k in cm.tolist()[1]]) + "\n")
        file.write("class,precision,recall,f1_score,support\n")
        for key in report:
            values = []
            values.append(str(key))
            if "accuracy" in key:
                values.append(",," + str(report[key]))
            else:
                for measure in report[key]:
                    values.append(str(report[key][measure]))
            file.write(",".join(values) + "\n")
            file.flush()
        file.write("\n")
    file.close()


def decision_tree_k_fold(training_data_frame, k=10):
    copy_frame = copy.deepcopy(training_data_frame)
    x_data = copy_frame.drop(training_data_frame.columns[-1], axis=1)
    y_data = copy_frame[training_data_frame.columns[-1]]
    # x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.10)
    result_list = []
    for i in range(0, k):
        lower_bound = int(i * training_data_frame.shape[0] / k)
        upper_bound = int(i * training_data_frame.shape[0] / k + training_data_frame.shape[0] / k)
        x_data_test_subset = x_data[lower_bound:upper_bound]
        y_data_test_subset = y_data[lower_bound:upper_bound]
        x_data_train_subset = pd.concat([x_data[0:lower_bound], x_data[upper_bound:]])
        y_data_train_subset = pd.concat([y_data[0:lower_bound], y_data[upper_bound:]])

        classifier = DecisionTreeClassifier()
        classifier.fit(x_data_train_subset, y_data_train_subset)
        y_predicted = classifier.predict(x_data_test_subset)

        cm = confusion_matrix(y_data_test_subset, y_predicted)
        report = classification_report(y_data_test_subset, y_predicted, digits=4, output_dict=True)
        result_list.append((i, cm, report))
        print("Round: " + str(i))
        print(cm)
        print(classification_report(y_data_test_subset, y_predicted, digits=4))
    return result_list


def adaboost_k_fold(training_data_frame, k=10):
    copy_frame = copy.deepcopy(training_data_frame)
    x_data = copy_frame.drop(training_data_frame.columns[-1], axis=1)
    y_data = copy_frame[training_data_frame.columns[-1]]
    result_list = []
    for i in range(0, k):
        lower_bound = int(i * training_data_frame.shape[0] / k)
        upper_bound = int(i * training_data_frame.shape[0] / k + training_data_frame.shape[0] / k)
        x_data_test_subset = x_data[lower_bound:upper_bound]
        y_data_test_subset = y_data[lower_bound:upper_bound]
        x_data_train_subset = pd.concat([x_data[0:lower_bound], x_data[upper_bound:]])
        y_data_train_subset = pd.concat([y_data[0:lower_bound], y_data[upper_bound:]])

        adaboost_classifier = AdaBoostClassifier(DecisionTreeClassifier(), n_estimators=50, learning_rate=0.5)
        adaboost_classifier.fit(x_data_train_subset, y_data_train_subset)
        y_predicted = adaboost_classifier.predict(x_data_test_subset)

        cm = confusion_matrix(y_data_test_subset, y_predicted)
        report = classification_report(y_data_test_subset, y_predicted, digits=4, output_dict=True)
        result_list.append((i, cm, report))
        print("AdaBoost Round: " + str(i))
        print(cm)
        print(classification_report(y_data_test_subset, y_predicted, digits=4))
    return result_list


def gradientBoost_k_fold(training_data_frame, k=10):
    copy_frame = copy.deepcopy(training_data_frame)
    x_data = copy_frame.drop(training_data_frame.columns[-1], axis=1)
    y_data = copy_frame[training_data_frame.columns[-1]]
    result_list = []
    for i in range(0, k):
        lower_bound = int(i * training_data_frame.shape[0] / k)
        upper_bound = int(i * training_data_frame.shape[0] / k + training_data_frame.shape[0] / k)
        x_data_test_subset = x_data[lower_bound:upper_bound]
        y_data_test_subset = y_data[lower_bound:upper_bound]
        x_data_train_subset = pd.concat([x_data[0:lower_bound], x_data[upper_bound:]])
        y_data_train_subset = pd.concat([y_data[0:lower_bound], y_data[upper_bound:]])

        gb_clf = GradientBoostingClassifier(n_estimators=200, learning_rate=0.5, max_features=2, max_depth=2, random_state=0)
        gb_clf.fit(x_data_train_subset, y_data_train_subset)
        y_predicted = gb_clf.predict(x_data_test_subset)

        cm = confusion_matrix(y_data_test_subset, y_predicted)
        report = classification_report(y_data_test_subset, y_predicted, digits=4, output_dict=True)
        result_list.append((i, cm, report))
        print("GradientBoost Round: " + str(i))
        print(cm)
        print(classification_report(y_data_test_subset, y_predicted, digits=4))
    return result_list


def dt_generate_final_data(training_data_frame, test_data_frame, save_path):
    copy_frame = copy.deepcopy(training_data_frame)
    x_train_data = copy_frame.drop(training_data_frame.columns[-1], axis=1)
    y_train_data = copy_frame[training_data_frame.columns[-1]]

    classifier = DecisionTreeClassifier()
    classifier.fit(x_train_data, y_train_data)
    y_predicted = classifier.predict(test_data_frame)

    file = open(save_path, "a+")
    file.truncate(0)
    file.write('\n'.join([str(i) for i in y_predicted.tolist()]))
    file.flush()
    file.close()


def adaboost_generate_final_data(training_data_frame, test_data_frame, save_path):
    copy_frame = copy.deepcopy(training_data_frame)
    x_train_data = copy_frame.drop(training_data_frame.columns[-1], axis=1)
    y_train_data = copy_frame[training_data_frame.columns[-1]]

    adaboost_classifier = AdaBoostClassifier(DecisionTreeClassifier(), n_estimators=50, learning_rate=0.5)
    adaboost_classifier.fit(x_train_data, y_train_data)
    y_predicted = adaboost_classifier.predict(test_data_frame)

    file = open(save_path, "a+")
    file.truncate(0)
    file.write('\n'.join([str(i) for i in y_predicted.tolist()]))
    file.flush()
    file.close()


def gradientBoost_generate_final_data(training_data_frame, test_data_frame, save_path):
    copy_frame = copy.deepcopy(training_data_frame)
    x_train_data = copy_frame.drop(training_data_frame.columns[-1], axis=1)
    y_train_data = copy_frame[training_data_frame.columns[-1]]

    gb_clf = GradientBoostingClassifier(n_estimators=200, learning_rate=0.5, max_features=2, max_depth=2, random_state=0)
    gb_clf.fit(x_train_data, y_train_data)
    y_predicted = gb_clf.predict(test_data_frame)

    file = open(save_path, "a+")
    file.truncate(0)
    file.write('\n'.join([str(i) for i in y_predicted.tolist()]))
    file.flush()
    file.close()


if __name__ == "__main__":
    training_data_frame = pd.read_excel(os.getcwd() + os.sep + "CMPT459DataSetforStudents.xls", sheet_name="Training Data", header=None)
    test_data_frame = pd.read_excel(os.getcwd() + os.sep + "CMPT459DataSetforStudents.xls", sheet_name="Test data", header=None)
    training_data_frame.columns = list(string.ascii_lowercase)[0:training_data_frame.shape[1]]
    test_data_frame.columns = list(string.ascii_lowercase)[0:test_data_frame.shape[1]]

    training_data_stats = get_statistics(training_data_frame, os.getcwd() + os.sep + "stats_training.csv")
    test_data_stats = get_statistics(test_data_frame, os.getcwd() + os.sep + "stats_test.csv")

    df2db("data.db", "training_dataset", training_data_frame)
    df2db("data.db", "test_dataset", test_data_frame)

    counts = shannon_entropy(list(training_data_frame[list(string.ascii_lowercase)[0:training_data_frame.shape[1]][-1]]))
    score = compute_fisher_score(counts, training_data_frame, training_data_stats, os.getcwd() + os.sep + "fisher_score_training.csv")

    dt_report = decision_tree_k_fold(training_data_frame, 10)
    average_report(dt_report)
    save_report(dt_report, os.getcwd() + os.sep + "report_dt.csv")

    adaboost_report = adaboost_k_fold(training_data_frame, 10)
    average_report(adaboost_report)
    save_report(adaboost_report, os.getcwd() + os.sep + "report_adaboost.csv")

    gb_report = gradientBoost_k_fold(training_data_frame, 10)
    average_report(gb_report)
    save_report(gb_report, os.getcwd() + os.sep + "report_gradientboost.csv")

    dt_generate_final_data(training_data_frame, test_data_frame, os.getcwd() + os.sep + "final_dt.csv")
    adaboost_generate_final_data(training_data_frame, test_data_frame, os.getcwd() + os.sep + "final_adaboost.csv")
    gradientBoost_generate_final_data(training_data_frame, test_data_frame, os.getcwd() + os.sep + "final_gradientboost.csv")

    print("EOS")
