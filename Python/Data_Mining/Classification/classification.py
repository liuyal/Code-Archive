import os
import sys
import time
import string
import pandas as pd




if __name__ == "__main__":

    attribute = list(string.ascii_lowercase)

    training_data_frame = pd.read_excel(os.getcwd() + os.sep + "CMPT459DataSetforStudents.xls", sheet_name="Training Data", header=None)
    test_data_frame = pd.read_excel(os.getcwd() + os.sep + "CMPT459DataSetforStudents.xls", sheet_name="Test data", header=None)

    training_data_attribute = attribute[0:training_data_frame.shape[1]]
    test_data_attribute = attribute[0:test_data_frame.shape[1]]

    training_data_frame.columns = training_data_attribute
    test_data_attribute.columns = test_data_attribute


    print(attribute)

