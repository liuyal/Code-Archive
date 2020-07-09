import os, sys, time, shutil, re, threading, datetime, argparse, six, subprocess
from distutils.dir_util import copy_tree
import numpy as np


def innovus_run_range(thread_id, auto_result_folder, sdc_template, floorplan_template, run_range, sweep="f"):
    for i in run_range:
        if sweep == "f":
            unit = "MHz"
            period = float(1.00 / float(i) * 1000.00)
            sys.stdout.write("[" + str(thread_id) + "] Running: " + str(i) + unit + " (" + str('%.10f' % period) + "us)\n")

            o_file = open(sdc_template, "r+")
            text = o_file.read()
            o_file.close()

            str_a = "-period"
            str_b = "}"
            new_str = str_a + " " + str('%.10f' % period) + " -waveform {0 " + str('%.10f' % (period / 2.0)) + str_b
            text_search = text[text.find(str_a):text.find(str_b) + len(str_b)]
            new_text = text.replace(text_search, new_str, 1)

            file = open(sdc_template, "wt")
            file.truncate(0)
            file.write(new_text)
            file.flush()
            file.close()
        else:
            density = float(i)
            period = 100.0
            unit = "%"
            i = str('%.2f' % (density * 100.0))
            sys.stdout.write("[" + str(thread_id) + "] Running Density: " + str('%.2f' % (density * 100.0)) + "%\n")

            o_file = open(sdc_template, "r+")
            text = o_file.read()
            o_file.close()

            str_a = "-period"
            str_b = "}"
            new_str = str_a + " " + str('%.10f' % period) + " -waveform {0 " + str('%.10f' % (period / 2.0)) + str_b
            text_search = text[text.find(str_a):text.find(str_b) + len(str_b)]
            new_text = text.replace(text_search, new_str, 1)

            file = open(sdc_template, "wt")
            file.truncate(0)
            file.write(new_text)
            file.flush()
            file.close()

            o_file = open(floorplan_template, "r+")
            text = o_file.read()
            o_file.close()

            ltc = ""
            for line in text.split("\n"):
                if "floorPlan" in line and "." in line and "#" not in line:
                    ltc = line

            text_list = ltc.split(" ")
            text_list[3] = str('%.2f' % density)
            new_str = " ".join(text_list)
            new_text = text.replace(ltc, new_str, 1)

            file = open(floorplan_template, "wt")
            file.truncate(0)
            file.write(new_text)
            file.flush()
            file.close()

        os.system("tcsh ./setup.csh")

        src = os.getcwd() + os.sep + "DBS"
        shutil.rmtree(src)
        os.mkdir(src)

        src = os.getcwd() + os.sep + "timingReports"
        # dst = auto_result_folder + os.sep + "results_" + str(i) + unit + os.sep + "timingReports"
        # shutil.move(src, dst)
        shutil.rmtree(src)
        os.mkdir(src)

        src = os.getcwd() + os.sep + "results"
        dst = auto_result_folder + os.sep + "results_" + str(i) + unit + os.sep + "results"
        shutil.move(src, dst)
        os.mkdir(src)

        src = os.getcwd() + os.sep + "inputs"
        dst = auto_result_folder + os.sep + "results_" + str(i) + unit + os.sep + "inputs"
        copy_tree(src, dst)

        src = os.getcwd() + os.sep + "scripts"
        dst = auto_result_folder + os.sep + "results_" + str(i) + unit + os.sep + "scripts"
        copy_tree(src, dst)

        cleanup()


