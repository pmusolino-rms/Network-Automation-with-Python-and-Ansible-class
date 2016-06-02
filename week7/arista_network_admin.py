#!/usr/bin/env python
'''
Program to manage Arista Network Switches utilizng the python eapi module
Currently only allows vlan management
'''

import argparse
import pyeapi

class Vlan(object):
    '''
    Vlan class to simplify passing of commonly used variables
    '''
    def __init__(self, vlan_id, name):
        self.vlan_id = vlan_id
        self.name = name
        self.__exists__ = False

    def pprint(self):
        '''
        Print out vlan in a pretty fashion
        '''
        print "Vlan Name: %s" %self.name
        print "Vlan ID: %s" %self.vlan_id

    def get_exists(self):
        '''
        accessor function for vlan existence
        '''
        return self.__exists__

class AristaNetworkAdmin(object):
    '''
    Class for managing pyeapi connection object
    Can add/remove/list vlans
    checks if vlan exists
    '''

    def __init__(self, switch):
        self.switch = switch
        self.vlans = switch.api('vlans')
        self.vlans.autorefresh = True

    def __get_vlan(self, vlan_id):
        '''
        Internal Method to return a pyeapi vlan object
        '''
        return self.vlans.get(vlan_id)

    def vlan_exists(self, vlan):
        '''
        Method to return boolean status of vlan existance
        used for idempotency for apps like Ansible
        '''
        my_vlan = self.__get_vlan(vlan.vlan_id)
        if my_vlan:
            return my_vlan['name'] == vlan.name
        else:
            return False

    def vlan_add(self, vlan):
        '''
        Add a vlan based on if it exists and if
        the name is not identical to existing name
        '''
        my_vlan = self.__get_vlan(vlan.vlan_id)
        if my_vlan:
            if my_vlan['name'] == vlan.name:
                return False
            else:
                self.vlans.set_name(vlan.vlan_id, vlan.name)
                return True
        else:
            self.vlans.create(vlan.vlan_id)
            self.vlans.set_name(vlan.vlan_id, vlan.name)
            return True

    def vlan_remove(self, vlan):
        '''
        Removes a vlan if it exists
        '''
        if not self.__get_vlan(vlan.vlan_id):
            return False
        else:
            print "Deleting %s" %vlan.vlan_id
            self.vlans.delete(vlan.vlan_id)
            return True

    def vlan_list(self, vlan):
        '''
        Lists a singular vlan or all vlans based on vlan name argument
        passed.  It will list all vlans if all is specified as vlan name
        '''
        if vlan.name == "all":
            for my_vlan in list(self.vlans.values()):
                print "   Vlan Id: {vlan_id}, Name: {name}".format(**my_vlan)
            return list(self.vlans.values())
        else:
            my_vlan = self.__get_vlan(vlan.vlan_id)
            if my_vlan:
                #print "  Vlan ID: {}, Name: {}".format(vl['vlan_id'],vl['name'])
                return my_vlan
            else:
                print "Vlan %s does not exist!" %vlan.vlan_id
                return

def parse_args():
    '''
    Parse the arguments passed on the command line
    Version will print version
    i specifies vlan id
    add uses subparser to do adds of vlan
    remove uses subparser to do removal of vlan
    list uses subparser to list one or all vlans
    '''
    parser = argparse.ArgumentParser(description='Add or create Vlans on Aristas')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s (version 1.0)')
    parser.add_argument("-i", "--vlan_id", action="store", type=int)

    subparsers = parser.add_subparsers(help="add/list/remove help")

    list_parser = subparsers.add_parser('list', help="list vlan")
    list_parser.add_argument('-a', '--all', help="List all vlans", action="store_true")
    list_parser.set_defaults(mode="list")

    add_parser = subparsers.add_parser('add', help="Add a vlan")
    add_parser.add_argument("name", action="store", type=str)
    add_parser.set_defaults(mode="add")

    remove_parser = subparsers.add_parser('remove', help='remove a vlan')
    remove_parser.set_defaults(mode="remove")

    mode = "list"
    name = None
    args = parser.parse_args()
    mode = args.mode
    vlan_id = args.vlan_id

    if mode == "add":
        name = args.name
    if mode == "list":
        if args.all:
            name = "all"
            vlan_id = None
    if mode == "remove":
        pass
    return(mode, vlan_id, name)

def main():
    '''
    Main function setting up variables and objects
    '''
    switch = pyeapi.connect_to("pynet-sw4")
    mode, vlan_id, name = parse_args()
    vlan = Vlan(vlan_id, name)
    network_admin = AristaNetworkAdmin(switch)
    if mode == "add":
        status = network_admin.vlan_add(vlan)
        if not status:
            print "Vlan already exists!"
        else:
            print "Vlan created!"
    if mode == "list":
        network_admin.vlan_list(vlan)
    if mode == "remove":
        status = network_admin.vlan_remove(vlan)
        if not status:
            print "Vlan does not exist!"
        else:
            print "Vlan removed!"

if __name__ == "__main__":
    main()
