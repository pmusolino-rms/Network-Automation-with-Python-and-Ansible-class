#!/usr/bin/env python

import django
from net_system.models import NetworkDevice, Credentials

def main():
  django.setup()

  devices = NetworkDevice.objects.all()

  for dev in devices:
    if 'test' in dev.device_name:
      print dev.device_name
      dev.delete()
    else:
      next

if __name__ == '__main__':
  main()
