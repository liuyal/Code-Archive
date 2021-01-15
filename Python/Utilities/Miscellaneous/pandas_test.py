import os, time, sys
import csv
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', 9999)

df = pd.read_csv("../Create_Data_CUBE/cube.csv")

state_sum = df.groupby("State").sum()
state_sum_values = state_sum.values

city_sum = df.groupby(["State", "City"]).sum()
city_sum_values = city_sum.values

college_sum = df.groupby(["State", "City", "College"]).sum()
college_sum_values = college_sum.values

total = state_sum_values.sum()

pd.reset_option('display.max_rows')

data = [state_sum_values, city_sum_values, college_sum_values]
fig7, ax7 = plt.subplots()
ax7.set_title('Multiple Samples with Different sizes')
ax7.boxplot(data)

plt.show()

