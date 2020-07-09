import os, sys, time, subprocess, shutil
import binascii, random
#Computer\HKEY_CURRENT_USER\Software\Microsoft\Wlansvc\UserData\Profiles\
#Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Profiles\

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
    Array.append(ApClass(ssid="Airport2", pwd="1234567890", usr="", type="WPA-TKIP"))
    Array.append(ApClass(ssid="Airport3", pwd="1234567890", usr="", type="WPA-AES"))
    Array.append(ApClass(ssid="Airport4", pwd="", usr="", type="OPEN"))
    Array.append(ApClass(ssid="Airport5", pwd="1234567890", usr="", type="WPA-TKIP"))
    Array.append(ApClass(ssid="Airport6", pwd="1234567890", usr="", type="WPA-AES"))
    Array.append(ApClass(ssid="Airport7", pwd="1234567890", usr="", type="WPA2-AES"))
    Array.append(ApClass(ssid="Airport8", pwd="1234567890", usr="", type="WPA2-TKIP"))
    Array.append(ApClass(ssid="Airport9", pwd="newworld", usr="peapuser", type="WPA2-ENT"))
    Array.append(ApClass(ssid="Airport10", pwd="", usr="", type="OPEN"))
    Array.append(ApClass(ssid="Airport11", pwd="1234567890", usr="", type="WPA2-AES"))
    Array.append(ApClass(ssid="Airport12", pwd="1234567890", usr="", type="WPA2-TKIP"))
    Array.append(ApClass(ssid="Airport13", pwd="newworld", usr="peapuser", type="WPA2-ENT"))
    Array.append(ApClass(ssid="Airport14", pwd="1234567890", usr="", type="WPA2-AES"))
    Array.append(ApClass(ssid="Airport15", pwd="1234567890", usr="", type="WPA2-TKIP"))
    Array.append(ApClass(ssid="Airport16", pwd="newworld", usr="peapuser", type="WPA2-ENT"))
    Array.append(ApClass(ssid="Airport17", pwd="1234567890", usr="", type="WPA2-AES"))
    Array.append(ApClass(ssid="Airport18", pwd="1234567890", usr="", type="WPA2-TKIP"))
    Array.append(ApClass(ssid="Airport19", pwd="newworld", usr="peapuser", type="WPA2-ENT"))
    return Array

def create_ApArray_MGOS():
    Array = []
    Array.append(ApClass(ssid="MG_AP1", pwd="", usr="", type="OPEN"))
    Array.append(ApClass(ssid="MG_AP2", pwd="1234567890", usr="", type="WPA"))
    Array.append(ApClass(ssid="MG_AP3", pwd="newworld", usr="peapuser", type="WPA-ENT"))
    Array.append(ApClass(ssid="MG_AP4", pwd="1234567890", usr="", type="WPA2"))
    Array.append(ApClass(ssid="MG_AP5", pwd="newworld", usr="peapuser", type="WPA2-ENT"))
    Array.append(ApClass(ssid="MG_AP6", pwd="", usr="", type="OPEN"))
    Array.append(ApClass(ssid="MG_AP7", pwd="1234567890", usr="", type="WPA2"))
    Array.append(ApClass(ssid="MG_AP8", pwd="newworld", usr="peapuser", type="WPA2-ENT"))
    Array.append(ApClass(ssid="MG_AP9", pwd="", usr="", type="OPEN"))
    Array.append(ApClass(ssid="MG_AP10", pwd="1234567890", usr="", type="WPA2"))
    Array.append(ApClass(ssid="MG_AP11", pwd="newworld", usr="peapuser", type="WPA2-ENT"))
    Array.append(ApClass(ssid="MG_AP12", pwd="", usr="", type="OPEN"))
    Array.append(ApClass(ssid="MG_AP13", pwd="1234567890", usr="", type="WPA2"))
    Array.append(ApClass(ssid="MG_AP14", pwd="newworld", usr="peapuser", type="WPA2-ENT"))
    Array.append(ApClass(ssid="MG_AP15", pwd="", usr="", type="OPEN"))
    Array.append(ApClass(ssid="MG_AP16", pwd="1234567890", usr="", type="WPA2"))
    Array.append(ApClass(ssid="MG_AP17", pwd="newworld", usr="peapuser", type="WPA2-ENT"))
    return Array

