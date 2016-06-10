#!/usr/bin/env python

from pprint import pprint
from juniper_connection import juniper_connection_setup,JuniperObject


def main():
   
   dev = juniper_connection_setup()
   juniper_object = JuniperObject(dev)
   juniper_object.config_mode()
   print "From Set"
   if not juniper_object.get_diff():
       juniper_object.send_command("set system host-name humbaba","set",True)
   else:
       print "Outstanding commits"
   print juniper_object.get_diff()
   juniper_object.commit()
   print "From xml file"
   if not juniper_object.get_diff():
       juniper_object.file_command("hostname.xml","xml",True)
   else:
       print "Outstanding commits"
   print juniper_object.get_diff()
   juniper_object.rollback()
   print "Rollback {}".format(juniper_object.get_diff())
   print "From text file"
   if not juniper_object.get_diff():
       juniper_object.file_command("hostname.cfg", "text", True)
   else:
       print "outstanding commits"
   print juniper_object.get_diff()
   juniper_object.rollback()
   if not juniper_object.get_diff():
       juniper_object.send_command("set system host-name pynet-jnpr-srx1","set",True)
   else:
       print "outstanding commits"
   print juniper_object.get_diff()
   juniper_object.commit(comment="Reset to default")
   juniper_object.unlock()

if __name__ == "__main__":
    main()
