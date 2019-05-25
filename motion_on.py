import io
import sys

def on():
    data[5] = '# @motion_detection on'
    with open('/etc/motioneye/thread-2.conf') as file:
        file.writelines(data)

on()
