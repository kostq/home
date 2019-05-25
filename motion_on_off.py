import paramiko
import io
import sys

def check():
    user = 'kostq'
    password = 'kochergin2112955'
    ip = '192.168.1.16'
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ip,username=user,password=password,look_for_keys=False,allow_agent=False)
    stdin,stdout,stderr = client.exec_command('python3 /home/kostq/projects/home/check_motion.py')
    result = stdout.read().decode('ascii').strip("\n")
    return result
    client.close()

check()