def gen_innous_data(results_folder_path, verbose=True, csv=True):
    results_data = {}
    rerun_list = []
    folder_list = os.listdir(results_folder_path)
    folder_list.sort(key=lambda f: int(re.sub('\D', '', f)))
    for folder in folder_list:
        if "MHz" in folder and "_" in folder:
            files = os.listdir(results_folder_path + os.sep + folder)
            results_data[folder] = {}
            results_data[folder]["sdc"] = []
            # report_list[folder]["tcl"] = []
            if "inputs" in files and "results" in files:

                inputs = os.listdir(results_folder_path + os.sep + folder + os.sep + "inputs")
                sdc_file = [results_folder_path + os.sep + folder + os.sep + "inputs" + os.sep + s for s in inputs if ".sdc" in s]
                results_data[folder]["sdc"] = sdc_file

                # scripts = os.listdir(results_folder_path + os.sep + folder + os.sep + "scripts")
                # powerplan_file = [results_folder_path + os.sep + folder + os.sep + "scripts" + os.sep + s for s in inputs if ".tcl" in s]
                # report_list[folder]["inputs"]["tcl"] = powerplan_file

                results_folder = os.listdir(results_folder_path + os.sep + folder + os.sep + "results")
                timing_folder = os.listdir(results_folder_path + os.sep + folder + os.sep + "results" + os.sep + "timing")
                summary_folder = os.listdir(results_folder_path + os.sep + folder + os.sep + "results" + os.sep + "summary")

                ctsrpt_file = [results_folder_path + os.sep + folder + os.sep + "results" + os.sep + s for s in results_folder if ".ctsrpt" in s]
                cpu_file = [results_folder_path + os.sep + folder + os.sep + "results" + os.sep + s for s in results_folder if "CPU" in s and ".txt" in s]
                hold_file = [results_folder_path + os.sep + folder + os.sep + "results" + os.sep + "timing" + os.sep + s for s in timing_folder if ".rpt" in s and "hold" in s]
                setup_file = [results_folder_path + os.sep + folder + os.sep + "results" + os.sep + "timing" + os.sep + s for s in timing_folder if ".rpt" in s and "setup" in s]
                summary_file = [results_folder_path + os.sep + folder + os.sep + "results" + os.sep + "summary" + os.sep + s for s in summary_folder if ".rpt" in s]

                results_data[folder]["ctsrpt"] = ctsrpt_file
                results_data[folder]["tcpu"] = cpu_file
                results_data[folder]["rpt"] = summary_file
                results_data[folder]["timing_hold"] = hold_file
                results_data[folder]["timing_setup"] = setup_file
            else:
                rerun_list.append(results_folder_path + os.sep + folder)
                del results_data[folder]

    for key in list(results_data):
        for item in results_data[key]:
            for file in results_data[key][item]:
                try:
                    o_file = open(file, "r+")
                    text = o_file.read()
                    o_file.close()
                    if len(text) == 0: raise Exception
                except:
                    rerun_list.append(results_folder_path + os.sep + key)
                    del results_data[key]
                    break

    cts_header = "Period (ns),Freq (MHz),CPU Run Time(ms),Max Skew (ps),Rise Delay (ps),Fall Delay (ps),Levels,Buffers,FF (Sinks)"
    fp_header = "Standard Cell Area (um^2),Standard Cell Area (Subtracting Physical Cells) (um^2),Core Area (um^2),Chip Area (um^2)"
    density_header = "Pure Gate Density #1 (Subtracting BLOCKAGES),Pure Gate Density #2 (Subtracting BLOCKAGES and Physical Cells),Pure Gate Density #3 (Subtracting MACROS),Pure Gate Density #4 (Subtracting MACROS and Physical Cells),Pure Gate Density #5 (Subtracting MACROS and BLOCKAGES),Pure Gate Density #6 (Subtracting MACROS and BLOCKAGES for insts are not placed)"
    density_header_2 = "Core Density (Counting Std Cells and MACROs),Core Density #2(Subtracting Physical Cells),Chip Density (Counting Std Cells and MACROs and IOs),Chip Density #2(Subtracting Physical Cells)"
    metal_header = "Metal1 wire length (um),Metal2 wire length (um),Metal3 wire length (um),Metal4 wire length (um),Metal5 wire length (um),Metal6 wire length (um),Metal7 wire length (um),Metal8 wire length (um),Metal9 wire length (um),Metal10 wire length (um),Total wire length (um),Average wire length/net (um)"
    hold_header = "Hold Slack Path 1 (ns),Hold Slack Path 2 (ns),Hold Slack Path 3 (ns),Hold Slack Path 4 (ns),Hold Slack Path 5 (ns),Hold Slack Path 6 (ns),Hold Slack Path 7 (ns),Hold Slack Path 8 (ns),Hold Slack Path 9 (ns),Hold Slack Path 10 (ns)"
    setup_header = "Setup Slack Path 1 (ns),Setup Slack Path 2 (ns),Setup Slack Path 3 (ns),Setup Slack Path 4 (ns),Setup Slack Path 5 (ns),Setup Slack Path 6 (ns),Setup Slack Path 7 (ns),Setup Slack Path 8 (ns),Setup Slack Path 9 (ns),Setup Slack Path 10 (ns)"
    critical_path_header = "Critical Path 1 (ns),Critical Path 2 (ns),Critical Path 3 (ns),Critical Path 4 (ns),Critical Path 5 (ns),Critical Path 6 (ns),Critical Path 7 (ns),Critical Path 8 (ns),Critical Path 9 (ns),Critical Path 10 (ns)"
    slowest_path_header = "Slowest Path 1 (ns),Slowest Path 2 (ns),Slowest Path 3 (ns),Slowest Path 4 (ns),Slowest Path 5 (ns),Slowest Path 6 (ns),Slowest Path 7 (ns),Slowest Path 8 (ns),Slowest Path 9 (ns),Slowest Path 10 (ns)"
    header = cts_header + "," + fp_header + "," + density_header + "," + density_header_2 + "," + metal_header + "," + hold_header + "," + setup_header + "," + slowest_path_header + "," + critical_path_header
    if verbose: print("\n" + header)

    data = []

    for folder in list(results_data):
        o_file = open(results_data[folder]["sdc"][0], "r+")
        sdc_text = o_file.read()
        o_file.close()

        o_file = open(results_data[folder]["ctsrpt"][0], "r+")
        ctsrpt_text = o_file.read()
        o_file.close()

        o_file = open(results_data[folder]["tcpu"][0], "r+")
        tcpu_text = o_file.read()
        o_file.close()

        rpt_files = []
        for i in range(0, len(results_data[folder]["rpt"])):
            o_file = open(results_data[folder]["rpt"][i], "r+")
            rpt_text = o_file.read()
            rpt_files.append(rpt_text)
            o_file.close()

        hold_files = []
        for i in range(0, len(results_data[folder]["timing_hold"])):
            o_file = open(results_data[folder]["timing_hold"][i], "r+")
            timing_text = o_file.read()
            hold_files.append(timing_text)
            o_file.close()

        setup_files = []
        for i in range(0, len(results_data[folder]["timing_setup"])):
            o_file = open(results_data[folder]["timing_setup"][i], "r+")
            timing_text = o_file.read()
            setup_files.append(timing_text)
            o_file.close()

        freq = folder.split("_")[-1].split("M")[0]
        period = sdc_text[sdc_text.find("-period"):sdc_text.find("-waveform") + len("-waveform")].split(" ")[1]
        if abs(1.0 / float(freq) * 1000.0 - float(period)) > 0.1: rerun_list.append(results_folder_path + os.sep + folder)
        cpu_run_time = tcpu_text[tcpu_text.find("time:"):tcpu_text.find("ms")].split(":")[-1].replace(" ", "")
        max_skew = ctsrpt_text[ctsrpt_text.find("Trig. Edge Skew"):ctsrpt_text.find("\n", ctsrpt_text.find("Trig. Edge Skew"))].split(" ")
        max_skew = [s for s in max_skew if "" != s][-2].split("(")[0]
        r_latency = ctsrpt_text[ctsrpt_text.find("Rise Phase Delay"):ctsrpt_text.find("\n", ctsrpt_text.find("Rise Phase Delay"))].split(" ")
        r_latency = [s for s in r_latency if "" != s][-2].split("(")[0]
        f_latency = ctsrpt_text[ctsrpt_text.find("Fall Phase Delay"):ctsrpt_text.find("\n", ctsrpt_text.find("Fall Phase Delay"))].split(" ")
        f_latency = [s for s in f_latency if "" != s][-2].split("(")[0]
        levels = ctsrpt_text[ctsrpt_text.find("Nr. of Level (including gates)"):ctsrpt_text.find("\n", ctsrpt_text.find("Nr. of Level (including gates)"))].split(" ")[-1]
        buffers = ctsrpt_text[ctsrpt_text.find("Nr. of Buffer"):ctsrpt_text.find("\n", ctsrpt_text.find("Nr. of Buffer"))].split(" ")[-1]
        sinks = ctsrpt_text[ctsrpt_text.find("Nr. of Sinks"):ctsrpt_text.find("\n", ctsrpt_text.find("Nr. of Sinks"))].split(" ")[-1]

        i = -1
        section = rpt_files[i][rpt_files[i].find("Floorplan/Placement Information"):-1]

        std_cell_area = section[section.find("Standard cells:"):section.find("\n", section.find("Standard cells:"))].split(" ")
        std_cell_area = [s for s in std_cell_area if "" != s][-2]
        std_cell_area_no_phy = section[section.find("Standard cells(Subtracting"):section.find("\n", section.find("Standard cells(Subtracting"))].split(" ")
        std_cell_area_no_phy = [s for s in std_cell_area_no_phy if "" != s][-2]
        core_area = section[section.find("area of Core:"):section.find("\n", section.find("area of Core:"))].split(" ")
        core_area = [s for s in core_area if "" != s][-2]
        chip_area = section[section.find("area of Chip:"):section.find("\n", section.find("area of Chip:"))].split(" ")
        chip_area = [s for s in chip_area if "" != s][-2]

        density_1 = section[section.find("(Subtracting BLOCKAGES)"):section.find("\n", section.find("(Subtracting BLOCKAGES)"))].split(" ")
        density_1 = [s for s in density_1 if "" != s][-1].replace("%", "")
        density_2 = section[section.find("(Subtracting BLOCKAGES and Physical Cells)"):section.find("\n", section.find("(Subtracting BLOCKAGES and Physical Cells)"))].split(" ")
        density_2 = [s for s in density_2 if "" != s][-1].replace("%", "")
        density_3 = section[section.find("(Subtracting MACROS)"):section.find("\n", section.find("(Subtracting MACROS)"))].split(" ")
        density_3 = [s for s in density_3 if "" != s][-1].replace("%", "")
        density_4 = section[section.find("(Subtracting MACROS and Physical Cells)"):section.find("\n", section.find("(Subtracting MACROS and Physical Cells)"))].split(" ")
        density_4 = [s for s in density_4 if "" != s][-1].replace("%", "")
        density_5 = section[section.find("(Subtracting MACROS and BLOCKAGES)"):section.find("\n", section.find("(Subtracting MACROS and BLOCKAGES)"))].split(" ")
        density_5 = [s for s in density_5 if "" != s][-1].replace("%", "")
        density_6 = section[section.find("insts are not placed)"):section.find("\n", section.find("insts are not placed)"))].split(" ")
        density_6 = [s for s in density_6 if "" != s][-1].replace("%", "")

        core_density_1 = section[section.find("(Counting Std Cells and MACROs)"):section.find("\n", section.find("(Counting Std Cells and MACROs)"))].split(" ")
        core_density_1 = [s for s in core_density_1 if "" != s][-1].replace("%", "")
        core_density_2 = section[section.find("Core Density #2(Subtracting Physical Cells)"):section.find("\n", section.find("Core Density #2(Subtracting Physical Cells)"))].split(" ")
        core_density_2 = [s for s in core_density_2 if "" != s][-1].replace("%", "")
        chip_density_1 = section[section.find("(Counting Std Cells and MACROs and IOs)"):section.find("\n", section.find("(Counting Std Cells and MACROs and IOs)"))].split(" ")
        chip_density_1 = [s for s in chip_density_1 if "" != s][-1].replace("%", "")
        chip_density_2 = section[section.find("Chip Density #2(Subtracting Physical Cells)"):section.find("\n", section.find("Chip Density #2(Subtracting Physical Cells)"))].split(" ")
        chip_density_2 = [s for s in chip_density_2 if "" != s][-1].replace("%", "")

        metal_1 = section[section.find("metal1"):section.find("\n", section.find("metal1"))].split(" ")
        metal_1 = [s for s in metal_1 if "" != s][-2]
        metal_2 = section[section.find("metal2"):section.find("\n", section.find("metal2"))].split(" ")
        metal_2 = [s for s in metal_2 if "" != s][-2]
        metal_3 = section[section.find("metal3"):section.find("\n", section.find("metal3"))].split(" ")
        metal_3 = [s for s in metal_3 if "" != s][-2]
        metal_4 = section[section.find("metal4"):section.find("\n", section.find("metal4"))].split(" ")
        metal_4 = [s for s in metal_4 if "" != s][-2]
        metal_5 = section[section.find("metal5"):section.find("\n", section.find("metal5"))].split(" ")
        metal_5 = [s for s in metal_5 if "" != s][-2]
        metal_6 = section[section.find("metal6"):section.find("\n", section.find("metal6"))].split(" ")
        metal_6 = [s for s in metal_6 if "" != s][-2]
        metal_7 = section[section.find("metal7"):section.find("\n", section.find("metal7"))].split(" ")
        metal_7 = [s for s in metal_7 if "" != s][-2]
        metal_8 = section[section.find("metal8"):section.find("\n", section.find("metal8"))].split(" ")
        metal_8 = [s for s in metal_8 if "" != s][-2]
        metal_9 = section[section.find("metal9"):section.find("\n", section.find("metal9"))].split(" ")
        metal_9 = [s for s in metal_9 if "" != s][-2]
        metal_10 = section[section.find("metal10"):section.find("\n", section.find("metal10"))].split(" ")
        metal_10 = [s for s in metal_10 if "" != s][-2]
        metal_total = section[section.find("Total wire length:"):section.find("\n", section.find("Total wire length:"))].split(" ")
        metal_total = [s for s in metal_total if "" != s][-2]
        metal_avg = section[section.find("Average wire length/net"):section.find("\n", section.find("Average wire length/net"))].split(" ")
        metal_avg = [s for s in metal_avg if "" != s][-2]

        hold_text_list = hold_files[i].split("\n")
        indices = [i for i, x in enumerate(hold_text_list) if "Slack" in x]

        hold_slack = ""
        for index in indices:
            line = hold_text_list[index]
            slack = line.split(" ")[-1]
            hold_slack = hold_slack + "," + slack

        setup_text_list = setup_files[i].split("\n")
        indices = [i for i, x in enumerate(setup_text_list) if "Slack" in x]
        setup_slack = ""
        for index in indices:
            line = setup_text_list[index]
            slack = line.split(" ")[-1]
            setup_slack = setup_slack + "," + slack

        indices = [i for i, x in enumerate(hold_text_list) if "Arrival Time" in x and "End" not in x and "Beginpoint" not in x]
        slowest_path = ""
        for index in indices:
            line = hold_text_list[index]
            spath = line.split(" ")[-1]
            slowest_path = slowest_path + "," + spath

        indices = [i for i, x in enumerate(setup_text_list) if "- Arrival Time " in x and "END" not in x and "Beginpoint" not in x]
        critical_path = ""
        for index in indices:
            line = setup_text_list[index]
            cpath = line.split(" ")[-1]
            critical_path = critical_path + "," + cpath

        cts_data = period + "," + freq + "," + cpu_run_time + "," + max_skew + "," + r_latency + "," + f_latency + "," + levels + "," + buffers + "," + sinks
        area_data = std_cell_area + "," + std_cell_area_no_phy + "," + core_area + "," + chip_area
        density_data = density_1 + "," + density_2 + "," + density_3 + "," + density_4 + "," + density_5 + "," + density_6 + "," + core_density_1 + "," + core_density_2 + "," + chip_density_1 + "," + chip_density_2
        metal_data = metal_1 + "," + metal_2 + "," + metal_3 + "," + metal_4 + "," + metal_5 + "," + metal_6 + "," + metal_7 + "," + metal_8 + "," + metal_9 + "," + metal_10 + "," + metal_total + "," + metal_avg
        hold_slack = hold_slack[1:-1]
        setup_slack = setup_slack[1:-1]
        slowest_path = slowest_path[1:-1]
        critical_path = critical_path[1:-1]

        data_line = cts_data + "," + area_data + "," + density_data + "," + metal_data + "," + hold_slack + "," + setup_slack + "," + slowest_path + "," + critical_path
        data.append(data_line)
        if verbose: print(data_line)

    if csv:
        w_file = open(results_folder_path.split(os.sep)[-1] + ".csv", "a+")
        w_file.truncate(0)
        w_file.write(header + "\n")
        for line in data:
            w_file.write(line + "\n")


