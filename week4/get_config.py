#!/usr/bin/env python

import ConfigParser

def getConfig():
  rtrs_list = []
  try:
    config = ConfigParser.SafeConfigParser()
    config.read('config.ini')
  except ConfigParser.ParsingError, err:
    print 'Cound not parse:', err

  for section_name in config.sections():
    rtr_dict={}
    rtr_dict['rtr_name']=section_name
    for name,value in config.items(section_name):
        if name =="user":
          rtr_dict['username']=value
          next
        if name == "device_type":
          rtr_dict['device_type']=value
          next
        if name == "ip":
          rtr_dict['ip']=value
          next
        if name == "port":
          rtr_dict['port']=int(value)
          next
    rtrs_list.append(rtr_dict)
  return rtrs_list
