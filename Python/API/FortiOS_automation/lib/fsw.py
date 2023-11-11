import os
import sys
import time
import ssh
import utility


class FSW():

    def __init__(self, ip, usr, pwd, jump_host=None):

        self.ip = ip
        self.usr = usr
        self.pwd = pwd
        self.serial_number = ""
        self.device_type = ""
        self.device_model = ""
        self.device_version = ""
        self.device_build = 0
        self.device_branch = 0
        self.ssh_jump_host = jump_host
        self.ssh_client = None

        self.create_ssh_client()
        self.get_version()
        self.cs_log("FortiSwitch Device Connection Established!\n")
        self.print_fgt_info()

    def cs_log(self, text, type="INFO"):
        utility.cs_log(text, type)

    def print_fgt_info(self):
        self.cs_log("FSW_IP: " + self.ip + '\n')
        self.cs_log("FSW_SERIAL#: " + self.serial_number + '\n')
        self.cs_log("FSW_TYPE: " + self.device_type + '\n')
        self.cs_log("FSW_MODEL: " + self.device_model + '\n')
        self.cs_log("FSW_VERSION: " + self.device_version + '\n')
        self.cs_log("FSW_BUILD: " + str(self.device_build).zfill(4) + '\n')
        self.cs_log("FSW_BRANCH: " + str(self.device_branch).zfill(4) + '\n')

    def create_ssh_client(self):
        try:
            client = ssh.SSH(host_ip=self.ip, username=self.usr, password=self.pwd, jump_client=self.ssh_jump_host)
            self.ssh_client = client.ssh_client
        except:
            sys.exit(-1)

    def get_version(self):
        stdin, stdout, stderr = self.ssh_client.exec_command("get system status")
        for line in stdout.read().split(b'\n'):
            line = str(line.decode('utf-8'))
            line_list = line.split(' ')
            for i in range(0, len(line_list)):
                if "build" in line_list[i]:
                    info = line_list[i].split(',')
                    self.device_version = info[0]
                    self.device_build = int(info[1].replace('build', ''))
                if "forti".lower() in line_list[i].lower() and '-' in line_list[i]:
                    self.device_type = line_list[i].split('-')[0]
                    self.device_model = line_list[i].split('-')[-1]
            if "Branch".lower() in line.lower():
                self.device_branch = line.split(':')[-1]
            if "Serial".lower() in line.lower():
                self.serial_number = line.split(':')[-1].replace(' ', '')
        self.device_build = int(self.device_build)
        self.device_branch = int(self.device_branch)