def extract_gif(results_folder):
    gif_folder_path = os.getcwd() + os.sep + "_extracted_gif"
    if not os.path.exists(gif_folder_path): os.makedirs(gif_folder_path)
    folder_list = os.listdir(results_folder)
    folder_list.sort(key=lambda f: int(re.sub('\D', '', f)))
    for item in folder_list:
        print("Processing: " + item)
        ab_path = results_folder + os.sep + item + os.sep + "results" + os.sep + "images"
        src = ab_path
        dst = gif_folder_path + os.sep + "images_" + item.split("_")[-1]
        if not os.path.exists(dst): os.makedirs(dst)
        copy_tree(src, dst)
    return gif_folder_path


def create_gif(gif_foler):
    keywords = {}
    split_folder_name = "_split_gif"
    folder_list = os.listdir(gif_foler)
    for file in os.listdir(gif_foler + os.sep + folder_list[0]):
        new_folder = file.split(".")[-2]
        if not os.path.exists(os.getcwd() + os.sep + split_folder_name + os.sep + new_folder):
            os.makedirs(os.getcwd() + os.sep + split_folder_name + os.sep + new_folder)
        else:
            shutil.rmtree(os.getcwd() + os.sep + split_folder_name + os.sep + new_folder)
            os.makedirs(os.getcwd() + os.sep + split_folder_name + os.sep + new_folder)
        keywords[new_folder] = os.getcwd() + os.sep + split_folder_name + os.sep + new_folder

    folder_list.sort(key=lambda f: int(re.sub('\D', '', f)))
    for item in folder_list:
        print("Splitting: " + item)
        gif_folder = gif_foler + os.sep + item
        subfolder_list = os.listdir(gif_folder)
        for file in subfolder_list:
            src = gif_folder + os.sep + file
            dst = keywords[file.split(".")[-2]] + os.sep + item.split("_")[-1].split(".")[0] + "_" + file.split(".")[-2] + ".gif"
            shutil.copy(src, dst)

    if sys.version_info.major == 3:
        import imageio
        gif_path = os.getcwd() + os.sep + "_gif"
        if not os.path.exists(gif_path): os.makedirs(gif_path)
        for folder in keywords:
            print("Creating " + folder + " GIF...")
            images = []
            file_list = os.listdir(keywords[folder])
            file_list.sort(key=lambda f: int(re.sub('\D', '', f)))
            for item in file_list:
                image_path = keywords[folder] + os.sep + item
                images.append(imageio.imread(image_path))
            imageio.mimsave(gif_path + os.sep + folder + ".gif", images, fps=10)


