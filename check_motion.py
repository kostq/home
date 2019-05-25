import io

def check_status():

    with open('/etc/motioneye/thread-2.conf') as file:
        data = file.readlines()
    print data[5]

    if 'motion_detection on' in data[5]:
        print('DETECTION ON')
    else:
        print('DETECTION OFF')
