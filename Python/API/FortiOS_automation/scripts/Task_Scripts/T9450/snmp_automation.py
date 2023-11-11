import os
import sys
import time
import json
import datetime
import paramiko
import pandas
import random
import difflib


def load_config(config_file_path):
    with open(config_file_path) as f: data = json.load(f)
    return data


def read_xlsx(path, filter="", sheet="Sheet1", max=-1):
    df = pandas.read_excel(path, sheet_name=sheet)
    id_list = []
    for index, row in df.iterrows():
        if int(index) + 2 == max: break
        if filter in row['name']: id_list.append((index + 2, row['name'], row['oid']))
    return id_list


def check_ex_list(exclude_oid, oid_list):
    for index, item, oid in oid_list:
        if exclude_oid == oid:
            return True
    return False


def create_ssh_client(host_ip, host_usr, host_pwd="", jump_host=True):
    if jump_host:
        ssh_jump_host = paramiko.SSHClient()
        ssh_jump_host.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_jump_host.connect("172.17.216.160", username="ljerry", key_filename=r"C:\Users\ljerry\.ssh\id_rsa")
        jump_host_transport = ssh_jump_host.get_transport()
        jump_ip, jump_port = jump_host_transport.getpeername()
        src_addr = (jump_ip, 22)
        dst_addr = (host_ip, 22)
        jump_host_channel = jump_host_transport.open_channel("direct-tcpip", dst_addr, src_addr)
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(host_ip, username=host_usr, password=host_pwd, sock=jump_host_channel)
    else:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(host_ip, username=host_usr, password=host_pwd)
    return ssh_client


def run_ssh_cmd(ssh, cmd):
    output = []
    stdin, stdout, stderr = ssh.exec_command(cmd)
    for line in stdout.read().split(b'\n'):
        line = str(line.decode('utf-8'))
        output.append(line)
    return output


def generate_cmd(oid_list, snmp_cmd_template, fgt_config_template, vdom=""):
    cmd_list = []
    for index, item, oid in oid_list:
        snmp_cmd = snmp_cmd_template.replace("<ID>", oid)
        fgt_config_cmd = fgt_config_template.replace("<ID>", oid)
        fgt_config_cmd = fgt_config_cmd.replace("set exclude .<EID>", "")
        if vdom != "":
            fgt_config_cmd = fgt_config_cmd.replace("<VDOM>", vdom)
        else:
            fgt_config_cmd = fgt_config_cmd.replace("set vdoms <VDOM>", "")
        cmd_list.append((index, item, oid, snmp_cmd, fgt_config_cmd))
    return cmd_list


def generate_tc_list(oid_list):
    processed_oid_list = []
    new_oid_list = []
    for index, item, oid in oid_list:
        new_item = '.'.join(item.split('.')[0:-1])
        new_oid = '.'.join(oid.split('.')[0:-1])
        sub_oid = '.' + oid.split('.')[-1:][0]
        processed_oid_list.append((index, new_item, new_oid, sub_oid))

    head_oid = []
    sub_oid_list = []
    for index, item, oid, sub_oid in processed_oid_list:
        if len(head_oid) == 0:
            head_oid.append(index)
            head_oid.append(item)
            head_oid.append(oid)
        elif len(head_oid) > 0 and oid != head_oid[2]:
            head_oid.append(sub_oid_list)
            new_oid_list.append(head_oid)
            head_oid = []
            sub_oid_list = []
            head_oid.append(index)
            head_oid.append(item)
            head_oid.append(oid)
        if oid == head_oid[2]:
            sub_oid_list.append(sub_oid)

    if len(new_oid_list) == 0:
        head_oid.append(sub_oid_list)
        new_oid_list.append(head_oid)

    return new_oid_list


def generate_filter_cmd(oid_filter_list, snmp_cmd_template, fgt_config_template):
    filter_cmd_list = []
    n = 1
    for index, item, oid, sub_oid_list in oid_filter_list:
        oid_include_list = [oid]
        oid_exclude_list = []

        if len(sub_oid_list) == 1:
            n = 1
            exclude = True
        elif len(sub_oid_list) == 0:
            exclude = False
        else:
            max = int(len(sub_oid_list) / 2) + 1
            n = random.randrange(1, max)
            exclude = True
        if exclude == True:
            sub_oid_sample = random.sample(sub_oid_list, n)
            for sub_oid in sub_oid_sample:
                oid_exclude_list.append(oid + sub_oid)

        snmp_cmd = snmp_cmd_template.replace("<ID>", '.'.join(oid.split('.')[0:-1]))
        fgt_config_cmd = fgt_config_template.replace("<ID>", ' .'.join(oid_include_list))
        fgt_config_cmd = fgt_config_cmd.replace("<EID>", ' .'.join(oid_exclude_list))
        fgt_config_cmd = fgt_config_cmd.replace("set vdoms <VDOM>", " ")
        filter_cmd_list.append((index, item, oid, snmp_cmd, fgt_config_cmd))

    return filter_cmd_list


