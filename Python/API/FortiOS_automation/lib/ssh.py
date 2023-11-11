import os
import sys
import time
import socket
import paramiko
import traceback
import utility


class SSH():

    def __init__(self, host_ip, port=22, usr='', pwd='', key='', jump_host_ip='', jump_port=22, jump_usr='', jump_pwd='', jump_key='', jump_client=None, timeout=300, verbose=False):
        try:
            socket.inet_aton(host_ip)
        except socket.error:
            raise Exception('Invalid Host IP')

        if port < 1 or port > 65535:
            raise Exception('Invalid SSH PORT')

        self.host_ip = host_ip
        self.port = port
        self.usr = usr
        self.pwd = pwd
        self.key = key

        self.jump_host_ip = jump_host_ip
        self.jump_port = jump_port
        self.jump_usr = jump_usr
        self.jump_pwd = jump_pwd
        self.jump_key = jump_key

        self.timeout = timeout
        self.channel = None
        self.transport = None
        self.ssh_client = None
        self.jump_client = jump_client

        self.create_connection(verbose)

    def ssh_cs_log(self, text, type="INFO"):
        utility.cs_log(text, type)

    def create_connection(self, verbose=False):
        if verbose:
            self.ssh_cs_log("Creating SSH Connection to " + self.host_ip + "\n")
        if self.jump_client != None:
            self.ssh_client = self.create_connection_via_jump_host_ip(self.jump_client)
            self.create_channel()
        elif self.jump_host_ip != '' and self.jump_client == None:
            self.jump_client = self.create_client(self.jump_host_ip, self.jump_port, self.jump_usr, self.pwd, self.jump_key)
            self.ssh_client = self.create_connection_via_jump_host_ip(self.jump_client)
            self.create_channel()
        else:
            self.ssh_client = self.create_client(self.host_ip, self.port, self.usr, self.pwd, self.key)
            self.create_channel()

    def create_connection_via_jump_host_ip(self, jump_client):
        try:
            jump_host_ip_transport = jump_client.get_transport()
            jump_host_ip, jump_port = jump_host_ip_transport.getpeername()
            src_addr = (jump_host_ip, 22)
            dst_addr = (self.host_ip, 22)
            jump_host_ip_channel = jump_host_ip_transport.open_channel("direct-tcpip", dst_addr, src_addr)
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=self.host_ip, port=self.port, username=self.usr, password=self.pwd, sock=jump_host_ip_channel)
            return ssh_client
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            raise e

    def create_client(self, ip, port, user, pwd, key=""):
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if key == '':
                ssh_client.connect(hostname=ip, port=port, username=user, password=pwd, timeout=self.timeout)
            else:
                ssh_client.connect(hostname=ip, port=port, username=user, key_filename=key, timeout=self.timeout)
            return ssh_client
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            raise e

    def create_channel(self):
        try:
            self.transport = self.ssh_client.get_transport()
            self.channel = self.transport.open_session()
            self.channel.settimeout(self.timeout)
            self.channel.get_pty()
            self.channel.invoke_shell()
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            raise e

    def close(self):
        try:
            self.channel.close()
            self.transport.close()
            self.ssh_client.close()
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            raise e

    def exec_cmd(self, cmd, queue=None, verbose=False):
        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(cmd)
            msg = stdout.read().decode('utf-8')
            msg_err = stderr.read().decode('utf-8')
            if verbose:
                for line in msg.strip().split('\n'):
                    self.ssh_cs_log("STDOUT: " + line + "\n")
                for line in msg_err.strip().split('\n'):
                    self.ssh_cs_log("STDERR: " + line + "\n")
            if queue != None: queue.put(msg)
            return msg
        except Exception as e:
            self.close()
            traceback.print_tb(e.__traceback__)
            raise e

    def run_cmd_listen(self, cmd, queue=None, timeout=60, expect_str="", verbose=False):
        data = ""
        ssh_channel = self.ssh_client.invoke_shell()
        ssh_channel.timeout = timeout
        ssh_channel.send(cmd + '\n')
        while not ssh_channel.recv_ready(): time.sleep(5)
        current_time = time.time()
        try:
            while time.time() - current_time < timeout:
                if ssh_channel.recv_ready():
                    stdout = ssh_channel.recv(9999)
                    data = data + stdout.decode("ascii")
                    if verbose: sys.stdout.write(stdout.decode("ascii"))
                    if expect_str in data and expect_str != "": break
            if queue != None: queue.put(data)
            return data
        except socket.timeout:
            return data
        except Exception as e:
            self.close()
            traceback.print_tb(e.__traceback__)
            raise e

    def send(self, cmd):
        try:
            self.channel.send(cmd + '\n')
        except Exception as e:
            self.close()
            traceback.print_tb(e.__traceback__)
            raise e

    def receive(self, queue=None, timeout=60, expect_str="", verbose=False):
        data = ""
        self.channel.settimeout(timeout)
        current_time = time.time()
        try:
            while time.time() - current_time < timeout:
                if self.channel.recv_ready():
                    stdout = self.channel.recv(9999)
                    data += stdout.decode('utf-8')
                    if verbose: sys.stdout.write(stdout.decode("ascii"))
                    if expect_str in data and expect_str != "": break
            if queue != None: queue.put(data)
            return data
        except socket.timeout:
            return data
        except Exception as e:
            self.close()
            traceback.print_tb(e.__traceback__)
            raise e
