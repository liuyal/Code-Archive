import os
import sys
import time
import stat
import shutil
import subprocess


def git_clone(url, folder):
    if os.path.exists(os.getcwd() + os.sep + folder):
        shutil.rmtree(os.getcwd() + os.sep + folder)
    cmd = "git clone " + url + ' ' + folder
    p = subprocess.Popen(cmd.split(' '), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate()
    print(cmd)
    print(output.decode('utf-8'))
    print(err.decode('utf-8'))


def clean_git_folder(folder):
    print("Clean " + folder + " folder")
    for file_name in os.listdir(os.getcwd() + os.sep + folder):
        if '.git' not in file_name or '.gitignore' == file_name:
            if os.path.isdir(os.getcwd() + os.sep + folder + os.sep + file_name):
                shutil.rmtree(os.getcwd() + os.sep + folder + os.sep + file_name)
            else:
                os.remove(os.getcwd() + os.sep + folder + os.sep + file_name)


def sync_folder(src_folder, dst_folder):
    print("Sync " + dst_folder + " folder with " + src_folder + "...")
    for file_name in os.listdir(os.getcwd() + os.sep + src_folder):
        if '.git' != file_name:
            shutil.move(os.getcwd() + os.sep + src_folder + os.sep + file_name, os.getcwd() + os.sep + dst_folder)


def git_commit_push(folder, clear_cache=False):
    print("Running git commands in " + folder + "...")
    cmd0 = 'cd ' + os.getcwd() + os.sep + folder
    cmd1 = 'git rm -r --cached .'
    cmd2 = 'git add .'
    cmd3 = 'git commit -am "Auto update"'
    cmd4 = "git push"

    if clear_cache:
        cmd_list = [cmd0, cmd1, cmd2, cmd3, cmd4]
    else:
        cmd_list = [cmd0, cmd2, cmd3, cmd4]
    cmd = ' && '.join(cmd_list)
    os.system(cmd)
    time.sleep(1)


def on_rm_error(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)


def clean_up(folder):
    print("Cleaning up...")
    dir = os.getcwd() + os.sep + folder
    for i in os.listdir(dir):
        if i.endswith('git'):
            tmp = os.path.join(dir, i)
            while True:
                subprocess.call(['attrib', '-H', tmp])
                break
            shutil.rmtree(tmp, onerror=on_rm_error)
    if os.path.exists(os.getcwd() + os.sep + folder):
        shutil.rmtree(os.getcwd() + os.sep + folder)


# TODO: add clear cache flag
if __name__ == "__main__":
    github_folder = "0_github"
    gitlab_folder = "1_gitlab"

    github_url = "git@github.com:liuyal/FortiOS_Automation.git"
    gitlab_url = "ssh://git@gitlab.devqalab.fortilab.net:2222/ljerry/fos_automation.git"

    git_clone(github_url, github_folder)
    git_clone(gitlab_url, gitlab_folder)

    clean_git_folder(gitlab_folder)
    sync_folder(github_folder, gitlab_folder)
    git_commit_push(gitlab_folder, False)

    clean_up(github_folder)
    clean_up(gitlab_folder)

    print("\nGIT SYNC COMPLETE!")
