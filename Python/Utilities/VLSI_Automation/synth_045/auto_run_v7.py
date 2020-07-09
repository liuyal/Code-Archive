import os, sys, time, shutil, re, threading, datetime, argparse, six, subprocess
from distutils.dir_util import copy_tree
import numpy as np


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def mt_run_range(thread_id, synth_template, auto_result_folder, run_range, debug=False):
    unit = "MHz"
    for i in run_range:
        period = float(1.00 / float(i) * 1000.00)
        sys.stdout.write("[" + str(thread_id) + "] Running: " + str(i) + unit + " (" + str('%.10f' % period) + "us)\n")
        new_results_folder = os.getcwd() + os.sep + "results" + "_" + str(i) + unit
        if not os.path.exists(new_results_folder): os.makedirs(new_results_folder)

        o_file = open(synth_template, "r+")
        text = o_file.read()
        o_file.close()
        str_a = "-period"
        str_b = "{clk}"
        new_str = str_a + " " + str('%.10f' % period) + " -waveform {0 " + str('%.10f' % (period / 2.0)) + "} " + str_b
        text_search = text[text.find(str_a):text.rfind(str_b) + len(str_b)]
        new_text = text.replace(text_search, new_str, 1)
        new_text2 = new_text.replace("results", "results" + "_" + str(i) + unit)
        new_text3 = new_text2.replace(".rpt", "." + str(i) + unit + ".rpt")  # ******
        new_syth_file = os.getcwd() + os.sep + "scripts" + os.sep + "synth_" + str(i) + unit + ".tcl"
        file = open(new_syth_file, "wt")
        file.truncate(0)
        file.write(new_text3)
        file.flush()
        file.close()

        run_text = "#!/bin/bash\nsource /etc/profile.d/ensc-cmc.csh\nsource /CMC/setups/CDS_setup.csh\nsource /CMC/setups/FE_setup.csh\ndc_shell-xg-t -f scripts/synth.tcl\necho \"done\"\n"
        new_run_file = os.getcwd() + os.sep + "run_" + str(i) + unit + ".sh"
        new_run_text = run_text.replace("synth", "synth_" + str(i) + unit, 1)
        file = open(new_run_file, "wt")
        file.truncate(0)
        file.write(new_run_text)
        file.flush()
        file.close()

        if debug == False:
            time.sleep(2)
            cmd = "tcsh ./" + "run_" + str(i) + unit + ".sh"
            os.system(cmd)
            # out, err = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
            time.sleep(2)
        else:
            # FOR TESTING
            # sys.stdout.write("\n!!!FAKE DC_SHELL!!!\n")
            fromDirectory = os.getcwd() + os.sep + "results_template"
            toDirectory = os.getcwd() + os.sep + "results" + "_" + str(i) + unit
            copy_tree(fromDirectory, toDirectory)
            os.rename(toDirectory + os.sep + "square_root.rpt", toDirectory + os.sep + "square_root." + str(i) + unit + ".rpt")

        src = new_syth_file
        dst = os.getcwd() + os.sep + "results" + "_" + str(i) + unit + os.sep + "synth_" + str(i) + unit + ".tcl"
        shutil.move(src, dst)

        src = new_run_file
        dst = os.getcwd() + os.sep + "results" + "_" + str(i) + unit + os.sep + "run_" + str(i) + unit + ".sh"
        shutil.move(src, dst)

        src = os.getcwd() + os.sep + "results" + "_" + str(i) + unit
        dst = auto_result_folder
        shutil.move(src, dst)


def clean_up():
    scripts_path = os.getcwd() + os.sep + "scripts"
    for item in os.listdir(scripts_path):
        if ".tcl" in item and "MHz" in item and "template" not in item:
            os.remove(scripts_path + os.sep + item)
    for item in os.listdir(os.getcwd()):
        if "run" in item and "MHz" in item and "_" in item and ".sh" in item:
            os.remove(os.getcwd() + os.sep + item)
        elif os.path.isdir(os.getcwd() + os.sep + item) and "MHz" in item and "_" in item:
            shutil.rmtree(os.getcwd() + os.sep + item)


