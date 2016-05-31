#!/usr/bin/env python

import django
from netmiko import ConnectHandler
from net_system.models import NetworkDevice, Credentials
from datetime import datetime

def main():
  django.setup()

  devices = NetworkDevice.objects.all()
  starttime=datetime.now()
  for dev in devices:
    print "#"*30 + " " + dev.device_name + " " + "#" * 30
    conn = ConnectHandler(device_type=dev.device_type,ip=dev.ip_address,username=dev.credentials.username,password=dev.credentials.password,port=dev.port)
    print conn.send_command_expect('show version')
    print "#" * 80
    print

  totaltime=datetime.now() - starttime
  print
  print "Elapsed time " + str(totaltime)
  print
if __name__ == '__main__':
  main()
