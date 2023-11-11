import os
import sys
import time
import traceback

import ssh
import utility
from scp import SCPClient


class TFTP():

    def __init__(self, ip, usr, pwd, path, jump_host=None):
        self.tftp_ip = ip
        self.tftp_usr = usr
        self.tftp_pwd = pwd
        self.tftp_path = path
        self.tftp_ssh_jump_host = jump_host
        self.tftp_ssh_client = None

        self.tftp_connect()

    def tftp_cs_log(self, text, type="INFO"):
        utility.cs_log(text, type)

    def tftp_connect(self):
        try:
            client = ssh.SSH(host_ip=self.tftp_ip, usr=self.tftp_usr, pwd=self.tftp_pwd, jump_client=self.tftp_ssh_jump_host)
            self.tftp_ssh_client = client.ssh_client
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            raise e

    def tftp_upload(self, local_path, remote_path):
        self.tftp_cs_log("Uploading file to tftp server...\n")
        time.sleep(5)
        scp = SCPClient(self.tftp_ssh_client.get_transport())
        time.sleep(5)
        scp.put(local_path, remote_path + local_path.split(os.sep)[-1])

    def tftp_clear_site(self, tftp_path, extension=''):
        rm_list = []
        stdin, stdout, stderr = self.tftp_ssh_client.exec_command("ls -al " + tftp_path)
        for line in stdout.read().split(b'\n'):
            line = str(line.decode('utf-8'))
            if extension in line:
                image_name = line.split(' ')[-1].replace('\n', '')
                rm_list.append(tftp_path + image_name)
        for item in rm_list:
            self.tftp_ssh_client.exec_command("rm " + item)
