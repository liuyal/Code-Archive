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
    return output


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


def wait(file, sleep_time):
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = '[' + time_stamp + '] Sleeping for ' + str(sleep_time) + 's...'
    print(msg)
    file.write(msg + '\n')
    file.flush()
    time.sleep(sleep_time)


def ping_flood(file, ssh):
    msg = '[' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] Running Ping Flood...\n'
    print(msg, end='')
    file.write(msg)
    file.flush()

    cmd = r'ping 10.100.2.2 -i 0.001 -c 1000'
    stdout = '\n'.join(run_ssh_cmd(ssh, cmd))

    msg = '[' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] Ping Flood Complete\n'
    print(msg, end='')
    file.write(msg)
    file.flush()


def vpn_tunnel_flush(file, ssh):
    msg = '[' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] Flushing VPN Shortcuts...\n'
    print(msg, end='')
    file.write(msg)
    file.flush()

    run_ssh_cmd(ssh, 'c v\ned spoke1\nd vpn t flush\n')

    cmd = 'c v\ned spoke1\nd sys sdwan service\n'
    stdout = run_ssh_cmd(ssh, cmd)
    for line in stdout:
        if line != '':
            print(str(line) + '\n', end='')
            file.write(msg)
            file.flush()


def check_sdwan_service(file, ssh):
    msg = '[' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '] Checking SDWAN service...\n'
    print(msg, end='')
    file.write(msg)
    file.flush()

    cmd = 'c v\ned spoke1\nd sys sdwan service\n'
    stdout = run_ssh_cmd(ssh, cmd)
    for line in stdout:
        if line != '':
            print(line + '\n', end='')
            file.write(line)
            file.flush()

    msg = '[' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ']\n'
    print(msg, end='')
    file.write(msg)
    file.flush()

    tunnel_list = []
    for line in stdout:
        if "Seq_num" in line and "gid" in line:
            tunnel_list.append(line)
            print(line + '\n', end='')
            file.write(line)
            file.flush()

    if len(tunnel_list) > 3:
        msg = '[' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " ERROR SDWAN CHECK Failed"
        print(msg + '\n', end='')
        file.write(msg)
        file.flush()

        for line in stdout:
            if line != '':
                print(line + '\n', end='')
                file.write(line)
                file.flush()


if __name__ == "__main__":

    fgt = create_ssh_client("172.18.16.174", "admin", "", False)
    pc141 = create_ssh_client("172.18.16.141", "root", "123456", False)

    time_stamp = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    if not os.path.exists(os.getcwd() + os.sep + "results"): os.mkdir(os.getcwd() + os.sep + "results")
    f = open(os.getcwd() + os.sep + "results" + os.sep + time_stamp + "_results.txt", 'a+')
    f.truncate(0)
    sleep_time = 10

    while True:
        vpn_tunnel_flush(f, fgt)

        wait(f, sleep_time)

        ping_flood(f, pc141)

        wait(f, sleep_time)

        check_sdwan_service(f, fgt)

        wait(f, sleep_time)

        vpn_tunnel_flush(f, fgt)