def select_lib(synth_template_path):
    o_file = open(synth_template_path, "r+")
    text = o_file.read()
    o_file.close()
    path = "~/"
    lines = text.split("\n")
    lib_list = []
    for item in lines:
        if "set search_path" in item:
            path = item
            lib_list.append(item)
            print(bcolors.BOLD + bcolors.OKBLUE + "\nPath: " + item.split(" ")[-1] + "\n" + bcolors.ENDC)
        elif "set target_library" in item:
            lib_list.append(item)

    for i in range(0, len(lib_list)):
        if "library" in lib_list[i]:
            print("[" + str(i - 1) + "] " + lib_list[i].split(" ")[-1].replace('"', ''))

    try:
        index = six.moves.input(bcolors.BOLD + "\nSelect Library:" + bcolors.ENDC)
        val = int(index)
    except ValueError:
        sys.exit("Invalid input")

    lib = lib_list[val + 1].replace("#", "")
    file = lib.replace('"', '').split(" ")[-1]
    if not os.path.isfile(file):
        if not os.path.isfile(path + lib):
            sys.exit(file + " path not found")

    text2 = text.replace("#set target_library", "set target_library")
    text2 = text2.replace("set target_library", "#set target_library")
    text2 = text2.replace("#" + lib, lib)

    file = open(synth_template_path, "wt")
    file.truncate(0)
    file.write(text2)
    file.flush()
    file.close()

    set_lib = lib.split(" ")[-1].split("/")[-1].replace(".db", "").replace('"', '')
    print(bcolors.BOLD + "Running Library:  " + set_lib + "\n" + bcolors.ENDC)
    return set_lib


def distribution(run_array, n_threads, sort_arr=False):
    run_list = run_array.tolist()
    npt = int(len(run_array) / n_threads)
    arr = {}
    set_max = False
    for j in range(0, n_threads): arr[j] = []
    for i in range(0, npt):
        set_max = not set_max
        for j in range(0, n_threads):
            if set_max:
                max_value = run_list.pop(run_list.index(max(run_list)))
                arr[j].append(max_value)
            else:
                min_value = run_list.pop(run_list.index(min(run_list)))
                arr[j].append(min_value)
    if len(run_list) > 0:
        set_max = not set_max
        for j in range(0, n_threads):
            if set_max:
                max_value = run_list.pop(run_list.index(max(run_list)))
                arr[j].append(max_value)
            else:
                min_value = run_list.pop(run_list.index(min(run_list)))
                arr[j].append(min_value)
            if len(run_list) == 0: break
    if sort_arr:
        for j in range(0, n_threads): arr[j] = sorted(arr[j])
    return arr


def auto_run(threads, run_array, debug=False, library=""):
    clean_up()
    synth_template_path = os.getcwd() + os.sep + "scripts" + os.sep + "synth_template.tcl"

    if not os.path.exists(synth_template_path):
        sys.exit("[ERROR] Missing synth_template.tcl!")
    elif library == "":
        lib = select_lib(synth_template_path)
    elif library != "":
        lib = library

    results_folder_path = os.getcwd() + os.sep + "auto_results_" + lib.lower() + "_" + datetime.datetime.now().strftime("%y%m%d_%H%M%S")

    if not os.path.exists(results_folder_path):
        os.makedirs(results_folder_path)

    if not os.path.exists(os.getcwd() + os.sep + "work"):
        os.makedirs(os.getcwd() + os.sep + "work")

    if not os.path.exists(os.getcwd() + os.sep + "logs"):
        os.makedirs(os.getcwd() + os.sep + "logs")

    if not os.path.isfile(os.getcwd() + os.sep + ".synopsys_vss.setup"):
        os.system("cp /CMC/setups/ensc450/rgb2grayscale/syn_045/.synopsys_vss.setup .")

    if len(run_array) < threads: threads = len(run_array)

    # split_range = np.array_split(run_array, threads)
    split_range_even = distribution(run_array, threads)

    if threads == 1:
        mt_run_range(0, synth_template_path, results_folder_path, run_array, debug=debug)
    else:
        thread_list = []
        for i in range(0, threads):
            gen_thread = threading.Thread(target=mt_run_range, args=(i, synth_template_path, results_folder_path, split_range_even[i], debug))
            thread_list.append(gen_thread)
        for item in thread_list: item.start()
        for item in thread_list: item.join()

    return results_folder_path, lib


