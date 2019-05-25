import io
import sys

def off():
    data[5] = '# @motion_detection off'
    with open('/etc/motioneye/thread-2.conf') as file:
        file.writelines(data)

off()
