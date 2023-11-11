import os
import sys
import time
import traceback
import datetime
import shutil
import paramiko
import subprocess
import socket
import platform
import re


def split_on_empty_lines(s):
    blank_line_regex = r"(?:\r?\n){2,}"
    return re.split(blank_line_regex, s.strip())


def ping(ip, count=1, verbose=False):
    try:
        socket.inet_aton(ip)
    except socket.error:
        raise Exception('Invalid IP')
    if count < 1:
        raise Exception('Invalid Ping Count')
    param = '-n' if 'windows' in platform.system().lower() else '-c'
    command = ['ping', param, str(count), ip]
    output, error = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if verbose: print(output.decode('utf-8'))
    if "(0% loss)" in str(output) or ", 0% packet loss" in str(output):
        return True
    else:
        return False


def ssh_create_client(ip, port=22, user='', pwd='', key=''):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if key == '':
            ssh_client.connect(hostname=ip, port=port, username=user, password=pwd)
        else:
            ssh_client.connect(hostname=ip, port=port, username=user, key_filename=key)
        return ssh_client
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        raise e


def ssh_create_connection_jump_host(jump_host, ip, port=22, usr='', pwd=''):
    try:
        jump_host_transport = jump_host.get_transport()
        jump_ip, jump_port = jump_host_transport.getpeername()
        src_addr = (jump_ip, 22)
        dst_addr = (ip, 22)
        jump_host_channel = jump_host_transport.open_channel("direct-tcpip", dst_addr, src_addr)
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=ip, port=port, username=usr, password=pwd, sock=jump_host_channel)
        return ssh_client
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        raise e


if __name__ == "__main__":

    fgt_ip = "10.59.71.85"
    id_rsa_path = r'C:\Users\ljerry\OneDrive - Fortinet\3_Code\Python\FGT_Test_Server\key\id_rsa'
    time_stamp = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    output_folder = os.getcwd() + os.sep + "results"
    output_filename = output_folder + os.sep + time_stamp + "_results.txt"

    if not os.path.exists(output_folder): os.mkdir(output_folder)

    if (ping(fgt_ip, 1)) == False:
        jump_host = ssh_create_client(ip="172.17.216.160", user="ljerry", key=id_rsa_path)
        fgt = ssh_create_connection_jump_host(jump_host=jump_host, ip="10.59.71.85", usr="admin")
    else:
        fgt = ssh_create_client(ip=fgt_ip, user="admin")

    while True:

        try:
            ts = datetime.datetime.now().strftime("%y%m%d %H:%M:%S")
            stdin, stdout, stderr = fgt.exec_command("c v\ned root\nd sys link-monitor status\n")
            for line in split_on_empty_lines(stdout.read().decode('utf-8')):
                if "Link Monitor" in line:
                    print('\n--------------------------------------------' + ts + '----------------------------------------\n\n')
                    print(line + '\n')
                    f = open(output_filename, 'a+')
                    f.write('\n--------------------------------------------' + ts + '----------------------------------------\n\n')
                    f.write(line + '\n')
                    f.flush()
                    f.close()
        except:
            fgt.close()
            if (ping(fgt_ip, 1)) == False:
                jump_host = ssh_create_client(ip="172.17.216.160", user="ljerry", key=id_rsa_path)
                fgt = ssh_create_connection_jump_host(jump_host=jump_host, ip="10.59.71.85", usr="admin")
            else:
                fgt = ssh_create_client(ip=fgt_ip, user="admin")

        time.sleep(1)
