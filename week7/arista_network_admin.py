#!/usr/bin/env python

import pyeapi
import argparse

class Vlan(object):
  def __init__(self,vlan_id,name):
    self.vlan_id = vlan_id
    self.name = name
    self.exists = False

class AristaNetworkAdmin(object):
  def __init__(self,switch):
    self.switch=switch
    self.vlans=switch.api('vlans')
    self.vlans.autorefresh=True

  def __get_vlan(self,vlan_id):
    return self.vlans.get(vlan_id)

  def vlan_add(self,vlan):
    if self.__get_vlan(vlan.vlan_id):
      print"Vlan %s already exists!" %vlan.vlan_id
      exit(1)
    else:
      print "Adding vlan %s with name %s" %(vlan.vlan_id,vlan.name)
      self.vlans.create(vlan.vlan_id)
      self.vlans.set_name(vlan.vlan_id,vlan.name)

  def vlan_remove(self,vlan):
    if not self.__get_vlan(vlan.vlan_id):
      print"Vlan %s does not exist!" %vlan.vlan_id
      exit(1)
    else:
      print "Deleting %s" %vlan.vlan_id
      self.vlans.delete(vlan.vlan_id)

  def vlan_list(self,vlan):
    if vlan.name == "all":
      for vl in list(self.vlans.values()):
        print(("   Vlan Id: {vlan_id}, Name: {name}".format(**vl)))
    else:
      vl=self.__get_vlan(vlan.vlan_id)
      if vl:
        print "  Vlan ID: {}, Name: {}".format(vl['vlan_id'],vl['name'])
      else:
        print "Vlan %s does not exist!" %vlan.vlan_id

def parseArgs():
  parser = argparse.ArgumentParser(description='Add or create Vlans on Aristas')
  parser.add_argument('-v', '--version', action='version',version='%(prog)s (version 1.0)')
  parser.add_argument("-d", "--debug", help="Verbose output", action="store_true")
  parser.add_argument("-i", "--vlan_id", action="store", type=int)

  subparsers = parser.add_subparsers(help="add/list/remove help")

  list_parser=subparsers.add_parser('list', help="list vlan")
  list_parser.add_argument('-a', '--all', help="List all vlans",action="store_true")
  list_parser.set_defaults(mode="list")

  add_parser=subparsers.add_parser('add', help="Add a vlan")
  add_parser.add_argument("name", action="store", type=str)
  add_parser.set_defaults(mode="add")

  remove_parser=subparsers.add_parser('remove', help='remove a vlan')
  remove_parser.set_defaults(mode="remove")

  mode="list"
  name=None
  debug = False
  args = parser.parse_args()
  mode=args.mode
  vlan_id=args.vlan_id

  if args.debug:
    debug = True
  if mode=="add":
    name=args.name
  if mode=="list":
    if args.all:
      name="all"
      vlan_id=None
  if mode=="remove":
    pass
  return(mode,vlan_id,name)

def main():
  switch=pyeapi.connect_to("pynet-sw4")
  mode,vlan_id,name=parseArgs()
  vlan=Vlan(vlan_id,name)
  network_admin=AristaNetworkAdmin(switch)
  if mode=="add":
    network_admin.vlan_add(vlan)
  if mode=="list":
    network_admin.vlan_list(vlan)
  if mode=="remove":
    network_admin.vlan_remove(vlan)  
  
if __name__ == "__main__":
  main()
