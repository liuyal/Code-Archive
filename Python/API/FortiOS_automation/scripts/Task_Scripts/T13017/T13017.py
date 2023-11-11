import os
import sys
import time
import datetime
import paramiko


def run_ssh_cmd(ssh, cmd):
    output = []
    stdin, stdout, stderr = ssh.exec_command(cmd)
    for line in stdout.read().split(b'\n'):
        line = str(line.decode('utf-8'))
        output.append(line)
    return '\n'.join(output)


def create_ssh_client(host_ip, host_usr='admin', host_pwd="", jump_host=True):
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


def log(f, text):
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = '[' + time_stamp + '] ' + text
    print(msg)
    f.write(msg + '\n')
    f.flush()


def wait(file, sleep_time):
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = '[' + time_stamp + '] Sleeping for ' + str(sleep_time) + 's...'
    print(msg)
    file.write(msg + '\n')
    file.flush()
    time.sleep(sleep_time)


def clear_log(ssh):
    cmd = 'c v\ned vd1\nexec log delete-all\ny\n'
    run_ssh_cmd(ssh, cmd)


def read_log(file, ssh):
    cmd = 'c v\ned vd1\nexec log filter category 1\nexec log display\n'
    res = run_ssh_cmd(ssh, cmd)
    output = res.splitlines()
    for i in range(0, len(output)):
        if 'Service disabled caused by no outgoing path' not in output[i]:
            output[i] = ''
    output = list(filter(None, output))
    file.write('\n' + '\n'.join(output) + '\n\n')
    file.flush()
    print('\n'.join(output) + '\n')


if __name__ == "__main__":
    time_stamp = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    fgt = create_ssh_client("10.59.71.82", jump_host=True)

    disable_intf_cmd = 'c v\ned root\nc sys int\ned r10\nset status down\nnext\n\ned r20\nset status down\nend\n'
    enable_intf_cmd = 'c v\ned root\nc sys int\ned r10\nset status up\nnext\n\ned r20\nset status up\nend\n'

    if not os.path.exists(os.getcwd() + os.sep + "results"): os.mkdir(os.getcwd() + os.sep + "results")
    f = open(os.getcwd() + os.sep + "results" + os.sep + time_stamp + "_results.txt", 'a+')
    f.truncate(0)

    while True:
        log(f, "Enable interface")
        run_ssh_cmd(fgt, enable_intf_cmd)

        wait(f, 5)

        log(f, "clear log")
        clear_log(fgt)

        wait(f, 5)

        log(f, "Disable interface")
        run_ssh_cmd(fgt, disable_intf_cmd)

        wait(f, 20)

        log(f, "read log")
        read_log(f, fgt)

        wait(f, 5)
