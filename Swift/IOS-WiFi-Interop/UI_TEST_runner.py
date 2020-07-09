import subprocess, time, os, sys
import shlex

if __name__ == "__main__":

    ALEOS = '''xcodebuild -workspace Wifi_test.xcworkspace -scheme "Wifi_testUITests" -destination 'platform=iOS,name=iPhone6' -destination 'platform=iOS,name=iPadmini' -destination 'platform=iOS,name=iPad5' '-only-testing:Wifi_testUITests/Wifi_testUITests/testTimer_ALEOS' test'''
    MGOS = '''xcodebuild -workspace Wifi_test.xcworkspace -scheme "Wifi_testUITests" -destination 'platform=iOS,name=iPhone6' -destination 'platform=iOS,name=iPadmini' -destination 'platform=iOS,name=iPad5' '-only-testing:Wifi_testUITests/Wifi_testUITests/testTimer_MGOS' test'''
    duration = 5*60*60
    wait_time = 10

    if len(sys.argv) < 2: sys.exit("ERROR, no input parameter Enter ALEOS or MGOS")

    print("Starting UI Test Script in "+str(wait_time/2)+" seconds...")
    time.sleep(wait_time/2)

    while True:

        if sys.argv[1] == "ALEOS": proc = subprocess.Popen(ALEOS,shell=True)
        else: proc = subprocess.Popen(MGOS,shell=True)

        print("Start process with pid " + str(proc.pid) + " | Run for " + str(int(duration/60)) + " minutes")

        time.sleep(duration)

        if proc.poll() is None:
            print ("Killing process with pid " + str(proc.pid))
            proc.kill()
            print("Sleep for %d seconds" %wait_time)
            time.sleep(wait_time)