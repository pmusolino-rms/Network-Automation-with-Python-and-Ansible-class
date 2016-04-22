from snmp_helper import snmp_get_oid,snmp_extract
import ConfigParser
import json
import yaml
import pickle

class SNMPUptimeRetreiver(object):
  def __init__(self,device_tuple,user_tuple):
    self.device = device_tuple
    self.user = user_tuple
    self.save_file = "/tmp/config_diff.json"

    ccmHistoryRunningLastChanged = '1.3.6.1.4.1.9.9.43.1.1.1.0'   
    ccmHistoryRunningLastSaved = '1.3.6.1.4.1.9.9.43.1.1.2.0'   
    ccmHistoryStartupLastChanged = '1.3.6.1.4.1.9.9.43.1.1.3.0'
    sysUptime = "1.3.6.1.2.1.1.3.0"
    sysName=".1.3.6.1.2.1.1.5.0"

  def __open_save_file(self):
    return open(self.save_file,"w")

if __name__ == "__main__":

  try:
    config = ConfigParser.SafeConfigParser()
    config.read('config.ini')
  except ConfigParser.ParsingError, err:
    print 'Cound not parse:', err

  for section_name in config.sections():
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

  router = ("50.76.53.27",8061)
  user = (snmp_user,auth_key,encrypt_key)
  