def get_device_info(ssh):
    stdout = run_ssh_cmd(ssh, "get sys status")
    return


def run(fgt_client, pc_client, fgt_del_cmd, cmd_list, output_path, summary_path, static_fgt=False, skip_bad_oid=True):
    cmd1 = "c g\nshow system snmp mib-view"
    cmd2 = "c g\nshow system snmp community"
    cmd3 = "c g\nshow system snmp user"
    config_match_ratio_str = ""
    config_match_ratio = 0
    stdout_list = []
    error_list = []

    if static_fgt:
        run_ssh_cmd(fgt_client, fgt_del_cmd)
        index, item, oid, snmp_cmd, fgt_config_cmd = cmd_list[0]
        run_ssh_cmd(fgt_client, fgt_config_cmd)

    for index, item, oid, snmp_cmd, fgt_config_cmd in cmd_list:
        if not static_fgt:
            stdout1 = run_ssh_cmd(fgt_client, fgt_del_cmd)
            stdout2 = run_ssh_cmd(fgt_client, fgt_config_cmd)
            stdout_a = run_ssh_cmd(fgt_client, cmd1)
            stdout_b = run_ssh_cmd(fgt_client, cmd2)
            stdout_c = run_ssh_cmd(fgt_client, cmd3)

            stdout_list = ["c g"] + stdout_a + stdout_b + stdout_c
            for i in range(0, len(stdout_list)):
                if "# config" in stdout_list[i]:
                    stdout_list[i] = stdout_list[i].split("# ")[-1]
                elif "#" in stdout_list[i] and "# config" not in stdout_list[i]:
                    stdout_list[i] = ""
                if '"' in stdout_list[i]:
                    stdout_list[i] = stdout_list[i].replace('"', '')

            stdout_list = list(filter(None, stdout_list))
            config_out = '\n'.join(stdout_list).replace('\n', '').replace(' ', '')
            config_in = fgt_config_cmd.replace('\n', '').replace(' ', '')
            config_match_ratio = difflib.SequenceMatcher(None, config_out, config_in).ratio() * 100.00
            config_match_ratio_str = "{:.2f}".format(config_match_ratio)
            if not static_fgt and config_match_ratio < 95.00:
                if skip_bad_oid: continue
                error_str = 'ERROR in Test: [' + str(index) + '] ' + item + " " + oid + " Config Match ERROR " + config_match_ratio_str + "%"
                error_list.append(error_str)
                print(error_str)

        stdout3 = run_ssh_cmd(pc_client, snmp_cmd)

        if not static_fgt:
            stdout4 = run_ssh_cmd(fgt_client, fgt_del_cmd)

        start = fgt_config_cmd.index("include")
        end = fgt_config_cmd.index("\n", start)
        include_list = fgt_config_cmd[start:end].split(' ')[1:]
        exclude_list = []
        for i in range(0, len(stdout3)):
            line = stdout3[i]
            for in_id in include_list:
                if '.' != in_id and "No more" not in line and "No Such" not in line and line.split(' ')[0][1:] != '':
                    if (in_id[1:] + ' ' not in line.split(' ')[0][1:] and in_id[1:] + '.' not in line.split(' ')[0][1:]):
                        error_str = 'ERROR in Test: [' + str(index) + '] ' + item + ' [line ' + str(i) + ']' + line + " [Expected ID] " + in_id
                        error_list.append(error_str)
                        print(error_str)

        if "exclude" in fgt_config_cmd:
            start = fgt_config_cmd.index("exclude")
            end = fgt_config_cmd.index("\n", start)
            exclude_list = fgt_config_cmd[start:end].split(' ')[1:]
            if '.<EID>' not in exclude_list:
                for i in range(0, len(stdout3)):
                    for ex_oid in exclude_list:
                        line = stdout3[i]
                        if '.' != ex_oid and "No more" not in line and "No Such" not in line and line.split(' ')[0][1:] != '':
                            if (ex_oid[1:] + ' ' in line.split(' ')[0][1:] or ex_oid[1:] + '.' in line.split(' ')[0][1:]):
                                error_str = 'ERROR in Test: [' + str(index) + '] ' + item + ' [line ' + str(i) + ']' + line + " [Expected ID] Excluded " + ex_oid
                                error_list.append(error_str)
                                print(error_str)

        item = item.replace(':', '-')
        if '.' not in item:
            result_file_name = str(index) + "_" + item + '_' + output_path.split(os.sep)[-1] + "_test_results.txt"
            config_in_file_name = str(index) + "_" + item + '_' + output_path.split(os.sep)[-1] + "_config_in.txt"
            config_out_file_name = str(index) + "_" + item + '_' + output_path.split(os.sep)[-1] + "_config_out.txt"
        else:
            result_file_name = str(index) + "_" + item.split('.')[-1] + '_' + output_path.split(os.sep)[-1] + "_test_results.txt"
            config_in_file_name = str(index) + "_" + item.split('.')[-1] + '_' + output_path.split(os.sep)[-1] + "_config_in.txt"
            config_out_file_name = str(index) + "_" + item.split('.')[-1] + '_' + output_path.split(os.sep)[-1] + "_config_out.txt"

        f = open(output_path + os.sep + result_file_name, "a+")
        f.truncate(0)
        f.write("Configuration Match: " + config_match_ratio_str + "%\n")
        f.write("Include List: " + ' '.join(include_list) + "\n")
        f.write("Exclude List: " + ' '.join(exclude_list) + "\n")
        f.write("OID INPUT: " + oid + "\n\n")
        for i in range(0, len(stdout3)):
            if stdout3[i] != '':
                f.write('[' + str(i) + ']' + stdout3[i] + '\n')
                f.flush()
        f.close()

        if not static_fgt:
            f = open(output_path + os.sep + config_in_file_name, "a+")
            f.truncate(0)
            f.write(snmp_cmd + '\n\n' + fgt_config_cmd)
            f.flush()
            f.close()

        if not static_fgt and config_match_ratio < 95.00:
            f = open(output_path + os.sep + config_out_file_name, "a+")
            f.truncate(0)
            config_output = '\n'.join(stdout_list).replace('c g', '\n\nc g\n')
            config_output = config_output.replace("end\nconfig", "end\n\nconfig")
            f.write(config_output)
            f.flush()
            f.close()

        # TODO: fix parsing test_summary_str
        f = open(summary_path, 'a+')
        test_type = summary_path.split(os.sep)[-1].split('_')[1]
        if "filter" in summary_path.split(os.sep)[-1].lower():
            test_type = test_type + "_" + summary_path.split(os.sep)[-1].split('_')[2]
        test_summary = [str(index), "Complete", test_type, config_match_ratio_str + "%", item, oid]
        test_summary_str = ' '.join(test_summary)
        f.write(test_summary_str + '\n')
        f.flush()
        f.close()

        print(test_summary_str)

    if static_fgt:
        run_ssh_cmd(fgt_client, fgt_del_cmd)
        stdout_a = run_ssh_cmd(fgt_client, cmd1)
        stdout_b = run_ssh_cmd(fgt_client, cmd2)
        stdout_c = run_ssh_cmd(fgt_client, cmd3)
        stdout_list = ["c g"] + stdout_a + stdout_b + stdout_c
        for i in range(0, len(stdout_list)):
            if "# config" in stdout_list[i]:
                stdout_list[i] = stdout_list[i].split("# ")[-1]
            elif "#" in stdout_list[i] and "# config" not in stdout_list[i]:
                stdout_list[i] = ""
            if '"' in stdout_list[i]:
                stdout_list[i] = stdout_list[i].replace('"', '')
        f = open(output_path + os.sep + "_static_fgt_config.txt", "a+")
        f.truncate(0)
        config_output = '\n'.join(list(filter(None, stdout_list))).replace('c g', '\n\nc g\n')
        config_output = config_output.replace("end\nconfig", "end\n\nconfig")
        f.write(config_output)
        f.flush()
        f.close()

    error_path = summary_path.replace(".txt", "_errors.txt")
    f = open(error_path, 'a+')
    f.truncate(0)
    f.write("ERRORS: " + str(len(error_list)) + '\n')
    f.write("\n".join(error_list))
    f.flush()
    f.close()


