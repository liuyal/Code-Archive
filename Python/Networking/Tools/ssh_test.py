import os, sys, time
import paramiko

hostname = "192.168.1.100"
username = "root"
password = "1234"
port = 22

client = paramiko.client.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=hostname, username=username, password=password, port=port)

stdin, stdout, stderr = client.exec_command('ls -al')

print(stdout.readlines())
print(stderr.readlines())

client.close()
