#!/usr/bin/env python
import pyeapi

switch = pyeapi.connect_to("pynet-sw4")
command= switch.enable('show interfaces')
show_interfaces=command[0]['result']['interfaces']
for interface in show_interfaces:
  if "Vlan" in interface:
    next
  else:
    print "Interface: " + interface
    print "In Octets: " + str(show_interfaces[interface]['interfaceCounters']['inOctets'])
    print "Out Octets: " + str(show_interfaces[interface]['interfaceCounters']['outOctets'])
    print "-*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*-"
