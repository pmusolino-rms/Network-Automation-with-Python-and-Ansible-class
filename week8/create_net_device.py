#!/usr/bin/env python

import django
from net_system.models import NetworkDevice, Credentials

def main():
  django.setup()
  test_rtr1 = NetworkDevice(device_name='test_rtr1',device_type='dell',ip_address='10.2.3.3',port='8222')
  test_rtr1.save()
  test_rtr2 = NetworkDevice.objects.get_or_create(device_name='test_rtr2',device_type='procurve',ip_address='10.2.4.3',port='8322')

  devices = NetworkDevice.objects.all()
  for dev in devices:
    if 'test' in dev.device_name:
      print dev.device_name,dev.device_type,dev.ip_address,dev.port

if __name__ == '__main__':
  main()
