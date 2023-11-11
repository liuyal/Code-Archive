import os
import sys
import time
import datetime
import paramiko


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


if __name__ == "__main__":

    ssh = create_ssh_client("172.18.16.132", "root", "123456")

    shell = ssh.invoke_shell()
    output = shell.recv(1024)
    print(output)
    print(shell.send_ready())

    shell.send(b'snmpwalk -v 3 -u u1 172.18.16.189 .1.3.6 -On\n')

    counter = 0
    while True:
        output = shell.recv(1024)

        if output.decode("ascii") == '':
            counter += 1
        if counter >= 100:
            break

    print(1)