import os
import sys
import time
import datetime
import subprocess

if __name__ == "__main__":

    try:
        bn = '_' + sys.argv[1]
    except:
        bn = ''

    input_path = os.getcwd() + os.sep + "input.txt"
    output_path = 'capture' + bn + '.pcap'

    if sys.platform == "win32":
        fgt2 = os.getcwd() + os.sep + "fgt2eth.exe"
        subprocess.check_call([fgt2, "-in", input_path, "-out", output_path])
    else:
        fgt2 = os.getcwd() + os.sep + "fgt2.pl"
        subprocess.check_call(["perl", fgt2, input_path, output_path])
