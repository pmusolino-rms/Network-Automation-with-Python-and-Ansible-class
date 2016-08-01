#!/usr/bin/env python
"""
Program to use Django DB and update
vendor field based on device type
"""

import django
from net_system.models import NetworkDevice


def main():
    """
    Main function doing all the heavy lifting
    """

    django.setup()

    devices = NetworkDevice.objects.all()

    for dev in devices:
        if 'cisco' in dev.device_type:
            dev.vendor = "Cisco"
        elif 'juniper' in dev.device_type:
            dev.vendor = "Juniper"
        elif 'arista' in dev.device_type:
            dev.vendor = "Arista"
        dev.save()

    for dev in devices:
        print dev.device_name, dev.vendor

if __name__ == '__main__':
    main()
