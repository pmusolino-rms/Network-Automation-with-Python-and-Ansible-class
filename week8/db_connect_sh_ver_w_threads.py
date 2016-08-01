#!/usr/bin/env python

import django
from netmiko import ConnectHandler
from net_system.models import NetworkDevice, Credentials
import threading
from datetime import datetime


def show_version(dev):

    print "#"*30 + " " + dev.device_name + " " + "#" * 30
    conn = ConnectHandler(device_type=dev.device_type, ip=dev.ip_address, username=dev.credentials.username,
                          password=dev.credentials.password, port=dev.port)
    print conn.send_command_expect('show version')
    print "#" * 80
    print


def main():
    django.setup()

    devices = NetworkDevice.objects.all()
    starttime = datetime.now()
    for dev in devices:
        my_thread = threading.Thread(target=show_version, args=(dev,))
        my_thread.start()

    main_thread = threading.currentThread()

    for thread in threading.enumerate():
        if thread != main_thread:
            print thread
            thread.join()

    totaltime = datetime.now() - starttime
    print
    print "Elapsed time " + str(totaltime)
    print

if __name__ == '__main__':
    main()
