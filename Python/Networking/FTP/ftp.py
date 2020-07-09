import sys, os, time, shutil, ftplib, threading, random
from ftplib import FTP
import ssh_airlink

slash = '\\' if os.name == 'nt' else '/'

def FtpRmTree(ftp, path):
    wd = ftp.pwd()
    try: names = ftp.nlst(path)
    except ftplib.all_errors as e: return
    for name in names:
        if os.path.split(name)[1] in ('.', '..'): continue
        try:
            ftp.cwd(name)
            ftp.cwd(wd)
            FtpRmTree(ftp, name)
        except ftplib.all_errors: ftp.delete(name)
    try:ftp.rmd(path)
    except: return


def secondsToHMS(seconds):
    h = int(seconds/3600); m = int((seconds%3600)/60); s = int((seconds%3600)%60)
    hSting = str(h); mSting = str(m); sSting = str(s)
    if h < 10: hSting = "0"+ hSting
    if m < 10: mSting = "0"+ mSting
    if s < 10: sSting = "0"+ sSting
    return (hSting + ':' + mSting + ':' + sSting)


def humanbytes(B):
   B = float(B)
   KB = float(1024)
   MB = float(KB ** 2) # 1,048,576
   GB = float(KB ** 3) # 1,073,741,824
   TB = float(KB ** 4) # 1,099,511,627,776
   if B < KB: return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
   elif KB <= B < MB: return '{0:.2f} KB'.format(B/KB)
   elif MB <= B < GB: return '{0:.2f} MB'.format(B/MB)
   elif GB <= B < TB: return '{0:.2f} GB'.format(B/GB)
   elif TB <= B: return '{0:.2f} TB'.format(B/TB)


def save_results(results, time_stamp, file_name, flag=0):
    if flag == 0: action = "Upload"
    else: action = "Download"
    report_fd = ''
    result_dir = os.getcwd() + slash + "results"
    if not os.path.exists(result_dir): os.mkdir(result_dir)
    report_name = os.getcwd() + slash + "results" + slash + time_stamp + file_name
    try: report_fd = open(report_name, "w+"); cslog(""); cslog("Creating results under " + report_name)
    except IOError: cslog("File creation failed.")
    report_fd.write(action + " Test Start Time: " + time_stamp.split('_')[0] + ' ' + time_stamp.split('_')[1].replace('-',':')  + '\n\n')
    report_fd.write("-------------------------------------------\n")
    total_time = 0
    total_size = 0
    for i in results:
        session_time = 0
        session_size = 0
        for key in results[i]:
            total_time = total_time + results[i][key]["time"]
            total_size = total_size + results[i][key]["size"]
            session_time = session_time + results[i][key]["time"]
            session_size = session_size + results[i][key]["size"]
        report_fd.write("Cycle " + str(i) + ' ' + action + " Time: " + secondsToHMS(session_time) + '\n')
        report_fd.write("Cycle " + str(i) + ' ' + action + " Size: " + humanbytes(session_size) + '\n')
        report_fd.write("Cycle " + str(i) + ' ' + action + " Speed: " + humanbytes(session_size/session_time) + '/s\n\n')
    report_fd.write("\nTotal " + action + ' ' + "Time: " + secondsToHMS(total_time) + '\n')
    report_fd.write("Total " + action + ' ' + "Size: " + humanbytes(total_size) + '\n')
    report_fd.write("Average " + action + ' ' + "Time: " + secondsToHMS(total_time/len(results)) + '\n')
    report_fd.write("Average " + action + ' ' + "Size: " + humanbytes(total_size/len(results)) + '\n')
    report_fd.write("Average " + action + ' ' + "Speed: " + humanbytes( (total_size/len(results)) / (total_time/len(results)) ) + '/s\n')


def cslog(cmd):
    time_stamp = time.strftime("[%Y-%m-%d %H:%M:%S] ")

    if cmd == "":
        log_name_fd.write(cmd + '\n')
        log_name_fd.flush()
    else:
        log_name_fd.write(time_stamp + cmd + '\n')
        log_name_fd.flush()

    if cmd == "": print("")
    else: print(time_stamp + cmd)


