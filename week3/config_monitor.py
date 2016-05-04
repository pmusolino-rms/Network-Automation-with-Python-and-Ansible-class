#!/usr/bin/env python

from snmp_helper import snmp_get_oid_v3,snmp_extract
from email_helper import send_mail
from json import JSONEncoder
import ConfigParser
import json
import yaml
import pickle
import time

class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class SNMPv3ConfigChangeRetriever(object):
  def __init__(self,device_tuple,user_tuple):
    self.device = device_tuple
    self.user = user_tuple
    self.sysName = self.__get_sysName()
    self.uptime = self.__get_uptime()
    self.running_last_changed = None
    self.running_last_saved = None
    self.startup = None
  def __snmp_get(self,oid):
    data = snmp_get_oid_v3(self.device,self.user,oid=oid,display_errors=False)
    return snmp_extract(data)
  def __get_running_last_changed(self):
    oid = '1.3.6.1.4.1.9.9.43.1.1.1.0'
    return self.__snmp_get(oid)
  def __get_startup_last_changed(self):
    oid = '1.3.6.1.4.1.9.9.43.1.1.3.0'
    return self.__snmp_get(oid)
  def __get_running_last_saved(self):
    oid = '1.3.6.1.4.1.9.9.43.1.1.2.0'   
    return self.__snmp_get(oid)
  def __get_uptime(self):
    oid = "1.3.6.1.2.1.1.3.0"
    return self.__snmp_get(oid)
  def __get_sysName(self):
    oid = ".1.3.6.1.2.1.1.5.0"
    return self.__snmp_get(oid)
  def update_counters(self):
    self.uptime = self.__get_uptime()
    self.running_last_changed = self.__get_running_last_changed()
    self.running_last_saved = self.__get_running_last_saved()
    self.startup_last_changed = self.__get_startup_last_changed()

def update_data(save,data,config):
  config.update_counters()
  data["uptime"] = config.uptime
  data["running_last_changed"] = config.running_last_changed
  data["running_last_saved"] = config.running_last_saved
  data["startup_last_changed"] = config.startup_last_changed
  with open(save,"w") as f:
    json.dump(data,f)

def main():
  try:
    config = ConfigParser.SafeConfigParser()
    config.read('config.ini')
  except ConfigParser.ParsingError, err:
    print 'Cound not parse:', err

  for section_name in config.sections():
    if section_name == "snmp_credentials":
      for name,value in config.items(section_name):
        if name =="snmp_user":
          snmp_user = value
          next
        if name == "auth_key":
          auth_key = value
          next
        if name == "encrypt_key":
          encrypt_key = value
          next
    if section_name == "smtp_data":
      for name,value in config.items(section_name):
        if name =="sender":
          smtp_sender = value
          next
        if name =="recipient":
          smtp_recipient = value
          next
        if name =="subject":
          smtp_subject = value
          next
        if name =="server":
          smtp_server = value
          next
    else:
     for name,value in config.items(section_name):
       if name =="ip":
         ip=value
       if name =="port":
         port = int(value)
     
  user = (snmp_user,auth_key,encrypt_key)
  device = (ip,port)
  config_status = SNMPv3ConfigChangeRetriever(device,user)
  save_file = "/tmp/" + config_status.sysName + ".config_diff.json"
  with open(save_file,"a+") as f:
    f.seek(0,0)
    first_char = f.read(1)
    if not first_char:
      data = {
        "sysName" : config_status.sysName,
        "uptime" : config_status.uptime,
        "running_last_changed" : None,
        "running_last_saved" : None,
        "startup_last_changed" : None
      }
      update_data(save_file,data,config_status)
      exit(0)
    else:
      f.seek(0,0)
      data = json.load(f)

  old_uptime = data["uptime"]
  old_run_last_change = data["running_last_changed"]
  old_run_last_save = data["running_last_saved"]
  old_start_last_change = data["startup_last_changed"]
  update_data(save_file,data,config_status)
  if (data["running_last_saved"] == "0") and (data["running_last_changed"] != old_run_last_change):
    #reboot
    print "Reboot"
    send_mail(smtp_recipient,smtp_subject,"Reboot detected",smtp_sender)
    #exit(0)
    try:
      time.sleep(900)
      main()
    except KeyboardInterrupt:
      print "Exiting"
      exit(0)
  if (data["running_last_saved"] != old_run_last_save) and (data["startup_last_changed"] != old_start_last_change):
    print "write mem"
    send_mail(smtp_recipient,smtp_subject,"Wr mem",smtp_sender)
    #exit(0)
    try:
      time.sleep(900)
      main()
    except KeyboardInterrupt:
      print "Exiting"
      exit(0)
  if (data["running_last_saved"] != old_run_last_save) and (data["startup_last_changed"] == old_start_last_change):
    print "sh run or wr term"
    send_mail(smtp_recipient,smtp_subject,"sh run or write terminal",smtp_sender)
    #exit(0)
    try:
      time.sleep(900)
      main()
    except KeyboardInterrupt:
      print "Exiting"
      exit(0)
  if (data["running_last_changed"] != old_run_last_change):
    print "Config Change"
    send_mail(smtp_recipient,smtp_subject,"Config change",smtp_sender)
    #exit(0)
    try:
      time.sleep(900)
      main()
    except KeyboardInterrupt:
      print "Exiting"
      exit(0)
  print "NO Change"
  #exit(0)
  try:
    time.sleep(900)
    main()
  except KeyboardInterrupt:
    print "Exiting"
    exit(0)

if __name__ == "__main__":
  main()
