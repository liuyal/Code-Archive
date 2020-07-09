
import os, sys, time, subprocess

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
    # Array.append(ApClass(ssid="MG_TLS", pwd="12345678", usr="labtop.sierra.inmotion.com", type="ENT-TLS"))
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

def cslog(msg):

    time_stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print("[" + time_stamp + "] " + msg)


if __name__ == "__main__":

    if os.geteuid() != 0:
        sys.exit("Currently not super user, run as su.")

    if len(sys.argv) < 2:
        sys.exit("ERROR, no input parameter Enter ALEOS or MGOS")

    if sys.argv[1] == "ALEOS": ApArray = create_ApArray_ALEOS()
    else: ApArray = create_ApArray_MGOS()

    iface = "wlp2s0"
    host_name = "google.com"
    max_ping_fail = 5
    ping_failure = 0

    user_path = "/home/wolf"
    device_cert_path = user_path + "/Desktop/WiFi-Interop/Certificate/Device_4096.pem"
    root_cert_path = user_path + "/Desktop/WiFi-Interop/Certificate/ca_4096.pem"
    pkey_path = user_path + "/Desktop/WiFi-Interop/Certificate/Device_4096_unencrypted.key"

    cmd_wifi_off = "nmcli radio wifi off"
    cmd_wifi_on = "nmcli radio wifi on"
    cmd_ping = "ping -c 1 " + host_name

    cmd_list_profile = "ls /etc/NetworkManager/system-connections/"
    cmd_rm_profile = "rm /etc/NetworkManager/system-connections/"
    cmd_service_restart = "service NetworkManager restart"
    cmd_disconnect = "nmcli d disconnect iface " + iface

    cslog("Removing Wireless Network Profiles...")
    subprocess.Popen(cmd_wifi_off, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    time.sleep(1)

    out, err = subprocess.Popen(cmd_list_profile, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    profile_list = out.split('\n')
    for item in profile_list:
        if item == "": break
        out, err = subprocess.Popen(cmd_rm_profile + "\"" + item + "\"", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
        time.sleep(1)
    cslog("Profiles Removed, Restarting NetworkManager")
    subprocess.Popen(cmd_service_restart, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    time.sleep(2)

    subprocess.Popen(cmd_wifi_on, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    cslog("Starting Test\n")
    time.sleep(5)
    i = 0
    # main loop
    # Connect to AP and ping until 5 failures
    while True:
        item = ApArray[i]
        cslog("Attempt to connect to: " + item.ssid)
        # Clear DNS Cache
        if "ENT" in item.type:
            # Turn off
            subprocess.Popen(cmd_wifi_off, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
            time.sleep(1)
            # create profile
            cmd_create = "nmcli con add type wifi ifname " + iface + " con-name " + item.ssid + " ssid " + item.ssid
            out_c, err = subprocess.Popen(cmd_create, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
            cslog(out_c.replace('\n', ''))
            time.sleep(1)

            if "PEAP" in item.type:
                # edit profile
                cmd_edit_profile_1 = "nmcli c modify " + item.ssid + " 802-1x.eap PEAP 802-1x.identity " + item.username + " 802-1x.password " + item.password + " 802-1x.phase2-auth MSCHAPV2"
                subprocess.Popen(cmd_edit_profile_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
                time.sleep(1)
                cmd_edit_profile_2 = "nmcli c modify " + item.ssid + " wifi-sec.key-mgmt wpa-eap wifi.mode infrastructure"
                subprocess.Popen(cmd_edit_profile_2, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
                time.sleep(1)
            else:
                cmd_edit_profile_1 ="nmcli con mod "+item.ssid+" 802-1x.eap tls 802-1x.client-cert "+device_cert_path+" 802-1x.identity "+item.username +\
                " 802-1x.private-key-password "+item.password+" 802-1x.private-key "+pkey_path+" 802-1x.ca-cert "+root_cert_path
                out, err = subprocess.Popen(cmd_edit_profile_1, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True).communicate()
                time.sleep(1)
                cmd_edit_profile_2 = "nmcli c modify " + item.ssid + " wifi-sec.key-mgmt wpa-eap"
                subprocess.Popen(cmd_edit_profile_2, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
                time.sleep(1)
            # service restart
            subprocess.Popen(cmd_service_restart, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
            time.sleep(4)
            # turn on
            subprocess.Popen(cmd_wifi_on, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
            time.sleep(5)
            #  ping test
            while True:
                out_p, err = subprocess.Popen(cmd_ping, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()

                if " 0% packet loss" not in out_p:
                    ping_failure += 1
                    cslog(str(ping_failure) + " Consecutive Ping Failures")
                else:
                    cslog("Connected to: " + item.ssid + '\n' + out_p.replace('\n\n', '\n'))
                    ping_failure = 0

                if ping_failure >= max_ping_fail:
                    cslog("Max Ping Failure Reached, Resetting NetworkManager")
                    ping_failure = 0
                    subprocess.Popen(cmd_wifi_off, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
                    time.sleep(1)
                    subprocess.Popen(cmd_rm_profile + item.ssid, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
                    time.sleep(1)
                    subprocess.Popen(cmd_service_restart, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
                    time.sleep(4)
                    subprocess.Popen(cmd_wifi_on, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
                    time.sleep(3)
                    break
                time.sleep(2)
        else:
            # For open/wpa/wpa2 profiles
            if item.type == "OPEN":  cmd_connect = "nmcli d wifi connect " + item.ssid
            else: cmd_connect = "nmcli d wifi connect " + item.ssid + " password " + item.password
            out, err = subprocess.Popen(cmd_connect, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
            time.sleep(1)
            if out != "":
                cslog(out.replace('\n', '').replace('\r',''))
               # ping monitor
                while True:
                    out_p, err = subprocess.Popen(cmd_ping, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()

                    if " 0% packet loss" not in out_p:
                        ping_failure += 1
                        cslog(str(ping_failure) + " Consecutive Ping Failures")
                    else:
                        cslog("Connected to: " + item.ssid + '\n' + out_p.replace('\n\n','\n'))
                        ping_failure = 0

                    if ping_failure >= max_ping_fail:
                        cslog("Max Ping Failure Reached, Resetting NetworkManager")
                        ping_failure = 0
                        subprocess.Popen(cmd_wifi_off, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
                        time.sleep(1)
                        subprocess.Popen(cmd_rm_profile + item.ssid, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
                        time.sleep(1)
                        subprocess.Popen(cmd_service_restart, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
                        time.sleep(4)
                        subprocess.Popen(cmd_wifi_on, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
                        time.sleep(3)
                        break
                    time.sleep(2)
            else:
                cslog(err.replace('\n',''))

        time.sleep(5)
        i += 1
        if i == len(ApArray): i = 0; print("")