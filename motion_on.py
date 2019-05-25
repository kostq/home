import io
import os
import sys
import subprocess

def motion_on():
    password = 'kochergin2112955'
    with open('/etc/motioneye/thread-2.conf','r') as file:
        data = file.readlines()
    data[5] = '# @motion_detection on' + '\n'
    with open('/etc/motioneye/thread-2.conf','w') as file:
        file.writelines(data)
    command = os.system('echo kochergin2112955 | sudo -S systemctl restart motioneye')
motion_on()
