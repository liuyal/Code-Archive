
import sys, os, time, subprocess

class ApClass():

    ssid = ""
    password = ""
    username = ""
    type = ""
    status = 0

    def __init__(self, ssid, pwd, usr, type):
        self.ssid = ssid
        self.password = pwd
        self.username = usr
        self.type = type


def create_ApArray_ALEOS():
    Array = []
    Array.append(ApClass(ssid="Airport1", pwd="", usr="", type="OPEN"))
    Array.append(ApClass(ssid="Airport2", pwd="1234567890", usr="", type="WPA/WPA2"))
    Array.append(ApClass(ssid="Airport3", pwd="1234567890", usr="", type="WPA/WPA2"))
    Array.append(ApClass(ssid="Airport4", pwd="", usr="", type="OPEN"))
    Array.append(ApClass(ssid="Airport5", pwd="1234567890", usr="", type="WPA/WPA2"))
    Array.append(ApClass(ssid="Airport6", pwd="1234567890", usr="", type="WPA/WPA2"))
    Array.append(ApClass(ssid="Airport7", pwd="1234567890", usr="", type="WPA/WPA2"))
    Array.append(ApClass(ssid="Airport8", pwd="1234567890", usr="", type="WPA/WPA2"))
    Array.append(ApClass(ssid="Airport9", pwd="newworld", usr="peapuser", type="ENT-PEAP"))
    Array.append(ApClass(ssid="Airport10", pwd="", usr="", type="OPEN"))
    Array.append(ApClass(ssid="Airport11", pwd="1234567890", usr="", type="WPA/WPA2"))
    Array.append(ApClass(ssid="Airport12", pwd="1234567890", usr="", type="WPA/WPA2"))
    Array.append(ApClass(ssid="Airport13", pwd="newworld", usr="peapuser", type="ENT-PEAP"))
    Array.append(ApClass(ssid="Airport14", pwd="1234567890", usr="", type="WPA/WPA2"))
    Array.append(ApClass(ssid="Airport15", pwd="1234567890", usr="", type="WPA/WPA2"))
    Array.append(ApClass(ssid="Airport16", pwd="newworld", usr="peapuser", type="ENT-PEAP"))
    Array.append(ApClass(ssid="Airport17", pwd="1234567890", usr="", type="WPA/WPA2"))
    Array.append(ApClass(ssid="Airport18", pwd="1234567890", usr="", type="WPA/WPA2"))
    Array.append(ApClass(ssid="Airport19", pwd="newworld", usr="peapuser", type="ENT-PEAP"))
    return Array

def create_ApArray_MGOS():
    Array = []
    Array.append(ApClass(ssid="MG_AP1", pwd="", usr="", type="OPEN"))
    Array.append(ApClass(ssid="MG_AP2", pwd="1234567890", usr="", type="WPA/WPA2"))
    Array.append(ApClass(ssid="MG_AP3", pwd="newworld", usr="peapuser", type="ENT-PEAP"))
    Array.append(ApClass(ssid="MG_AP4", pwd="1234567890", usr="", type="WPA/WPA2"))
    Array.append(ApClass(ssid="MG_AP5", pwd="newworld", usr="peapuser", type="ENT-PEAP"))
    Array.append(ApClass(ssid="MG_AP6", pwd="", usr="", type="OPEN"))
    Array.append(ApClass(ssid="MG_AP7", pwd="1234567890", usr="", type="WPA/WPA2"))
    Array.append(ApClass(ssid="MG_AP8", pwd="newworld", usr="peapuser", type="ENT-PEAP"))
    Array.append(ApClass(ssid="MG_AP9", pwd="", usr="", type="OPEN"))
    Array.append(ApClass(ssid="MG_AP10", pwd="1234567890", usr="", type="WPA/WPA2"))
    Array.append(ApClass(ssid="MG_AP11", pwd="newworld", usr="peapuser", type="ENT-PEAP"))
    Array.append(ApClass(ssid="MG_AP12", pwd="", usr="", type="OPEN"))
    Array.append(ApClass(ssid="MG_AP13", pwd="1234567890", usr="", type="WPA/WPA2"))
    Array.append(ApClass(ssid="MG_AP14", pwd="newworld", usr="peapuser", type="ENT-PEAP"))
    Array.append(ApClass(ssid="MG_AP15", pwd="", usr="", type="OPEN"))
    Array.append(ApClass(ssid="MG_AP16", pwd="1234567890", usr="", type="WPA/WPA2"))
    Array.append(ApClass(ssid="MG_AP17", pwd="newworld", usr="peapuser", type="ENT-PEAP"))
    return Array


def preferred_ent_check(cmd, ent_array):
    out, err = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    preferred_list = out.split('\n\t')
    for item in ent_array:
        if item not in preferred_list: cslog("ENT: " + item + " Not found in preferred list")


def cslog(msg):
    time_stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print("[" + time_stamp + "] " + msg)



