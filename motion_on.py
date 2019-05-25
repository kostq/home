import io
import sys

def motion_on():
    with open('/etc/motioneye/thread-2.conf','r') as file:
        data = file.readlines()
    data[5] = '# @motion_detection on' + '\n'
    with open('/etc/motioneye/thread-2.conf','w') as file:
        file.writelines(data)

motion_on()