def FTP_upload(HOST, PORT, USER, PWD, folder_name, cycle, DEBUG=False):
    path = os.getcwd()
    upload_folder_path = path + slash + folder_name

    try: os.listdir(upload_folder_path)
    except: sys.exit("The system cannot find the path specified")

    ftp = FTP(timeout=60)
    if DEBUG: ftp.set_debuglevel(2)
    cslog("Connecting to: " + str(HOST) + ':' + str(PORT))
    ftp.connect(HOST, PORT)
    cslog("Login to: " + str(USER) + ':' + str(PWD))
    ftp.login(USER, PWD)
    cslog("Removing FTP upload folder...")
    FtpRmTree(ftp,ftp.pwd())

    results = {}
    cslog("Starting FTP Upload Test")

    for folder in os.listdir(upload_folder_path):
        ftp.mkd(folder)
        ftp.cwd(folder)
        start_time = time.time()

        session_size = 0
        # https://stackoverflow.com/questions/19692739/python-ftplib-hangs-at-end-of-transfer
        for file in os.listdir(upload_folder_path + slash + folder):
            size = os.path.getsize(upload_folder_path + slash + folder + slash + file)
            session_size = session_size + size
            cslog("Uploading " + str(file) + " [" + humanbytes(size) + "] from " + folder)
            cmd =  upload_folder_path + slash + folder + slash + file
            cmd2 = 'STOR ' + ftp.pwd() + '/' + file
            ftp.storbinary(cmd2, open(cmd, 'rb'))
            ftp.voidcmd('NOOP')

        end_time = time.time()
        ftp.cwd("../")
        elapsed_time = end_time - start_time - len(os.listdir(upload_folder_path + slash + folder))
        results[folder] = {}
        results[folder]["time"] = elapsed_time
        results[folder]["size"] = session_size

    cslog("FTP Upload Test Complete")

    total_time = 0
    total_size = 0
    for key in sorted(results.iterkeys()):
        total_time = total_time + results[key]["time"]
        total_size = total_size + results[key]["size"]

    cslog("Cycle " + str(cycle) + " Total Download Time: " + secondsToHMS(total_time))
    cslog("Cycle " + str(cycle) + " Total Download Size: " + humanbytes(total_size))
    cslog("Cycle " + str(cycle) + " Download Speed: " + humanbytes(total_size/total_time) + "/s")
    cslog("Cleaning up upload folder @" + str(HOST) + ':' + str(PORT) + '...')
    FtpRmTree(ftp, ftp.pwd())
    ftp.quit()
    return results


def FTP_download(HOST, PORT, USER, PWD, folder_name, cycle, DEBUG=False):
    Download_Site = folder_name
    dir = os.getcwd() + slash + Download_Site
    if os.path.exists(dir): shutil.rmtree(dir)
    os.mkdir(dir)

    ftp = FTP(timeout=10)
    if DEBUG: ftp.set_debuglevel(2)
    cslog("Connecting to: " + str(HOST) + ':' + str(PORT))
    ftp.connect(HOST, PORT)
    cslog("Login to: " + str(USER) + ':' + str(PWD))
    ftp.login(USER, PWD)
    cslog("Removing FTP download folder: " + folder_name)

    results = {}
    cslog("Starting FTP Download Test")
    for folder in ftp.nlst():
        ftp.cwd(folder)
        os.mkdir(os.getcwd() + slash + Download_Site + slash + folder)
        start_time = time.time()
        filenames = ftp.nlst()

        session_size = 0

        for item in filenames:
            size = ftp.size(ftp.pwd() + '/' + item)
            session_size = session_size + int(size)
            cslog("Downloading " + str(item) + " [" + humanbytes(size) + "] from " + folder )
            serverfilepath = ftp.pwd() + '/' + item
            localfilepath = os.getcwd() + slash + Download_Site + slash + folder + slash + item
            ftp.retrbinary('RETR %s' % serverfilepath, open(localfilepath, 'wb').write)
            ftp.voidcmd('NOOP')

        end_time = time.time()
        elapsed_time = end_time - start_time - len(filenames)
        results[folder] = {}
        results[folder]["time"] = elapsed_time
        results[folder]["size"] = session_size
        ftp.cwd("../")

    cslog("FTP Download Test Complete")
    total_time = 0
    total_size = 0
    for key in sorted(results.iterkeys()):
        total_time = total_time + results[key]["time"]
        total_size = total_size + results[key]["size"]

    cslog("Cycle " + str(cycle) + " Total Upload Time: " + secondsToHMS(total_time))
    cslog("Cycle " + str(cycle) + " Total Upload Size: " + humanbytes(total_size))
    cslog("Cycle " + str(cycle) + " Upload Speed: " + humanbytes(total_size / total_time) + "/s")
    cslog("Cleaning up download folder @" + folder_name)
    if os.path.exists(dir): shutil.rmtree(dir)
    ftp.quit()
    return results

