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


def enable_policy(ssh, cmd):
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = '[' + time_stamp + '] Enabling firewall policy'
    print(msg)
    f.write(msg + '\n')
    f.flush()
    run_ssh_cmd(ssh, cmd)


def disable_policy(ssh, cmd):
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = '[' + time_stamp + '] Disabling firewall policy'
    print(msg)
    f.write(msg + '\n')
    f.flush()
    run_ssh_cmd(ssh, cmd)


def user1_ping(user, cmd, enabled):
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = '[' + time_stamp + '] Running Ping...'
    print(msg,end='')
    f.write(msg)
    f.flush()

    stdout = '\n'.join(run_ssh_cmd(user, cmd))

    if enabled:
        if ", 0% packet loss" not in stdout:
            sys.exit("ERROR")
        else:
            msg = 'Ping Successful!'
            print(msg)
            f.write(msg + '\n')
            f.flush()
    else:
        if ", 100% packet loss" not in stdout:
            sys.exit("ERROR")
        else:
            msg = 'Ping Failed Successful!'
            print(msg)
            f.write(msg + '\n')
            f.flush()


if __name__ == "__main__":

    time_stamp = datetime.datetime.now().strftime("%y%m%d_%H%M%S")

    f = open(os.getcwd() + os.sep + "vd1_cmd_template.txt", 'r')
    vd1_cmd_template = f.read()
    f.close()

    user1_cmd = "c v\n\ned user1\n\nexec ping-options repeat-count 1\n\nexec ping 20.100.1.2\n"
    policy_enable_cmd = vd1_cmd_template.replace("<SET>", "enable")
    policy_disable_cmd = vd1_cmd_template.replace("<SET>", "disable")

    fgt_user1 = create_ssh_client("172.18.71.91", "admin", "", False)
    fgt_vd1 = create_ssh_client("172.18.71.91", "admin", "", False)

    if not os.path.exists(os.getcwd() + os.sep + "results"): os.mkdir(os.getcwd() + os.sep + "results")
    f = open(os.getcwd() + os.sep + "results" + os.sep + time_stamp + "_results.txt", 'a+')
    f.truncate(0)
    sleep_time = 5

    while True:
        enable_policy(fgt_vd1, policy_enable_cmd)

        wait(f, sleep_time)

        user1_ping(fgt_user1, user1_cmd, True)

        wait(f, sleep_time)

        disable_policy(fgt_vd1, policy_disable_cmd)

        wait(f, sleep_time)

        user1_ping(fgt_user1, user1_cmd, False)

        wait(f, sleep_time)
