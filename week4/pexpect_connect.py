#!/usr/bin/env python

import pexpect
import time
import sys
import re
from get_config import getConfig
from getpass import getpass

class pexpect_connection(object):
  def __init__(self,connection,timeout=3):
    self.timeout=timeout
    self.connection=connection
    self.connection.logfile=sys.stdout
    self.connection.timeout=self.timeout
    self.prompt = None

  def pexpect_login(self,passwd):
    self.connection.expect('ssword:')
    self.connection.sendline(passwd)
    self.connection.expect('#')
    
  def pexpect_get_prompt(self):
    self.connection.sendline('')
    self.connection.expect('#')
    self.prompt =  self.connection.before.lstrip()+self.connection.after

  def pexpect_send_command(self,command):
    self.connection.sendline(command)
    self.connection.expect(self.prompt)
    time.sleep(1)
    return self.connection.before

  def pexpect_send_config_command(self,command):
    self.connection.sendline('configure terminal')
    self.connection.expect('#')
    time.sleep(1)
    self.pexpect_get_prompt()
    if ("config" in self.prompt):
      time.sleep(2)
      print "\nConfig Mode"
      self.connection.sendline(command)
      self.connection.expect("\(config\)#")
      self.connection.sendline("end")
      self.connection.expect("#")
      self.pexpect_get_prompt()
      return
    else:
      print "not in config mode"
      return

  def pexpect_set_pager(self):
    self.pexpect_send_command('terminal length 0')
    return

def main():
  device_list = getConfig()
  for device in device_list:
    if 'juniper' in device.get('device_type'):
      print "Skipping Juniper device: " + device.get('rtr_name')
      next
    else:
      print "Please input password for: " + device.get('rtr_name')
      password=getpass()
    
      connection = pexpect.spawn('ssh -l {} {} -p {}'.format(device.get('username'),device.get('ip'),device.get('port')))
      pexpect_conn = pexpect_connection(connection)
      pexpect_conn.pexpect_login(password)
      pexpect_conn.pexpect_get_prompt()
      pexpect_conn.pexpect_set_pager()
      pexpect_conn.pexpect_send_command('sh ip interface brief')
      pexpect_conn.pexpect_send_config_command('logging buffered 20012')
      pexpect_conn.pexpect_send_command('sh run | include buffered')
      pexpect_conn.connection.close()
    
if __name__ == "__main__":
  main()