def gen_results(results_folder_path, verbose=True, csv=True):
    dir_list = os.listdir(results_folder_path)
    for item in dir_list:
        if not os.path.isdir(results_folder_path + os.sep + item):
            dir_list.remove(item)
    dir_list.sort(key=lambda f: int(re.sub('\D', '', f)))

    report_list = []
    rerun_list = []

    for folder in dir_list:
        if "MHz" in folder and "_" in folder:
            files = os.listdir(results_folder_path + os.sep + folder)
            found = False
            for name in files:
                if ".rpt" in name:
                    file = results_folder_path + os.sep + folder + os.sep + name
                    report_list.append(file)
                    found = True
                    break
            if found == False:
                rerun_list.append(folder.split("_")[-1])
                report_list.append(results_folder_path + os.sep + folder + os.sep + "missing")

    data = []
    library = ""
    header = "Period (ns), Freq (MHz), Area (um^2), Area (KGate), Leakage (uW), Dynamic (uW), Dynamic (uW/MHz), slack (ns), Critical Path (ns), OC, Library"
    if verbose: print("\n" + header)

    for report in report_list:
        try:
            name = report
            name_list = name.split(os.sep)
            freq = 0.00
            for item in name_list:
                if "MHz" in item and "_" in item and "auto" not in item and ".rpt" not in item:
                    freq = float((item.split("_")[-1]).replace("MHz", ""))
            period = float(1.00 / float(freq) * 1000.00)

            if name_list[-1] == "missing": raise Exception

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
            op_cond = ""
            rpt_period = ""
            crit = ""

            for line in text:
                if "Total" in line and "references" in line:
                    total_area = line.split(" ")[-1].replace("\n", "")
                elif "Total Dynamic Power" in line:
                    dynamic = line.split("=")[-1].split("(")[0].replace("\n", "")
                elif "Cell Leakage Power" in line:
                    leakage = line.split("=")[-1].replace("\n", "")
                elif "slack (MET)" in line or "slack (VIOLATED)" in line:
                    slack = line.replace("\n", "").split(" ")[-1]
                elif "Operating Conditions" in line and "Library" in line:
                    library = line.replace("\n", "").split(":")[-1]
                    op_cond = line.replace("\n", "").split(" ")[2]
                elif "clock CLK" in line and "(rise edge)" in line:
                    rpt_period = line.replace("\n", "").split(" ")[-1]
                elif "data arrival time" in line and "-" not in line:
                    crit = line.replace("\n", "").split(" ")[-1]

            if abs(float(rpt_period) - float(period)) > 0.1: rerun_list.append(str(freq) + "MHz")

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
            elif dynamic_unit == "nW":
                dynamic_value = str(float(dynamic_value) / 1000.0)
            elif dynamic_unit == "pW":
                dynamic_value = str(float(dynamic_value) / 1000.0 / 1000.0)

            if leakage_unit == "mW":
                leakage_value = str(float(leakage_value) * 1000.0)
            elif leakage_unit == "nW":
                leakage_value = str(float(leakage_value) / 1000.0)
            elif leakage_unit == "pW":
                leakage_value = str(float(leakage_value) / 1000.0 / 1000.0)

            data_line = str('%.10f' % period) + "," + str(freq) + "," + str(total_area) + ",," + str(leakage_value) + "," + str(dynamic_value) + ",," + str(slack) + "," + str(crit) + "," + op_cond + "," + library
            data.append(data_line)
            if verbose: print(data_line)
        except Exception as error:
            data_line = str('%.10f' % period) + "," + str(freq)
            data.append(data_line)
            rerun_list.append(str(freq) + "MHz")
            if verbose: print(data_line)

    if csv:
        w_file = open(results_folder_path + ".csv", "a+")
        w_file.truncate(0)
        w_file.write(header + "\n")
        for line in data:
            w_file.write(line + "\n")
        w_file.close()

    return data, library, rerun_list


def extract_rpt(results_folder_path):
    src_list = []
    dst_list = []

    extracted_folder = results_folder_path + "_rpt_extracted"
    if not os.path.exists(extracted_folder):
        os.makedirs(extracted_folder)

    dir_list = os.listdir(results_folder_path)
    for item in dir_list:
        data_file_list = os.listdir(results_folder_path + os.sep + item)
        for file in data_file_list:
            if ".rpt" in file:
                src_list.append(results_folder_path + os.sep + item + os.sep + file)
                dst_list.append(extracted_folder + os.sep + file)

    if len(src_list) != len(dst_list):
        sys.exit("ERROR")

    for i in range(0, len(src_list)):
        shutil.copy(src_list[i], dst_list[i])


