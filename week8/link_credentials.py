#!/usr/bin/env python
'''
Program to link credentials to network device based on device name
'''

import django
from net_system.models import NetworkDevice, Credentials

def main():
    '''
    Main Process
    '''
    django.setup()

    devices = NetworkDevice.objects.all()
    creds = Credentials.objects.all()
    std_cred = creds[0]
    arista_cred = creds[1]

    for dev in devices:
        if 'pynet-sw' in dev.device_name:
            dev.credentials = arista_cred
        else:
            dev.credentials = std_cred
        dev.save()

    for dev in devices:
        print dev.device_name, dev.credentials

if __name__ == '__main__':
    main()
