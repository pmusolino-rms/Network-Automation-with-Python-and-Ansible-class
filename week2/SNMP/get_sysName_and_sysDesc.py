#!/usr/bin/env python
from snmp_helper import snmp_get_oid,snmp_extract

ip_addr="50.76.53.27"
port_list=[7961,8061]
community = "galileo"

sysDesc=".1.3.6.1.2.1.1.1.0"
sysName=".1.3.6.1.2.1.1.5.0"

for i in port_list:
  device = (ip_addr,community,i)
  name = snmp_get_oid(device,oid=sysName)
  desc = snmp_get_oid(device,oid=sysDesc)
  print (snmp_extract(name))
  print (snmp_extract(desc))
