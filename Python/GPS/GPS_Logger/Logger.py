import os,time,sys, datetime
from multiprocessing import Process
import threading
from threading import Thread

def logger (file_id,list):
    for i in range(0, len(list)):
        file_id.write(list[i] + "\n")
        file_id.flush()
        print("Line: " + str(i) + " | Message: " + list[i])
        time.sleep(1)

data_file_path =  os.getcwd() + os.sep + "gps.txt"
output_path = os.getcwd() + os.sep + "output"

GGA_out = "GGA_ouput.txt"
GSA_out = "GSA_ouput.txt"
GSV_out = "GSV_ouput.txt"
GNS_out = "GNS_ouput.txt"
RMC_out = "RNC_ouput.txt"
PSRF_out = "PSRF_ouput.txt"

GGA_out_id = open(output_path + "\\" + GGA_out, "w"); GGA_out_id.truncate(0)
GSA_out_id = open(output_path + "\\" + GSA_out, "w"); GSA_out_id.truncate(0)
GSV_out_id = open(output_path + "\\" + GSV_out, "w"); GSV_out_id.truncate(0)
GNS_out_id = open(output_path + "\\" + GNS_out, "w"); GNS_out_id.truncate(0)
RMC_out_id = open(output_path + "\\" + RMC_out, "w"); GGA_out_id.truncate(0)
PSRF_out_id = open(output_path + "\\" + PSRF_out, "w"); PSRF_out_id.truncate(0)

file_id = open(data_file_path, "r")
gps_file = file_id.read().split("\n")

message_list = []
GGA_list = []; GSA_list = []; GSV_list = []
GNS_list = []; RMC_list = []; PSRF_list = []

for i in range(0, len(gps_file)):
    message = gps_file[i]
    message_list.append(message)
    if "GGA" in gps_file[i]: GGA_list.append(message)
    elif "GSA" in gps_file[i]: GSA_list.append(message)
    elif "GSV" in gps_file[i]: GSV_list.append(message)
    elif "GNS" in gps_file[i]: GNS_list.append(message)
    elif "RMC" in gps_file[i]: RMC_list.append(message)
    elif "PSRF" in gps_file[i]: PSRF_list.append(message)

sum = len(GGA_list) + len(GSA_list) + len(GSV_list) + len(GNS_list) + len(RMC_list) + len(PSRF_list)
print("File Length: \t\t" + str(len(message_list)) + "\n" + "List Sum Length: \t" + str(sum))

logger(GGA_out_id, GGA_list)