def zip_results(results_folder_path, delete_results_folder=True):
    shutil.make_archive(results_folder_path.split(os.sep)[-1], 'zip', results_folder_path)
    if delete_results_folder:
        shutil.rmtree(results_folder_path)


def folder_selection():
    result_folders_list = os.listdir(os.getcwd())
    result_folders = []
    for item in result_folders_list:
        if (sys.argv[1] == "-g" or sys.argv[1] == "-x" or sys.argv[1] == "-e") and os.path.isdir(os.getcwd() + os.sep + item) and "auto_result" in item and "_extracted" not in item:
            result_folders.append(item)
        elif sys.argv[1] == "-z" and os.path.isdir(os.getcwd() + os.sep + item) and "auto_result" in item:
            result_folders.append(item)
        elif sys.argv[1] == "-p" and ".out" in item:
            result_folders.append(item)

    if len(result_folders) <= 0:
        sys.exit(bcolors.BOLD + bcolors.FAIL + "\nNO Files/Folders Found!" + bcolors.ENDC)
    elif len(result_folders) == 1:
        index = 0
    else:
        for i in range(0, len(result_folders)): print("[" + str(i) + "] " + result_folders[i])
        index = six.moves.input(bcolors.BOLD + "\nSelect Index:" + bcolors.ENDC)
    try:
        val = int(index)
    except ValueError:
        sys.exit("Invalid input")
    return result_folders[val]


# TODO: Create HTML plotter
def gen_html(folder_name):
    print(bcolors.BOLD + bcolors.FAIL + "GEN_HTML" + bcolors.ENDC)
    print(folder_name)


def combine_data(folder_name):
    data = {}
    folder = os.getcwd() + os.sep + folder_name
    dir_list = os.listdir(folder)
    for i in range(0, len(dir_list)):
        if os.path.isdir(folder + os.sep + dir_list[i]) and "auto_result" in dir_list[i] and ".idea" != dir_list[i] and "_extracted" not in dir_list[i]:
            print("\n" + folder + os.sep + dir_list[i])
            results, library, rerun_list = gen_results(folder + os.sep + dir_list[i], csv=False)
            if library not in data:
                data[library] = []
            data[library].append(results)

    for library in data:
        arr = []
        for item in data[library]:
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
        header = "Period (ns), Freq (MHz), Area (um^2), Area (KGate), Leakage (uW), Dynamic (uW), Dynamic (uW/MHz), slack (ns), Critical Path (ns), OC, Library"
        print("\n**Combined Data " + library + "**")
        print(header)
        w_file = open(os.getcwd() + os.sep + "combine_" + library + ".csv", "a+")
        w_file.truncate(0)
        w_file.write(header + "\n")
        for line in arr:
            joined = ",".join(line)
            w_file.write(joined + "\n")
            print(joined)
        w_file.close()


