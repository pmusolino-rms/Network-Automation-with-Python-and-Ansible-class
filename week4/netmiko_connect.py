#!/usr/bin/env python
from netmiko import ConnectHandler
from getpass import getpass
from get_config import getConfig

def main():
  device_list = getConfig()
  for device in device_list:
    print "Please input password for: " + device.get('rtr_name')
    device['password']=getpass()
    device.pop("rtr_name",None)
    conn=ConnectHandler(**device)
    conn.config_mode()
    if (conn.check_config_mode):
      print "In config"
      conn.exit_config_mode()
    print "Arp table\n" + conn.send_command("sh arp")
    if ('cisco_ios' in device.get('device_type')):
      config_commands = ["do show run | i buffered","logging buffered 12000","do sh run | i buffered"]
      output = conn.send_config_set(config_commands)
      print output
      output = conn.send_config_from_file(config_file='config_file.txt')
      print output

if __name__ == "__main__":
  main()

