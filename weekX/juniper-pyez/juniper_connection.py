#!/usr/bin/env python

from pprint import pprint
from jnpr.junos import Device
from jnpr.junos.op.ethport import EthPortTable
from jnpr.junos.op.routes import RouteTable
from jnpr.junos.utils.config import Config
from net_system.models import NetworkDevice
import django

class JuniperObject(object):
    def __init__(self,jnp_dev):
        self.conn = jnp_dev
        self.config = None
        self.ports = {}
        self.routes = {}

    def __get_ports(self):
        self.ports = EthPortTable(self.conn)
        self.ports.get()

    def __get_routes(self):
        self.routes = RouteTable(self.conn)
        self.routes.get()
   
    def config_mode(self):
        self.config = Config(self.conn)
        self.config.lock()

    def send_command(self, command, cmd_format, cmd_merge):
       self.config.load(command, format=cmd_format, merge=cmd_merge)

    def file_command(self,file_path,file_format,file_merge):
        self.config.load(path=file_path, format=file_format, merge=file_merge)
   
    def get_diff(self):
        return self.config.diff()

    def commit(self,comment=None):
        self.config.commit(comment=comment)
   
    def rollback(self):
        self.config.rollback(0)

    def unlock(self):
        self.config.unlock()

    def show_all_interfaces(self):
        self.__get_ports()
        print "Juniper SRX Interface Statistics"
        for my_key in self.ports.keys():
            print "---------------------------------"
            print my_key + ":"
            print "Operational Status: " + self.ports[my_key]['oper']
            print "Packets In: " + self.ports[my_key]['rx_packets']
            print "Packets Out: " + self.ports[my_key]['tx_packets']

    def show_all_routes(self):
        self.__get_routes()
        print "Juniper SRX Routing Table"
        for my_key in self.routes.keys():
            print "---------------------------------"
            print my_key + ":"
            print "  Next Hop: {}".format(self.routes[my_key]['nexthop'])
            print "  Age: {}".format(self.routes[my_key]['age'])
            print "  via: {}".format(self.routes[my_key]['via'])
            print "  Protocol: {}".format(self.routes[my_key]['protocol'])

def juniper_connection_setup():
   django.setup()

   device = NetworkDevice.objects.get(device_name='juniper-srx')
   print "Connecting to device: %s" %device.device_name
   jnp_dev = Device(host=device.ip_address,user=device.credentials.username,password=device.credentials.password)
   jnp_dev.open()
   jnp_dev.timeout = 120
   if jnp_dev.facts:
       return jnp_dev
   else:
       return None

def main():
    print "Juniper connection setup"
    dev = juniper_connection_setup()
    print dev.facts

if __name__ == "__main__":
    main()
