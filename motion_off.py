import io
import sys

def off():
    with open('/etc/motioneye/thread-2.conf') as file:
        data = file.readlines()
    data[5] = '# @motion_detection off'
    with open('/etc/motioneye/thread-2.conf') as file:
        file.writelines(data)

off()