if __name__== "__main__":

    if len(sys.argv) < 2: sys.exit("Please enter -u upload or -d download as parameters")
    if len(sys.argv) < 3: sys.exit("Please enter number of cycles")
    if len(sys.argv) < 4: print("-debug for debug mode")
    try:
        if sys.argv[2] and sys.argv[3] == "-debug": debug = True
        else: debug = False
    except: debug = False

    time_stamp_main = time.strftime("%Y-%m-%d_%H-%M-%S_")
    log_dir = os.getcwd() + slash + "results"
    if not os.path.exists(log_dir): os.mkdir(log_dir)
    if sys.argv[1] == "upload" or sys.argv[1] == "-u": log_name = log_dir + slash + time_stamp_main + "upload_logs.log"
    else: log_name = log_dir + slash + time_stamp_main + "download_logs.log"
    try: log_name_fd = open(log_name, "w+")
    except IOError: cslog("File creation failed.")

    ssh_ip = "192.168.14.31"
    ssh_port = 22
    ssh_user = "root"
    ssh_pwd =  r'*=.qJ_BnAp~oeLr=7\yI'

    cnt = 0
    wait_time = 60
    min_sleep = 15
    max_sleep = 30
    total_result = {}
    while cnt < int(sys.argv[2]):
        cslog("")
        if sys.argv[1] == "upload" or sys.argv[1] == "-u": cslog("Upload Cycle " + str(cnt + 1))
        else: cslog("Download Cycle " + str(cnt + 1))

        try:
            if sys.argv[1] == "upload" or sys.argv[1] == "-u":
                # upload_results = FTP_upload("208.81.123.36", 15415, "pub", "123456", "Upload_Site", cnt+1, debug)
                # upload_results = FTP_upload("20.1.100.101", 21, "pub", "123456", "Upload_Site", cnt + 1, debug)
                upload_results = FTP_upload("192.171.1.112", 2023, "selva", "sierra!12345", "Upload_Site", cnt+1, debug)
                total_result[cnt + 1] = upload_results
            else:
                # download_results = FTP_download("208.81.123.36", 15415, "pub2", "123456", "Download_Site", cnt+1)
                download_results = FTP_download("192.168.13.100", 2022, "selva", "sierra!12345", "Download_Site", cnt+1, debug)
                total_result[cnt + 1] = download_results

        except KeyboardInterrupt:
                cslog("KeyboardInterrupt. Stopping script.")
                if cnt < 1: sys.exit("Less than 1 cycle")
                break
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            cslog(str(exc_type) + str(fname) + str(exc_tb))
            cslog(str(e))
            cslog("Error, retry connection in " + str(wait_time) + " seconds")
            cnt -= 1
            time.sleep(wait_time)
			
        cnt += 1
        rand_sleep = random.randint(min_sleep*60, max_sleep*60)
        print("Cyle complete! sleep for " + str(rand_sleep/60) + " minutes")
        time.sleep(rand_sleep)
		
    if sys.argv[1] == "upload" or sys.argv[1] == "-u":
        save_results(total_result, time_stamp_main, "upload_results.txt", 0)
    else:
        save_results(total_result, time_stamp_main, "download_results.txt", 1)
