import io

def check_status():

    with open('/etc/motioneye/thread-2.conf') as file:
        data = file.readlines()
    if 'motion_detection on' in data[5]:
        return 'on'
    else:
        return 'off'

check_status()