def tc_community(oid_list, snmp_template, fgt_config_template):
    community_test_output_path = output_path + os.sep + "community"
    community_test_summary_path = community_test_output_path + os.sep + "0_community_test_summary.txt"
    if not os.path.exists(community_test_output_path): os.mkdir(community_test_output_path)
    oid_community_cmd_list = generate_cmd(oid_list, snmp_template, fgt_config_template)
    run(fgt, pc, fgt_del_cmd, oid_community_cmd_list, community_test_output_path, community_test_summary_path)


def tc_user(oid_list, snmp_template, fgt_config_template):
    user_test_output_path = output_path + os.sep + "user"
    user_test_summary_path = user_test_output_path + os.sep + "0_user_test_summary.txt"
    if not os.path.exists(user_test_output_path): os.mkdir(user_test_output_path)
    oid_usr_cmd_list = generate_cmd(oid_list, snmp_template, fgt_config_template)
    run(fgt, pc, fgt_del_cmd, oid_usr_cmd_list, user_test_output_path, user_test_summary_path)


def tc_vdom_vd1(oid_list, snmp_template, fgt_config_template):
    vdom_test_output_path = output_path + os.sep + "vdom-vd1"
    vdom_test_summary_path = vdom_test_output_path + os.sep + "0_vdom-vd1_test_summary.txt"
    if not os.path.exists(vdom_test_output_path): os.mkdir(vdom_test_output_path)
    oid_vdom_cmd_list = generate_cmd(oid_list, snmp_template, fgt_config_template, "vd1")
    run(fgt, pc, fgt_del_cmd, oid_vdom_cmd_list, vdom_test_output_path, vdom_test_summary_path)


