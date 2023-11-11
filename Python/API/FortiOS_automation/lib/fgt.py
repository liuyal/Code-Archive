import os
import re
import sys
import time
import socket

import ssh
import utility


class FGT():

    def __init__(self, ip, port=22, usr='admin', pwd='', vdom='', api_token='', ssh_client=None, jump_client=None, verbose=False):

        try:
            socket.inet_aton(ip)
        except socket.error:
            raise Exception('Invalid FGT IP')
        if port < 1 or port > 65535:
            raise Exception('Invalid FGT SSH PORT')

        self.ip = ip
        self.port = port
        self.usr = usr
        self.pwd = pwd

        self.vdom = vdom
        self.api_token = api_token

        self.system_status = {}
        self.serial_number = ""
        self.device_type = ""
        self.device_model = ""
        self.device_version = ""
        self.device_build = 0
        self.device_branch = 0

        self.ssh_client = ssh_client
        self.jump_client = jump_client

        self.create_ssh_client()
        self.get_system_status()
        self.get_version()

        if verbose: self.print_info()

    def cs_log(self, text, type="INFO"):
        utility.cs_log(text, type)

    def print_info(self):
        self.cs_log("IP: " + self.ip + '\n')
        self.cs_log("SERIAL#: " + self.serial_number + '\n')
        self.cs_log("TYPE: " + self.device_type + '\n')
        self.cs_log("MODEL: " + self.device_model + '\n')
        self.cs_log("VERSION: " + self.device_version + '\n')
        self.cs_log("BUILD: " + str(self.device_build).zfill(4) + '\n')
        self.cs_log("BRANCH: " + str(self.device_branch).zfill(4) + '\n')

    def create_ssh_client(self):
        if self.ssh_client is None:
            self.ssh_client = ssh.SSH(host_ip=self.ip, port=self.port, usr=self.usr, pwd=self.pwd, jump_client=self.jump_client)
        self.get_system_status()

    def end_session(self):
        try:
            if self.ssh_client is not None:
                self.ssh_client.close()
            return True
        except:
            return False

    def run_cmd(self, cmd, remove_hostname=True):
        if self.vdom != '':
            input_cmd = 'c v' + '\n' + 'ed ' + self.vdom + '\n' + cmd
        elif self.vdom == 'global':
            input_cmd = 'c g' + '\n' + cmd
        else:
            input_cmd = cmd

        if self.ssh_client != None:
            result = self.ssh_client.exec_cmd(input_cmd)
        else:
            raise Exception('To run FGT CLI command SSH/TELNET connection is needed')

        try:
            hostname = self.system_status['hostname']
            hostname_variant = []
            if self.vdom != '':
                hostname_variant.append(hostname + ' (' + self.vdom + ') #')
                hostname_variant.append(hostname + ' (global) #')
                hostname_variant.append(hostname + ' (vdom) #')
                hostname_variant.append(hostname + ' #')
            else:
                hostname_variant.append(hostname + ' #')
            if remove_hostname:
                for hostname in hostname_variant:
                    result = result.replace(hostname, '')
        except:
            pass

        return result.replace('\r', '').strip()

    def create_api_token(self, user_name="api_user", vdom="root", accprofile="super_admin"):
        cmd_0 = "c g\nconfig system api-user\n"
        cmd_1 = "edit <1>\n".replace("<1>", user_name)
        cmd_2 = "set accprofile <2>\n".replace("<2>", accprofile)
        cmd_3 = "set vdom <3>\nnext\nend\n".replace("<3>", vdom)
        cmd_4 = "execute api-user generate-key <1>\n".replace("<1>", user_name)
        config_api_user_cmd = cmd_0 + cmd_1 + cmd_2 + cmd_3 + cmd_4
        output = self.ssh_client.run_cmd_listen(cmd=config_api_user_cmd, time_out=10)
        start_index = output.find("New API key:")
        end_index = output.find('\n', start_index)
        if start_index != -1 and end_index != -1:
            token = output[start_index:end_index].split(':')[-1].strip()
            return token
        else:
            return ""

    def set_output_standard(self):
        cmd0 = 'end\nend\nend\nend\n'
        cmd1 = 'config global\n'
        cmd2 = 'config system console\n'
        cmd3 = 'set output standard\n'
        cmd4 = 'end\n'
        cmd = cmd0 + cmd1 + cmd2 + cmd3 + cmd4
        if self.ssh_client != None:
            self.run_cmd(cmd)
        else:
            raise Exception('To set FGT system console SSH/TELNET connection is needed')

    def get_system_status_helper(self, txt, start_string, end_string, attr):
        start_index = txt.find(start_string)
        end_index = txt.find(end_string, start_index)
        if start_index != -1 and end_index != -1:
            self.system_status[attr] = txt[start_index + len(start_string): end_index].strip()
        else:
            self.system_status[attr] = ''

    def get_system_status(self):
        if self.ssh_client != None:
            status_txt = self.run_cmd('get sys status')
        else:
            raise Exception('To get FGT system status SSH connection is needed')

        if status_txt == '': return

        start_index = status_txt.find('Version:')
        end_index = status_txt.find('\n', start_index)
        if start_index != -1 and end_index != -1:
            version_txt = status_txt[start_index + len('Version:'): end_index].strip()
            self.device_model = re.split(r'[,\s]+', version_txt)[0]
            self.device_version = re.split(r'[,\s]+', version_txt)[1]

        start_index = status_txt.find('Branch point:')
        end_index = status_txt.find('\n', start_index)
        if start_index != -1 and end_index != -1:
            self.device_build = int(status_txt[start_index + len('Branch point:'): end_index].strip())

        info_list = [('Version:', 'version'),
                     ('Firmware Signature:', 'firmware_signature'),
                     ('Virus-DB:', 'virus_db'),
                     ('Extended DB:', 'extended_db'),
                     ('Extreme DB:', 'extreme_db'),
                     ('AV AI/ML Model:', 'av_ai_ml_model'),
                     ('IPS-DB:', 'ips_db'),
                     ('IPS-ETDB:', 'ips_etdb'),
                     ('APP-DB:', 'app_db'),
                     ('INDUSTRIAL-DB:', 'industrial_db'),
                     ('IPS Malicious URL Database:', 'ips_malicious_url_database'),
                     ('Serial-Number:', 'serial_number'),
                     ('License Status:', 'license_status'),
                     ('License Expiration Date:', 'license_expiration_date'),
                     ('VM Resources:', 'vm_resources'),
                     ('BIOS version:', 'bios_version'),
                     ('System Part-Number:', 'system_part_number'),
                     ('Log hard disk:', 'log_hard_disk'),
                     ('Hostname:', 'hostname'),
                     ('Private Encryption:', 'private_encryption'),
                     ('Operation Mode:', 'operation_mode'),
                     ('Current virtual domain:', 'current_virtual_domain'),
                     ('Max number of virtual domains:', 'max_number_of_virtual_domains'),
                     ('Virtual domains status:', 'virtual_domains_status'),
                     ('Virtual domain configuration:', 'virtual_domain_configuration'),
                     ('FIPS-CC mode:', 'fips_cc_mode'),
                     ('Current HA mode:', 'current_ha_mode'),
                     ('Cluster uptime:', 'cluster_uptime'),
                     ('Cluster state change time:', 'cluster_state_change_time'),
                     ('Branch point:', 'branch_point'),
                     ('Release Version Information:', 'release_version_information'),
                     ('FortiOS x86-64:', 'fortios_x86_64'),
                     ('System time:', 'system_time'),
                     ('Last reboot reason:', 'last_reboot_reason')]

        for item, attr in info_list:
            self.get_system_status_helper(status_txt, item, '\n', attr)

    def get_version(self):
        stdout = self.run_cmd("get system status")
        for line in stdout.split('\n'):
            line_list = line.split(' ')
            for i in range(0, len(line_list)):
                if "build" in line_list[i]:
                    info = line_list[i].split(',')
                    self.device_version = info[0]
                    self.device_build = int(info[1].replace('build', ''))
                if "forti".lower() in line_list[i].lower() and '-' in line_list[i]:
                    self.device_type = line_list[i].split('-')[0]
                    self.device_model = line_list[i].split('-')[-1]
            if "Branch point".lower() in line.lower():
                self.device_branch = line.split(' ')[-1]
            if "Serial-Number".lower() in line.lower():
                self.serial_number = line.split(' ')[-1]
        self.device_build = int(self.device_build)
        self.device_branch = int(self.device_branch)

    def exec_upgrade(self, target_version, target_branch, image_name, tftp_ip):
        upgrade_cmd = "c g\nexecute restore image tftp " + image_name + ' ' + tftp_ip + '\n'
        ssh_channel = self.ssh_client.ssh_client.invoke_shell()
        recv_bytes = 2048
        time_sleep = 10
        time_out = 300

        ssh_channel.send(upgrade_cmd)
        while not ssh_channel.recv_ready(): time.sleep(time_sleep)
        start_time = time.time()
        while True:
            stdout = ssh_channel.recv(recv_bytes)
            stdout_list = re.split(', |\n|\r', stdout.decode("ascii"))
            for item in list(filter(None, stdout_list)):
                self.cs_log(item.replace('\n', '') + '\n')
                start_time = time.time()
                if '#' in item or '.' == item: time.sleep(time_sleep / 2)
            if "(y/n)" in stdout.decode("ascii"):
                ssh_channel.send(b'y')
            connection = utility.check_connections("FortiGate", self.ip, self.jump_client, False)
            if connection == False:
                time.sleep(time_sleep)
                break
            if time.time() - start_time > time_out: break

        connection = utility.check_connections("FortiGate", self.ip, self.jump_client, False)
        if connection:
            raise Exception("ERROR: Image upgrade command not complete!")

        time.sleep(time_sleep * 2)
        self.check_system_down()
        self.check_system_up()
        self.get_version()
        self.print_info()
        self.check_upgrade_version(target_version, target_branch)
        self.cs_log("Upgrade Complete!\n")
        self.cs_log("Upgraded to: " + self.device_version + " Build: " + str(self.device_build).zfill(4) + " Branch Point: " + str(self.device_branch).zfill(4) + '\n')

    def check_system_down(self, timeout=10 * 60):
        connection = True
        start_time = time.time()
        self.cs_log("Waiting for device to go down...\n")
        while connection == True:
            connection = utility.check_connections("FortiGate", self.ip, self.jump_client, False)
            if time.time() - start_time > timeout: break
        self.cs_log("Device Down Successful!\n", "FLAG")
        return True

    def check_system_up(self, timeout=10 * 60):
        connection = False
        start_time = time.time()
        self.cs_log("Waiting for device to boot...\n")
        while connection == False:
            connection = utility.check_connections("FortiGate", self.ip, self.jump_client, False)
            if time.time() - start_time > timeout:
                self.cs_log("ERROR Device timed out..\n", "Error")
                sys.exit(-1)
        self.cs_log("Ping Successful!\n", "FLAG")
        self.ssh_client = None
        start_time = time.time()
        self.cs_log("Trying SSH Connection...\n")
        while self.ssh_client == None:
            try:
                self.create_ssh_client()
            except:
                self.ssh_client = None
            if self.ssh_client == None and time.time() - start_time > timeout:
                self.cs_log("ERROR Device timed out..", "Error")
                sys.exit(-1)
        return True

    def check_upgrade_version(self, target_version, target_branch):
        self.cs_log("Checking Device Version...\n")
        if int(target_version) != int(self.device_version.split('.')[0].replace('v', '')):
            self.cs_log("ERROR Mismatch FortiOS Version...\n")
            sys.exit(-1)
        if int(target_branch) != int(self.device_branch):
            self.cs_log("ERROR Mismatch FortiOS Build...\n")
            sys.exit(-1)
        return

    def exec_upload_config(self, tftp_ip, config_file_name):
        upload_cmd = "c g\nexecute restore config tftp " + config_file_name.split('/')[-1] + ' ' + tftp_ip + '\n'
        ssh_channel = self.ssh_client.ssh_client.invoke_shell()
        recv_bytes = 2048
        time_sleep = 5
        time_out = 15

        ssh_channel.send(upload_cmd)
        while not ssh_channel.recv_ready(): time.sleep(time_sleep)
        start_time = time.time()

        while True:
            stdout = ssh_channel.recv(recv_bytes)
            stdout_list = re.split(', |\n|\r', stdout.decode("ascii"))
            for item in stdout_list:
                if item != '' and item != '\n':
                    self.cs_log(item.replace('\n', '') + '\n')
            if "(y/n)" in stdout.decode("ascii"): break
            if time.time() - start_time > time_out: break

        ssh_channel.send(b'y')
        while not ssh_channel.recv_ready(): time.sleep(time_sleep)
        start_time = time.time()

        while True:
            stdout = ssh_channel.recv(recv_bytes)
            stdout_list = re.split(', |\n|\r', stdout.decode("ascii"))
            for item in stdout_list:
                if item != '' and item != '\n':
                    self.cs_log(item.replace('\n', '') + '\n')
            if "Command fail" in stdout.decode("ascii"): sys.exit(-1)
            if "File check OK." in stdout.decode("ascii"): break
            if time.time() - start_time > time_out: break

        time.sleep(time_sleep * 2)
        self.check_system_down()
        self.check_system_up()
        self.cs_log("Config Upload Complete!\n")
