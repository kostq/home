import io

def check_status():

    with open('/etc/motioneye/thread-1.conf') as file:
        data = file.readlines()
    if 'motion_detection on' in data[5]:
        print ("on")
    else:
        print ("off")

check_status()