def setup():
    main_script = "PNR_script.tcl"
    setup = '#!/bin/bash\nsource /etc/profile.d/ensc-cmc.csh\nsource /CMC/setups/CDS_setup.csh\nsource /CMC/setups/BE_setup.csh\nsource /CMC/setups/FE_setup.csh\ninnovus\necho "done"\n'
    enc = 'puts "************************"\nputs "*    Startup Script    *"\nputs "************************"\nafter 5000\nputs "Starting Main script..."\nsource scripts/' + main_script + '\n'

    if not os.path.exists(os.getcwd() + os.sep + "enc.tcl"):
        file = open(os.getcwd() + os.sep + "enc.tcl", "wt")
        file.truncate(0)
        file.write(enc)
        file.flush()
        file.close()
    if not os.path.exists(os.getcwd() + os.sep + "setup.csh"):
        file = open(os.getcwd() + os.sep + "setup.csh", "wt")
        file.truncate(0)
        file.write(setup)
        file.flush()
        file.close()

    if os.path.exists(os.getcwd() + os.sep + "DBS"): shutil.rmtree(os.getcwd() + os.sep + "DBS")
    os.makedirs(os.getcwd() + os.sep + "DBS")
    if os.path.exists(os.getcwd() + os.sep + "results"): shutil.rmtree(os.getcwd() + os.sep + "results")
    os.makedirs(os.getcwd() + os.sep + "results")
    if os.path.exists(os.getcwd() + os.sep + "timingReports"): shutil.rmtree(os.getcwd() + os.sep + "timingReports")
    os.makedirs(os.getcwd() + os.sep + "timingReports")


def cleanup():
    for item in os.listdir(os.getcwd()):
        if ".log" in item or ".cmd" in item or ".tif" in item or ".txt" in item or ".rpt" in item:
            os.remove(os.getcwd() + os.sep + item)
        elif os.path.isdir(os.getcwd() + os.sep + item) and "temp" in item:
            shutil.rmtree(os.getcwd() + os.sep + item)


if __name__ == "__main__":

    cleanup()
    mode = "f"
    start = 1.0
    end = 10.0
    step = 1.0
    run_array = np.arange(float(start), float(end + step), float(step))

    sdc_path = os.getcwd() + os.sep + "inputs" + os.sep + "square_root.sdc"
    floorplan_template_path = os.getcwd() + os.sep + "scripts" + os.sep + "01-powerPlan.tcl"
    results_folder_path = os.getcwd() + os.sep + "auto_innovus_" + datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    if not os.path.exists(results_folder_path): os.makedirs(results_folder_path)

    setup()
    innovus_run_range(0, results_folder_path, sdc_path, floorplan_template_path, run_array, sweep=mode)
    gen_innous_data(results_folder_path)
    cleanup()

    # gen_innous_data(os.getcwd() + os.sep + "pnr_data")
