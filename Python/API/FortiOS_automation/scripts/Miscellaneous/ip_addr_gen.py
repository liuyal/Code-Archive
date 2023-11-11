import os
import sys
import time
import threading
import subprocess


def ping_run(id, cmd):
    command = cmd.split()
    output, error = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    sys.stdout.write("[" + str(id) + "] " + cmd + " | " + '\n')


if __name__ == "__main__":
    # cmd = "ip -6 addr add 2011::<I> dev ens192"
    #
    # for i in range(2, 255):
    #     cm = cmd.replace('<I>', str(i))
    #     print(cm)
    #
    # cmd2 = "sudo ip addr add 11.1.1.<I>/24 dev ens192"
    # for i in range(2, 255):
    #     cm = cmd2.replace('<I>', str(i))
    #     print(cm)


    if sys.argv[1] == "-6":
        cmd_ping = "ping6 2013::10 -I 2011::<I> -c 2"
    else:
        cmd_ping = "ping 13.1.1.10 -I 11.1.1.<I> -c 2"

    print(cmd_ping)

    thread_list = []

    for i in range(2, 255):
        cmd_thread = cmd_ping.replace("<I>", str(i))
        thread = threading.Thread(target=ping_run, args=(i, cmd_thread))
        thread_list.append(thread)

    for item in thread_list:
        item.start()

    for item in thread_list:
        item.join()
