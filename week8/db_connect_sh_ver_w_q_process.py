#!/usr/bin/env pyhthon
"""
Program to access a Django database to create connections
to all devices contained therein.
A command is run to get the show version output of each device
The program utilizes multiple processes and Queues to deserialize the I/O
and organize them by device
"""

from multiprocessing import Process, Queue
from datetime import datetime
from net_system.models import NetworkDevice
from netmiko import ConnectHandler
import django


def show_version(dev, queue):
    """
    Function to show the devices version
    Uses a Queue to sort output from the multiple processes
    """
    output_dict = {}
    output = "#" * 80
    output += "\n"
    conn = ConnectHandler(device_type=dev.device_type, ip=dev.ip_address,
                          username=dev.credentials.username, password=dev.credentials.password,
                          port=dev.port)
    output += conn.send_command_expect('show version')
    output += "#" * 80
    output += "\n\n"
    output_dict[dev.device_name] = output
    queue.put(output_dict)


def main():
    """
    Main function which sets up variables
    Starts other processes
    iterates through devices in database
    """

    django.setup()

    devices = NetworkDevice.objects.all()
    starttime = datetime.now()
    queue = Queue(maxsize=20)
    procs = []
    for dev in devices:
        my_proc = Process(target=show_version, args=(dev, queue))
        my_proc.start()
        procs.append(my_proc)

    for proc in procs:
        proc.join()

    while not queue.empty():
        my_dict = queue.get()
        for key, value in my_dict.iteritems():
            print key
            print value

    totaltime = datetime.now() - starttime
    print
    print "Elapsed time " + str(totaltime)
    print

if __name__ == '__main__':
    main()
