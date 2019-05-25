import io

def check_status():

    with open('/etc/motioneye/thread-2.conf') as file:
        data = file.readlines()
    if 'motion_detection on' in data[5]:
        print ('on')
    else:
        print ('off')

check_status()