def parse_hspice(file):
    measure_key = []
    cells = []
    cell_key = ["inv ", "nor ", "nand ", "buf ", "or3 "]
    print(bcolors.BOLD + "\nLooking for cells: " + bcolors.OKBLUE + str("".join(cell_key)) + "\n" + bcolors.ENDC)

    o_file = open(file, "r+")
    text = o_file.read()
    o_file.close()

    lines = text.split("\n")
    for item in lines:
        for key in cell_key:
            if key in item and "xcell" not in item: cells.append(item[1:])
        if "meas_variable" in item and len(measure_key) < 4:
            measure_key.append(item.split("=")[-1].replace(" ", ""))

    cells = list(dict.fromkeys(cells))
    measure_key = list(dict.fromkeys(measure_key))
    gates = {}
    debug_values = []

    for item in cells:

        data = []
        index_number = []
        gate = item.split(" ")[0].lower()
        index_2 = re.sub(r'[a-z]+', '', item.split(" ")[1].lower(), re.I) + "fF"
        ds = item.split(" ")[2].lower()

        if gate + " " + ds not in gates: gates[gate + " " + ds] = {}
        for match in re.finditer(item.lower(), text):
            start = match.start() - 136
            end = match.end()
            index_number.append(start)
            index_number.append(end)

        section = text[min(index_number):max(index_number)].split("\n")

        for i in range(0, len(section)):
            if "parameter" in section[i] and "warning" not in section[i]: data.append("\n" + section[i])
            for cell in cells:
                if cell.lower() in section[i]: data.append(section[i])
            for key in measure_key:
                if key in section[i] and "parameter" not in section[i] and "meas_variable" not in section[i]: data.append(section[i])

        for i in range(0, len(data)):
            if "parameter" in data[i]:
                index_1 = ""
                t_time = data[i].split(" ")[-2]
                if t_time == "1.000E-09":
                    index_1 = "1ns"
                elif t_time == "2.000E-09":
                    index_1 = "2ns"
                gates[gate + " " + ds][index_1 + "," + index_2] = {}
                gates[gate + " " + ds][index_1 + "," + index_2][measure_key[0]] = data[i + 2].split(" ")[5]
                gates[gate + " " + ds][index_1 + "," + index_2][measure_key[1]] = data[i + 3].split(" ")[5]
                gates[gate + " " + ds][index_1 + "," + index_2][measure_key[2]] = data[i + 4].split(" ")[5]
                gates[gate + " " + ds][index_1 + "," + index_2][measure_key[3]] = data[i + 5].split(" ")[5]
            debug_values.append(data[i])

    x_1_2 = ""
    x_1_10 = ""
    x_2_2 = ""
    x_2_10 = ""
    final_values = []
    final_values.append("***********************************")

    for key in gates.keys():
        final_values.append("[" + key + "]\n")
        for act in measure_key:
            for item in gates[key]:
                if "1ns,2fF" in item:
                    if "E-10" in gates[key][item][act]:
                        x_1_2 = "0." + gates[key][item][act].split("E-10")[0].replace(".", "")
                    elif "E-11" in gates[key][item][act]:
                        x_1_2 = "0.0" + gates[key][item][act].split("E-11")[0].replace(".", "")
                elif "1ns,10fF" in item:
                    if "E-10" in gates[key][item][act]:
                        x_1_10 = "0." + gates[key][item][act].split("E-10")[0].replace(".", "")
                    elif "E-11" in gates[key][item][act]:
                        x_1_10 = "0.0" + gates[key][item][act].split("E-11")[0].replace(".", "")
                elif "2ns,2fF" in item:
                    if "E-10" in gates[key][item][act]:
                        x_2_2 = "0." + gates[key][item][act].split("E-10")[0].replace(".", "")
                    elif "E-11" in gates[key][item][act]:
                        x_2_2 = "0.0" + gates[key][item][act].split("E-11")[0].replace(".", "")
                elif "2ns,10fF" in item:
                    if "E-10" in gates[key][item][act]:
                        x_2_10 = "0." + gates[key][item][act].split("E-10")[0].replace(".", "")
                    elif "E-11" in gates[key][item][act]:
                        x_2_10 = "0.0" + gates[key][item][act].split("E-11")[0].replace(".", "")
            final_values.append(act)
            final_values.append('"' + x_1_2 + "," + x_1_10 + "\",\"" + x_2_2 + "," + x_2_10 + '"\n')
        final_values.append("***********************************")

    for i in range(0, len(debug_values)):
        for item in cells:
            if item in debug_values[i] and "trig" in debug_values[i - 1]:
                debug_values[i] = ""

    # for item in debug_values: print(item); print()
    for item in final_values: print(item)
    print(bcolors.BOLD + "\nFound Cells: " + bcolors.WARNING + str(", ".join(cells)) + bcolors.ENDC)

    w_file = open(os.getcwd() + os.sep + file.split(".")[0] + "_LUT_values.txt", "a+")
    w_file.truncate(0)
    for line in final_values:
        w_file.write(line + "\n")
    for line in debug_values:
        w_file.write(line + "\n")
    w_file.close()


