import os, sys, time, subprocess, shutil, re
from distutils.dir_util import copy_tree
import numpy as np

def auto_run():

    path = os.getcwd()
    synth_file = path + os.sep + "scripts" + os.sep + "synth.tcl"
    auto_result_folder = path + os.sep + "auto_result"
    
    start = 1.0
    end = 100.0
    step = 0.1
    unit = "MHz"
    run_range = np.arange(start, end, step)

    for i in run_range:
        period = float(1.00 / float(i) * 1000.00)
        print("Running: " + str(i) + unit + " (" + str('%.10f' % period) + "us)")

        o_file = open(synth_file, "r+")
        text = o_file.read()
        o_file.close()

        str_a = "-period"
        str_b = "{clk}"
        new_str = str_a + " " + str('%.10f' % period) + " -waveform {0 " + str('%.10f' % (period/2.0)) + "} " + str_b

        text_search = text[text.find(str_a):text.rfind(str_b) + len(str_b)]
        new_text = text.replace(text_search, new_str, 1)
        
        file = open(synth_file, "wt")
        file.truncate(0)
        file.write(new_text)
        file.flush()
        file.close()

        os.system("tcsh ./run.sh")

        time.sleep(2)
        os.rename("results", "results" + "_" + str(i) + unit)
        os.mkdir("results")
        time.sleep(2)

        #fromDirectory = os.getcwd() + os.sep + "results" + "_" + str(i) + unit
        #toDirectory = os.getcwd() + os.sep + "results"
        #copy_tree(fromDirectory, toDirectory)

        src = os.getcwd() + os.sep + "scripts" + os.sep + "synth.tcl"
        dst = os.getcwd() + os.sep + "results" + "_" + str(i) + unit + os.sep + "synth.tcl"
        shutil.copyfile(src, dst)

        src = os.getcwd() + os.sep + "results" + "_" + str(i) + unit
        dst = auto_result_folder
        shutil.move(src, dst)


def gen_results(folder_path):
    auto_result_folder = folder_path
    dir_list = os.listdir(auto_result_folder)
    dir_list.sort(key=lambda f: int(re.sub('\D', '', f)))
    report_list = []

    for folder in dir_list:
        if ("MHz" in folder or "kHz" in folder) and "_" in folder:
            files = os.listdir(auto_result_folder + os.sep + folder)
            for name in files:
                if ".rpt" in name:
                    file = auto_result_folder + os.sep + folder + os.sep + name
                    report_list.append(file)
                    break

    data = []
    header = "Period(ns), Freq(MHz), Area(um^2), Area(KGate), Leakage(uW), Dynamic(uW), Dynamic(uW/MHz), slack(ns)"
    print(header)

    for report in report_list:
        name = report
        name_list = name.split(os.sep)
        freq = 0.00
        for item in name_list:
            if "MHz" in item and "_" in item and "auto" not in item:
                freq = float((item.split("_")[-1]).replace("MHz",""))
            elif "kHz" in item and "_" in item and "auto" not in item:
                freq = float((item.split("_")[-1]).replace("kHz",""))/1000.0

        period = float(1.00 / float(freq) * 1000.00)

        o_report = open(report, "r+")
        text = o_report.readlines()
        o_report.close()

        total_area = ""
        dynamic = ""
        leakage = ""
        slack = ""
        dynamic_value = ""
        dynamic_unit = ""
        leakage_value = ""
        leakage_unit = ""

        for line in text:
            if "Total" in line and "references" in line:
                total_area = line.split(" ")[-1].replace("\n","")
            elif "Total Dynamic Power" in line:
                dynamic = line.split("=")[-1].split("(")[0].replace("\n","")
            elif "Cell Leakage Power" in line:
                leakage = line.split("=")[-1].replace("\n","")
            elif "slack (MET)" in line or "slack (VIOLATED)" in line:
                slack = line.replace("\n","").split(" ")[-1]

        total_area = total_area.replace(" ", "")
        dynamic_list = dynamic.split(" ")

        for item in dynamic_list:
            if "." in item:
                dynamic_value = item
            elif "W" in item:
                dynamic_unit = item

        leakage_list = leakage.split(" ")
        for item in leakage_list:
            if "." in item:
                leakage_value = item
            elif "W" in item:
                leakage_unit = item

        if dynamic_unit == "mW":
            dynamic_value = str(float(dynamic_value) * 1000.0)

        if leakage_unit == "mW":
            leakage_value = str(float(leakage_value) * 1000.0)

        # print("total_area: " + str(total_area))
        # print("KGate: " + str(float(total_area)/0.8/1000.0))
        # print("dynamic: " + str(dynamic_value) + " " + dynamic_unit)
        # print("leakage: " + str(leakage_value) + " " + leakage_unit)

        data_line = str('%.10f' % period) + "," + str(freq) + "," + str(total_area) + "," + str(float(total_area)/0.8/1000.0) + "," + str(leakage_value) + "," + str(dynamic_value) + ",," + str(slack)
        data.append(data_line)
        print(data_line)

    # w_file = open(folder_name+".txt" , "a+")
    # w_file.truncate(0)
    # w_file.write(header + "\n")
    # for line in data:
    #      w_file.write(line + "\n")
    # w_file.close()
    return data


def combine_data():
    data = []
    # folder = os.getcwd() + os.sep + "data_pre"
    folder = os.getcwd() + os.sep + "data_post"
    dir_list = os.listdir(folder)
    for item in dir_list:
        if os.path.isdir(folder + os.sep + item) and ".idea" != item:
            print("\n" + folder + os.sep + item)
            data.append(gen_results(folder + os.sep + item))

    arr = []
    for item in data:
        for line in item:
            arr.append(line.split(","))

    def swap(i, j):
        arr[i], arr[j] = arr[j], arr[i]

    n = len(arr)
    swapped = True
    x = -1
    while swapped:
        swapped = False
        x = x + 1
        for i in range(1, n - x):
            if float(arr[i - 1][1]) > float(arr[i][1]):
                swap(i - 1, i)
                swapped = True

    w_file = open(folder.split(os.sep)[-1] + ".txt", "a+")
    w_file.truncate(0)
    for line in arr:
        joined = ",".join(line)
        w_file.write(joined + "\n")
        print(joined)
    w_file.close()



if __name__ == "__main__":

    #auto_run()

    combine_data()