def cslog(msg):
    time_stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print("[" + time_stamp + "] " + msg)

# Create xml profiles base on testcase arrays
def create_profiles(ApArray, ENT_Array):
    cslog("Creating test case wifi profiles")
    path = os.getcwd()+ "\\" + "profiles"
    while True:
        try:
            if os.path.exists(path): shutil.rmtree(path)
            os.mkdir(path)
            break
        except:
            print("Access Denied Retry...")
            time.sleep(1)

    for item in ApArray:
        if item.ssid not in ENT_Array:
            if item.type == "OPEN":
                with open("templates\open_template.xml",'r') as stream: template = stream.read()
                hex = binascii.hexlify(item.ssid).upper()
                file_name = "Wi-Fi-" + item.ssid + ".xml"
                seed = int(str(random.randint(1000000000,4000000000)))
                raw_xml = template.replace("<name></name>","<name>" + item.ssid + "</name>")
                raw_xml = raw_xml.replace("<hex></hex>","<hex>" + hex + "</hex>")
                raw_xml = raw_xml.replace("<randomizationSeed></randomizationSeed>","<randomizationSeed>" + str(seed) + "</randomizationSeed>")
                file_id = open(path + "\\" + file_name,'w')
                file_id.write(raw_xml)
                file_id.close()
            elif item.type == "WPA" or item.type == "WPA-TKIP":
                with open("templates\wpa_psk_template.xml",'r') as stream: template = stream.read()
                hex = binascii.hexlify(item.ssid).upper()
                file_name = "Wi-Fi-" + item.ssid + ".xml"
                seed = int(str(random.randint(1000000000, 4000000000)))
                raw_xml = template.replace("<name></name>","<name>" + item.ssid + "</name>")
                raw_xml = raw_xml.replace("<hex></hex>","<hex>" + hex + "</hex>")
                raw_xml = raw_xml.replace("<randomizationSeed></randomizationSeed>","<randomizationSeed>" + str(seed) + "</randomizationSeed>")
                file_id = open(path + "\\" + file_name,'w')
                file_id.write(raw_xml)
                file_id.close()
            elif item.type == "WPA-AES":
                with open("templates\wpa_aes_template.xml", 'r') as stream: template = stream.read()
                hex = binascii.hexlify(item.ssid).upper()
                file_name = "Wi-Fi-" + item.ssid + ".xml"
                seed = int(str(random.randint(1000000000, 4000000000)))
                raw_xml = template.replace("<name></name>", "<name>" + item.ssid + "</name>")
                raw_xml = raw_xml.replace("<hex></hex>", "<hex>" + hex + "</hex>")
                raw_xml = raw_xml.replace("<randomizationSeed></randomizationSeed>","<randomizationSeed>" + str(seed) + "</randomizationSeed>")
                file_id = open(path + "\\" + file_name, 'w')
                file_id.write(raw_xml)
                file_id.close()
            elif item.type == "WPA-ENT":
                with open("templates\wpa_ent_template.xml",'r') as stream: template = stream.read()
                hex = binascii.hexlify(item.ssid).upper()
                file_name = "Wi-Fi-" + item.ssid + ".xml"
                seed = int(str(random.randint(1000000000, 4000000000)))
                raw_xml = template.replace("<name></name>","<name>" + item.ssid + "</name>")
                raw_xml = raw_xml.replace("<hex></hex>","<hex>" + hex + "</hex>")
                raw_xml = raw_xml.replace("<randomizationSeed></randomizationSeed>","<randomizationSeed>" + str(seed) + "</randomizationSeed>")
                file_id = open(path + "\\" + file_name,'w')
                file_id.write(raw_xml)
                file_id.close()
            elif item.type == "WPA2" or item.type == "WPA2-AES":
                with open("templates\wpa2_psk_template.xml", 'r') as stream: template = stream.read()
                hex = binascii.hexlify(item.ssid).upper()
                file_name = "Wi-Fi-" + item.ssid + ".xml"
                seed = int(str(random.randint(1000000000, 4000000000)))
                raw_xml = template.replace("<name></name>", "<name>" + item.ssid + "</name>")
                raw_xml = raw_xml.replace("<hex></hex>", "<hex>" + hex + "</hex>")
                raw_xml = raw_xml.replace("<randomizationSeed></randomizationSeed>","<randomizationSeed>" + str(seed) + "</randomizationSeed>")
                file_id = open(path + "\\" + file_name, 'w')
                file_id.write(raw_xml)
                file_id.close()
            elif item.type == "WPA2-TKIP":
                with open("templates\wpa2_tkip_template.xml", 'r') as stream: template = stream.read()
                hex = binascii.hexlify(item.ssid).upper()
                file_name = "Wi-Fi-" + item.ssid + ".xml"
                seed = int(str(random.randint(1000000000, 4000000000)))
                raw_xml = template.replace("<name></name>", "<name>" + item.ssid + "</name>")
                raw_xml = raw_xml.replace("<hex></hex>", "<hex>" + hex + "</hex>")
                raw_xml = raw_xml.replace("<randomizationSeed></randomizationSeed>","<randomizationSeed>" + str(seed) + "</randomizationSeed>")
                file_id = open(path + "\\" + file_name, 'w')
                file_id.write(raw_xml)
                file_id.close()
            elif item.type == "WPA2-ENT":
                with open("templates\wpa2_ent_template.xml", 'r') as stream: template = stream.read()
                hex = binascii.hexlify(item.ssid).upper()
                file_name = "Wi-Fi-" + item.ssid + ".xml"
                seed = int(str(random.randint(1000000000, 4000000000)))
                raw_xml = template.replace("<name></name>", "<name>" + item.ssid + "</name>")
                raw_xml = raw_xml.replace("<hex></hex>", "<hex>" + hex + "</hex>")
                raw_xml = raw_xml.replace("<randomizationSeed></randomizationSeed>","<randomizationSeed>" + str(seed) + "</randomizationSeed>")
                file_id = open(path + "\\" + file_name, 'w')
                file_id.write(raw_xml)
                file_id.close()

