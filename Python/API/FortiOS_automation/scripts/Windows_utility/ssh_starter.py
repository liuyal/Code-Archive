import os
import sys
import time
import signal
import psutil
import subprocess


def get_sshd_pid():
    pid = 0
    cmd = "powershell netstat -ano | Select-string -Pattern :22"
    p = subprocess.Popen(cmd.split(' '), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate()
    for line in output.decode('utf-8').split('\n'):
        if "0.0.0.0:22" in line:
            text_list = list(filter(None, line.replace('\r', '').replace('\n', '').split(' ')))
            pid = int(text_list[-1])
    print("SSHD PID: " + str(pid))
    time.sleep(1)
    return pid


def restart_sshd(pid):
    # os.system('wmic process where name="sshd.exe" call terminate')
    os.system('taskkill /F /im ' + str(pid))
    os.system('powershell restart-service sshd')
    time.sleep(1)


def restart_wsl_service():
    os.system('wsl -u root -e sudo service ssh start')
    os.system('wsl -u root -e sudo service cron start')
    os.system('wsl -u root -e sudo service jenkins start')


if __name__ == "__main__":

    pid = get_sshd_pid()
    restart_sshd(pid)
    pid2 = get_sshd_pid()

    restart_wsl_service()

    if pid == pid2: sys.exit("ERROR: SSHD did not restart correctly...")
    print("SSHD Restarted. PID: " + str(pid2))