if __name__ == "__main__":
    print("")

    if len(sys.argv) < 2:
        sys.exit("Error, no input parameter.\nPlease enter ALEOS or MGOS")

    if sys.argv[1] == "ALEOS": ApArray = create_ApArray_ALEOS()
    else: ApArray = create_ApArray_MGOS()

    ENT_Array = ["MG_AP3","MG_AP5","MG_AP8","MG_AP11","MG_AP14","MG_AP17","Airport9","Airport13","Airport16","Airport19"]

    interface = "en0"
    host_name = "google.com"
    ping_failure = 0
    max_ping_fail = 5
    counter = 0

    cmd_wifi_off = "networksetup -setairportpower " + interface + " off"
    cmd_wifi_on = "networksetup -setairportpower " + interface + " on"
    cmd_remove_all = "networksetup -removeallpreferredwirelessnetworks " + interface
    cmd_remove = "networksetup -removepreferredwirelessnetwork " + interface + " "

    cmd_list_preferred = "networksetup -listpreferredwirelessnetworks " + interface
    cmd_ping = "ping -c 1 " + host_name
    cmd_add_prefer_tail = "networksetup -addpreferredwirelessnetworkatindex " + interface + " end_header 99 open"

    cmd_find_key = "security find-generic-password "
    cmd_remove_key = "security delete-generic-password "
    cmd_flush_dns = "sudo killall -HUP mDNSResponder"

    subprocess.Popen(cmd_add_prefer_tail, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    time.sleep(1)

    preferred_ent_check(cmd_list_preferred, ENT_Array)

    cslog("Removing Preferred Wireless Network...")
    subprocess.Popen(cmd_wifi_off, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    time.sleep(1)
    out, err = subprocess.Popen(cmd_list_preferred, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()

    preferred_list = out.split('\n\t')

    for item in preferred_list[1:len(preferred_list)]:
        if item not in ENT_Array:
            out, err = subprocess.Popen(cmd_remove + item.replace('\n',''), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
            cslog(out.replace('\n','')); time.sleep(1)
        else:
            cslog("Will not remove: " + item + ", Found in ENT Array")

    subprocess.Popen(cmd_wifi_on, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    cslog("Starting Test\n")
    time.sleep(1)

    start = time.time()
    i = 0
    # main loop
    # Connect to AP and ping until 5 failures
    while True :

        item = ApArray[i]
        cslog("Flushing DNS Cache")
        subprocess.Popen(cmd_flush_dns, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
        
        cslog("Trying to connect to: " + item.ssid)
        if "ENT" in item.type:
            # For eap-peap profiles
            cslog("Auto Connect to Active ENT-AP: " + item.ssid)
            subprocess.Popen(cmd_wifi_off, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
            time.sleep(2)
            subprocess.Popen(cmd_wifi_on, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
            time.sleep(2)
            # ping monitor
            while True:
                try: out, err = subprocess.Popen(cmd_ping, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
                except: out = "Ping Failed"

                if " 0.0% packet loss" not in out or "Ping Failed" in out:
                    ping_failure += 1
                    cslog(str(ping_failure) + " Consecutive Ping Failures")
                else:
                    cmd_airport = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I | awk '/ SSID/ {print substr($0, index($0, $2))}'"
                    out1, err = subprocess.Popen(cmd_airport, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
                    cslog("Connected to: " + out1.replace('\n','') + '\n' + out.replace('\n\n', '\n'))
                    ping_failure = 0

                if ping_failure >= max_ping_fail:
                    cslog("Max Ping Failure Reached")
                    cslog("Attempt to connect to next SSID")
                    ping_failure = 0
                    break
                time.sleep(2)
        else:
            # For open/wpa/wpa2 profiles
            cmd_connect = "networksetup -setairportnetwork " + interface + " " + item.ssid + " " + item.password
            out, err = subprocess.Popen(cmd_connect, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
            time.sleep(1)

            if out == "" :
                cslog("Connection Established. Try to Ping internet...")
                # ping monitor
                while True:
                    try: out, err = subprocess.Popen(cmd_ping, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
                    except: out = "Ping Failed"

                    if " 0.0% packet loss" not in out or "Ping Failed" in out:
                        ping_failure += 1
                        cslog(str(ping_failure) + " Consecutive Ping Failures")
                    else:
                        cmd_airport = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I | awk '/ SSID/ {print substr($0, index($0, $2))}'"
                        out1, err = subprocess.Popen(cmd_airport, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
                        cslog("Connected to: " + out1.replace('\n', '') + '\n' + out.replace('\n\n', '\n'))
                        ping_failure = 0

                    if ping_failure >= max_ping_fail:
                        cslog("Max Ping Failure Reached. Attempt to connect to next SSID")
                        ping_failure = 0
                        subprocess.Popen(cmd_wifi_off, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
                        time.sleep(1)
                        out, err = subprocess.Popen(cmd_remove + item.ssid, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
                        time.sleep(1)
                        subprocess.Popen(cmd_wifi_on, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
                        time.sleep(2)
                        break
                    time.sleep(2)
            else:
                cslog(out.replace('\n',''))
        time.sleep(1)
        i += 1
        if i == len(ApArray): i = 0; print("")