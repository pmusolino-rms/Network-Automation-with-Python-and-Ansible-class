#!/usr/bin/env python

from ciscoconfparse import CiscoConfParse

config = CiscoConfParse("./cisco_ipsec.txt")

def get_children(search):
  print
  for i in search:
    print i.text
    my_list = i.all_children
    for j in my_list:
      print j.text
    print
  print

crypto_map = config.find_objects(r"crypto map CRYPTO")
print "All crypto maps"
get_children(crypto_map)

crypto_map = config.find_objects_w_child(parentspec=r"^crypto map CRYPTO", childspec = r"set pfs group2")
print "PFS2 maps"
get_children(crypto_map)

crypto_map = config.find_objects_wo_child(parentspec=r"^crypto map CRYPTO", childspec = r"AES")
print "Non-AES Maps"
get_children(crypto_map)

exit(0)
