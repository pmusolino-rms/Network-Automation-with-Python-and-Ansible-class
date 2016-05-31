#!/usr/bin/env pyhthon
import django
from netmiko import ConnectHandler
from net_system.models import NetworkDevice, Credentials
from multiprocessing import Process,current_process,Queue
from datetime import datetime

def show_version(dev,q):
  output_dict = {}
  output = "#" * 80
  output += "\n"
  conn = ConnectHandler(device_type=dev.device_type,ip=dev.ip_address,username=dev.credentials.username,password=dev.credentials.password,port=dev.port)
  output += conn.send_command_expect('show version')
  output += "#" * 80
  output += "\n\n"
  output_dict[dev.device_name]=output
  q.put(output_dict)

def main():
  django.setup()

  devices = NetworkDevice.objects.all()
  starttime=datetime.now()
  q=Queue(maxsize=20)
  procs = []
  for dev in devices:
    my_proc=Process(target=show_version, args=(dev,q))
    my_proc.start()
    procs.append(my_proc)

  for proc in procs:
      proc.join()

  while not q.empty():
    my_dict = q.get()
    for k,v in my_dict.iteritems():
      print k
      print v

  totaltime=datetime.now() - starttime
  print
  print "Elapsed time " + str(totaltime)
  print
if __name__ == '__main__':
  main()