def tc_1_ifDescr(oid_list, snmp_template, fgt_config_template):
    filter_test_output_path_tc1 = output_path + os.sep + "filter-tc1"
    filter_test_summary_path_tc1 = filter_test_output_path_tc1 + os.sep + "0_filter-tc1_summary.txt"
    if not os.path.exists(filter_test_output_path_tc1): os.mkdir(filter_test_output_path_tc1)
    oid_filter_list_tc1 = [[445, "IF-MIB:interfaces.ifTable.ifEntry.ifDescr", "1.3.6.1.2.1.2.2.1.2", []]]
    oid_filter_cmd_list_tc1 = generate_filter_cmd(oid_filter_list_tc1, snmp_template, fgt_config_template)
    run(fgt, pc, fgt_del_cmd, oid_filter_cmd_list_tc1, filter_test_output_path_tc1, filter_test_summary_path_tc1)


def tc_2_ifTable(oid_list, snmp_template, fgt_config_template):
    filter_test_output_path_tc2 = output_path + os.sep + "filter-tc2"
    filter_test_summary_path_tc2 = filter_test_output_path_tc2 + os.sep + "0_filter-tc2_summary.txt"
    if not os.path.exists(filter_test_output_path_tc2): os.mkdir(filter_test_output_path_tc2)
    oid_filter_list_tc2 = generate_tc_list(oid_list)
    oid_filter_cmd_list_tc2 = generate_filter_cmd(oid_filter_list_tc2, snmp_template, fgt_config_template)
    run(fgt, pc, fgt_del_cmd, oid_filter_cmd_list_tc2, filter_test_output_path_tc2, filter_test_summary_path_tc2)


def tc_filter_all(oid_list, snmp_template, fgt_config_template):
    filter_test_output_path_tc_all = output_path + os.sep + "filter-tc-all"
    filter_test_summary_path_tc_all = filter_test_output_path_tc_all + os.sep + "0_filter-tc-all_summary.txt"
    if not os.path.exists(filter_test_output_path_tc_all): os.mkdir(filter_test_output_path_tc_all)
    oid_filter_list_tc_all = generate_tc_list(oid_list)
    oid_filter_cmd_list_tc = generate_filter_cmd(oid_filter_list_tc_all, snmp_template, fgt_config_template)
    run(fgt, pc, fgt_del_cmd, oid_filter_cmd_list_tc, filter_test_output_path_tc_all, filter_test_summary_path_tc_all)


def tc_filter_vd1_core(oid_list, snmp_template, fgt_config_template):
    filter_test_output_path_tc_vdom1 = output_path + os.sep + "filter-tc-vd1"
    filter_test_summary_path_tc_vdom1 = filter_test_output_path_tc_vdom1 + os.sep + "0_filter-tc-vd1_summary.txt"
    if not os.path.exists(filter_test_output_path_tc_vdom1): os.mkdir(filter_test_output_path_tc_vdom1)
    oid_filter_list_tc_vdom = generate_cmd(oid_list, snmp_template, fgt_config_template, "vd1")
    run(fgt, pc, fgt_del_cmd, oid_filter_list_tc_vdom, filter_test_output_path_tc_vdom1, filter_test_summary_path_tc_vdom1)


