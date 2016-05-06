#!/usr/bin/env pythong
from snmp_helper import snmp_get_oid_v3,snmp_extract
import pygal
from  config_monitor import SNMPv3ConfigChangeRetriever
import time
import ConfigParser

class SNMPv3TrafficStats(SNMPv3ConfigChangeRetriever):
  def __init__(self,device,user,interface_index):
    SNMPv3ConfigChangeRetriever.__init__(self,device,user)
    self.interface = interface_index
    self.ifDesc = self.__get_ifDesc()
    self.inOctets = self.__get_inOctets()
    self.inUcastPkts = self.__get_inUcastPkts()
    self.outOctets = self.__get_outOctets()
    self.outUcastPkts = self.__get_outUcastPkts()

  def __get_ifDesc(self):
    oid = '1.3.6.1.2.1.2.2.1.2.' + self.interface
    return self._snmp_get(oid)
  def __get_inOctets(self):
    oid = '1.3.6.1.2.1.2.2.1.10.' + self.interface
    return int(self._snmp_get(oid))
  def __get_inUcastPkts(self):
    oid = '1.3.6.1.2.1.2.2.1.11.' + self.interface
    return int(self._snmp_get(oid))
  def __get_outOctets(self):
    oid = '1.3.6.1.2.1.2.2.1.16.' + self.interface
    return int(self._snmp_get(oid))
  def __get_outUcastPkts(self):
    oid = '1.3.6.1.2.1.2.2.1.17.' + self.interface
    return int(self._snmp_get(oid))
  def update_counters(self):
    SNMPv3ConfigChangeRetriever.update_counters(self)
    self.inOctets = self.__get_inOctets()
    self.outOctets = self.__get_outOctets()
    self.inUcastPkts = self.__get_inUcastPkts()
    self.outUcastPkts = self.__get_outUcastPkts()
  def __str__(self):
    return self.ifDesc + ":\nInput Octets: " +  str(self.inOctets) + "\nOutput Octets: " + str(self.outOctets) + "\nInputPkts: " + str(self.inUcastPkts) + "\nOutput Packets: " + str(self.outUcastPkts)

def get_raw_data(o):
  a = o.inOctets
  b = o.outOctets
  c = o.inUcastPkts
  d = o.outUcastPkts
  return a,b,c,d

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
    else:
     for name,value in config.items(section_name):
       if name =="ip":
         ip=value
       if name =="port":
         port = int(value)
       if name =="int_index":
         index=value

  user = (snmp_user,auth_key,encrypt_key)
  device = (ip,port)
  print "Initializing"
  router_stats = SNMPv3TrafficStats(device,user,index)
  in_octets=[]
  out_octets=[]
  in_pkts=[]
  out_pkts=[]
  raw_in_bytes,raw_out_bytes,raw_in_pkts,raw_out_pkts = get_raw_data(router_stats)
#  raw_out_bytes = router_stats.outOctets
#  raw_in_pkts = router_stats.inUcastPkts
#  raw_out_pkts = router_stats.outUcastPkts
  print router_stats
  for i in range(12):
    time.sleep(300)
    print "Updating counters interation: " + str(i)
    router_stats.update_counters()
    in_octets.append(router_stats.inOctets - raw_in_bytes)
    out_octets.append(router_stats.outOctets - raw_out_bytes)
    in_pkts.append(router_stats.inUcastPkts - raw_in_pkts)
    out_pkts.append(router_stats.outUcastPkts - raw_out_pkts)
    raw_in_bytes,raw_out_bytes,raw_in_pkts,raw_out_pkts = get_raw_data(router_stats)
    print router_stats

  line_chart = pygal.Line()
  line_chart.title=router_stats.ifDesc + ' Inout/Output Packets and Bytes'
  line_chart.x_labels = ['5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60']
  line_chart.add('InPackets',in_pkts)
  line_chart.add('OutPackets',out_pkts)
  line_chart.add('InBytes',in_octets)
  line_chart.add('OutBytes',out_octets)
  line_chart.render_to_file(router_stats.ifDesc +'_stats.svg')

if __name__ == "__main__":
  main()
