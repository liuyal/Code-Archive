import sys, time, subprocess, os

# cmd = "iperf -c 192.168.5.1 -p6000 -t600"
cmd = "ping -n 1 8.8.8.8"

for cnt in range(0,10):
    print ("----------------------- Cycle " + str(cnt+1)+ " -----------------------")
    # out, err = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    # print(out)
    os.system(cmd)
    time.sleep(5)