def tc_filter_root_core(oid_list, snmp_template, fgt_config_template):
    filter_test_output_path_tc_root = output_path + os.sep + "filter-tc-vdom-root"
    filter_test_summary_path_tc_root = filter_test_output_path_tc_root + os.sep + "0_filter-tc-vdom-root_summary.txt"
    if not os.path.exists(filter_test_output_path_tc_root): os.mkdir(filter_test_output_path_tc_root)
    oid_filter_list_tc_root = generate_cmd(oid_list, snmp_template, fgt_config_template, "root")
    run(fgt, pc, fgt_del_cmd, oid_filter_list_tc_root, filter_test_output_path_tc_root, filter_test_summary_path_tc_root)


def tc_filter_static_fgt_config(oid_list, snmp_template, fgt_config_template):
    filter_test_output_path_static = output_path + os.sep + "static-fgt-config"
    filter_test_summary_path_tc_static = filter_test_output_path_static + os.sep + "0_static-fgt-config_summary.txt"
    if not os.path.exists(filter_test_output_path_static): os.mkdir(filter_test_output_path_static)
    oid_filter_list_static = generate_cmd(oid_list, snmp_template, fgt_config_template, "root")
    run(fgt, pc, fgt_del_cmd, oid_filter_list_static, filter_test_output_path_static, filter_test_summary_path_tc_static, True)


if __name__ == "__main__":
    time_stamp = datetime.datetime.now().strftime("%y%m%d_%H%M%S")

    config_file_path = os.getcwd() + os.sep + "config.json"
    config = load_config(config_file_path)
    fgt = create_ssh_client(config["FGT"]["IP"], config["FGT"]["USR"], config["FGT"]["PWD"], False)
    pc = create_ssh_client(config["PC"]["IP"], config["PC"]["USR"], config["PC"]["PWD"], False)

    oid_list_all = read_xlsx(os.getcwd() + os.sep + "OIDs.xlsx")
    oid_list_table = read_xlsx(os.getcwd() + os.sep + "OIDs.xlsx", "Table")
    oid_list_core = read_xlsx(os.getcwd() + os.sep + "OIDs.xlsx", "Table", "Sheet1", 657)
    oid_list_tc2 = read_xlsx(os.getcwd() + os.sep + "OIDs.xlsx", "Table", "filter_tc2")

    # output_path = os.getcwd() + os.sep + time_stamp + "_output"
    output_path = r'C:\Users\ljerry\Desktop\snmp_temp_output' + os.sep + time_stamp + "_output"
    if not os.path.exists(r'C:\Users\ljerry\Desktop\snmp_temp_output'): os.mkdir(r'C:\Users\ljerry\Desktop\snmp_temp_output')
    if not os.path.exists(output_path): os.mkdir(output_path)

    snmp_community_cmd_template = "snmpwalk -v 2c -c public " + config["FGT"]["IP"] + " .<ID> -On"
    snmp_user_cmd_template = "snmpwalk -v 3 -u u1 " + config["FGT"]["IP"] + " .<ID> -On"
    f = open(os.getcwd() + os.sep + "fgt_config_template.txt", 'r+')
    fgt_config_template = f.read()
    f.close()
    f = open(os.getcwd() + os.sep + "fgt_del_template.txt", 'r+')
    fgt_del_cmd = f.read()
    f.close()
    f = open(os.getcwd() + os.sep + "fgt_config_static_template.txt", 'r+')
    fgt_config_static_template = f.read()
    f.close()

    # tc_community(oid_list_core, snmp_community_cmd_template, fgt_config_template)
    # tc_user(oid_list_core, snmp_user_cmd_template, fgt_config_template)
    # tc_vdom_vd1(oid_list_table, snmp_user_cmd_template, fgt_config_template)
    # tc_1_ifDescr(oid_list_table, snmp_user_cmd_template, fgt_config_template)
    # tc_2_ifTable(oid_list_tc2, snmp_user_cmd_template, fgt_config_template)
    tc_filter_all(oid_list_all, snmp_user_cmd_template, fgt_config_template)
    tc_filter_vd1_core(oid_list_core, snmp_user_cmd_template, fgt_config_template)
    tc_filter_root_core(oid_list_core, snmp_user_cmd_template, fgt_config_template)
    tc_filter_static_fgt_config(oid_list_core, snmp_user_cmd_template, fgt_config_static_template)