if __name__ == "__main__":

    # TODO: Add more run info/error info/error checking, show result information at end of script
    # TODO: Add start, end, step, number of threads as possible input 
    #       option1:  -r  [0, 100, 1] [start, end, step]
    #       option2:  -r  prompt to enter 3 parameters
    # TODO: Add keyboard interrupt exception

    parser = argparse.ArgumentParser(description='', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-a', "--run", dest="auto_run", action='store_const', const=True, default=False, help='Automatically run synthesiser with dc_shell [DEFAULT]')
    try:
        if "-g" == sys.argv[1] or "-x" == sys.argv[1] or "-z" == sys.argv[1] or "-e" == sys.argv[1]:
            parser.add_argument('-g', "--gen", dest="gen", action='store', nargs="?", help='Generate CSV file from <PATH> >folder')
            parser.add_argument('-e', "--html", dest="html", action='store', nargs="?", help='Generate HTML plot from <PATH> folder')
            parser.add_argument('-x', "--extract", dest="extract", action='store', nargs="?", help='Extract .rpt files from <PATH> folder')
            parser.add_argument('-z', "--zip", dest="zip", action='store', nargs="?", help='Compress <PATH> folder into single zip folder')
        else:
            parser.add_argument('-g', "--gen", dest="gen", action='store_const', const=True, default=False, help='Generate CSV file from results folder')
            parser.add_argument('-e', "--html", dest="html", action='store_const', const=True, default=False, help='Generate HTML plot from results folder')
            parser.add_argument('-x', "--extract", dest="extract", action='store_const', const=True, default=False, help='Extract .rpt files from results folder')
            parser.add_argument('-z', "--zip", dest="zip", action='store_const', const=True, default=False, help='Compress results folder into single zip folder')
    except:
        parser.add_argument('-g', "--gen", dest="gen", action='store_const', const=True, default=False, help='Generate CSV file from results folder')
        parser.add_argument('-g', "--gen", dest="gen", action='store_const', const=True, default=False, help='Generate CSV file from results folder')
        parser.add_argument('-x', "--extract", dest="extract", action='store_const', const=True, default=False, help='Extract .rpt files from results folder')
        parser.add_argument('-z', "--zip", dest="zip", action='store_const', const=True, default=False, help='Compress results folder into single zip folder')
    parser.add_argument('-c', "--combine", dest="comb_path", action='store', nargs='?', const="." + os.sep, help='Combine results in folder: <PATH>')
    parser.add_argument('-p', "--parse", dest="hspice_file", action='store', nargs='?', help='Parse Hspice output file at: <PATH>')
    parser.add_argument('-d', "--debug", dest="debug", action='store_const', const=True, default=False, help='Debug Mode')
    input_arg = parser.parse_args()

    try:
        sys.argv[1]
    except:
        parser.print_help()
        sys.exit()

    if input_arg.auto_run:
        threads = 5
        start = 1.0
        end = 10.0
        step = 1.0
        run_array = np.arange(float(start), float(end + step), float(step))

        keep_running = True
        lib_name = ""
        while keep_running:

            results_folder, lib_name = auto_run(threads, run_array, debug=input_arg.debug, library=lib_name)
            data, library, rerun_list = gen_results(results_folder, verbose=False, csv=False)

            if len(rerun_list) > 0:
                rerun = ", ".join(list(dict.fromkeys(rerun_list))).replace("MHz", "")
                yes = six.moves.input("\n" + bcolors.FAIL + "FAILED" + bcolors.ENDC + " at Frequencies: [" + rerun + "]\nRerun? (y/n)")
                if "y" in yes.lower() or "yes" in yes.lower():
                    print("Rerunning Frequencies: [" + rerun + "]")
                    time.sleep(1)
                    run_array = np.asarray([float(x) for x in rerun.split(",")])
                else:
                    print()
                    keep_running = False
            else:
                keep_running = False

            if input_arg.gen: gen_results(results_folder)
            if input_arg.html: gen_html(results_folder)
            if input_arg.extract: extract_rpt(results_folder)
            if input_arg.zip: zip_results(results_folder)

    elif sys.argv[1] == "-g":
        if input_arg.gen == None:
            gen_results(folder_selection())
        else:
            gen_results(os.getcwd() + os.sep + input_arg.gen)
    elif sys.argv[1] == "-e":
        if input_arg.html == None:
            gen_html(folder_selection())
        else:
            gen_html(os.getcwd() + os.sep + input_arg.html)
    elif sys.argv[1] == "-x":
        if input_arg.extract == None:
            extract_rpt(folder_selection())
        else:
            extract_rpt(os.getcwd() + os.sep + input_arg.extract)
    elif sys.argv[1] == "-z":
        if input_arg.zip == None:
            zip_results(folder_selection())
        else:
            zip_results(os.getcwd() + os.sep + input_arg.zip)
    elif sys.argv[1] == "-p":
        if input_arg.hspice_file == None:
            parse_hspice(folder_selection())
        else:
            parse_hspice(input_arg.hspice_file)

    if input_arg.comb_path != None: combine_data(input_arg.comb_path)

    print(bcolors.BOLD + bcolors.OKGREEN + "\n[COMPLETE]" + bcolors.ENDC)
