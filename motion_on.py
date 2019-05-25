import io
import os
import sys
import subprocess

def motion_on():
    with open('/etc/motioneye/thread-1.conf','r') as file:
        data_1 = file.readlines()
    data_1[5] = '# @motion_detection on' + '\n'
    with open('/etc/motioneye/thread-1.conf','w') as file:
        file.writelines(data_1)
    with open('/etc/motioneye/thread-2.conf','r') as file:
        data_2 = file.readlines()
    data_2[5] = '# @motion_detection on' + '\n'
    with open('/etc/motioneye/thread-2.conf','w') as file:
        file.writelines(data_2)
    command = os.system('echo kochergin2112955 | sudo -S systemctl restart motioneye')
motion_on()
