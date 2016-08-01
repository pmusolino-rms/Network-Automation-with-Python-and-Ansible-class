#!/usr/bin/env pyhthon
import django
from netmiko import ConnectHandler
from net_system.models import NetworkDevice, Credentials
from multiprocessing import Process,current_process
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
    procs = []
    for dev in devices:
        my_proc = Process(target=show_version, args=(dev,))
        my_proc.start()
        procs.append(my_proc)

    for proc in procs:
        print proc
        proc.join()

    totaltime = datetime.now() - starttime
    print
    print "Elapsed time " + str(totaltime)
    print

if __name__ == '__main__':
  main()
