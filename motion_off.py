import io
import sys
import os

def motion_off():
    with open('/etc/motioneye/thread-2.conf','r') as file:
        data = file.readlines()
    data[5] = '# @motion_detection off' + '\n'
    with open('/etc/motioneye/thread-2.conf','w') as file:
        file.writelines(data)
    command = os.system('echo kochergin2112955 | sudo -S systemctl restart motioneye')
motion_off()
