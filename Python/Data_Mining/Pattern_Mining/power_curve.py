# ----------------------------------------------------------------------
# DATE: 2020/07/10
# AUTHOR: Jerry Liu
# EMAIL: Liuyal@sfu.ca
#
# DESCRIPTION:
# Script for estimating power law distribution (power curve regression)
# and plotting aganist distribution values
# ----------------------------------------------------------------------
import os
import sys
import time
import datetime
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def load_csv_data(file_name):
    file = open(file_name, "r+", encoding="utf8")
    data_output = file.readlines()
    header = data_output.pop(0)
    file.close()
    return header, data_output


def estimate_coef(x, y):
    # number of observations/points
    n = np.size(x)
    # mean of x and y vector
    m_x, m_y = np.mean(x), np.mean(y)
    # calculating cross-deviation and deviation about x
    SS_xy = np.sum(y * x) - n * m_y * m_x
    SS_xx = np.sum(x * x) - n * m_x * m_x
    # calculating regression coefficients
    b_1 = SS_xy / SS_xx
    b_0 = m_y - b_1 * m_x

    return (b_0, b_1)


if __name__ == "__main__":
    print("START Time: " + datetime.datetime.now().strftime("%Y%m%d %H:%M:%S") + "\n")

    # Load length and support values for D1 and D2
    files = os.listdir(os.getcwd() + os.sep + "output_patterns")
    header_list = {}
    for file in files:
        header, data = load_csv_data(os.getcwd() + os.sep + "output_patterns" + os.sep + file)
        if file.split('_')[1] not in header_list.keys(): header_list[file.split('_')[1]] = []
        header_list[file.split('_')[1]].append((file.split('_')[2], header.replace('\n', '')))

    d1_x = []
    d1_y = []
    d2_x = []
    d2_y = []

    # parse value from dictionary
    for key in header_list:
        if "d1" in key:
            for length, support in header_list[key]:
                d1_x.append(int(''.join(filter(str.isdigit, length))))
                d1_y.append(int(support.split(',')[-1]))
        else:
            for length, support in header_list[key]:
                d2_x.append(int(''.join(filter(str.isdigit, length))))
                d2_y.append(int(support.split(',')[-1]))

    # Calculate log values for length(x) and support(y)
    d1_log_x = [math.log(y, 10) for y in d1_x]
    d1_log_y = [math.log(y, 10) for y in d1_y]
    d2_log_x = [math.log(y, 10) for y in d2_x]
    d2_log_y = [math.log(y, 10) for y in d2_y]

    # Calculate Linear regression coefficient on log values 
    a1, b1 = estimate_coef(np.array(d1_log_x), np.array(d1_log_y))
    a2, b2 = estimate_coef(np.array(d2_log_x), np.array(d2_log_y))

    # Create the vectors X and Y
    x = np.arange(start=0.1, stop=6, step=0.01)
    y1 = 10 ** a1 * x ** b1
    y2 = 10 ** a2 * x ** b2

    # Plot power curve fit results D1
    plt.xlim(0, 5)
    plt.ylim(0, 500)
    plt.scatter(d1_x, d1_y, color='red', label="D1 Distribution")
    plt.plot(x, y1, label="Best Power Curve Fit")
    plt.legend(loc="upper right")
    plt.show()

    # Plot power curve fit results D2
    plt.xlim(0, 5)
    plt.ylim(0, 5000)
    plt.scatter(d2_x, d2_y, color='red', label="D2 Distribution")
    plt.plot(x, y2, label="Best Power Curve Fit")
    plt.legend(loc="upper right")
    plt.show()

    print("END Time: " + datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"))
