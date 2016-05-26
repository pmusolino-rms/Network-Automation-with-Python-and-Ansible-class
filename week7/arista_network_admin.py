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

  def vlan_exists(self,vlan):
    vl=self.__get_vlan(vlan.vlan_id)
    if vl:
      if vl['name'] == vlan.name:
        return True
      else:
        return False
    else:
      return False

  def vlan_add(self,vlan):
    
    vl=self.__get_vlan(vlan.vlan_id)
    if vl:
      if (vl['name'] == vlan.name):
        return False
      #print"Vlan %s already exists!" %vlan.vlan_id
      #exit(1)
      else:
        self.vlans.set_name(vlan.vlan_id,vlan.name)
        return True
    else:
      #print "Adding vlan %s with name %s" %(vlan.vlan_id,vlan.name)
      self.vlans.create(vlan.vlan_id)
      self.vlans.set_name(vlan.vlan_id,vlan.name)
      return True

  def vlan_remove(self,vlan):
    if not self.__get_vlan(vlan.vlan_id):
      #print"Vlan %s does not exist!" %vlan.vlan_id
      #exit(1)
      return False
    else:
      print "Deleting %s" %vlan.vlan_id
      self.vlans.delete(vlan.vlan_id)
      return True

  def vlan_list(self,vlan):
    if vlan.name == "all":
      for vl in list(self.vlans.values()):
        print(("   Vlan Id: {vlan_id}, Name: {name}".format(**vl)))
      return list(self.vlans.values()) 
    else:
      vl=self.__get_vlan(vlan.vlan_id)
      if vl:
        #print "  Vlan ID: {}, Name: {}".format(vl['vlan_id'],vl['name'])
        return vl
      else:
        print "Vlan %s does not exist!" %vlan.vlan_id
        return

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
    status=network_admin.vlan_add(vlan)
    if not status:
      print "Vlan already exists!"
    else:
      print "Vlan created!"
  if mode=="list":
    network_admin.vlan_list(vlan)
  if mode=="remove":
    status=network_admin.vlan_remove(vlan)
    if not status:
      print "Vlan does not exist!"
    else:
      print "Vlan removed!"

if __name__ == "__main__":
  main()
