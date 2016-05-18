#!/usr/bin/env python

import paramiko
import time
from get_config import getConfig
from getpass import getpass

def command_send(conn,cmd):
  output=""
  if conn.recv_ready():
    output=conn.recv(5000)
  conn.send(cmd + '\n')
  time.sleep(3)
  while conn.recv_ready():
    output+=conn.recv(65535)
  return output

def main():
  device_list = getConfig()
  for device in device_list:
    if 'juniper' in device.get('device_type'):
      print "Skipping Juniper device: " + device.get('rtr_name')
      next
    else:
      print "Please input password for: " + device.get('rtr_name')
      password=getpass()
      connection_setup = paramiko.SSHClient()
      connection_setup.load_system_host_keys()
      connection_setup.connect(device.get('ip'),username=device.get('username'),password=password,look_for_keys=False,allow_agent=False,port=device.get('port'))
      connection = connection_setup.invoke_shell()

      connection.settimeout(10.0)
      out=connection.recv(5000)
      out=command_send(connection,'terminal length 0')
      out = command_send(connection,'sh version')
      print out
      print "Old Value: " + command_send(connection,"sh logging | i Log\ Buffer")   
      out=command_send(connection,'configure terminal')

      if ("config" in out):
        out=command_send(connection,'logging buffered 20012')
        out=command_send(connection,'end')
        print "New Value: " + command_send(connection,"sh logging | i Log\ Buffer")   
      else:
        print "Not in config mode"

if __name__ == "__main__":
  main() 