# perferred ent_list check
def preferred_ent_check(cmd_profile_list, ent_array):
    out, err = subprocess.Popen(cmd_profile_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True).communicate()
    profile_list = []
    for item in out.replace('\r', '').split('\n'):
        if "All User Profile" in item: profile_list.append(item.split(': ')[1])

    for item in ent_array:
        if item not in profile_list:
            cslog("ENT Profile: " + item + " Not found in profile list")


if __name__ == "__main__":
	
    if len(sys.argv) < 2: sys.exit("Please enter ALEOS or MGOS as parameters")
    if sys.argv[1] == "ALEOS": ApArray = create_ApArray_ALEOS()
    else: ApArray = create_ApArray_MGOS()

    # list of aps not to be removed
    ENT_Array = ["MG_AP3","MG_AP5","MG_AP8","MG_AP11","MG_AP14","MG_AP17","Airport9","Airport13","Airport16","Airport19"]

    iface = "wlan"
    host_name = "google.com"
    max_ping_fail = 5
    ping_failure = 0

    cmd_off = "netsh interface set interface Wi-Fi disable"
    cmd_on = "netsh interface set interface Wi-Fi enable"
    cmd_profile_list = "netsh " + iface + " show profiles"
    cmd_ping = "ping -n 1 " + host_name
    cmd_disconnect = "netsh wlan disconnect"
    cmd_flush_dns = "ipconfig /flushdns"

    cslog("Turn on wifi")
    out, err = subprocess.Popen(cmd_on, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    if "(Run as administrator)" in out: sys.exit(out.replace('\n','').replace('\r',''))
    time.sleep(1)

    preferred_ent_check(cmd_profile_list, ENT_Array)

    out, err = subprocess.Popen(cmd_profile_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    time.sleep(1)
    profile_list = []
    for item in out.replace('\r','').split('\n'):
        if "All User Profile" in item: profile_list.append(item.split(': ')[1])

    cslog("Removing Wireless Network Profiles...")
    for item in profile_list:
        if item not in ENT_Array:
            cmd_remove_item = "netsh wlan delete profile name=\"" + item + "\""
            out, err = subprocess.Popen(cmd_remove_item, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
            cslog(out.replace('\r\n', ''))
            time.sleep(1)

    create_profiles(ApArray, ENT_Array)

    profile_path = os.getcwd() + "\\" + "profiles"
    files = os.listdir(profile_path)
    for item in files:
        if item.split('.')[0].split('-')[2] not in ENT_Array:
            cmd_add_profile = "netsh " + iface + " add profile filename=\"" + profile_path + '\\' + item + '\"'
            out, err = subprocess.Popen(cmd_add_profile, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
            cslog(out.replace('\r','').replace('\n',''))

    cslog("Starting Test\n")
    time.sleep(3)
    i = 0
    # main loop
    # Connect to AP and ping until 5 failures
    while True:
        item = ApArray[i]
        cslog("Flush DNS Cache")
        subprocess.Popen(cmd_flush_dns, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
		
        cslog("Attempt to connect to: " + item.ssid)
        # For eap-peap profiles
        if "ENT" in item.type:
            cmd_connect = "netsh wlan connect name=\"" + item.ssid + '\"'
            out, err = subprocess.Popen(cmd_connect, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
            cslog(out.replace('\r', '').replace('\n', ''))
            time.sleep(2)

            cslog("Check for ping...")
            # ping monitor
            while True:
                out_p, err = subprocess.Popen(cmd_ping, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True).communicate()

                if "(0% loss)" not in out_p:
                    ping_failure += 1
                    cslog(str(ping_failure) + " Consecutive Ping Failures")
                else:
                    cslog("Connected to: " + item.ssid + '\n' + out_p.replace('\r\n\r\n', '\n')[2:len(out_p)])
                    ping_failure = 0

                if ping_failure >= max_ping_fail:
                    cslog("Max Ping Failure Reached, Resetting NetworkManager")
                    ping_failure = 0
                    out, err = subprocess.Popen(cmd_disconnect, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True).communicate()
                    break
                time.sleep(2)
        else:
            # For open/wpa/wpa2 profiles
            cmd_connect = "netsh wlan connect name=\"" + item.ssid + '\"'
            out, err = subprocess.Popen(cmd_connect, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True).communicate()
            cslog(out.replace('\r', '').replace('\n', ''))
            time.sleep(2)
            cslog("Check for ping...")
            # ping monitor
            while True:
                out_p, err = subprocess.Popen(cmd_ping, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True).communicate()

                if "(0% loss)" not in out_p:
                    ping_failure += 1
                    cslog(str(ping_failure) + " Consecutive Ping Failures")
                else:
                    cslog("Connected to: " + item.ssid + '\n' + out_p.replace('\r\n\r\n','\n')[2:len(out_p)])
                    ping_failure = 0

                if ping_failure >= max_ping_fail:
                    cslog("Max Ping Failure Reached, Resetting NetworkManager")
                    ping_failure = 0
                    out, err = subprocess.Popen(cmd_disconnect, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
                    break
                time.sleep(2)
        time.sleep(2)
        i += 1
        if i == len(ApArray): i = 0; print("")
