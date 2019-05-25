import io

def check_status():

    with open('/etc/motioneye/thread-2.conf') as file:
        data = file.readlines()
    print (data[5])

    if 'motion_detection on' in data[5]:
        return True
    else:
        return False

check_status()
